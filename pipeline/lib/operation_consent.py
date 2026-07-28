"""Canonical, fail-closed operation consent primitives.

This module deliberately has no provider, transport, or logging integration.  It
owns the stable bytes used to bind a human approval to a later operation.
"""

from __future__ import annotations

import base64
import hashlib
import math
import secrets
import time
import unicodedata
from dataclasses import dataclass, field, is_dataclass, replace
from enum import Enum
from typing import Any, Callable, Mapping, Sequence


APPROVAL_TTL_SECONDS = 60
_HEX_DIGEST_LENGTH = 64


class ConsentError(ValueError):
    """Base class for rejected consent input or state."""


class CanonicalValueError(ConsentError):
    pass


class AuthUnavailableError(ConsentError):
    pass


class PlanExpiredError(ConsentError):
    pass


class PlanScopeChangedError(ConsentError):
    pass


class ApprovalExpiredError(ConsentError):
    pass


class ApprovalConsumedError(ConsentError):
    pass


class ApprovalRejectedError(ConsentError):
    pass


class LedgerStateError(ConsentError):
    """An unknown, already-resolved, or closed ledger position was addressed."""


class LedgerBudgetError(ConsentError):
    """A hold would reserve more than the approved maximum."""


class LedgerOverspendError(ConsentError):
    """A verified response reported more actual usage than its hold reserved."""


class LedgerInvariantError(ConsentError):
    """The reserved >= actual invariant was violated."""


class AuthMode(str, Enum):
    AUTO = "auto"
    OAUTH = "oauth"
    API_KEY = "api-key"


@dataclass(frozen=True)
class ResolvedAuth:
    requested: AuthMode
    resolved: AuthMode


def _auth_mode(value: AuthMode | str) -> AuthMode:
    try:
        return value if isinstance(value, AuthMode) else AuthMode(value)
    except (TypeError, ValueError) as exc:
        raise ConsentError("auth mode must be auto, oauth, or api-key") from exc


def resolve_auth_mode(
    requested: AuthMode | str, *, oauth_available: bool, api_key_available: bool
) -> ResolvedAuth:
    """Resolve a requested mode without ever treating ``auto`` as an API-key fallback."""
    mode = _auth_mode(requested)
    if mode in (AuthMode.AUTO, AuthMode.OAUTH):
        if not oauth_available:
            raise AuthUnavailableError("OAuth is required for auto and oauth auth modes")
        return ResolvedAuth(requested=mode, resolved=AuthMode.OAUTH)
    if not api_key_available:
        raise AuthUnavailableError("API key auth was explicitly requested but is unavailable")
    return ResolvedAuth(requested=mode, resolved=AuthMode.API_KEY)


def _text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConsentError(f"{name} must be a nonempty string")
    return unicodedata.normalize("NFC", value)


