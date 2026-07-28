"""Offline contracts for the provider-independent Audio operation boundary.

This module plans and validates Audio work; it deliberately does not construct a
provider client, encode audio, or send email.
"""
from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import math
import os
import re
import shutil
import stat
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from .operation_consent import (
    AuthMode,
    ConsentError,
    OperationClaim,
    OperationMaxima,
    ProviderTask,
    canonical_json_bytes,
    sha256_hex,
)

MIN_TARGET_SECONDS = 30
MAX_TARGET_SECONDS = 3600
MAX_SCRIPT_BYTES = 120_000
MIN_CHUNK_CHARS = 500
MAX_CHUNK_CHARS = 4_000
MAX_CHUNKS = 32
MAX_CHUNK_SECONDS = 120
MAX_CHUNK_BYTES = 6 * 1024 * 1024
MAX_MP3_BYTES = 64 * 1024 * 1024
DISK_RESERVATION_BYTES = 90 * 1024 * 1024
CODEC_MEMORY_BYTES = 8 * 1024 * 1024
PCM_SAMPLE_RATE = 24_000
PCM_BYTES_PER_SAMPLE = 2
GAP_SECONDS = 0.250
# Single Python-side authority for the inter-chunk gap. The codec wrapper
# (bin/audio-encode-lamejs.mjs) pins the same 6,000-sample block; a
# cross-boundary test asserts the two never drift apart again (D1).
SILENCE_SAMPLES = round(GAP_SECONDS * PCM_SAMPLE_RATE)
# MEASURED, not guessed: lamejs@1.2.1 at 24 kHz emits MPEG-2 Layer III with
# 576 samples per frame. A full residue sweep mod 576 measured a worst-case
# added framing of 1,727 samples = 0.071958 s, so a 0.100 s reserve is
# sufficient with 0.028042 s of headroom.
FRAMING_RESERVE = 0.100
# PRE-DISPATCH SCHEDULING BUDGET ONLY (= 3599.900 s). This is deliberately NOT
# the hard ceiling: MAX_TARGET_SECONDS stays the validator maximum enforced by
# validate_audio_output. Admission control schedules against the smaller budget
# so encoder framing can never push a run that already paid for TTS past the
# ceiling and have its output discarded after the spend (D3).
AUDIO_BUDGET_SECONDS = MAX_TARGET_SECONDS - FRAMING_RESERVE
TRANSFER_TTL_SECONDS = 300


class AudioOperationError(ConsentError):
    """A rejected Audio input, artifact, or lifecycle transition."""


class AudioTempRecoveryAmbiguous(AudioOperationError):
    """The Audio root cannot be safely inspected, so Audio must be disabled."""


_HEX = re.compile(r"^[0-9a-f]{64}$")
_OP_NAME = re.compile(r"^audio-op-([0-9a-f]{64})$")


def _digest(value: str, name: str) -> str:
    if not isinstance(value, str) or not _HEX.fullmatch(value):
        raise AudioOperationError(f"{name} must be a 64-character lowercase hexadecimal digest")
    return value


def _text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise AudioOperationError(f"{name} must be a nonempty string")
    return value


def _integer(value: int, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise AudioOperationError(f"{name} must be an integer in {minimum}..{maximum}")
    return value


def _bytes_digest(domain: bytes, value: bytes) -> str:
    return hashlib.sha256(domain + value).hexdigest()


@dataclass(frozen=True)
class PaperAudioInputV1:
    """Retained paper context, including the ordered related-paper connections."""

    asset_digest: str
    title: str
    review: str
    connections: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "asset_digest", _digest(self.asset_digest, "asset_digest"))
        object.__setattr__(self, "title", _text(self.title, "title"))
        object.__setattr__(self, "review", _text(self.review, "review"))
        if isinstance(self.connections, (str, bytes)):
            raise AudioOperationError("connections must be an ordered sequence")
        object.__setattr__(self, "connections", tuple(_text(item, "connection") for item in self.connections))

    def canonical_value(self) -> dict[str, object]:
        return {"asset_digest": self.asset_digest, "connections": list(self.connections), "review": self.review, "title": self.title}

    @property
    def source_digest(self) -> str:
        return _bytes_digest(b"pc-audio-paper-v1\0", canonical_json_bytes(self.canonical_value()))


