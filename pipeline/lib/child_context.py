"""Fail-closed fd3 operation-context transport.

The transport is deliberately provider-independent.  It moves a bounded child
subclaim over an anonymous Unix stream; operation authority and secrets stay
in memory and are never serialized to an argv, environment, or filesystem.
"""
from __future__ import annotations

import base64
import hmac
import os
import secrets
import select
import socket
import stat
import struct
import time
from dataclasses import dataclass, field
from typing import Mapping, Sequence

from pipeline.lib.operation_consent import canonical_json_bytes, sha256_hex

FD3 = 3
KEY_BYTES = 32
NONCE_BYTES = 32
MAC_BYTES = 32
MAX_FRAME_BYTES = 64 * 1024


class ChildContextError(ValueError):
    """Base class for a rejected or unavailable operation-context channel."""


class ChildContextUnavailableError(ChildContextError):
    pass


class ChildContextVerificationError(ChildContextError):
    pass


class ChildContextEOFError(ChildContextError):
    pass


class ChildContextTimeoutError(ChildContextError):
    pass


class ChildContextCancelledError(ChildContextError):
    pass


class ChildContextFrameError(ChildContextError):
    pass


def _text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ChildContextError(f"{name} must be a nonempty string")
    return value


def _digest(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ChildContextError(f"{name} must be a lowercase SHA-256 digest")
    return value


def _budget(value: Mapping[str, int], name: str) -> dict[str, int]:
    if not isinstance(value, Mapping):
        raise ChildContextError(f"{name} must be a mapping")
    result: dict[str, int] = {}
    for key, amount in value.items():
        key = _text(key, f"{name} key")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
            raise ChildContextError(f"{name} values must be nonnegative integers")
        result[key] = amount
    return result


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64_decode(value: object, name: str, expected_size: int) -> bytes:
    if not isinstance(value, str) or "=" in value:
        raise ChildContextFrameError(f"{name} is not canonical base64url")
    try:
        decoded = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except (ValueError, UnicodeError) as exc:
        raise ChildContextFrameError(f"{name} is not canonical base64url") from exc
    if len(decoded) != expected_size or _b64_encode(decoded) != value:
        raise ChildContextFrameError(f"{name} has an invalid size or encoding")
    return decoded


@dataclass(frozen=True, repr=False)
class ChildOperationContext:
    """The operation subclaim a child asks the parent to accept."""

    operation_id: str
    subclaim_digest: str
    member: str
    budget: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "operation_id", _text(self.operation_id, "operation_id"))
        object.__setattr__(self, "subclaim_digest", _digest(self.subclaim_digest, "subclaim_digest"))
        object.__setattr__(self, "member", _text(self.member, "member"))
        object.__setattr__(self, "budget", _budget(self.budget, "budget"))

    def canonical_value(self) -> dict[str, object]:
        return {
            "budget": dict(self.budget),
            "member": self.member,
            "operation_id": self.operation_id,
            "subclaim_digest": self.subclaim_digest,
        }

    def __repr__(self) -> str:
        return "ChildOperationContext(<redacted>)"

    __str__ = __repr__


@dataclass(frozen=True, repr=False)
class ChildContextPolicy:
    """Exact parent-side bounds that a child context must satisfy."""

    operation_id: str
    subclaim_digest: str
    members: Sequence[str]
    budget: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "operation_id", _text(self.operation_id, "operation_id"))
        object.__setattr__(self, "subclaim_digest", _digest(self.subclaim_digest, "subclaim_digest"))
        if isinstance(self.members, (str, bytes)):
            raise ChildContextError("members must be a sequence")
        members = tuple(_text(member, "member") for member in self.members)
        if not members:
            raise ChildContextError("members must not be empty")
        object.__setattr__(self, "members", members)
        object.__setattr__(self, "budget", _budget(self.budget, "budget"))

    def __repr__(self) -> str:
        return "ChildContextPolicy(<redacted>)"

    __str__ = __repr__