def _tuple(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ConsentError(f"{name} must be an ordered sequence")
    return tuple(_text(value, name) for value in values)


def _nonnegative(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ConsentError(f"{name} must be a nonnegative integer")
    return value


def _positive(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConsentError(f"{name} must be a positive integer")
    return value


def _digest(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != _HEX_DIGEST_LENGTH:
        raise ConsentError(f"{name} must be a 64-character lowercase hexadecimal digest")
    if any(character not in "0123456789abcdef" for character in value):
        raise ConsentError(f"{name} must be a 64-character lowercase hexadecimal digest")
    return value


@dataclass(frozen=True)
class ProviderTask:
    """One ordered provider/model/task choice and its ordered declared fallbacks."""

    provider: str
    model: str
    task: str
    fallbacks: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "provider", _text(self.provider, "provider"))
        object.__setattr__(self, "model", _text(self.model, "model"))
        object.__setattr__(self, "task", _text(self.task, "task"))
        object.__setattr__(self, "fallbacks", _tuple(self.fallbacks, "fallback"))

    def canonical_value(self) -> dict[str, Any]:
        return {
            "fallbacks": list(self.fallbacks),
            "model": self.model,
            "provider": self.provider,
            "task": self.task,
        }


@dataclass(frozen=True)
class OperationMaxima:
    attempts: int = 0
    tokens: int = 0
    items: int = 0
    searches: int = 0
    audio_seconds: int = 0
    recipients: int = 0
    concurrency: int = 0

    def __post_init__(self) -> None:
        for name in (
            "attempts", "tokens", "items", "searches", "audio_seconds", "recipients", "concurrency"
        ):
            object.__setattr__(self, name, _nonnegative(getattr(self, name), name))

    def canonical_value(self) -> dict[str, int]:
        return {name: getattr(self, name) for name in (
            "attempts", "audio_seconds", "concurrency", "items", "recipients", "searches", "tokens"
        )}


@dataclass(frozen=True)
class OperationClaim:
    """Immutable scope for a potentially effectful operation."""

    version: int
    operation_id: str
    task: str
    command: str
    topic: str
    source: str
    ingress: str
    auth: AuthMode | str
    providers: tuple[ProviderTask, ...] = ()
    maxima: OperationMaxima = field(default_factory=OperationMaxima)
    input_digests: tuple[str, ...] = ()
    resource_digests: tuple[str, ...] = ()
    external_allowlist: tuple[str, ...] = ()
    read_allowlist: tuple[str, ...] = ()
    write_allowlist: tuple[str, ...] = ()
    effect_allowlist: tuple[str, ...] = ()
    deploy_allowlist: tuple[str, ...] = ()
    created_at: int = 0
    expires_at: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise ConsentError("version must be a positive integer")
        for name in ("operation_id", "task", "command", "topic", "source", "ingress"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        object.__setattr__(self, "auth", _auth_mode(self.auth))
        if isinstance(self.providers, (str, bytes)):
            raise ConsentError("providers must be an ordered sequence")
        providers = tuple(self.providers)
        if not all(isinstance(provider, ProviderTask) for provider in providers):
            raise ConsentError("providers must contain ProviderTask values")
        object.__setattr__(self, "providers", providers)
        if not isinstance(self.maxima, OperationMaxima):
            raise ConsentError("maxima must be an OperationMaxima value")
        for name in ("input_digests", "resource_digests"):
            values = getattr(self, name)
            if isinstance(values, (str, bytes)):
                raise ConsentError(f"{name} must be an ordered sequence")
            object.__setattr__(self, name, tuple(_digest(value, name) for value in values))
        for name in ("external_allowlist", "read_allowlist", "write_allowlist", "effect_allowlist", "deploy_allowlist"):
            object.__setattr__(self, name, _tuple(getattr(self, name), name))
        object.__setattr__(self, "created_at", _nonnegative(self.created_at, "created_at"))
        object.__setattr__(self, "expires_at", _nonnegative(self.expires_at, "expires_at"))
        if self.expires_at and self.expires_at < self.created_at:
            raise ConsentError("expires_at must not precede created_at")

    def canonical_value(self) -> dict[str, Any]:
        return {
            "auth": self.auth.value,
            "command": self.command,
            "created_at": self.created_at,
            "deploy_allowlist": list(self.deploy_allowlist),
            "effect_allowlist": list(self.effect_allowlist),
            "expires_at": self.expires_at,
            "external_allowlist": list(self.external_allowlist),
            "ingress": self.ingress,
            "input_digests": list(self.input_digests),
            "maxima": self.maxima.canonical_value(),
            "operation_id": self.operation_id,
            "providers": [provider.canonical_value() for provider in self.providers],
            "read_allowlist": list(self.read_allowlist),
            "resource_digests": list(self.resource_digests),
            "source": self.source,
            "task": self.task,
            "topic": self.topic,
            "version": self.version,
            "write_allowlist": list(self.write_allowlist),
        }

    @property
    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.canonical_value())

    @property
    def plan_hash(self) -> str:
        return sha256_hex(self.canonical_bytes)


def _canonical_value(value: Any) -> Any:
    if isinstance(value, float):
        raise CanonicalValueError("floating-point values are not canonical")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, Enum):
        return _canonical_value(value.value)
    canonical = getattr(value, "canonical_value", None)
    if callable(canonical):
        return _canonical_value(canonical())
    if isinstance(value, Mapping):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalValueError("canonical JSON object keys must be strings")
            key = unicodedata.normalize("NFC", key)
            if key in output:
                raise CanonicalValueError("NFC-normalized JSON object keys must be unique")
            output[key] = _canonical_value(item)
        return output
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    if is_dataclass(value):
        raise CanonicalValueError("dataclass values must explicitly define canonical_value")
    raise CanonicalValueError(f"noncanonical value type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Return sorted-key, NFC-normalized, compact UTF-8 JSON without floats."""
    import json

    return json.dumps(
        _canonical_value(value), ensure_ascii=False, allow_nan=False,
        separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    if not isinstance(value, bytes):
        raise CanonicalValueError("SHA-256 input must be bytes")
    return hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class OperationPlan:
    operation_id: str
    plan_hash: str
    claim: OperationClaim = field(repr=False)
    operation_digest: str | None = None

    def __post_init__(self) -> None:
        _text(self.operation_id, "operation_id")
        _digest(self.plan_hash, "plan_hash")
        if self.operation_digest is not None:
            _digest(self.operation_digest, "operation_digest")

@dataclass(frozen=True, repr=False)
class ApprovalCredential:
    """Opaque, one-use secret bound to a frozen operation snapshot."""

    token: str
    operation_id: str
    plan_hash: str
    operation_digest: str
    expires_at: int

    def __post_init__(self) -> None:
        if not isinstance(self.token, str) or len(self.token) != 43:
            raise ConsentError("approval credential must be 43 unpadded base64url characters")
        if "=" in self.token or any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for char in self.token):
            raise ConsentError("approval credential must be unpadded base64url")
        try:
            decoded = base64.urlsafe_b64decode(self.token + "=")
        except (ValueError, UnicodeError) as exc:
            raise ConsentError("approval credential must be unpadded base64url") from exc
        if len(decoded) != 32 or base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=") != self.token:
            raise ConsentError("approval credential must canonically encode 32 random bytes")
        _text(self.operation_id, "operation_id")
        _digest(self.plan_hash, "plan_hash")
        _digest(self.operation_digest, "operation_digest")
        _nonnegative(self.expires_at, "expires_at")

    def __repr__(self) -> str:
        return "ApprovalCredential(<redacted>)"

    __str__ = __repr__


@dataclass
class _ApprovalState:
    plan: OperationPlan
    expires_at: int
    consumed: bool = False


class OperationConsent:
    """In-memory plan/approval authority for adapters to call before an effect."""

    def __init__(self, *, clock: Callable[[], float] = time.time, token_bytes: Callable[[int], bytes] = secrets.token_bytes):
        self._clock = clock
        self._token_bytes = token_bytes
        self._plans: dict[str, OperationPlan] = {}
        self._approvals: dict[str, _ApprovalState] = {}

    def create_plan(self, claim: OperationClaim) -> OperationPlan:
        if not isinstance(claim, OperationClaim):
            raise ConsentError("claim must be an OperationClaim")
        plan = OperationPlan(claim.operation_id, claim.plan_hash, claim=claim)
        existing = self._plans.get(plan.operation_id)
        if existing is not None and existing.plan_hash != plan.plan_hash:
            raise PlanScopeChangedError("operation id is already bound to another plan scope")
        self._plans[plan.operation_id] = existing or plan
        return self._plans[plan.operation_id]

    def bind_plan(self, operation_id: str, plan_hash: str, operation_digest: str) -> OperationPlan:
        """Irreversibly bind an operation claim to its frozen execution snapshot."""
        operation_id = _text(operation_id, "operation_id")
        plan_hash = _digest(plan_hash, "plan_hash")
        operation_digest = _digest(operation_digest, "operation_digest")
        plan = self._plans.get(operation_id)
        if plan is None or plan.plan_hash != plan_hash:
            raise PlanScopeChangedError("operation snapshot must bind the exact planned scope")
        if plan.operation_digest is not None and plan.operation_digest != operation_digest:
            raise PlanScopeChangedError("operation id is already bound to another execution snapshot")
        if plan.operation_digest is None:
            plan = replace(plan, operation_digest=operation_digest)
            self._plans[operation_id] = plan
        return plan

    def approve(self, operation_id: str, plan_hash: str, *, decision: str = "approve") -> ApprovalCredential:
        plan = self._plans.get(operation_id)
        if plan is None or plan.plan_hash != plan_hash or plan.operation_digest is None:
            raise PlanScopeChangedError("approval must name an exact frozen planned scope")
        if decision != "approve":
            raise ApprovalRejectedError("approval decision must be approve")
        now = int(self._clock())
        if plan.claim.expires_at and now >= plan.claim.expires_at:
            raise PlanExpiredError("operation plan has expired")
        token = base64.urlsafe_b64encode(self._token_bytes(32)).decode("ascii").rstrip("=")
        credential = ApprovalCredential(
            token, operation_id, plan_hash, plan.operation_digest, now + APPROVAL_TTL_SECONDS
        )
        self._approvals[token] = _ApprovalState(plan=plan, expires_at=credential.expires_at)
        return credential

    def redeem(self, credential: ApprovalCredential | str, claim: OperationClaim) -> OperationClaim:
        token = credential.token if isinstance(credential, ApprovalCredential) else credential
        state = self._approvals.get(token)
        if state is None:
            raise ApprovalConsumedError("unknown approval credential")
        # Scope is checked before token state so mutation cannot consume authority.
        if not isinstance(claim, OperationClaim) or claim.plan_hash != state.plan.plan_hash:
            raise PlanScopeChangedError("operation scope differs from the approved plan")
        if claim.operation_id != state.plan.operation_id:
            raise PlanScopeChangedError("operation id differs from the approved plan")
        if state.plan.operation_digest is None:
            raise PlanScopeChangedError("approved operation has no frozen execution snapshot")
        if isinstance(credential, ApprovalCredential) and (
            credential.operation_id != state.plan.operation_id
            or credential.plan_hash != state.plan.plan_hash
            or credential.operation_digest != state.plan.operation_digest
        ):
            raise PlanScopeChangedError("approval credential differs from the frozen operation")
        if state.consumed:
            raise ApprovalConsumedError("approval credential was already consumed")
        now = int(self._clock())
        if now >= state.expires_at or (claim.expires_at and now >= claim.expires_at):
            raise ApprovalExpiredError("approval credential or operation has expired")
        state.consumed = True
        return state.plan.claim


# --- Duration hold/settle ledger --------------------------------------------
#
# Stage-12's "pre-debit at worst case and never refund" rule governs provider
# ATTEMPTS: constructing a provider call spends an attempt whether or not it
# ever returns, so attempts are debited immediately before construction and are
# never given back.  That rule deliberately does NOT govern the duration hold
# below.  A hold is a *reservation* of worst-case seconds taken immediately
# before construction, so an over-long response can never be authorized after
# the fact; the verified response then settles its actual usage and the
# untouched remainder returns to the budget in the same step.  Debiting worst
# case per chunk *and* the actual on top would double-count (32 chunks x 120 s
# = 3840 s against a 3600 s maximum) and would fail legal runs.  The release is
# therefore correct accounting, not a refund: settled seconds are never
# released, only reservations that were never consumed.  Do not "fix" this
# release back into a leak.


class _BilledUsageUnavailable:
    """The provider reported no billed audio seconds.

    Distinct from ``0``: zero is a provider claim, this is the absence of one.
    Gemini returns token ``usageMetadata`` rather than billed audio seconds, so
    this sentinel is the normal case.  It canonicalizes to JSON ``null`` and is
    never consulted for authorization.
    """

    __slots__ = ()
    _singleton: _BilledUsageUnavailable | None = None

    def __new__(cls) -> _BilledUsageUnavailable:
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return "BILLED_USAGE_UNAVAILABLE"

    __str__ = __repr__

    def __bool__(self) -> bool:
        return False

    def __copy__(self) -> _BilledUsageUnavailable:
        return self

    def __deepcopy__(self, memo: Any) -> _BilledUsageUnavailable:
        return self

    def canonical_value(self) -> None:
        """Advisory usage is reported as JSON null, never as a zero measurement."""
        return None


BILLED_USAGE_UNAVAILABLE = _BilledUsageUnavailable()


def _billed_usage(value: int | None | _BilledUsageUnavailable) -> int | _BilledUsageUnavailable:
    """Normalize advisory usage; ``None`` and the sentinel both mean unreported."""
    if value is None or isinstance(value, _BilledUsageUnavailable):
        return BILLED_USAGE_UNAVAILABLE
    return _nonnegative(value, "billed usage")


def whole_units(value: float | int, name: str = "measured usage") -> int:
    """Round a measured, nonnegative, finite duration UP to whole ledger units.

    Measured PCM seconds are fractional while OperationMaxima budgets are whole
    integers.  Rounding up is the only safe direction: flooring would settle
    less than was actually produced and silently under-charge the budget.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ConsentError(f"{name} must be a nonnegative finite number")
    return math.ceil(value)


class HoldState(str, Enum):
    HELD = "HELD"
    SETTLED = "SETTLED"
    RELEASED = "RELEASED"


class LedgerState(str, Enum):
    OPEN = "OPEN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class OperationHold:
    """One worst-case reservation and, once resolved, its exact accounting."""

    hold_id: str
    label: str
    reserved: int
    state: HoldState | str = HoldState.HELD
    settled: int = 0
    released: int = 0
    billed: int | _BilledUsageUnavailable = BILLED_USAGE_UNAVAILABLE
    held_at: int = 0
    resolved_at: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "hold_id", _text(self.hold_id, "hold_id"))
        object.__setattr__(self, "label", _text(self.label, "label"))
        object.__setattr__(self, "reserved", _positive(self.reserved, "reserved"))
        try:
            state = self.state if isinstance(self.state, HoldState) else HoldState(self.state)
        except (TypeError, ValueError) as exc:
            raise ConsentError("hold state must be HELD, SETTLED, or RELEASED") from exc
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "settled", _nonnegative(self.settled, "settled"))
        object.__setattr__(self, "released", _nonnegative(self.released, "released"))
        object.__setattr__(self, "billed", _billed_usage(self.billed))
        object.__setattr__(self, "held_at", _nonnegative(self.held_at, "held_at"))
        if self.resolved_at is not None:
            object.__setattr__(self, "resolved_at", _nonnegative(self.resolved_at, "resolved_at"))
        if self.settled > self.reserved:
            raise LedgerOverspendError("a hold can never settle more than it reserved")
        if state is HoldState.HELD and (self.settled or self.released or self.resolved_at is not None):
            raise LedgerStateError("an open hold has settled nothing and released nothing")
        if state is not HoldState.HELD and self.settled + self.released != self.reserved:
            raise LedgerStateError("a resolved hold must account for exactly what it reserved")
        if state is HoldState.RELEASED and self.settled:
            raise LedgerStateError("a released hold settles nothing")

    @property
    def outstanding(self) -> int:
        """Seconds still reserved but neither charged nor returned."""
        return self.reserved if self.state is HoldState.HELD else 0

    def canonical_value(self) -> dict[str, Any]:
        return {
            "billed": self.billed,
            "held_at": self.held_at,
            "hold_id": self.hold_id,
            "label": self.label,
            "released": self.released,
            "reserved": self.reserved,
            "resolved_at": self.resolved_at,
            "settled": self.settled,
            "state": self.state.value,
        }


@dataclass(frozen=True)
class OperationLedgerRecord:
    """Immutable per-operation view of reserved / settled / billed accounting."""

    operation_id: str
    resource: str
    budget: int
    reserved: int
    outstanding: int
    settled: int
    released: int
    destroyed: int
    state: LedgerState | str = LedgerState.OPEN
    billed: int | _BilledUsageUnavailable = BILLED_USAGE_UNAVAILABLE
    reason: str | None = None
    holds: tuple[OperationHold, ...] = ()

    def __post_init__(self) -> None:
        for name in ("operation_id", "resource"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        for name in ("budget", "reserved", "outstanding", "settled", "released", "destroyed"):
            object.__setattr__(self, name, _nonnegative(getattr(self, name), name))
        try:
            state = self.state if isinstance(self.state, LedgerState) else LedgerState(self.state)
        except (TypeError, ValueError) as exc:
            raise ConsentError("ledger state must be OPEN, COMPLETED, FAILED, or CANCELLED") from exc
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "billed", _billed_usage(self.billed))
        if self.reason is not None:
            object.__setattr__(self, "reason", _text(self.reason, "reason"))
        if isinstance(self.holds, (str, bytes)):
            raise ConsentError("holds must be an ordered sequence")
        holds = tuple(self.holds)
        if not all(isinstance(hold, OperationHold) for hold in holds):
            raise ConsentError("holds must contain OperationHold values")
        object.__setattr__(self, "holds", holds)
        if self.settled + self.released + self.outstanding != self.reserved:
            raise LedgerStateError("every reserved unit must be settled, released, or still held")
        if self.destroyed > self.settled:
            raise LedgerStateError("destroyed usage can never exceed settled usage")

    @property
    def actual(self) -> int:
        """Verified actual usage charged against the budget (actual_pcm_seconds)."""
        return self.settled

    @property
    def remaining(self) -> int:
        """Budget still available: settled spend and live holds, never billed usage."""
        return self.budget - self.settled - self.outstanding

    @property
    def invariant_holds(self) -> bool:
        return (
            self.reserved >= self.actual
            and all(hold.reserved >= hold.settled for hold in self.holds)
            and self.settled + self.outstanding <= self.budget
        )

    def assert_invariants(self) -> None:
        """``reserved >= actual_pcm_seconds`` per hold and for the whole operation."""
        if not self.invariant_holds:
            raise LedgerInvariantError("reserved must always cover verified actual usage")

    def canonical_value(self) -> dict[str, Any]:
        return {
            "billed": self.billed,
            "budget": self.budget,
            "destroyed": self.destroyed,
            "holds": [hold.canonical_value() for hold in self.holds],
            "operation_id": self.operation_id,
            "outstanding": self.outstanding,
            "reason": self.reason,
            "released": self.released,
            "reserved": self.reserved,
            "resource": self.resource,
            "settled": self.settled,
            "state": self.state.value,
        }


class OperationLedger:
    """Single enforcement authority for one bounded duration budget.

    Pure in-memory accounting: no provider, transport, or logging knowledge, no
    I/O, and no wall clock other than the injected seam.  Callers serialize
    their own concurrency exactly as they do for ``OperationConsent``; every
    transition validates before it mutates, so a rejected call leaves the
    ledger byte-identical.
    """

    def __init__(self, budget: int, *, operation_id: str = "operation", resource: str = "audio_seconds",
                 clock: Callable[[], float] = time.time) -> None:
        self._budget = _nonnegative(budget, "budget")
        self._operation_id = _text(operation_id, "operation_id")
        self._resource = _text(resource, "resource")
        self._clock = clock
        self._holds: dict[str, OperationHold] = {}
        self._sequence = 0
        self._state = LedgerState.OPEN
        self._reason: str | None = None

    @classmethod
    def for_claim(cls, claim: OperationClaim, *, resource: str = "audio_seconds",
                  clock: Callable[[], float] = time.time) -> OperationLedger:
        """Bind a ledger to exactly one approved OperationMaxima budget."""
        if not isinstance(claim, OperationClaim):
            raise ConsentError("claim must be an OperationClaim")
        if resource not in claim.maxima.canonical_value():
            raise ConsentError("resource must name an OperationMaxima budget")
        return cls(getattr(claim.maxima, resource), operation_id=claim.operation_id,
                   resource=resource, clock=clock)

    @property
    def budget(self) -> int:
        return self._budget

    @property
    def resource(self) -> str:
        return self._resource

    @property
    def state(self) -> LedgerState:
        return self._state

    @property
    def reserved(self) -> int:
        return sum(hold.reserved for hold in self._holds.values())

    @property
    def outstanding(self) -> int:
        return sum(hold.outstanding for hold in self._holds.values())

    @property
    def settled(self) -> int:
        return sum(hold.settled for hold in self._holds.values())

    @property
    def released(self) -> int:
        return sum(hold.released for hold in self._holds.values())

    @property
    def remaining(self) -> int:
        return self._budget - self.settled - self.outstanding

    def hold(self, amount: int, *, label: str | None = None) -> OperationHold:
        """Reserve worst case immediately before construction.  This is NOT a debit.

        Authorization consults settled spend and live holds only; advisory
        provider-billed usage is never part of this decision.
        """
        self._require_open()
        amount = _positive(amount, "hold amount")
        if self.settled + self.outstanding + amount > self._budget:
            raise LedgerBudgetError(f"{self._resource} hold exceeds the approved maximum")
        self._sequence += 1
        hold_id = f"{self._resource}-{self._sequence}"
        hold = OperationHold(hold_id, hold_id if label is None else _text(label, "label"), amount,
                             held_at=int(self._clock()))
        self._holds[hold_id] = hold
        return hold

    def settle(self, hold: OperationHold | str, actual: int, *,
               billed: int | None | _BilledUsageUnavailable = BILLED_USAGE_UNAVAILABLE) -> OperationHold:
        """Charge ``min(actual, hold)`` and release the remainder in one atomic step."""
        self._require_open()
        open_hold = self._open_hold(hold)
        actual = _nonnegative(actual, "actual")
        if actual > open_hold.reserved:
            # Asserted impossible: a chunk is accepted only after the existing
            # 120 s / 6 MiB per-chunk validation, so a verified response can
            # never exceed its own worst-case hold.  Clamping here would hide an
            # unbounded provider response inside a bounded budget, so raise.
            raise LedgerOverspendError(
                f"verified actual {actual} exceeds the {open_hold.reserved} {self._resource} hold")
        charged = min(actual, open_hold.reserved)  # identity given the guard above; kept explicit
        settled = replace(open_hold, state=HoldState.SETTLED, settled=charged,
                          released=open_hold.reserved - charged, billed=_billed_usage(billed),
                          resolved_at=int(self._clock()))
        self._holds[settled.hold_id] = settled
        return settled

    def release(self, hold: OperationHold | str) -> OperationHold:
        """Return an unconsumed reservation to the budget (failed, skipped, or cancelled)."""
        self._require_open()
        open_hold = self._open_hold(hold)
        released = replace(open_hold, state=HoldState.RELEASED, released=open_hold.reserved,
                           resolved_at=int(self._clock()))
        self._holds[released.hold_id] = released
        return released

    def complete(self) -> OperationLedgerRecord:
        """Close a delivered operation.  Every hold must already be resolved."""
        self._require_open()
        if self.outstanding:
            raise LedgerStateError("cannot complete an operation with outstanding holds")
        self._state = LedgerState.COMPLETED
        return self.record()

    def fail(self, reason: str) -> OperationLedgerRecord:
        """Mid-run failure: settled chunks stay settled, outstanding holds are released."""
        return self._abandon(LedgerState.FAILED, reason)

    def cancel(self, reason: str) -> OperationLedgerRecord:
        """Mid-stream cancellation accounts exactly like a mid-run failure."""
        return self._abandon(LedgerState.CANCELLED, reason)

    def record(self) -> OperationLedgerRecord:
        """Frozen snapshot, buildable at any point including mid-run."""
        holds = tuple(self._holds.values())
        reports = [hold.billed for hold in holds if isinstance(hold.billed, int)]
        settled = sum(hold.settled for hold in holds)
        return OperationLedgerRecord(
            operation_id=self._operation_id,
            resource=self._resource,
            budget=self._budget,
            reserved=sum(hold.reserved for hold in holds),
            outstanding=sum(hold.outstanding for hold in holds),
            settled=settled,
            released=sum(hold.released for hold in holds),
            # Paid-but-destroyed: an abandoned run delivers no audio, yet the
            # settled seconds were really produced and really spent.  Surfacing
            # them is the point; hiding them would misreport the loss.
            destroyed=settled if self._state in (LedgerState.FAILED, LedgerState.CANCELLED) else 0,
            state=self._state,
            billed=sum(reports) if reports else BILLED_USAGE_UNAVAILABLE,
            reason=self._reason,
            holds=holds,
        )

    def assert_invariants(self) -> None:
        """Assert ``reserved >= actual_pcm_seconds`` at any point in the run."""
        self.record().assert_invariants()

    def _abandon(self, state: LedgerState, reason: str) -> OperationLedgerRecord:
        self._require_open()
        reason = _text(reason, "reason")
        now = int(self._clock())
        for hold_id, hold in list(self._holds.items()):
            if hold.state is HoldState.HELD:
                self._holds[hold_id] = replace(hold, state=HoldState.RELEASED,
                                               released=hold.reserved, resolved_at=now)
        self._state = state
        self._reason = reason
        return self.record()

    def _require_open(self) -> None:
        if self._state is not LedgerState.OPEN:
            raise LedgerStateError(f"ledger is {self._state.value} and accepts no further accounting")

    def _open_hold(self, hold: OperationHold | str) -> OperationHold:
        hold_id = hold.hold_id if isinstance(hold, OperationHold) else hold
        current = self._holds.get(_text(hold_id, "hold_id"))
        if current is None:
            raise LedgerStateError("unknown hold")
        if current.state is not HoldState.HELD:
            raise LedgerStateError(f"hold {current.hold_id} was already {current.state.value.lower()}")
        return current


class IdempotencyDisposition(str, Enum):
    STARTED = "STARTED"
    REPLAY = "REPLAY"
    IN_PROGRESS = "REQUEST_IN_PROGRESS"
    CONFLICT = "IDEMPOTENCY_CONFLICT"
    CREDENTIAL_CONSUMED = "CREDENTIAL_CONSUMED"


@dataclass(frozen=True)
class IdempotencyResult:
    disposition: IdempotencyDisposition
    request_digest: str


@dataclass
class _IdempotencyRecord:
    request_digest: str
    complete: bool = False


class IdempotencyRecords:
    """In-memory idempotency state; callers persist equivalent keys outside this slice."""

    def __init__(self) -> None:
        self._records: dict[tuple[str, str, str], _IdempotencyRecord] = {}
        self._consumed_credentials: set[str] = set()

    @staticmethod
    def validate_key(key: str) -> str:
        return _digest(key, "Idempotency-Key")

    def consume_credential(self, credential_id: str) -> None:
        self._consumed_credentials.add(_text(credential_id, "credential_id"))

    def begin(self, capability: str, route: str, key: str, request_digest: str, *, credential_id: str | None = None) -> IdempotencyResult:
        capability = _text(capability, "capability")
        route = _text(route, "route")
        key = self.validate_key(key)
        request_digest = _digest(request_digest, "request_digest")
        record_key = (capability, route, key)
        existing = self._records.get(record_key)
        if existing is not None:
            if existing.request_digest != request_digest:
                return IdempotencyResult(IdempotencyDisposition.CONFLICT, request_digest)
            return IdempotencyResult(
                IdempotencyDisposition.REPLAY if existing.complete else IdempotencyDisposition.IN_PROGRESS,
                request_digest,
            )
        if credential_id is not None and _text(credential_id, "credential_id") in self._consumed_credentials:
            return IdempotencyResult(IdempotencyDisposition.CREDENTIAL_CONSUMED, request_digest)
        self._records[record_key] = _IdempotencyRecord(request_digest)
        return IdempotencyResult(IdempotencyDisposition.STARTED, request_digest)

    def complete(self, capability: str, route: str, key: str, request_digest: str) -> None:
        record = self._records.get((_text(capability, "capability"), _text(route, "route"), self.validate_key(key)))
        if record is None or record.request_digest != _digest(request_digest, "request_digest"):
            raise ConsentError("cannot complete an unknown or conflicting idempotency record")
        record.complete = True