@dataclass(frozen=True)
class AudioAnswerInputV1:
    """Copied answer transfer.  Browser-provided prose is never accepted here."""

    capability: str
    operation_id: str
    result_digest: str
    query_digest: str
    final_digest: str
    payload_digest: str
    transfer_digest: str
    expires_at: int
    query: str
    final_payload: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "capability", _text(self.capability, "capability"))
        object.__setattr__(self, "operation_id", _text(self.operation_id, "operation_id"))
        for name in ("result_digest", "query_digest", "final_digest", "payload_digest", "transfer_digest"):
            object.__setattr__(self, name, _digest(getattr(self, name), name))
        if isinstance(self.expires_at, bool) or not isinstance(self.expires_at, int) or self.expires_at < 1:
            raise AudioOperationError("expires_at must be a positive integer")
        object.__setattr__(self, "query", _text(self.query, "query"))
        if not isinstance(self.final_payload, bytes) or not self.final_payload:
            raise AudioOperationError("final_payload must be nonempty bytes")
        if len(self.final_payload) > 2 * 1024 * 1024:
            raise AudioOperationError("final_payload exceeds the retained final limit")
        if sha256_hex(self.final_payload) != self.payload_digest:
            raise AudioOperationError("payload digest does not match retained final bytes")
        if self.query_digest != _bytes_digest(b"pc-query-v1\0", self.query.encode("utf-8")):
            raise AudioOperationError("query digest does not match retained query")
        if self.transfer_digest != answer_transfer_digest(self):
            raise AudioOperationError("transfer digest does not match retained transfer")

    def canonical_value(self) -> dict[str, object]:
        return {
            "capability": self.capability, "expires_at": self.expires_at, "final_digest": self.final_digest,
            "operation_id": self.operation_id, "payload_digest": self.payload_digest, "query_digest": self.query_digest,
            "result_digest": self.result_digest,
        }

    @property
    def source_digest(self) -> str:
        return _bytes_digest(b"pc-audio-answer-source-v1\0", canonical_json_bytes(self.canonical_value()))

    def reconstruct_text(self) -> str:
        try:
            answer = self.final_payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AudioOperationError("retained final payload must be UTF-8") from exc
        return f"[질문] {self.query}\n\n[답변] {answer}"


def answer_transfer_digest(value: AudioAnswerInputV1) -> str:
    """Domain-separated digest for the exact retained Normal/Deeper handoff."""
    payload = {
        "capability": value.capability, "expires_at": value.expires_at,
        "final_digest": value.final_digest, "operation_id": value.operation_id,
        "payload_digest": value.payload_digest, "query_digest": value.query_digest,
        "result_digest": value.result_digest,
    }
    return _bytes_digest(b"pc-answer-transfer-v1\0", canonical_json_bytes(payload))
def create_answer_input(*, capability: str, operation_id: str, result_digest: str,
                        query: str, final_digest: str, final_payload: bytes,
                        expires_at: int) -> AudioAnswerInputV1:
    """Create the exact copied transfer emitted by a completed answer operation."""
    payload_digest = sha256_hex(final_payload)
    query_digest = _bytes_digest(b"pc-query-v1\0", query.encode("utf-8"))
    transfer_fields = {
        "capability": capability, "expires_at": expires_at, "final_digest": final_digest,
        "operation_id": operation_id, "payload_digest": payload_digest, "query_digest": query_digest,
        "result_digest": result_digest,
    }
    transfer_digest = _bytes_digest(b"pc-answer-transfer-v1\0", canonical_json_bytes(transfer_fields))
    return AudioAnswerInputV1(
        capability=capability, operation_id=operation_id, result_digest=result_digest,
        query_digest=query_digest, final_digest=final_digest, payload_digest=payload_digest,
        transfer_digest=transfer_digest, expires_at=expires_at, query=query, final_payload=final_payload,
    )


def retain_answer_source(value: AudioAnswerInputV1, *, capability: str, now: int) -> AudioAnswerInputV1:
    """Validate a same-capability unexpired transfer and make an immutable copy."""
    if value.capability != capability:
        raise AudioOperationError("answer transfer capability differs from Audio capability")
    if now >= value.expires_at:
        raise AudioOperationError("answer transfer has expired")
    # Reconstructing validates all digest fields again, then copies mutable bytes defensively.
    return AudioAnswerInputV1(**{**value.__dict__, "final_payload": bytes(value.final_payload)})