class Fd3Socketpair:
    """Parent/child Unix socketpair with explicit child fd3 installation."""

    __slots__ = ("parent", "child")

    def __init__(self, parent: socket.socket, child: socket.socket) -> None:
        self.parent = parent
        self.child = child

    @classmethod
    def create(cls) -> "Fd3Socketpair":
        parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        parent.set_inheritable(False)
        child.set_inheritable(False)
        return cls(parent, child)

    def install_child_fd3(self) -> None:
        """Duplicate the child endpoint onto inheritable descriptor 3.

        Call only in the child immediately before exec.  The original child
        descriptor is closed after duplication, including when it was already
        descriptor 3.
        """
        if self.child is None:
            raise ChildContextUnavailableError("child endpoint is already closed")
        fd = self.child.detach()
        try:
            if fd != FD3:
                os.dup2(fd, FD3, inheritable=True)
                os.close(fd)
            else:
                os.set_inheritable(FD3, True)
        except BaseException:
            if fd != FD3:
                try:
                    os.close(fd)
                except OSError:
                    pass
            raise

    def close_parent(self) -> None:
        self.parent.close()

    def close_child(self) -> None:
        self.child.close()

    def close(self) -> None:
        for endpoint in (self.parent, self.child):
            try:
                endpoint.close()
            except OSError:
                pass

    def __repr__(self) -> str:
        return "Fd3Socketpair(<redacted>)"


def _check_socket_fd(fd: int) -> socket.socket:
    if fd != FD3:
        raise ChildContextUnavailableError("operation context is only accepted on fd 3")
    try:
        mode = os.fstat(fd).st_mode
    except OSError as exc:
        raise ChildContextUnavailableError("fd 3 is unavailable") from exc
    if not stat.S_ISSOCK(mode):
        raise ChildContextUnavailableError("fd 3 is not a socket")
    try:
        channel = socket.socket(fileno=fd)
    except OSError as exc:
        raise ChildContextUnavailableError("fd 3 cannot be opened as a socket") from exc
    if channel.family != socket.AF_UNIX or (channel.type & socket.SOCK_STREAM) != socket.SOCK_STREAM:
        channel.close()
        raise ChildContextUnavailableError("fd 3 must be an AF_UNIX SOCK_STREAM socket")
    return channel


def _cancelled(cancel: object | None) -> bool:
    if cancel is None:
        return False
    checker = getattr(cancel, "is_set", None)
    return bool(checker()) if callable(checker) else bool(cancel() if callable(cancel) else cancel)


def _recv_exact(channel: socket.socket, size: int, deadline: float | None, cancel: object | None) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        if _cancelled(cancel):
            raise ChildContextCancelledError("operation context receive was cancelled")
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise ChildContextTimeoutError("operation context receive timed out")
        readable, _, _ = select.select([channel], [], [], remaining)
        if not readable:
            raise ChildContextTimeoutError("operation context receive timed out")
        chunk = channel.recv(size - len(chunks))
        if not chunk:
            raise ChildContextEOFError("operation context channel closed")
        chunks.extend(chunk)
    return bytes(chunks)


def _send_frame(channel: socket.socket, value: Mapping[str, object]) -> None:
    payload = canonical_json_bytes(value)
    if not payload or len(payload) > MAX_FRAME_BYTES:
        raise ChildContextFrameError("operation context frame exceeds the size limit")
    channel.sendall(struct.pack("!I", len(payload)) + payload)


def _recv_frame(channel: socket.socket, timeout: float | None, cancel: object | None) -> dict[str, object]:
    if timeout is not None and (isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout < 0):
        raise ChildContextError("timeout must be a nonnegative number or None")
    deadline = None if timeout is None else time.monotonic() + timeout
    length = struct.unpack("!I", _recv_exact(channel, 4, deadline, cancel))[0]
    if not length or length > MAX_FRAME_BYTES:
        raise ChildContextFrameError("operation context frame exceeds the size limit")
    try:
        import json
        payload = _recv_exact(channel, length, deadline, cancel)
        decoded = json.loads(payload.decode("utf-8"))
        canonical = canonical_json_bytes(decoded)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ChildContextFrameError("operation context frame is not canonical JSON") from exc
    if not isinstance(decoded, dict) or canonical != payload:
        raise ChildContextFrameError("operation context frame is not canonical JSON")
    return decoded


