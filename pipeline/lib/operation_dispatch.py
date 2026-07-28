"""Authoritative, provider-free operation dispatch.

This module is the only mutable boundary between an approved operation and a
worker.  Workers receive opaque, single-use ready-step credentials; they never
supply prompts, queries, recipients, or source chunks.
"""
from __future__ import annotations

import base64
import secrets
import threading
import time
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Mapping, Sequence

from . import operation_dags
from .audio_operation import AudioPlan
from .operation_consent import (
    ApprovalCredential, ConsentError, OperationClaim, OperationConsent,
    canonical_json_bytes, sha256_hex,
)

FINAL_TTL_SECONDS = 300
IDEMPOTENCY_TTL_SECONDS = 600
EVENT_LIMIT = 64
DELTA_LIMIT_BYTES = 64 * 1024


class DispatchError(ConsentError):
    pass


class DispatchCredentialError(DispatchError):
    pass


class DispatchConflictError(DispatchError):
    pass


class DispatchStateError(DispatchError):
    pass


@dataclass(frozen=True)
class ReadyStep:
    operation_id: str
    step_id: str
    kind: str
    input_digest: str
    predecessor_digest: str
    ordinal: int
    attempt: int
    reservation: int
    expires_at: int
    credential: str


@dataclass(frozen=True)
class FinalDelivery:
    capability: str
    credential: str
    expires_at: int


@dataclass
class _StepAuthority:
    step: operation_dags.Step
    ordinal: int
    attempt: int
    credential: str
    input_digest: str
    predecessor_digest: str
    consumed: bool = False


@dataclass
class _Request:
    digest: str
    expires_at: int
    complete: bool = False
    response: Any = None


@dataclass
class _DeliveryState:
    payload: bytes
    digest: str
    expires_at: int
    credential: str
    used: bool = False
    retry_available: bool = True
    keys: dict[str, _Request] = field(default_factory=dict)


@dataclass
class _Operation:
    claim: OperationClaim
    dag: operation_dags.QueryDag
    retained: bytes
    retained_digest: str
    state: operation_dags.QueryState
    expires_at: int
    terminal: str | None = None
    step_authorities: dict[str, _StepAuthority] = field(default_factory=dict)
    completed_digests: dict[str, str] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    requests: dict[tuple[str, str], _Request] = field(default_factory=dict)
    final: _DeliveryState | None = None


def _token() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii").rstrip("=")


def _digest(value: Any) -> str:
    return sha256_hex(canonical_json_bytes(value))