@dataclass(frozen=True)
class AudioSettings:
    requested_target_seconds: int
    speakers: int
    script_max_bytes: int = MAX_SCRIPT_BYTES
    chunk_chars: int = MAX_CHUNK_CHARS
    max_chunks: int = MAX_CHUNKS

    def __post_init__(self) -> None:
        object.__setattr__(self, "requested_target_seconds", _integer(self.requested_target_seconds, "requested_target_seconds", MIN_TARGET_SECONDS, MAX_TARGET_SECONDS))
        object.__setattr__(self, "speakers", _integer(self.speakers, "speakers", 1, 3))
        object.__setattr__(self, "script_max_bytes", _integer(self.script_max_bytes, "script_max_bytes", 1, MAX_SCRIPT_BYTES))
        object.__setattr__(self, "chunk_chars", _integer(self.chunk_chars, "chunk_chars", MIN_CHUNK_CHARS, MAX_CHUNK_CHARS))
        object.__setattr__(self, "max_chunks", _integer(self.max_chunks, "max_chunks", 1, MAX_CHUNKS))

    def canonical_value(self) -> dict[str, int]:
        return {"chunk_chars": self.chunk_chars, "max_chunks": self.max_chunks, "requested_target_seconds": self.requested_target_seconds, "script_max_bytes": self.script_max_bytes, "speakers": self.speakers}


@dataclass(frozen=True)
class AudioPlan:
    claim: OperationClaim
    source_digest: str
    settings: AudioSettings
    dag: tuple[str, ...]
    prompt_digest: str | None = None
    output_path: str | None = None
    work_digest: str | None = None
    disk_reservation_bytes: int = DISK_RESERVATION_BYTES
    codec_memory_bytes: int = CODEC_MEMORY_BYTES
    def canonical_execution_value(self) -> dict[str, object]:
        return {
            "claim_plan_hash": self.claim.plan_hash,
            "codec_memory_bytes": self.codec_memory_bytes,
            "dag": list(self.dag),
            "disk_reservation_bytes": self.disk_reservation_bytes,
            "output_path": self.output_path,
            "prompt_digest": self.prompt_digest,
            "settings": self.settings.canonical_value(),
            "source_digest": self.source_digest,
            "work_digest": self.work_digest,
        }

    @property
    def operation_digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self.canonical_execution_value()))


def create_audio_plan(*, operation_id: str, topic: str, source: PaperAudioInputV1 | AudioAnswerInputV1,
                      settings: AudioSettings, auth: AuthMode | str, created_at: int, expires_at: int,
                      script_model: str, tts_model: str, prompt_digest: str | None = None,
                      output_path: str | None = None, include_email: bool = False) -> AudioPlan:
    """Create a Gemini-only claim.  Approval is intentionally delegated to OperationConsent."""
    if isinstance(source, AudioAnswerInputV1):
        source_digest = source.source_digest
    elif isinstance(source, PaperAudioInputV1):
        source_digest = source.source_digest
    else:
        raise AudioOperationError("source must be a retained paper or answer input")
    if prompt_digest is not None:
        prompt_digest = _digest(prompt_digest, "prompt_digest")
    if output_path is not None:
        output_path = _text(output_path, "output_path")
        if not Path(output_path).is_absolute():
            raise AudioOperationError("output_path must be absolute")
    providers = (
        ProviderTask("gemini", _text(script_model, "script_model"), "audio.script", ()),
        ProviderTask("gemini", _text(tts_model, "tts_model"), "audio.tts", ()),
    )
    dag = ("A01.script",) + tuple(f"A02.tts.{ordinal}" for ordinal in range(1, settings.max_chunks + 1)) + ("A03.assemble",) + (("A04.email",) if include_email else ())
    work_digest = None
    if prompt_digest:
        work_digest = sha256_hex(canonical_json_bytes({
            "expected_work": list(dag),
            "hard_actual_maximum_seconds": MAX_TARGET_SECONDS,
            "requested_target_seconds": settings.requested_target_seconds,
        }))
    claim = OperationClaim(
        version=1, operation_id=operation_id, task="audio.create", command="audio.create", topic=topic,
        source="retained-audio-source", ingress="localhost", auth=auth, providers=providers,
        maxima=OperationMaxima(attempts=1 + settings.max_chunks + int(include_email), audio_seconds=MAX_TARGET_SECONDS,
                                items=settings.max_chunks, recipients=int(include_email), concurrency=4),
        input_digests=(source_digest,) + ((prompt_digest, work_digest) if prompt_digest else ()),
        resource_digests=(), write_allowlist=(output_path,) if output_path else (),
        effect_allowlist=("audio.script", "audio.tts", "audio.write"),
        created_at=created_at, expires_at=expires_at,
    )
    return AudioPlan(
        claim=claim, source_digest=source_digest, settings=settings, dag=dag,
        prompt_digest=prompt_digest, output_path=output_path, work_digest=work_digest,
    )