class _Channel:
    __slots__ = ("_channel", "_key", "_nonce", "_outgoing", "_incoming", "_closed")

    def __init__(self, channel: socket.socket, key: bytes, nonce: bytes) -> None:
        self._channel = channel
        self._key = bytearray(key)
        self._nonce = nonce
        self._outgoing = 0
        self._incoming = 0
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        for index in range(len(self._key)):
            self._key[index] = 0
        self._nonce = b""
        try:
            self._channel.close()
        except OSError:
            pass

    def _fail(self, error: ChildContextError):
        self.close()
        raise error

    def _signed(self, body: Mapping[str, object], pid: int) -> dict[str, object]:
        self._outgoing += 1
        signed = {"body": dict(body), "nonce": _b64_encode(self._nonce), "pid": pid, "seq": self._outgoing}
        mac = hmac.digest(bytes(self._key), canonical_json_bytes(signed), "sha256")
        return {**signed, "mac": _b64_encode(mac)}

    def _verify(self, frame: Mapping[str, object], expected_pid: int | None) -> dict[str, object]:
        if set(frame) != {"body", "mac", "nonce", "pid", "seq"}:
            self._fail(ChildContextFrameError("operation context frame has unexpected fields"))
        try:
            nonce = _b64_decode(frame["nonce"], "nonce", NONCE_BYTES)
            mac = _b64_decode(frame["mac"], "mac", MAC_BYTES)
            sequence = frame["seq"]
            pid = frame["pid"]
            body = frame["body"]
            if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence != self._incoming + 1:
                raise ChildContextVerificationError("operation context sequence is not monotonic")
            if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
                raise ChildContextVerificationError("operation context pid is invalid")
            if expected_pid is not None and pid != expected_pid:
                raise ChildContextVerificationError("operation context pid differs from the expected child")
            if not isinstance(body, dict) or nonce != self._nonce:
                raise ChildContextVerificationError("operation context nonce is invalid")
            signed = {"body": body, "nonce": frame["nonce"], "pid": pid, "seq": sequence}
            expected_mac = hmac.digest(bytes(self._key), canonical_json_bytes(signed), "sha256")
            if not hmac.compare_digest(mac, expected_mac):
                raise ChildContextVerificationError("operation context MAC is invalid")
        except ChildContextError as exc:
            self._fail(exc)
        except (KeyError, TypeError, ValueError) as exc:
            self._fail(ChildContextFrameError("operation context frame is malformed"))
        self._incoming = sequence
        return body


class ParentChildContext(_Channel):
    """Parent endpoint.  It sends bootstrap material only through its socket."""

    @classmethod
    def open(cls, channel: socket.socket, *, parent_pid: int | None = None) -> "ParentChildContext":
        if not isinstance(channel, socket.socket) or channel.family != socket.AF_UNIX or (channel.type & socket.SOCK_STREAM) != socket.SOCK_STREAM:
            raise ChildContextUnavailableError("parent context channel must be an AF_UNIX SOCK_STREAM socket")
        pid = os.getpid() if parent_pid is None else parent_pid
        if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
            raise ChildContextError("parent_pid must be a positive integer")
        key = secrets.token_bytes(KEY_BYTES)
        nonce = secrets.token_bytes(NONCE_BYTES)
        result = cls(channel, key, nonce)
        try:
            _send_frame(channel, {"key": _b64_encode(key), "nonce": _b64_encode(nonce), "parent_pid": pid, "type": "bootstrap"})
        except (ChildContextError, OSError) as exc:
            result.close()
            if isinstance(exc, ChildContextError):
                raise
            raise ChildContextUnavailableError("operation context bootstrap could not be sent") from exc
        return result

    def receive(self, policy: ChildContextPolicy, *, expected_child_pid: int, timeout: float | None = None, cancel: object | None = None) -> ChildOperationContext:
        if not isinstance(policy, ChildContextPolicy):
            self._fail(ChildContextError("policy must be a ChildContextPolicy"))
        if isinstance(expected_child_pid, bool) or not isinstance(expected_child_pid, int) or expected_child_pid <= 0:
            self._fail(ChildContextError("expected_child_pid must be a positive integer"))
        try:
            body = self._verify(_recv_frame(self._channel, timeout, cancel), expected_child_pid)
            context = _context_from_body(body)
            _verify_policy(context, policy)
            return context
        except ChildContextError as exc:
            self._fail(exc)


