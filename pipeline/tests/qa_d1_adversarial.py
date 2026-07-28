#!/usr/bin/env python3
"""Adversarial QA harness for D1 (single inter-chunk gap authority).

This file is deliberately not named ``test_*.py``: it is a red-team harness, not
part of the default suite.  Run it explicitly from the repository root:

    python3 pipeline/tests/qa_d1_adversarial.py

It never mutates the production modules.  Every "old behavior" and "drifted
codec" variant is materialized in a throwaway copy of the tree under a
temporary directory, and the shipped test file is executed verbatim against
that copy so the tests themselves are proven to be real discriminators.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from pipeline.lib.audio_operation import (  # noqa: E402
    AudioOperationError, GAP_SECONDS, MAX_CHUNKS, MAX_TARGET_SECONDS,
    PCM_BYTES_PER_SAMPLE, PCM_SAMPLE_RATE, PcmChunk, SILENCE_SAMPLES,
    validate_audio_output,
)
import importlib  # noqa: E402

generate_audio = importlib.import_module("pipeline.generate_audio")

TEST_FILE = "pipeline/tests/test_audio_operation.py"
CROSS_BOUNDARY = f"{TEST_FILE}::AudioOperationTests::test_python_and_codec_inter_chunk_gap_are_identical"
CONCAT = f"{TEST_FILE}::AudioOperationTests::test_concat_pcm_builds_the_shared_250ms_gap"
GAP_250 = f"{TEST_FILE}::AudioOperationTests::test_gaps_are_exactly_250ms"

OLD_SILENCE_MS = 200
OLD_SILENCE_SAMPLES = 4_800

NEW_SAMPLE_RATE_BLOCK = (
    "# Single authority, shared with the codec and the accounting layer. Declaring a\n"
    "# second literal here is what let the inter-chunk gap drift (D1).\n"
    "SAMPLE_RATE = PCM_SAMPLE_RATE\n"
)
NEW_CONCAT_BODY = '    silence = b"\\x00" * (SILENCE_SAMPLES * PCM_BYTES_PER_SAMPLE)\n'
OLD_CONCAT_BODY = '    silence = b"\\x00\\x00" * int(SAMPLE_RATE * SILENCE_MS / 1000)\n'
LIBRARY_AUTHORITY_BLOCK = (
    "# Single Python-side authority for the inter-chunk gap. The codec wrapper\n"
    "# (bin/audio-encode-lamejs.mjs) pins the same 6,000-sample block; a\n"
    "# cross-boundary test asserts the two never drift apart again (D1).\n"
    "SILENCE_SAMPLES = round(GAP_SECONDS * PCM_SAMPLE_RATE)\n"
)
CODEC_DECLARATION = "const SILENCE_SAMPLES = 6_000;"

# Minimal fd3 driver: encodes two fixed chunks and prints the realized MP3 size,
# so a codec-side gap change can be measured in bytes instead of only in source text.
CODEC_PROBE_JS = """import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const encoder = path.join(root, 'bin/audio-encode-lamejs.mjs');
const canonical = (value) => Buffer.from(JSON.stringify(Object.fromEntries(
  Object.entries(value).sort(([a], [b]) => a.localeCompare(b)))));