@dataclass(frozen=True)
class PcmChunk:
    ordinal: int
    pcm: bytes

    def __post_init__(self) -> None:
        _integer(self.ordinal, "ordinal", 1, MAX_CHUNKS)
        if not isinstance(self.pcm, bytes):
            raise AudioOperationError("PCM chunk must be bytes")

    @property
    def samples(self) -> int:
        return len(self.pcm) // PCM_BYTES_PER_SAMPLE

    @property
    def seconds(self) -> float:
        return self.samples / PCM_SAMPLE_RATE


@dataclass(frozen=True)
class AudioUsage:
    actual_pcm_samples: int
    actual_pcm_seconds: float
    timeline_seconds: float
    actual_mp3_bytes: int
    provider_billed_units: int
def validate_script(script: str, settings: AudioSettings) -> None:
    """Reject empty or oversized script before a TTS task can be prepared."""
    if (
        not isinstance(script, str)
        or not script.strip()
        or len(script.encode("utf-8")) > settings.script_max_bytes
    ):
        raise AudioOperationError("script must be nonempty and within the approved byte maximum")



def admit_chunk(prev_samples: int, ordinal: int, max_next_seconds: float) -> bool:
    """Admission control: may this ordinal be dispatched to TTS at all? (D3)

    Pure predicate, evaluated BEFORE any provider spend. It answers whether the
    already-produced PCM, the gaps this ordinal implies, and the longest audio
    the next chunk could produce still fit inside AUDIO_BUDGET_SECONDS. The
    budget is the scheduling bound only; MAX_TARGET_SECONDS remains the hard
    ceiling enforced afterwards by validate_audio_output.

    Invalid input raises instead of returning False so a caller can never read
    "this input was malformed" as "the budget is full".
    """
    _integer(prev_samples, "prev_samples", 0, MAX_CHUNKS * MAX_CHUNK_SECONDS * PCM_SAMPLE_RATE)
    _integer(ordinal, "ordinal", 1, MAX_CHUNKS)
    if (
        isinstance(max_next_seconds, bool)
        or not isinstance(max_next_seconds, (int, float))
        or not math.isfinite(max_next_seconds)
        or max_next_seconds < 0
        or max_next_seconds > MAX_CHUNK_SECONDS
    ):
        raise AudioOperationError("max_next_seconds must be a finite duration in 0..120")
    scheduled = prev_samples / PCM_SAMPLE_RATE + GAP_SECONDS * (ordinal - 1) + max_next_seconds
    return scheduled <= AUDIO_BUDGET_SECONDS


def validate_audio_output(chunks: Sequence[PcmChunk], mp3: bytes, *, playable_seconds: float,
                          provider_billed_units: int = 0) -> AudioUsage:
    """Validate only measured output; target variance is deliberately not an error."""
    if isinstance(chunks, (str, bytes)) or not 1 <= len(chunks) <= MAX_CHUNKS:
        raise AudioOperationError("Audio requires 1..32 PCM chunks")
    if not isinstance(mp3, bytes) or not mp3 or len(mp3) > MAX_MP3_BYTES:
        raise AudioOperationError("MP3 must be nonempty and no larger than 64 MiB")
    if (
        isinstance(playable_seconds, bool)
        or not isinstance(playable_seconds, (int, float))
        or not math.isfinite(playable_seconds)
        or playable_seconds < 0
        or playable_seconds > MAX_TARGET_SECONDS
    ):
        raise AudioOperationError("playable duration exceeds 3600 seconds")
    if isinstance(provider_billed_units, bool) or not isinstance(provider_billed_units, int) or provider_billed_units < 0:
        raise AudioOperationError("provider billed usage must be a nonnegative integer")
    samples = 0
    for expected, chunk in enumerate(chunks, 1):
        if not isinstance(chunk, PcmChunk) or chunk.ordinal != expected:
            raise AudioOperationError("PCM chunks must be contiguous and ordered")
        length = len(chunk.pcm)
        if not length or length % PCM_BYTES_PER_SAMPLE or length > MAX_CHUNK_BYTES:
            raise AudioOperationError("PCM chunk is not nonempty mono 24kHz s16le within byte limit")
        if chunk.seconds > MAX_CHUNK_SECONDS:
            raise AudioOperationError("PCM chunk exceeds 120 seconds")
        samples += chunk.samples
    timeline = samples / PCM_SAMPLE_RATE + GAP_SECONDS * (len(chunks) - 1)
    if timeline > MAX_TARGET_SECONDS:
        raise AudioOperationError("PCM timeline exceeds 3600 seconds")
    return AudioUsage(
        samples,
        samples / PCM_SAMPLE_RATE,
        timeline,
        len(mp3),
        provider_billed_units,
    )
