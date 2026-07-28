"""Fail-closed, injectable boundaries for every external provider effect.

This module deliberately contains no provider SDK imports.  Callers supply a
constructor or transport after the adapter has verified its exact subclaim and
reserved its budget.  Secrets are accepted only as a single selected value and
are never serialized by these value objects.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .child_context import ChildContextPolicy, ChildOperationContext, operation_subclaim_digest
from .operation_consent import (
    BILLED_USAGE_UNAVAILABLE,
    ApprovalCredential,
    AuthMode,
    ConsentError,
    LedgerBudgetError,
    LedgerStateError,
    OperationClaim,
    OperationConsent,
    OperationHold,
    OperationLedger,
    canonical_json_bytes,
    sha256_hex,
)


class AdapterError(ConsentError):
    """A provider boundary was not explicitly authorized."""


class AdapterAuthorizationError(AdapterError):
    pass


class AdapterBudgetError(AdapterError):
    pass


@dataclass(frozen=True)
class EffectInventoryEntry:
    """One named, non-interchangeable external-effect boundary."""

    name: str
    provider: str
    task: str
    auth_modes: tuple[AuthMode, ...]
    budget: str
    requires_secret: bool = False
    read_only: bool = False


EFFECT_INVENTORY: tuple[EffectInventoryEntry, ...] = (
    EffectInventoryEntry("claude.oauth.cli", "claude", "cli", (AuthMode.OAUTH,), "attempts", True),
    EffectInventoryEntry("anthropic.api-key", "anthropic", "completion", (AuthMode.API_KEY,), "tokens", True),
    EffectInventoryEntry("gemini.script", "gemini", "script", (AuthMode.API_KEY,), "tokens", True),
    EffectInventoryEntry("gemini.tts", "gemini", "tts", (AuthMode.API_KEY,), "audio_seconds", True),
    EffectInventoryEntry("gemini.embedding", "gemini", "embedding", (AuthMode.API_KEY,), "items", True),
    EffectInventoryEntry("gemini.image", "gemini", "image", (AuthMode.API_KEY,), "items", True),
    EffectInventoryEntry("email.optional", "email", "send", (AuthMode.API_KEY,), "recipients", True),
    EffectInventoryEntry("zotero.read", "zotero", "read", (AuthMode.API_KEY,), "items", True, True),
    EffectInventoryEntry("http.web", "http", "fetch", (AuthMode.API_KEY,), "searches", False, True),
    EffectInventoryEntry("product.deploy", "product", "deploy", (AuthMode.API_KEY,), "attempts", False),
    EffectInventoryEntry("git.delivery", "git", "delivery", (AuthMode.API_KEY,), "attempts", False),
)
INVENTORY_BY_NAME = {entry.name: entry for entry in EFFECT_INVENTORY}


@dataclass(frozen=True, repr=False)
class AdapterCall:
    """Exact request metadata; payload and credentials remain caller-owned."""

    entry: str
    operation_id: str
    step_id: str
    provider: str
    model: str
    task: str
    attempt: int
    ingress: str
    amount: int = 1
    fallback: str | None = None

    def __post_init__(self) -> None:
        if self.entry not in INVENTORY_BY_NAME:
            raise AdapterAuthorizationError("adapter entry is undeclared")
        for name in ("operation_id", "step_id", "provider", "model", "task", "ingress"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise AdapterAuthorizationError(f"{name} must be a nonempty string")
        if isinstance(self.attempt, bool) or not isinstance(self.attempt, int) or self.attempt < 1:
            raise AdapterAuthorizationError("attempt must be a positive integer")
        if isinstance(self.amount, bool) or not isinstance(self.amount, int) or self.amount < 1:
            raise AdapterAuthorizationError("amount must be a positive integer")
        if self.fallback is not None and (not isinstance(self.fallback, str) or not self.fallback):
            raise AdapterAuthorizationError("fallback must be a nonempty string or None")

    def canonical_value(self) -> dict[str, object]:
        return {"amount": self.amount, "attempt": self.attempt, "entry": self.entry,
                "fallback": self.fallback, "ingress": self.ingress, "model": self.model,
                "operation_id": self.operation_id, "provider": self.provider,
                "step_id": self.step_id, "task": self.task}

    @property
    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self.canonical_value()))

    def __repr__(self) -> str:
        return "AdapterCall(<redacted>)"

    __str__ = __repr__


@dataclass(frozen=True, repr=False)
class SelectedSecret:
    """One secret selected for one exact boundary; aliases are intentionally absent."""

    value: str = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value:
            raise AdapterAuthorizationError("selected secret must be a nonempty string")

    def __repr__(self) -> str:
        return "SelectedSecret(<redacted>)"

    __str__ = __repr__


@dataclass(frozen=True)
class AdapterReservation:
    """One live ledger hold bound to exactly one ``AdapterCall``.

    The handle names both its hold and the digest of the call that placed it,
    so a caller with four chunks in flight can only settle its own reservation.
    """

    entry: str
    budget: str
    call_digest: str
    hold_id: str
    reserved: int


@dataclass(frozen=True)
class AdapterResult:
    """A constructed client/transport and the reservation its caller must resolve."""

    value: Any
    reservation: AdapterReservation | None = None


class ProviderAdapters:
    """Authorizes and pre-debits injected external constructors/transports.

    ``invoke`` is the sole effect-adjacent method.  It never retries, never
    falls back, and passes a minimal options mapping (`retries: 0`) to the
    injected callable.  A child must present the fd3-derived context supplied
    by ``ChildParentContext``; direct calls must consume a fresh root approval.

    An optional ``ledger`` makes ``OperationLedger`` the single authority for
    exactly one duration budget (``audio_seconds``).  Calls against that budget
    reserve their worst case through the ledger instead of debiting it, and the
    caller settles the verified actual with ``settle``.  Every other budget
    keeps the permanent pre-debit.  Ledger-backed budgets must go through
    ``invoke_reserved``, which returns the explicit per-call reservation.
    """

    def __init__(self, claim: OperationClaim, *, consent: OperationConsent | None = None,
                 ledger: OperationLedger | None = None) -> None:
        self.claim = claim
        self._consent = consent
        self._lock = threading.RLock()
        self._spent = {name: 0 for name in claim.maxima.canonical_value()}
        self._inflight = 0
        if ledger is not None:
            if not isinstance(ledger, OperationLedger):
                raise AdapterAuthorizationError("ledger must be an OperationLedger")
            if ledger.resource not in self._spent:
                raise AdapterAuthorizationError("ledger resource must name an OperationMaxima budget")
            if ledger.budget != getattr(claim.maxima, ledger.resource):
                raise AdapterAuthorizationError("ledger budget must be exactly the approved maximum")
        self._ledger = ledger
        # hold_id -> digest of the one AdapterCall that reserved it.  Live holds
        # are keyed by call, never by recency, so concurrent chunks can never
        # settle each other's reservation.
        self._reservations: dict[str, str] = {}

    @property
    def ledger(self) -> OperationLedger | None:
        """The single authority for the ledger-backed budget, when one is wired."""
        return self._ledger

    def spent(self) -> Mapping[str, int]:
        with self._lock:
            values = dict(self._spent)
            if self._ledger is not None:
                # Settled actual plus still-live reservations: exactly what is
                # unavailable to the next call.  A worst case is reserved rather
                # than charged, so a settled chunk is never counted twice.
                values[self._ledger.resource] = self._ledger.settled + self._ledger.outstanding
            return values

    def child_context_policy(self, call: AdapterCall) -> ChildContextPolicy:
        """Return the exact fd3 policy the parent must validate for this call."""
        entry = INVENTORY_BY_NAME[call.entry]
        if call.operation_id != self.claim.operation_id:
            raise AdapterAuthorizationError("adapter call is not bound to this operation")
        return ChildContextPolicy(
            operation_id=self.claim.operation_id,
            subclaim_digest=operation_subclaim_digest(call.operation_id, call.canonical_value()),
            members=(call.entry,),
            budget={entry.budget: call.amount},
        )

    def invoke(self, call: AdapterCall, *, secret: SelectedSecret | None,
               constructor: Callable[..., Any], child_context: ChildOperationContext | None = None,
               root_approval: ApprovalCredential | None = None, interactive: bool = False,
               payload: Any = None) -> Any:
        """Validate and reserve immediately before constructing a client/transport."""
        entry = INVENTORY_BY_NAME.get(call.entry)
        if entry is not None and self._ledger is not None and entry.budget == self._ledger.resource:
            # This form has nowhere to hand the reservation back, so its hold
            # could never be settled or released.  Fail closed rather than leak
            # an outstanding hold for the rest of the operation.
            raise AdapterAuthorizationError(
                "ledger-backed budgets must use invoke_reserved so the hold is settled")
        return self.invoke_reserved(call, secret=secret, constructor=constructor,
                                    child_context=child_context, root_approval=root_approval,
                                    interactive=interactive, payload=payload).value

    def invoke_reserved(self, call: AdapterCall, *, secret: SelectedSecret | None,
                        constructor: Callable[..., Any],
                        child_context: ChildOperationContext | None = None,
                        root_approval: ApprovalCredential | None = None, interactive: bool = False,
                        payload: Any = None) -> AdapterResult:
        """``invoke`` plus the explicit per-call reservation the caller must resolve."""
        if not callable(constructor):
            raise AdapterAuthorizationError("adapter constructor must be callable")
        entry = INVENTORY_BY_NAME.get(call.entry)
        if entry is None or call.operation_id != self.claim.operation_id:
            raise AdapterAuthorizationError("adapter call is not bound to this operation")
        self._authorize_context(call, entry, child_context, root_approval, interactive)
        self._authorize_scope(call, entry, secret)
        reservation = self._predebit(call, entry)
        # Construction is deliberately last.  No SDK, subprocess, or HTTP object
        # can exist before all scope and budget checks pass.
        try:
            value = constructor(secret.value if secret else None, payload, {"retries": 0})
        except BaseException:
            # An abandoned construction produced nothing, so its reservation was
            # never consumed and must not leak.  Settled seconds stay settled.
            if reservation is not None:
                self._resolve(reservation, actual=None, billed=BILLED_USAGE_UNAVAILABLE, quiet=True)
            raise
        finally:
            with self._lock:
                self._inflight -= 1
        return AdapterResult(value, reservation)

    def settle(self, reservation: AdapterReservation, actual: int, *,
               billed: Any = BILLED_USAGE_UNAVAILABLE) -> OperationHold:
        """Charge the verified actual for one adapter call and release the remainder."""
        return self._resolve(reservation, actual=actual, billed=billed, quiet=False)

    def release(self, reservation: AdapterReservation) -> OperationHold:
        """Return an unconsumed reservation (rejected or skipped chunk) to the budget."""
        return self._resolve(reservation, actual=None, billed=BILLED_USAGE_UNAVAILABLE, quiet=False)

    def _resolve(self, reservation: AdapterReservation, *, actual: int | None,
                 billed: Any, quiet: bool) -> OperationHold | None:
        # Settlement takes the same lock that guards hold placement and the
        # in-flight slot, so four concurrent chunks neither over-reserve nor
        # collide on hold ids.
        with self._lock:
            ledger = self._live_ledger(reservation, quiet=quiet)
            if ledger is None:
                return None
            try:
                hold = (ledger.release(reservation.hold_id) if actual is None
                        else ledger.settle(reservation.hold_id, actual, billed=billed))
            except LedgerStateError:
                if not quiet:
                    raise
                # fail()/cancel() already released every outstanding hold and
                # reported the run's settled seconds as paid-but-destroyed.
                self._reservations.pop(reservation.hold_id, None)
                return None
            self._reservations.pop(reservation.hold_id, None)
            return hold

    def _live_ledger(self, reservation: AdapterReservation, *, quiet: bool) -> OperationLedger | None:
        if not isinstance(reservation, AdapterReservation):
            raise AdapterAuthorizationError("reservation must be an AdapterReservation")
        if self._ledger is None or reservation.budget != self._ledger.resource:
            raise AdapterAuthorizationError("this adapter holds no ledger for that budget")
        if self._reservations.get(reservation.hold_id) != reservation.call_digest:
            if quiet:
                return None
            raise AdapterAuthorizationError("reservation does not name a live hold for this adapter call")
        return self._ledger

    def _authorize_context(self, call: AdapterCall, entry: EffectInventoryEntry,
                           context: ChildOperationContext | None,
                           root: ApprovalCredential | None, interactive: bool) -> None:
        if context is not None:
            expected = operation_subclaim_digest(call.operation_id, call.canonical_value())
            if (context.operation_id != self.claim.operation_id or context.member != call.entry
                    or context.subclaim_digest != expected or dict(context.budget) != {entry.budget: call.amount}):
                raise AdapterAuthorizationError("child context does not match the canonical adapter subclaim")
            return
        if not interactive or root is None or self._consent is None:
            raise AdapterAuthorizationError("fd3 child context or fresh interactive root approval is required")
        # Redeem is intentionally one-use, making each direct interactive effect fresh.
        self._consent.redeem(root, self.claim)

    def _authorize_scope(self, call: AdapterCall, entry: EffectInventoryEntry, secret: SelectedSecret | None) -> None:
        if self.claim.ingress != call.ingress:
            raise AdapterAuthorizationError("ingress is undeclared")
        mode = AuthMode.OAUTH if self.claim.auth is AuthMode.AUTO else self.claim.auth
        if mode not in entry.auth_modes:
            raise AdapterAuthorizationError("auth mode is not allowed for this adapter")
        if entry.requires_secret != (secret is not None):
            raise AdapterAuthorizationError("exactly the selected provider secret is required")
        matches = [provider for provider in self.claim.providers if provider.provider == call.provider and provider.model == call.model and provider.task == call.task]
        if len(matches) != 1 or entry.provider != call.provider or entry.task != call.task:
            raise AdapterAuthorizationError("provider, model, or task is undeclared")
        approved = matches[0]
        if call.fallback is not None or approved.fallbacks:
            # Fallbacks are a plan-level descriptive value, not permission to switch
            # adapters.  This boundary has exactly one provider/model/task.
            raise AdapterAuthorizationError("fallbacks are not executable adapter authority")
        if call.attempt > self.claim.maxima.attempts:
            raise AdapterAuthorizationError("attempt exceeds the approved maximum")

    def _predebit(self, call: AdapterCall, entry: EffectInventoryEntry) -> AdapterReservation | None:
        """Reserve this call's budget immediately before construction.

        The asymmetry below is deliberate.  Stage-12's "pre-debit at worst case
        and never refund" rule governs provider ATTEMPTS: attempts, tokens,
        items, searches, and recipients are spent by the act of constructing the
        call and are never given back.  The audio duration hold is not an
        attempt.  It is a reservation of worst-case seconds that the caller
        settles against the verified actual, so the untouched remainder returns
        to the budget.  Charging worst case per chunk *and* the actual on top
        would double-count (32 x 120 s = 3840 s against a 3600 s maximum) and
        would reject legal runs.  Do not unify these two paths.
        """
        amount = call.amount
        ledger = self._ledger if (self._ledger is not None
                                  and entry.budget == self._ledger.resource) else None
        limit = getattr(self.claim.maxima, entry.budget)
        with self._lock:
            if self._inflight >= self.claim.maxima.concurrency:
                raise AdapterBudgetError("concurrency exceeds the approved maximum")
            if ledger is None:
                if self._spent[entry.budget] + amount > limit:
                    raise AdapterBudgetError(f"{entry.budget} exceeds the approved maximum")
                self._spent[entry.budget] += amount
                self._inflight += 1
                # The caller constructs synchronously while this slot remains
                # reserved.  Failed construction still consumes this budget.
                return None
            try:
                hold = ledger.hold(amount, label=f"{call.entry}:{call.step_id}:{call.attempt}")
            except LedgerBudgetError as exc:
                raise AdapterBudgetError(f"{entry.budget} exceeds the approved maximum") from exc
            except LedgerStateError as exc:
                raise AdapterBudgetError(f"{entry.budget} ledger accepts no further effects") from exc
            reservation = AdapterReservation(entry=entry.name, budget=entry.budget,
                                             call_digest=call.digest, hold_id=hold.hold_id,
                                             reserved=hold.reserved)
            self._reservations[hold.hold_id] = reservation.call_digest
            self._inflight += 1
            return reservation


def resolve_auth_for_entry(entry: str, requested: AuthMode | str, *, oauth_available: bool,
                           api_key_available: bool) -> AuthMode:
    """Resolve `auto` to OAuth only; API keys never become an implicit fallback."""
    try:
        requested = AuthMode(requested)
    except ValueError as exc:
        raise AdapterAuthorizationError("auth mode is undeclared") from exc
    inventory = INVENTORY_BY_NAME.get(entry)
    if inventory is None:
        raise AdapterAuthorizationError("adapter entry is undeclared")
    if requested is AuthMode.AUTO:
        if AuthMode.OAUTH not in inventory.auth_modes or not oauth_available:
            raise AdapterAuthorizationError("auto requires this entry's OAuth authority")
        return AuthMode.OAUTH
    if requested not in inventory.auth_modes:
        raise AdapterAuthorizationError("auth mode is not allowed for this adapter")
    if requested is AuthMode.OAUTH and not oauth_available:
        raise AdapterAuthorizationError("OAuth is unavailable")
    if requested is AuthMode.API_KEY and not api_key_available:
        raise AdapterAuthorizationError("API key is unavailable")
    return requested