def _key(value: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise DispatchError("idempotency key must be a 64-character lowercase hexadecimal digest")
    return value


def _audio_dag(plan: AudioPlan) -> operation_dags.QueryDag:
    steps: list[operation_dags.Step] = []
    chunks = [name for name in plan.dag if name.startswith("A02.tts.")]
    for name in plan.dag:
        if name == "A01.script":
            deps: tuple[str, ...] = ()
        elif name.startswith("A02.tts."):
            deps = ("A01.script",)
        elif name == "A03.assemble":
            deps = tuple(chunks)
        else:
            deps = ("A03.assemble",)
        steps.append(operation_dags.Step(name, name, False, deps))
    return operation_dags.QueryDag("audio.create", "retained-audio-source", 600, 4, 1, tuple(steps), {})


class OperationDispatcher:
    """Thread-safe in-memory authority; restart invalidates every issued secret."""

    def __init__(self, consent: OperationConsent | None = None, *, clock: Callable[[], float] = time.time) -> None:
        self.consent = consent or OperationConsent(clock=clock)
        self._clock = clock
        self._lock = threading.RLock()
        self._operations: dict[str, _Operation] = {}
        # Provider adapters are opt-in: no registration means dispatch remains
        # provider-free and cannot construct an effect-adjacent client.
        self._adapter_steps: dict[tuple[str, str], Callable[[OperationClaim, ReadyStep, Any], Any]] = {}

    def register_plan(self, claim: OperationClaim, dag: operation_dags.QueryDag | AudioPlan,
                      retained_inputs: Mapping[str, Any] | Sequence[Any] | bytes) -> str:
        """Freeze the exact planned DAG and retained inputs before approval."""
        if isinstance(dag, AudioPlan):
            if dag.claim.plan_hash != claim.plan_hash:
                raise DispatchConflictError("Audio plan does not match operation claim")
            frozen_dag = _audio_dag(dag)
        elif isinstance(dag, operation_dags.QueryDag):
            frozen_dag = dag
        else:
            raise DispatchError("dag must be a QueryDag or AudioPlan")
        retained = retained_inputs if isinstance(retained_inputs, bytes) else canonical_json_bytes(retained_inputs)
        # Canonical bytes are intentionally copied and never re-read from a caller.
        retained = bytes(retained)
        operation_digest = self._operation_digest(
            frozen_dag, sha256_hex(retained), claim.expires_at
        )
        with self._lock:
            self._cleanup_locked()
            existing = self._operations.get(claim.operation_id)
            if existing is not None:
                if self._operation_digest(
                    existing.dag, existing.retained_digest, existing.expires_at
                ) != operation_digest:
                    raise DispatchConflictError("operation id is already bound to retained inputs or DAG")
                self.consent.create_plan(claim)
                self.consent.bind_plan(claim.operation_id, claim.plan_hash, operation_digest)
                return operation_digest
            self.consent.create_plan(claim)
            self.consent.bind_plan(claim.operation_id, claim.plan_hash, operation_digest)
            self._operations[claim.operation_id] = _Operation(
                claim, frozen_dag, retained, sha256_hex(retained), operation_dags.start(frozen_dag), claim.expires_at
            )
            return operation_digest

    def redeem(self, credential: ApprovalCredential | str, claim: OperationClaim) -> tuple[ReadyStep, ...]:
        """Redeem approval exactly once and issue only the frozen initial steps."""
        with self._lock:
            self._cleanup_locked()
            operation = self._operations.get(claim.operation_id)
            if operation is None or operation.claim.plan_hash != claim.plan_hash:
                raise DispatchConflictError("operation is not registered with this dispatcher")
            if self._operation_digest(
                operation.dag, operation.retained_digest, operation.expires_at
            ) != self._operation_digest(
                operation.dag, sha256_hex(operation.retained), operation.expires_at
            ):
                raise DispatchConflictError("frozen retained inputs do not match their digest")
            if operation.terminal:
                raise DispatchStateError("operation is terminal")
            self.consent.redeem(credential, claim)
            return self._issue_ready_locked(operation)

    # Descriptive alias used by transport adapters.
    start = redeem

    def ready_steps(self, operation_id: str) -> tuple[ReadyStep, ...]:
        with self._lock:
            self._cleanup_locked()
            operation = self._require_running_locked(operation_id)
            return tuple(self._ready_value(operation, authority) for authority in operation.step_authorities.values() if not authority.consumed)
    def register_adapter(self, operation_id: str, step_id: str,
                         adapter: Callable[[OperationClaim, ReadyStep, Any], Any]) -> None:
        """Bind an adapter to one declared step; registration alone has no effect."""
        if not callable(adapter):
            raise DispatchError("adapter must be callable")
        with self._lock:
            operation = self._operations.get(operation_id)
            if operation is None or operation.terminal:
                raise DispatchStateError("operation is unknown or terminal")
            if step_id not in {step.id for step in operation.dag.steps}:
                raise DispatchStateError("adapter step is undeclared")
            self._adapter_steps[(operation_id, step_id)] = adapter

    def invoke_adapter(self, operation_id: str, step_id: str, credential: str, value: Any = None) -> Any:
        """Invoke only an explicitly registered adapter for an issued ready step."""
        with self._lock:
            self._cleanup_locked()
            operation = self._require_running_locked(operation_id)
            authority = operation.step_authorities.get(step_id)
            adapter = self._adapter_steps.get((operation_id, step_id))
            if adapter is None:
                raise DispatchStateError("no adapter is registered for this step")
            if authority is None or authority.consumed or credential != authority.credential or len(credential) != 43:
                raise DispatchCredentialError("ready-step credential is invalid")
            ready = self._ready_value(operation, authority)
            claim = operation.claim
        return adapter(claim, ready, value)


    def accept(self, operation_id: str, step_id: str, credential: str, body: Mapping[str, Any], *,
               idempotency_key: str) -> Any:
        """Accept a bounded event or one terminal result for a ready step."""
        key = _key(idempotency_key)
        if not isinstance(body, Mapping):
            raise DispatchError("step body must be an object")
        body_digest = _digest(body)
        with self._lock:
            self._cleanup_locked()
            operation = self._operations.get(operation_id)
            if operation is None:
                raise DispatchStateError("operation is unknown")
            request_key = (step_id, key)
            previous = operation.requests.get(request_key)
            if previous:
                if previous.digest != body_digest:
                    raise DispatchConflictError("idempotency key was used for different bytes")
                if not previous.complete:
                    raise DispatchStateError("request is in progress")
                return previous.response
            if operation.terminal:
                raise DispatchStateError("operation is terminal")
            authority = operation.step_authorities.get(step_id)
            if authority is None or authority.consumed:
                raise DispatchStateError("step is undeclared, consumed, duplicate, or out of order")
            if credential != authority.credential or len(credential) != 43:
                raise DispatchCredentialError("ready-step credential is invalid")
            request = _Request(body_digest, self._now() + IDEMPOTENCY_TTL_SECONDS)
            operation.requests[request_key] = request
            try:
                event_type = body.get("type")
                if event_type in ("started", "delta"):
                    self._accept_event_locked(operation, step_id, body)
                    response = {"state": event_type.upper(), "step_id": step_id}
                elif event_type == "failed":
                    self._require_exact(body, {"type", "failure"}, {"metadata", "ref"})
                    if not isinstance(body["failure"], str) or not body["failure"]:
                        raise DispatchError("failure must be a nonempty type")
                    response = self._finish_locked(
                        operation,
                        authority,
                        {"status": "failed", "failure": body["failure"]},
                    )
                elif event_type == "completed":
                    self._require_exact(
                        body,
                        {"type", "digest", "length", "metadata", "ref", "result"},
                    )
                    result_bytes = canonical_json_bytes(body["result"])
                    if (
                        body["digest"] != sha256_hex(result_bytes)
                        or body["length"] != len(result_bytes)
                    ):
                        raise DispatchConflictError(
                            "completed digest or length does not match exact result bytes"
                        )
                    if not isinstance(body["metadata"], Mapping) or not isinstance(body["ref"], str) or not body["ref"]:
                        raise DispatchError("completed metadata and ref are required")
                    response = self._finish_locked(operation, authority, body["result"])
                else:
                    raise DispatchError(
                        "step type must be started, delta, completed, or failed"
                    )
            except Exception:
                operation.requests.pop(request_key, None)
                raise
            request.complete, request.response = True, response
            return response

    submit = accept

    def cancel(self, operation_id: str) -> None:
        with self._lock:
            operation = self._operations.get(operation_id)
            if operation and not operation.terminal:
                operation.terminal = "CANCELLED"
                operation.step_authorities.clear()
                self._event_locked(operation, {"type": "terminal", "state": "CANCELLED"})

    def restart(self) -> None:
        """Invalidate all ephemeral worker and download credentials."""
        with self._lock:
            for operation in self._operations.values():
                if not operation.terminal:
                    operation.terminal = "RESTARTED"
                    operation.step_authorities.clear()

    def status(self, operation_id: str) -> dict[str, Any]:
        with self._lock:
            self._cleanup_locked()
            operation = self._operations.get(operation_id)
            if operation is None:
                raise DispatchStateError("operation is unknown")
            return {"operation_id": operation_id, "state": operation.terminal or "RUNNING", "events": tuple(operation.events)}

    def final_delivery(self, operation_id: str) -> FinalDelivery:
        with self._lock:
            self._cleanup_locked()
            operation = self._operations.get(operation_id)
            if operation is None or operation.terminal != "COMPLETED" or operation.final is None:
                raise DispatchStateError("final artifact is unavailable")
            final = operation.final
            return FinalDelivery(operation_id, final.credential, final.expires_at)

    def get_final(self, operation_id: str, capability: str, credential: str, *, idempotency_key: str,
                  interrupted: bool = False) -> tuple[dict[str, str], bytes]:
        key = _key(idempotency_key)
        with self._lock:
            self._cleanup_locked()
            operation = self._operations.get(operation_id)
            if operation is None or operation.final is None:
                raise DispatchStateError("final artifact is unavailable")
            final = operation.final
            if capability != operation_id or credential != final.credential:
                raise DispatchCredentialError("final capability or credential is invalid")
            request = final.keys.get(key)
            if request is not None:
                if request.complete:
                    if not final.retry_available:
                        raise DispatchCredentialError("final delivery was consumed")
                    final.retry_available = False
                elif request.digest != final.digest:
                    raise DispatchConflictError("final idempotency key conflicts")
            elif final.used:
                raise DispatchCredentialError("final delivery was consumed")
            else:
                request = _Request(final.digest, self._now() + IDEMPOTENCY_TTL_SECONDS, True)
                final.keys[key] = request
                final.used = True
            if interrupted:
                # The same key gets exactly one retry; a different key cannot observe bytes.
                final.retry_available = True
                raise ConnectionError("final delivery interrupted")
            headers = {
                "Content-Type": "application/octet-stream",
                "Content-Length": str(len(final.payload)),
                "Content-Disposition": 'attachment; filename="paper-curation-final.bin"',
                "Cache-Control": "no-store",
                "Accept-Ranges": "none",
                "X-Content-Type-Options": "nosniff",
            }
            return headers, final.payload

    def _finish_locked(self, operation: _Operation, authority: _StepAuthority, result: Mapping[str, Any]) -> dict[str, Any]:
        authority.consumed = True
        operation.step_authorities.pop(authority.step.id, None)
        result_bytes = canonical_json_bytes(result)
        operation.completed_digests[authority.step.id] = sha256_hex(result_bytes)
        if operation.state.dag.command == "audio.create":
            done = dict(operation.state.completed)
            done[authority.step.id] = result
            additions = tuple(
                step for step in operation.state.dag.steps
                if step.id not in done and step.id not in operation.step_authorities
                and all(dependency in done for dependency in step.dependencies)
            )
            operation.state = replace(operation.state, completed=tuple(done.items()), ready=additions)
            if authority.step.id == operation.state.dag.steps[-1].id:
                payload = canonical_json_bytes(result)
                operation.terminal = "COMPLETED"
                operation.state = replace(operation.state, terminal="COMPLETED")
                operation.final = _DeliveryState(payload, sha256_hex(payload), self._now() + FINAL_TTL_SECONDS, _token())
                self._event_locked(operation, {"type": "terminal", "state": "COMPLETED"})
                return {"state": "COMPLETED", "ready": ()}
            return {"state": "RUNNING", "ready": self._issue_ready_locked(operation)}
        # The pure reducer is the DAG authority.  Its transition and successor issue
        # occur under this same lock, preventing two workers from racing successors.
        operation.state = operation_dags.reduce(operation.state, authority.step.id, result)
        if operation.state.terminal:
            operation.terminal = operation.state.terminal
            if operation.terminal == "COMPLETED":
                artifact = operation.state.final_artifact
                if artifact is None:
                    raise DispatchStateError("completed operation lacks authoritative final")
                payload = canonical_json_bytes(artifact["payload"])
                operation.final = _DeliveryState(payload, sha256_hex(payload), self._now() + FINAL_TTL_SECONDS, _token())
            self._event_locked(operation, {"type": "terminal", "state": operation.terminal})
            return {"state": operation.terminal, "ready": ()}
        return {"state": "RUNNING", "ready": self._issue_ready_locked(operation)}

    def _issue_ready_locked(self, operation: _Operation) -> tuple[ReadyStep, ...]:
        ready: list[ReadyStep] = []
        for step in operation.state.ready:
            if step.id in operation.step_authorities:
                continue
            predecessors = {dep: operation.completed_digests[dep] for dep in step.dependencies}
            authority = _StepAuthority(
                step, len(operation.completed_digests) + 1, 1, _token(),
                _digest({"retained": operation.retained_digest, "step": step.id, "kind": step.kind}),
                _digest(predecessors),
            )
            operation.step_authorities[step.id] = authority
            ready.append(self._ready_value(operation, authority))
        return tuple(ready)

    def _ready_value(self, operation: _Operation, authority: _StepAuthority) -> ReadyStep:
        return ReadyStep(operation.claim.operation_id, authority.step.id, authority.step.kind,
                         authority.input_digest, authority.predecessor_digest, authority.ordinal,
                         authority.attempt, 0, operation.expires_at, authority.credential)

    @staticmethod
    def _operation_digest(dag: operation_dags.QueryDag, retained_digest: str,
                          expires_at: int) -> str:
        return _digest({
            "dag": dag.canonical_value(),
            "expires_at": expires_at,
            "retained_input_digest": retained_digest,
        })


    @staticmethod
    def _require_exact(body: Mapping[str, Any], required: set[str], optional: set[str] = set()) -> None:
        if not required <= set(body) <= required | optional:
            raise DispatchError("step body has undeclared or missing fields")

    def _accept_event_locked(self, operation: _Operation, step_id: str, body: Mapping[str, Any]) -> None:
        if body["type"] == "started":
            self._require_exact(body, {"type"})
        else:
            self._require_exact(body, {"type", "delta"})
            if not isinstance(body["delta"], str) or len(body["delta"].encode("utf-8")) > DELTA_LIMIT_BYTES:
                raise DispatchError("delta must be bounded UTF-8 text")
        self._event_locked(operation, {"type": body["type"], "step_id": step_id})

    def _event_locked(self, operation: _Operation, event: dict[str, Any]) -> None:
        operation.events.append(event)
        del operation.events[:-EVENT_LIMIT]

    def _require_running_locked(self, operation_id: str) -> _Operation:
        operation = self._operations.get(operation_id)
        if operation is None:
            raise DispatchStateError("operation is unknown")
        if operation.terminal:
            raise DispatchStateError("operation is terminal")
        return operation

    def _now(self) -> int:
        return int(self._clock())

    def _cleanup_locked(self) -> None:
        now = self._now()
        for operation in self._operations.values():
            if not operation.terminal and operation.expires_at and now >= operation.expires_at:
                operation.terminal = "EXPIRED"
                operation.step_authorities.clear()
                self._event_locked(operation, {"type": "terminal", "state": "EXPIRED"})
            for key, record in tuple(operation.requests.items()):
                if now >= record.expires_at:
                    del operation.requests[key]
            if operation.final is not None and now >= operation.final.expires_at:
                operation.final = None