class ChildParentContext(_Channel):
    """Child endpoint loaded exclusively from fd3."""

    @classmethod
    def from_fd3(cls, *, expected_parent_pid: int | None = None, timeout: float | None = None, cancel: object | None = None) -> "ChildParentContext":
        channel = _check_socket_fd(FD3)
        try:
            bootstrap = _recv_frame(channel, timeout, cancel)
            if set(bootstrap) != {"key", "nonce", "parent_pid", "type"} or bootstrap["type"] != "bootstrap":
                raise ChildContextFrameError("operation context bootstrap is malformed")
            parent_pid = bootstrap["parent_pid"]
            if isinstance(parent_pid, bool) or not isinstance(parent_pid, int) or parent_pid <= 0:
                raise ChildContextFrameError("operation context bootstrap parent pid is invalid")
            expected = os.getppid() if expected_parent_pid is None else expected_parent_pid
            if parent_pid != expected:
                raise ChildContextVerificationError("operation context parent lineage differs")
            return cls(channel, _b64_decode(bootstrap["key"], "key", KEY_BYTES), _b64_decode(bootstrap["nonce"], "nonce", NONCE_BYTES))
        except ChildContextError:
            channel.close()
            raise

    def send(self, context: ChildOperationContext, *, pid: int | None = None) -> None:
        if not isinstance(context, ChildOperationContext):
            self._fail(ChildContextError("context must be a ChildOperationContext"))
        try:
            _send_frame(self._channel, self._signed(context.canonical_value(), os.getpid() if pid is None else pid))
        except ChildContextError as exc:
            self._fail(exc)


def _context_from_body(body: Mapping[str, object]) -> ChildOperationContext:
    if set(body) != {"budget", "member", "operation_id", "subclaim_digest"}:
        raise ChildContextFrameError("operation context body has unexpected fields")
    try:
        return ChildOperationContext(
            operation_id=body["operation_id"],  # type: ignore[arg-type]
            subclaim_digest=body["subclaim_digest"],  # type: ignore[arg-type]
            member=body["member"],  # type: ignore[arg-type]
            budget=body["budget"],  # type: ignore[arg-type]
        )
    except ChildContextError as exc:
        raise ChildContextVerificationError("operation context body is invalid") from exc


def _verify_policy(context: ChildOperationContext, policy: ChildContextPolicy) -> None:
    if context.operation_id != policy.operation_id:
        raise ChildContextVerificationError("operation context operation differs")
    if context.subclaim_digest != policy.subclaim_digest:
        raise ChildContextVerificationError("operation context subclaim digest differs")
    if context.member not in policy.members:
        raise ChildContextVerificationError("operation context member is not authorized")
    if set(context.budget) != set(policy.budget) or any(context.budget[name] > policy.budget[name] for name in policy.budget):
        raise ChildContextVerificationError("operation context budget exceeds authorization")


def operation_subclaim_digest(operation_id: str, subclaim: Mapping[str, object]) -> str:
    """Canonical digest used to bind an operation identifier to its subclaim."""
    return sha256_hex(canonical_json_bytes({"operation_id": _text(operation_id, "operation_id"), "subclaim": dict(subclaim)}))