def validate_output_path(root: Path, requested: Path | str) -> Path:
    """Return a new output path beneath a real local root without following links."""
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise AudioOperationError("Audio output root is unsafe")
    root = Path(os.path.abspath(root))
    candidate = Path(requested)
    if not candidate.is_absolute():
        raise AudioOperationError("Audio output path must be absolute")
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise AudioOperationError("Audio output path escapes the approved root") from exc
    if not relative.parts or candidate == root:
        raise AudioOperationError("Audio output path must name a file")
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise AudioOperationError("Audio output parent is unavailable") from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise AudioOperationError("Audio output parent is unsafe")
    try:
        info = os.lstat(candidate)
    except FileNotFoundError:
        return candidate
    except OSError as exc:
        raise AudioOperationError("Audio output path is unavailable") from exc
    if stat.S_ISLNK(info.st_mode):
        raise AudioOperationError("Audio output path is a symlink")
    raise AudioOperationError("Audio output already exists")


class FourOrdinalWindow:
    """Tracks the four verified-but-not-yet-encoder-acknowledged PCM ordinals."""

    def __init__(self, total_chunks: int) -> None:
        self.total_chunks = _integer(total_chunks, "total_chunks", 1, MAX_CHUNKS)
        self._verified: set[int] = set()
        self._acked = 0

    def may_launch(self, ordinal: int) -> bool:
        _integer(ordinal, "ordinal", 1, self.total_chunks)
        return ordinal <= self._acked + 4 and ordinal not in self._verified and ordinal > self._acked

    def verify(self, ordinal: int) -> None:
        if not self.may_launch(ordinal):
            raise AudioOperationError("ordinal is outside the four-chunk window")
        self._verified.add(ordinal)

    def acknowledge(self, ordinal: int) -> None:
        if ordinal != self._acked + 1 or ordinal not in self._verified:
            raise AudioOperationError("encoder acknowledgements must be ordered")
        self._verified.remove(ordinal)
        self._acked = ordinal


# The state format intentionally contains no source prose, credentials, or provider material.
_MARKER = "audio-operation-v1\n"
_FIXED_FILES = ("marker", "state.json", "lock")


def _lstat(path: Path) -> os.stat_result:
    try:
        return os.lstat(path)
    except OSError as exc:
        raise AudioTempRecoveryAmbiguous(f"cannot inspect Audio path {path.name}") from exc


def _owned_regular(path: Path, uid: int, mode: int) -> None:
    info = _lstat(path)
    if not stat.S_ISREG(info.st_mode) or info.st_uid != uid or stat.S_IMODE(info.st_mode) != mode or info.st_nlink != 1:
        raise AudioTempRecoveryAmbiguous(f"unsafe Audio file {path.name}")


def _owned_dir(path: Path, uid: int, mode: int) -> None:
    info = _lstat(path)
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != uid or stat.S_IMODE(info.st_mode) != mode:
        raise AudioTempRecoveryAmbiguous(f"unsafe Audio directory {path.name}")