const digest = (value) => crypto.createHash('sha256').update(value).digest('hex');
function sine(samples, phase = 0) {
  const pcm = Buffer.alloc(samples * 2);
  for (let i = 0; i < samples; i += 1) pcm.writeInt16LE(Math.round(Math.sin((i + phase) / 12) * 12000), i * 2);
  return pcm;
}
const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'g002-gap-'));
fs.chmodSync(directory, 0o700);
const output = path.join(directory, 'audio.mp3');
const chunks = [sine(24000), sine(24000, 5)];
const frames = [
  { type: 'start', operation_id: 'gap-probe', output_path: output, sample_rate: 24000, channels: 1,
    sample_format: 's16le', bitrate_kbps: 128, chunk_count: chunks.length },
  ...chunks.map((pcm, index) => {
    const target = path.join(directory, `pcm-${index + 1}.s16le`);
    fs.writeFileSync(target, pcm, { mode: 0o600 });
    fs.chmodSync(target, 0o600);
    return { type: 'chunk', operation_id: 'gap-probe', ordinal: index + 1, path: target,
             length: pcm.length, sha256: digest(pcm) };
  }),
  { type: 'finish', operation_id: 'gap-probe' },
];
const child = spawn(process.execPath, [encoder], { stdio: ['ignore', 'ignore', 'ignore', 'pipe'] });
const channel = child.stdio[3];
const key = crypto.randomBytes(32);
const nonce = crypto.randomBytes(32).toString('base64url');
const bootstrap = canonical({ key: key.toString('base64url'), nonce, parent_pid: process.pid, type: 'bootstrap' });
channel.write(Buffer.concat([Buffer.from([0, 0, bootstrap.length >> 8, bootstrap.length & 255]), bootstrap]));
let sequence = 0;
for (const input of frames) {
  const unsigned = { ...input, schema: 1, nonce, sequence: ++sequence };
  const mac = crypto.createHmac('sha256', key).update(canonical(unsigned)).digest('hex');
  channel.write(Buffer.concat([canonical({ ...unsigned, mac }), Buffer.from('\\n')]));
}
channel.end();
child.on('close', (status) => {
  const bytes = fs.existsSync(output) ? fs.statSync(output).size : 0;
  fs.rmSync(directory, { recursive: true, force: true });
  process.stdout.write(JSON.stringify({ status, bytes }) + '\\n');
});
"""

RESULTS: list[dict] = []
COMMANDS: list[dict] = []


def record(case: str, expected: str, observed: str, verdict: str) -> None:
    RESULTS.append({"case": case, "expected": expected, "observed": observed, "verdict": verdict})
    print(f"[{verdict.upper():>6}] {case}\n         observed: {observed}", flush=True)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"scratch build: expected exactly one occurrence of {label} ({text.count(old)} found)")
    return text.replace(old, new)


def clip(value: str, limit: int) -> str:
    value = value.strip()
    return value if len(value) <= limit else value[:limit] + " …"


def tail(text: str, lines: int = 14) -> str:
    """Last meaningful output lines, clipped so a dumped module source cannot bloat the report."""
    kept = [clip(line.rstrip(), 220) for line in text.strip().splitlines() if line.strip()]
    return clip(" | ".join(kept[-lines:]), 1_200)


def build_scratch(destination: Path, *, generator: str = "new", library: str = "new",
                  codec: str = "real", node_assets: bool = False) -> Path:
    """Materialize a self-contained copy of the tree with the requested variant."""
    root = destination
    (root / "pipeline" / "tests").mkdir(parents=True, exist_ok=True)
    (root / "bin").mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        REPOSITORY / "pipeline" / "lib",
        root / "pipeline" / "lib",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copy2(REPOSITORY / "pipeline" / "config_loader.py", root / "pipeline" / "config_loader.py")
    shutil.copy2(REPOSITORY / "pipeline" / "tests" / "test_audio_operation.py",
                 root / "pipeline" / "tests" / "test_audio_operation.py")

    source = (REPOSITORY / "pipeline" / "generate_audio.py").read_text(encoding="utf-8")
    if generator == "old":
        source = replace_once(source, "    SILENCE_SAMPLES,\n", "", "SILENCE_SAMPLES import")
        source = replace_once(source, NEW_SAMPLE_RATE_BLOCK, "SAMPLE_RATE = 24_000\n", "SAMPLE_RATE block")
        source = replace_once(source, "TTS_WORKERS = 4\n",
                              f"TTS_WORKERS = 4\nSILENCE_MS = {OLD_SILENCE_MS}\n", "TTS_WORKERS anchor")
        source = replace_once(source, NEW_CONCAT_BODY, OLD_CONCAT_BODY, "concat_pcm body")
    elif generator == "renamed":
        # Old 200 ms gap reintroduced under a name the string guard does not know.
        source = replace_once(source, "    SILENCE_SAMPLES,\n", "", "SILENCE_SAMPLES import")
        source = replace_once(source, NEW_SAMPLE_RATE_BLOCK, "SAMPLE_RATE = 24_000\n", "SAMPLE_RATE block")
        source = replace_once(source, "TTS_WORKERS = 4\n",
                              f"TTS_WORKERS = 4\nGAP_MS = {OLD_SILENCE_MS}\n", "TTS_WORKERS anchor")
        source = replace_once(source, NEW_CONCAT_BODY,
                              '    silence = b"\\x00\\x00" * int(SAMPLE_RATE * GAP_MS / 1000)\n',
                              "concat_pcm body")
    (root / "pipeline" / "generate_audio.py").write_text(source, encoding="utf-8")

    if library == "old":
        module = (root / "pipeline" / "lib" / "audio_operation.py").read_text(encoding="utf-8")
        module = replace_once(module, LIBRARY_AUTHORITY_BLOCK, "", "SILENCE_SAMPLES authority block")
        (root / "pipeline" / "lib" / "audio_operation.py").write_text(module, encoding="utf-8")

    codec_source = (REPOSITORY / "bin" / "audio-encode-lamejs.mjs").read_text(encoding="utf-8")
    if codec == "literal_drift":
        codec_source = replace_once(codec_source, CODEC_DECLARATION,
                                    f"const SILENCE_SAMPLES = {OLD_SILENCE_SAMPLES:_};", "codec declaration")
    elif codec == "expression_drift":
        codec_source = replace_once(codec_source, CODEC_DECLARATION,
                                    "const SILENCE_SAMPLES = 0.20 * 24_000;", "codec declaration")
    elif codec == "shadow_drift":
        codec_source = replace_once(
            codec_source, "function chunk(frame) {\n",
            f"function chunk(frame) {{\n  const SILENCE_SAMPLES = {OLD_SILENCE_SAMPLES:_};\n",
            "chunk() opener",
        )
    (root / "bin" / "audio-encode-lamejs.mjs").write_text(codec_source, encoding="utf-8")
    if node_assets:
        shutil.copytree(REPOSITORY / "vendor", root / "vendor")
        shutil.copytree(REPOSITORY / "tests", root / "tests",
                        ignore=shutil.ignore_patterns("node_modules"))
        (root / "qa-codec-gap-probe.mjs").write_text(CODEC_PROBE_JS, encoding="utf-8")
    return root


def run(command: list[str], *, cwd: Path, label: str) -> tuple[int, str]:
    environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True, text=True, timeout=600)
    output = (process.stdout or "") + (process.stderr or "")
    COMMANDS.append({
        "label": label,
        "command": " ".join(command),
        "cwd": "<scratch>" if cwd != REPOSITORY else ".",
        "exit_code": process.returncode,
    })
    return process.returncode, output


def run_variant(label: str, node_id: str, **variant: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="g002-d1-") as directory:
        scratch = build_scratch(Path(directory) / "tree", **variant)
        return run([sys.executable, "-m", "pytest", node_id, "-q", "--tb=short", "-p", "no:cacheprovider"],
                   cwd=scratch, label=label)


# --------------------------------------------------------------------------
# 1. Discriminator proof: the shipped tests must fail against the old behavior.
# --------------------------------------------------------------------------
def discriminator_proof() -> dict:
    evidence: list[str] = []

    control_code, control_output = run_variant("control scratch (verbatim copy)", TEST_FILE)
    record(
        "harness control: verbatim scratch copy runs the shipped suite green",
        "exit 0 (scratch harness itself introduces no failure)",
        f"exit {control_code}: {tail(control_output, 2)}",
        "passed" if control_code == 0 else "failed",
    )

    old_cross_code, old_cross_output = run_variant(
        "old generator (SILENCE_MS=200) vs cross-boundary test", CROSS_BOUNDARY, generator="old")
    record(
        "discriminator: old 4,800-sample generator vs test_python_and_codec_inter_chunk_gap_are_identical",
        "test FAILS (nonzero exit) when generate_audio.SILENCE_MS=200 is reintroduced",
        f"exit {old_cross_code}: {tail(old_cross_output, 6)}",
        "passed" if old_cross_code != 0 else "failed",
    )
    evidence.append(f"[old generator / cross-boundary] exit={old_cross_code} :: {tail(old_cross_output, 6)}")

    old_concat_code, old_concat_output = run_variant(
        "old generator (SILENCE_MS=200) vs concat test", CONCAT, generator="old")
    record(
        "discriminator: old 4,800-sample generator vs test_concat_pcm_builds_the_shared_250ms_gap",
        "test FAILS with a byte-length mismatch (9,600-byte gap instead of 12,000)",
        f"exit {old_concat_code}: {tail(old_concat_output, 6)}",
        "passed" if old_concat_code != 0 else "failed",
    )
    evidence.append(f"[old generator / concat] exit={old_concat_code} :: {tail(old_concat_output, 6)}")

    old_world_code, old_world_output = run_variant(
        "fully pre-retrofit tree (no library SILENCE_SAMPLES)", TEST_FILE, generator="old", library="old")
    record(
        "discriminator: fully pre-retrofit tree (library has no SILENCE_SAMPLES authority)",
        "the shipped test module fails to import, so both D1 tests cannot pass",
        f"exit {old_world_code}: {tail(old_world_output, 4)}",
        "passed" if old_world_code != 0 else "failed",
    )
    evidence.append(f"[pre-retrofit tree] exit={old_world_code} :: {tail(old_world_output, 4)}")

    return {
        "oldBehaviorFails": old_cross_code != 0 and old_concat_code != 0 and old_world_code != 0,
        "evidence": " || ".join(evidence),
        "controlExitCode": control_code,
    }


# --------------------------------------------------------------------------
# 2. Drift injection against synthetic codec fixtures (real codec untouched).
# --------------------------------------------------------------------------
def codec_drift_probes() -> None:
    literal_code, literal_output = run_variant(
        "synthetic codec fixture SILENCE_SAMPLES = 4_800", CROSS_BOUNDARY, codec="literal_drift")
    record(
        "drift injection: synthetic codec fixture declares SILENCE_SAMPLES = 4_800",
        "cross-boundary test FAILS (Python 6,000 != codec 4,800); real codec file untouched",
        f"exit {literal_code}: {tail(literal_output, 5)}",
        "passed" if literal_code != 0 else "failed",
    )

    expression_code, expression_output = run_variant(
        "synthetic codec fixture SILENCE_SAMPLES = 0.20 * 24_000", CROSS_BOUNDARY, codec="expression_drift")
    record(
        "drift injection: synthetic codec fixture uses a non-literal expression (0.20 * 24_000)",
        "cross-boundary test fails closed because the regex finds no integer declaration",
        f"exit {expression_code}: {tail(expression_output, 5)}",
        "passed" if expression_code != 0 else "failed",
    )

    with tempfile.TemporaryDirectory(prefix="g002-d1-") as directory:
        scratch = build_scratch(Path(directory) / "tree", codec="shadow_drift")
        syntax_code, syntax_output = run(["node", "--check", "bin/audio-encode-lamejs.mjs"],
                                         cwd=scratch, label="node --check shadowed-const fixture")
        shadow_code, shadow_output = run(
            [sys.executable, "-m", "pytest", CROSS_BOUNDARY, "-q", "--tb=short", "-p", "no:cacheprovider"],
            cwd=scratch, label="shadowed-const fixture vs cross-boundary test")
    record(
        "drift injection (hardening probe): valid-JS fixture shadows SILENCE_SAMPLES = 4_800 inside chunk()",
        "cross-boundary test should notice an effective codec gap of 4,800 samples",
        f"node --check exit {syntax_code} (fixture is valid ESM); pytest exit {shadow_code}: "
        f"{tail(shadow_output, 3)}"
        + ("; guard reads only the first declaration, so the shadowed drift escapes detection"
           if shadow_code == 0 else ""),
        "passed" if shadow_code != 0 else "failed",
    )

    renamed_cross_code, renamed_cross_output = run_variant(
        "renamed Python gap constant vs cross-boundary test", CROSS_BOUNDARY, generator="renamed")
    renamed_concat_code, renamed_concat_output = run_variant(
        "renamed Python gap constant vs concat test", CONCAT, generator="renamed")
    record(
        "drift injection: 200 ms gap reintroduced in Python under a different name (GAP_MS)",
        "the D1 pair still catches it (the string guard alone would not)",
        f"cross-boundary exit {renamed_cross_code} ({tail(renamed_cross_output, 1)}); "
        f"concat exit {renamed_concat_code}: {tail(renamed_concat_output, 4)}",
        "passed" if renamed_concat_code != 0 else "failed",
    )


def codec_output_drift_probe() -> None:
    """Measure a codec-side gap change in realized MP3 bytes, not only in source text."""
    measurements: dict[str, dict] = {}
    node_suite: dict[str, int] = {}
    for variant in ("real", "literal_drift"):
        with tempfile.TemporaryDirectory(prefix="g002-d1-") as directory:
            scratch = build_scratch(Path(directory) / "tree", codec=variant, node_assets=True)
            code, output = run(["node", "qa-codec-gap-probe.mjs"], cwd=scratch,
                               label=f"fd3 gap probe ({variant} codec)")
            try:
                measurements[variant] = json.loads(output.strip().splitlines()[-1])
            except (IndexError, ValueError):
                measurements[variant] = {"status": code, "bytes": 0, "raw": tail(output, 3)}
            suite_code, _ = run(["node", "--test", "tests/audio-codec.test.mjs"], cwd=scratch,
                                label=f"node codec suite ({variant} codec)")
            node_suite[variant] = suite_code

    real_bytes = measurements["real"].get("bytes", 0)
    drift_bytes = measurements["literal_drift"].get("bytes", 0)
    # 128 kbps CBR: 1,200 fewer silence samples == 0.05 s == 800 fewer MP3 bytes.
    expected_delta = round((SILENCE_SAMPLES - OLD_SILENCE_SAMPLES) / PCM_SAMPLE_RATE * 128_000 / 8)
    record(
        "behavioral proof: a 4,800-sample codec fixture really shortens the encoded MP3",
        f"two 1 s chunks encode ~{expected_delta} bytes smaller with a 4,800-sample gap "
        "(0.05 s at 128 kbps CBR)",
        f"real codec: {real_bytes} bytes (exit {measurements['real'].get('status')}); "
        f"drifted fixture: {drift_bytes} bytes; delta={real_bytes - drift_bytes} bytes",
        "passed" if real_bytes and drift_bytes and abs((real_bytes - drift_bytes) - expected_delta) <= 64
        else "failed",
    )
    record(
        "coverage gap (non-blocking): node --test tests/audio-codec.test.mjs against the 4,800-sample fixture",
        "the Node codec suite should also detect a codec-side gap regression",
        f"real codec exit {node_suite['real']}; drifted fixture exit {node_suite['literal_drift']}"
        + ("; the Node suite never asserts the gap size, so codec-side drift is caught only by the "
           "Python cross-boundary regex" if node_suite["literal_drift"] == 0 else ""),
        "passed" if node_suite["literal_drift"] != 0 else "failed",
    )


# --------------------------------------------------------------------------
# 3. Adversarial cases against the real, unmodified production modules.
# --------------------------------------------------------------------------
def concat_probes() -> None:
    gap_bytes = SILENCE_SAMPLES * PCM_BYTES_PER_SAMPLE

    empty = generate_audio.concat_pcm([])
    record(
        "adversarial: concat_pcm([]) on an empty part list",
        "returns b'' without raising and without emitting a gap",
        f"len={len(empty)} bytes, type={type(empty).__name__}",
        "passed" if empty == b"" else "failed",
    )

    single = generate_audio.concat_pcm([b"\x11\x22" * 1_000])
    record(
        "adversarial: concat_pcm with exactly one part adds zero gap",
        "output length equals the single part length (2,000 bytes)",
        f"len={len(single)} bytes, added={len(single) - 2_000}",
        "passed" if len(single) == 2_000 else "failed",
    )

    part = b"\x01\x02" * 512
    parts = [part] * MAX_CHUNKS
    joined = generate_audio.concat_pcm(parts)
    added_bytes = len(joined) - sum(map(len, parts))
    expected_bytes = (MAX_CHUNKS - 1) * SILENCE_SAMPLES * PCM_BYTES_PER_SAMPLE
    added_seconds = added_bytes / PCM_BYTES_PER_SAMPLE / PCM_SAMPLE_RATE
    old_seconds = (MAX_CHUNKS - 1) * OLD_SILENCE_SAMPLES / PCM_SAMPLE_RATE
    silence_only = joined[len(part):len(part) + gap_bytes]
    record(
        "adversarial: 32 parts / 31 gaps adds exactly 31 * 6000 * 2 bytes = 7.75 s",
        f"added silence == {expected_bytes} bytes == 7.75 s (old 4,800-sample gap gave {old_seconds:.2f} s)",
        f"added={added_bytes} bytes == {added_seconds:.4f} s; growth vs old = "
        f"{added_seconds - old_seconds:.4f} s; injected block is all-zero: {set(silence_only) == {0}}",
        "passed" if (added_bytes == expected_bytes and abs(added_seconds - 7.75) < 1e-9
                     and abs((added_seconds - old_seconds) - 1.55) < 1e-9
                     and set(silence_only) == {0}) else "failed",
    )

    odd_parts = [b"\x01" * 3, b"\x02" * 4]
    odd_joined = generate_audio.concat_pcm(odd_parts)
    codec_source = (REPOSITORY / "bin" / "audio-encode-lamejs.mjs").read_text(encoding="utf-8")
    codec_guard = "frame.length % 2" in codec_source
    try:
        validate_audio_output([PcmChunk(1, odd_joined)], b"mp3", playable_seconds=1)
        rejected = "accepted (no downstream guard)"
        odd_ok = False
    except AudioOperationError as error:
        rejected = f"AudioOperationError: {error}"
        odd_ok = True
    record(
        "adversarial: odd-length / non-even-byte parts never yield a silent half-sample",
        "the injected gap stays a whole number of samples, byte parity is passed through unmodified, "
        "and the misaligned buffer is rejected downstream instead of being padded or truncated",
        f"gap_bytes={gap_bytes} (even, {gap_bytes // PCM_BYTES_PER_SAMPLE} whole samples); "
        f"joined={len(odd_joined)} bytes (odd={len(odd_joined) % 2 == 1}) == "
        f"{sum(map(len, odd_parts))} input + {gap_bytes} gap; validate_audio_output -> {rejected}; "
        f"codec rejects odd chunk lengths ('frame.length % 2'): {codec_guard}",
        "passed" if (gap_bytes % PCM_BYTES_PER_SAMPLE == 0
                     and len(odd_joined) == sum(map(len, odd_parts)) + gap_bytes
                     and odd_ok and codec_guard) else "failed",
    )

    references = subprocess.run(
        ["git", "grep", "-n", "concat_pcm"], cwd=REPOSITORY, capture_output=True, text=True,
    ).stdout.strip().splitlines()
    non_test = [line for line in references if not line.startswith("pipeline/tests/")]
    record(
        "scope check: which production callers realize the Python-side gap",
        "report every non-test reference to concat_pcm",
        f"tracked references: {len(references)}; non-test references: {non_test or 'none'}",
        "passed",
    )


# --------------------------------------------------------------------------
# 4. Boundary / interaction probe against MAX_TARGET_SECONDS.
# --------------------------------------------------------------------------
def boundary_probe() -> dict:
    gaps = MAX_CHUNKS - 1
    ceiling_pcm_seconds = MAX_TARGET_SECONDS - GAP_SECONDS * gaps
    old_realized = ceiling_pcm_seconds + (OLD_SILENCE_SAMPLES / PCM_SAMPLE_RATE) * gaps
    new_realized = ceiling_pcm_seconds + (SILENCE_SAMPLES / PCM_SAMPLE_RATE) * gaps
    growth = new_realized - old_realized

    ceiling_samples = round(ceiling_pcm_seconds * PCM_SAMPLE_RATE)
    per_chunk = ceiling_samples // MAX_CHUNKS + 1
    last = ceiling_samples - per_chunk * (MAX_CHUNKS - 1)
    block = b"\x00" * (per_chunk * PCM_BYTES_PER_SAMPLE)
    chunks = [PcmChunk(ordinal, block) for ordinal in range(1, MAX_CHUNKS)]
    chunks.append(PcmChunk(MAX_CHUNKS, b"\x00" * (last * PCM_BYTES_PER_SAMPLE)))
    at_ceiling = validate_audio_output(chunks, b"mp3", playable_seconds=new_realized)

    over = list(chunks[:-1]) + [PcmChunk(MAX_CHUNKS, b"\x00" * ((last + 1) * PCM_BYTES_PER_SAMPLE))]
    try:
        validate_audio_output(over, b"mp3", playable_seconds=0)
        timeline_guard = "accepted (no timeline guard)"
    except AudioOperationError as error:
        timeline_guard = f"rejected: {error}"

    # One lamejs/lameenc MP3 frame at 24 kHz is 1,152 samples = 48 ms of padding.
    padded = new_realized + 1_152 / PCM_SAMPLE_RATE
    try:
        validate_audio_output(chunks, b"mp3", playable_seconds=padded)
        padded_result = "accepted"
    except AudioOperationError as error:
        padded_result = f"rejected: {error}"
    try:
        generate_audio.validate_playable_duration(padded)
        approval_result = "accepted"
    except generate_audio.AudioApprovalError as error:
        approval_result = f"rejected: {error}"

    arithmetic = (
        f"MAX_CHUNKS={MAX_CHUNKS} allows {gaps} gaps. The accounting timeline in validate_audio_output "
        f"has always used GAP_SECONDS={GAP_SECONDS} (D1 does not change it), so a run that passes the "
        f"timeline gate has at most {ceiling_pcm_seconds} s of PCM "
        f"({MAX_TARGET_SECONDS} - {GAP_SECONDS} * {gaps}); measured empirically, "
        f"{ceiling_samples} samples over 32 chunks yields timeline={at_ceiling.timeline_seconds} s "
        f"(accepted) and one extra sample is {timeline_guard}. Realized Python-side output for that same "
        f"maximum-length run: old = {ceiling_pcm_seconds} + (4800/24000) * {gaps} = {old_realized} s; "
        f"new = {ceiling_pcm_seconds} + (6000/24000) * {gaps} = {new_realized} s; growth = {growth:.3f} s "
        f"(0.050 s per gap). Headroom under MAX_TARGET_SECONDS={MAX_TARGET_SECONDS} therefore falls from "
        f"{MAX_TARGET_SECONDS - old_realized:.3f} s to {MAX_TARGET_SECONDS - new_realized:.3f} s. Adding a "
        f"single 1,152-sample MP3 frame of encoder padding (0.048 s) gives {padded:.3f} s, which "
        f"validate_audio_output {padded_result} and generate_audio.validate_playable_duration "
        f"{approval_result}."
    )
    conclusion = (
        "No previously-valid run is rejected by arithmetic alone: because the accounting timeline already "
        "charged 250 ms per gap, the worst realized duration after D1 is exactly 3600.000 s, which the "
        "3600-second gate still accepts. The risk is that D1 consumes the entire 1.55 s of slack that used "
        "to sit between the accounted timeline and the realized audio, so a maximum-length run now has zero "
        "tolerance for measurement or MP3 encoder padding; 48 ms of lame frame padding is enough to trip "
        "AUDIO_PLAYABLE_DURATION_EXCEEDED where it previously could not. This only bites on the Python-side "
        "concat_pcm assembly path (the fd3 codec already emitted 6,000-sample gaps, so the server path is "
        "unchanged). Reported as the slice-6 interaction risk; not fixed here."
    )
    record(
        "boundary probe: 50 ms-per-gap growth vs MAX_TARGET_SECONDS = 3600",
        "quantify whether a previously-valid maximum-length run can now exceed the 3600-second gate",
        f"ceiling PCM {ceiling_pcm_seconds} s; realized {old_realized} s -> {new_realized} s "
        f"(+{growth:.3f} s); headroom {MAX_TARGET_SECONDS - old_realized:.3f} s -> "
        f"{MAX_TARGET_SECONDS - new_realized:.3f} s; with 48 ms encoder padding: {padded_result}",
        "passed",
    )
    return {"arithmetic": arithmetic, "conclusion": conclusion}


# --------------------------------------------------------------------------
# 5. Required suites.
# --------------------------------------------------------------------------
def required_suites() -> None:
    gap_code, gap_output = run(
        [sys.executable, "-m", "pytest", GAP_250, "-q", "-p", "no:cacheprovider"],
        cwd=REPOSITORY, label="regression: test_gaps_are_exactly_250ms")
    record(
        "regression: pipeline/tests/test_audio_operation.py::test_gaps_are_exactly_250ms stays green",
        "exit 0",
        f"exit {gap_code}: {tail(gap_output, 2)}",
        "passed" if gap_code == 0 else "failed",
    )

    python_code, python_output = run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-q", "-p", "no:cacheprovider"],
        cwd=REPOSITORY, label="python suite")
    record(
        "suite: python3 -m pytest pipeline/tests/test_audio_operation.py -q",
        "exit 0, all tests pass",
        f"exit {python_code}: {tail(python_output, 2)}",
        "passed" if python_code == 0 else "failed",
    )

    node_code, node_output = run(["node", "--test", "tests/audio-codec.test.mjs"],
                                 cwd=REPOSITORY, label="node codec suite")
    summary = " | ".join(line.strip() for line in node_output.splitlines()
                         if line.strip().startswith(("# tests", "# pass", "# fail", "ℹ tests", "ℹ pass", "ℹ fail")))
    record(
        "suite: node --test tests/audio-codec.test.mjs",
        "exit 0, all tests pass with the real 6,000-sample codec gap",
        f"exit {node_code}: {summary or tail(node_output, 3)}",
        "passed" if node_code == 0 else "failed",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Adversarial QA harness for D1")
    parser.add_argument("--report", default="artifacts/g002-d1-qa-report.json")
    arguments = parser.parse_args()

    proof = discriminator_proof()
    codec_drift_probes()
    codec_output_drift_probe()
    concat_probes()
    probe = boundary_probe()
    required_suites()

    passed = sum(1 for item in RESULTS if item["verdict"] == "passed")
    failed = sum(1 for item in RESULTS if item["verdict"] == "failed")
    report = {
        "schemaVersion": 1,
        "kind": "package-test-report",
        "goal": "G002",
        "contract": "D1 single gap authority",
        "commands": COMMANDS,
        "results": RESULTS,
        "discriminatorProof": proof,
        "boundaryProbe": probe,
        "summary": {"passed": passed, "failed": failed},
    }
    destination = Path(arguments.report)
    if not destination.is_absolute():
        destination = REPOSITORY / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {destination} (passed={passed} failed={failed})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