class AudioTempStore:
    """Safe, narrow temporary state and crash scavenging for Audio only."""

    def __init__(self, root: Path | None = None, *, uid: int | None = None) -> None:
        self.uid = os.getuid() if uid is None else uid
        if root is None:
            tmp = Path(os.path.realpath(tempfile.gettempdir()))
            root = tmp / f"paper-curation-audio-v1-{self.uid}"
        self.root = Path(root)
        self.disabled_reason: str | None = None

    def _disable(self, exc: AudioTempRecoveryAmbiguous) -> None:
        self.disabled_reason = "AUDIO_TEMP_RECOVERY_AMBIGUOUS"
        raise exc

    def ensure_root(self) -> Path:
        try:
            parent = self.root.parent
            _owned_dir(parent, self.uid, stat.S_IMODE(_lstat(parent).st_mode))
            if self.root.exists() or self.root.is_symlink():
                _owned_dir(self.root, self.uid, 0o700)
            else:
                old = os.umask(0o077)
                try:
                    self.root.mkdir(mode=0o700)
                finally:
                    os.umask(old)
                _owned_dir(self.root, self.uid, 0o700)
            return self.root
        except AudioTempRecoveryAmbiguous as exc:
            self._disable(exc)

    def create_operation(self, operation_digest: str, *, expires_at: int) -> Path:
        _digest(operation_digest, "operation_digest")
        root = self.ensure_root()
        directory = root / f"audio-op-{operation_digest}"
        try:
            directory.mkdir(mode=0o700)
        except FileExistsError as exc:
            raise AudioOperationError("Audio operation directory already exists") from exc
        try:
            for name, data in (("marker", _MARKER.encode()), ("state.json", json.dumps({"expires_at": expires_at}, separators=(",", ":")).encode()), ("lock", b"")):
                fd = os.open(directory / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            self._verify_operation(directory)
        except BaseException:
            shutil.rmtree(directory, ignore_errors=True)
            raise
        return directory

    def lock_operation(self, directory: Path) -> int:
        self._verify_operation(directory)
        fd = os.open(directory / "lock", os.O_RDWR | os.O_NOFOLLOW)
        try:
            info = os.fstat(fd)
            if info.st_uid != self.uid or stat.S_IMODE(info.st_mode) != 0o600 or info.st_nlink != 1:
                raise AudioTempRecoveryAmbiguous("unsafe Audio lock")
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except BaseException:
            os.close(fd)
            raise

    def release_operation(self, lock_fd: int, directory: Path, *, remove: bool = True) -> None:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)
        if remove:
            self.remove_operation(directory)

    def _verify_operation(self, directory: Path) -> None:
        try:
            if directory.parent != self.root or not _OP_NAME.fullmatch(directory.name):
                raise AudioTempRecoveryAmbiguous("unexpected Audio operation name")
            _owned_dir(directory, self.uid, 0o700)
            names = {entry.name for entry in directory.iterdir()}
            if names != set(_FIXED_FILES):
                raise AudioTempRecoveryAmbiguous("unexpected Audio operation contents")
            for name in _FIXED_FILES:
                _owned_regular(directory / name, self.uid, 0o600)
            fd = os.open(directory / "marker", os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, "rb") as marker:
                if marker.read() != _MARKER.encode():
                    raise AudioTempRecoveryAmbiguous("invalid Audio marker")
            fd = os.open(directory / "state.json", os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, "rb") as state_file:
                state = json.loads(state_file.read().decode("utf-8"))
            if set(state) != {"expires_at"} or isinstance(state["expires_at"], bool) or not isinstance(state["expires_at"], int):
                raise AudioTempRecoveryAmbiguous("invalid Audio state marker")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AudioTempRecoveryAmbiguous("unreadable Audio operation state") from exc

    def remove_operation(self, directory: Path) -> None:
        self._verify_operation(directory)
        trash = self.root / f".{directory.name}.trash"
        if trash.exists() or trash.is_symlink():
            self._disable(AudioTempRecoveryAmbiguous("Audio trash name is occupied"))
        try:
            os.replace(directory, trash)
            root_fd = os.open(self.root, os.O_RDONLY)
            try:
                os.fsync(root_fd)
            finally:
                os.close(root_fd)
            # The tree was verified before its atomic isolation. No path outside trash is traversed.
            shutil.rmtree(trash)
        except OSError as exc:
            raise AudioOperationError("Audio cleanup failed") from exc

    def scavenge(self, *, now: int | None = None) -> int:
        """Remove only verified unlocked entries; any ambiguity leaves every entry intact."""
        self.ensure_root()
        try:
            entries = list(self.root.iterdir())
            for entry in entries:
                if not _OP_NAME.fullmatch(entry.name):
                    raise AudioTempRecoveryAmbiguous("unexpected entry in Audio root")
                self._verify_operation(entry)
            removed = 0
            for entry in entries:
                try:
                    fd = self.lock_operation(entry)
                except BlockingIOError as exc:
                    raise AudioTempRecoveryAmbiguous("Audio operation lock is held") from exc
                self.release_operation(fd, entry, remove=True)
                removed += 1
            return removed
        except AudioTempRecoveryAmbiguous as exc:
            self._disable(exc)


def cleanup_cancelled_or_expired(store: AudioTempStore, directory: Path) -> None:
    """Terminal cancellation and expiry share the same verified cleanup transition."""
    store.remove_operation(directory)
