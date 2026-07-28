"""Offline contract tests for fail-closed provider adapter boundaries."""
from __future__ import annotations

import threading
import unittest
from dataclasses import replace

from pipeline.lib.audio_operation import MAX_CHUNKS, MAX_CHUNK_SECONDS, MAX_TARGET_SECONDS
from pipeline.lib.child_context import ChildOperationContext, operation_subclaim_digest
from pipeline.lib.operation_consent import (
    AuthMode, HoldState, LedgerState, OperationClaim, OperationLedger, OperationMaxima, ProviderTask,
)
from pipeline.lib.provider_adapters import (
    AdapterAuthorizationError, AdapterBudgetError, AdapterCall, EFFECT_INVENTORY, INVENTORY_BY_NAME,
    ProviderAdapters, SelectedSecret, resolve_auth_for_entry,
)


DIGEST = "a" * 64


def claim(entry, **changes):
    values = dict(version=1, operation_id="op", task="query", command="query.normal", topic="topic",
                  source="snapshot", ingress="localhost",
                  auth=AuthMode.OAUTH if entry.name == "claude.oauth.cli" else AuthMode.API_KEY,
                  providers=(ProviderTask(entry.provider, "approved-model", entry.task),),
                  maxima=OperationMaxima(attempts=2, tokens=10, items=10, searches=10,
                                          audio_seconds=10, recipients=10, concurrency=1),
                  input_digests=(DIGEST,), created_at=1, expires_at=100)
    values.update(changes)
    return OperationClaim(**values)


def call(entry, **changes):
    values = dict(entry=entry.name, operation_id="op", step_id="step", provider=entry.provider,
                  model="approved-model", task=entry.task, attempt=1, ingress="localhost")
    values.update(changes)
    return AdapterCall(**values)


def context(value):
    entry = next(entry for entry in EFFECT_INVENTORY if entry.name == value.entry)
    return ChildOperationContext("op", operation_subclaim_digest("op", value.canonical_value()), value.entry,
                                 {entry.budget: value.amount})


class ProviderAdapterTests(unittest.TestCase):
    def test_every_inventory_entry_is_offline_and_predebits_before_constructor(self):
        for entry in EFFECT_INVENTORY:
            with self.subTest(entry=entry.name):
                adapter = ProviderAdapters(claim(entry))
                value = call(entry)
                observed = []

                def construct(secret, payload, options):
                    observed.append((secret, payload, options, adapter.spent()[entry.budget]))
                    return "offline"

                secret = SelectedSecret("only-this-secret") if entry.requires_secret else None
                self.assertEqual(adapter.invoke(value, secret=secret, constructor=construct,
                                                child_context=context(value), payload={"offline": True}), "offline")
                self.assertEqual(observed[0][2], {"retries": 0})
                self.assertEqual(observed[0][3], 1)

    def test_rejection_happens_before_constructor_and_secret_stays_redacted(self):
        entry = EFFECT_INVENTORY[1]
        value = call(entry, model="unapproved")
        invoked = []
        secret = SelectedSecret("provider-secret")
        with self.assertRaises(AdapterAuthorizationError):
            ProviderAdapters(claim(entry)).invoke(value, secret=secret,
                                                   constructor=lambda *_: invoked.append(True),
                                                   child_context=context(value))
        self.assertEqual(invoked, [])
        self.assertNotIn("provider-secret", repr(secret) + repr(value))

    def test_undeclared_attempt_fallback_ingress_and_budget_fail_closed(self):
        entry = EFFECT_INVENTORY[2]
        for changes in ({"attempt": 3}, {"fallback": "other"}, {"ingress": "remote"}):
            value = call(entry, **changes)
            with self.subTest(changes=changes), self.assertRaises(AdapterAuthorizationError):
                ProviderAdapters(claim(entry)).invoke(value, secret=SelectedSecret("s"),
                    constructor=lambda *_: None, child_context=context(value))
        limited = ProviderAdapters(claim(entry, maxima=OperationMaxima(attempts=2, tokens=1, concurrency=1)))
        value = call(entry, amount=2)
        with self.assertRaises(AdapterBudgetError):
            limited.invoke(value, secret=SelectedSecret("s"), constructor=lambda *_: None, child_context=context(value))

    def test_auto_is_oauth_only_and_api_key_has_no_carry(self):
        self.assertEqual(resolve_auth_for_entry("claude.oauth.cli", "auto", oauth_available=True,
                                                 api_key_available=False), AuthMode.OAUTH)
        with self.assertRaises(AdapterAuthorizationError):
            resolve_auth_for_entry("anthropic.api-key", "auto", oauth_available=True, api_key_available=True)
        with self.assertRaises(AdapterAuthorizationError):
            resolve_auth_for_entry("claude.oauth.cli", "api-key", oauth_available=True, api_key_available=True)

    def test_missing_child_context_rejects_noninteractive_before_constructor(self):
        entry = EFFECT_INVENTORY[1]
        invoked = []
        with self.assertRaises(AdapterAuthorizationError):
            ProviderAdapters(claim(entry)).invoke(call(entry), secret=SelectedSecret("s"),
                constructor=lambda *_: invoked.append(True))
        self.assertEqual(invoked, [])


TTS = INVENTORY_BY_NAME["gemini.tts"]
SCRIPT = INVENTORY_BY_NAME["gemini.script"]
ACTUAL = 100


def audio_claim(*, audio_seconds=MAX_TARGET_SECONDS, concurrency=1):
    return claim(TTS, maxima=OperationMaxima(attempts=2, audio_seconds=audio_seconds,
                                             concurrency=concurrency))


def chunk_call(ordinal, *, amount=MAX_CHUNK_SECONDS):
    return call(TTS, step_id=f"A02.tts.{ordinal}", amount=amount)


def wired(**changes):
    """One claim, one ledger bound to its audio_seconds maximum, one adapter."""
    approved = audio_claim(**changes)
    book = OperationLedger.for_claim(approved, clock=lambda: 100)
    return approved, book, ProviderAdapters(approved, ledger=book)


def run_chunk(adapter, value, constructor=lambda *_: "client"):
    return adapter.invoke_reserved(value, secret=SelectedSecret("only-this-secret"),
                                   constructor=constructor, child_context=context(value))


class LedgerBackedAudioBudgetTests(unittest.TestCase):
    def test_thirty_two_chunks_hold_worst_case_and_settle_actual_without_exhausting_the_budget(self):
        _, book, adapter = wired()
        peak = 0

        for ordinal in range(1, MAX_CHUNKS + 1):
            result = run_chunk(adapter, chunk_call(ordinal))
            self.assertEqual(result.value, "client")
            # Worst case is reserved before construction, never debited.
            self.assertEqual(result.reservation.reserved, MAX_CHUNK_SECONDS)
            self.assertEqual(book.outstanding, MAX_CHUNK_SECONDS)
            peak = max(peak, book.settled + book.outstanding)
            hold = adapter.settle(result.reservation, ACTUAL)
            self.assertEqual((hold.settled, hold.released), (ACTUAL, MAX_CHUNK_SECONDS - ACTUAL))
            book.assert_invariants()

        record = book.complete()
        self.assertEqual(record.state, LedgerState.COMPLETED)
        self.assertEqual(len(record.holds), MAX_CHUNKS)
        self.assertEqual(record.settled, MAX_CHUNKS * ACTUAL)
        self.assertEqual(record.reserved, MAX_CHUNKS * MAX_CHUNK_SECONDS)
        self.assertGreater(record.reserved, record.budget)
        self.assertLessEqual(peak, record.budget)
        self.assertEqual(record.outstanding, 0)
        self.assertEqual(record.destroyed, 0)

    def test_the_same_run_on_the_old_predebit_path_is_rejected(self):
        # Control for the test above: without a ledger the adapter permanently
        # debits the worst case, so a legal 32-chunk run dies after 30 chunks.
        adapter = ProviderAdapters(audio_claim())
        constructed = 0

        with self.assertRaises(AdapterBudgetError):
            for ordinal in range(1, MAX_CHUNKS + 1):
                value = chunk_call(ordinal)
                adapter.invoke(value, secret=SelectedSecret("only-this-secret"),
                               constructor=lambda *_: "client", child_context=context(value))
                constructed += 1

        self.assertEqual(constructed, MAX_TARGET_SECONDS // MAX_CHUNK_SECONDS)
        self.assertLess(constructed, MAX_CHUNKS)
        self.assertEqual(adapter.spent()["audio_seconds"], MAX_TARGET_SECONDS)

    def test_settling_charges_the_actual_once_and_never_the_worst_case_on_top(self):
        _, book, adapter = wired()
        result = run_chunk(adapter, chunk_call(1))

        # In flight: the worst case is unavailable but nothing is charged yet.
        self.assertEqual(adapter.spent()["audio_seconds"], MAX_CHUNK_SECONDS)
        self.assertEqual((book.settled, book.outstanding), (0, MAX_CHUNK_SECONDS))

        adapter.settle(result.reservation, ACTUAL)

        self.assertEqual(adapter.spent()["audio_seconds"], ACTUAL)
        self.assertNotEqual(adapter.spent()["audio_seconds"], ACTUAL + MAX_CHUNK_SECONDS)
        self.assertEqual(book.settled, ACTUAL)
        self.assertEqual(book.released, MAX_CHUNK_SECONDS - ACTUAL)
        self.assertEqual(book.remaining, MAX_TARGET_SECONDS - ACTUAL)

    def test_a_reservation_resolves_only_its_own_hold_and_only_once(self):
        _, book, adapter = wired(concurrency=4)
        reservations = [run_chunk(adapter, chunk_call(ordinal)).reservation
                        for ordinal in range(1, 5)]

        self.assertEqual(len({held.hold_id for held in reservations}), 4)
        self.assertEqual(len({held.call_digest for held in reservations}), 4)
        self.assertEqual(book.outstanding, 4 * MAX_CHUNK_SECONDS)

        # Settling out of order resolves the named hold, never the most recent.
        hold = adapter.settle(reservations[1], 90)
        self.assertEqual(hold.hold_id, reservations[1].hold_id)
        self.assertEqual(hold.label, "gemini.tts:A02.tts.2:1")
        self.assertEqual(hold.settled, 90)

        # A resolved reservation is dead, so a replay cannot double-charge.
        with self.assertRaises(AdapterAuthorizationError):
            adapter.settle(reservations[1], 90)
        # A handle forged from another call's digest names no live hold.
        with self.assertRaises(AdapterAuthorizationError):
            adapter.settle(replace(reservations[2], call_digest=reservations[0].call_digest), 90)
        with self.assertRaises(AdapterAuthorizationError):
            adapter.settle("audio_seconds-1", 90)

        self.assertEqual(book.settled, 90)
        self.assertEqual(book.outstanding, 3 * MAX_CHUNK_SECONDS)

    def test_four_concurrent_chunks_never_cross_settle(self):
        _, book, adapter = wired(concurrency=4)
        barrier = threading.Barrier(4, timeout=10)
        settled: dict[int, object] = {}
        reserved: dict[int, str] = {}
        errors: list[BaseException] = []

        def chunk(ordinal):
            try:
                # The barrier keeps all four constructions in flight at once, so
                # every hold is placed before any of them settles.
                result = run_chunk(adapter, chunk_call(ordinal), lambda *_: barrier.wait())
                reserved[ordinal] = result.reservation.hold_id
                settled[ordinal] = adapter.settle(result.reservation, ACTUAL + ordinal)
            except BaseException as exc:  # surfaced on the main thread below
                errors.append(exc)
                barrier.abort()

        threads = [threading.Thread(target=chunk, args=(ordinal,)) for ordinal in range(1, 5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        self.assertEqual([repr(error) for error in errors], [])
        self.assertEqual(len(set(reserved.values())), 4)
        for ordinal in range(1, 5):
            hold = settled[ordinal]
            self.assertEqual(hold.hold_id, reserved[ordinal])
            self.assertEqual(hold.settled, ACTUAL + ordinal)
            self.assertEqual(hold.label, f"gemini.tts:A02.tts.{ordinal}:1")
        self.assertEqual(book.settled, sum(ACTUAL + ordinal for ordinal in range(1, 5)))
        self.assertEqual(book.outstanding, 0)
        self.assertEqual(adapter.spent()["audio_seconds"], book.settled)

    def test_a_constructor_that_raises_leaks_no_hold(self):
        _, book, adapter = wired()

        def boom(*_):
            raise RuntimeError("provider client construction failed")

        with self.assertRaises(RuntimeError):
            run_chunk(adapter, chunk_call(1), boom)

        self.assertEqual((book.outstanding, book.settled), (0, 0))
        self.assertEqual(book.released, MAX_CHUNK_SECONDS)
        self.assertEqual(book.record().holds[0].state, HoldState.RELEASED)
        self.assertEqual(book.remaining, MAX_TARGET_SECONDS)
        self.assertEqual(adapter.spent()["audio_seconds"], 0)
        # The returned reservation is immediately usable by the next chunk.
        adapter.settle(run_chunk(adapter, chunk_call(2)).reservation, ACTUAL)
        self.assertEqual(book.settled, ACTUAL)

    def test_an_abandoned_run_records_paid_but_destroyed_rather_than_an_open_hold(self):
        _, book, adapter = wired()
        adapter.settle(run_chunk(adapter, chunk_call(1)).reservation, ACTUAL)

        def abandon(*_):
            book.fail("A02.tts.2 returned malformed PCM")
            raise RuntimeError("abandoned mid-construction")

        with self.assertRaises(RuntimeError):
            run_chunk(adapter, chunk_call(2), abandon)

        record = book.record()
        self.assertEqual(record.state, LedgerState.FAILED)
        self.assertEqual(record.outstanding, 0)
        self.assertEqual((record.settled, record.destroyed), (ACTUAL, ACTUAL))
        record.assert_invariants()

    def test_invoke_refuses_ledger_backed_budgets_so_no_hold_can_leak(self):
        _, book, adapter = wired()
        value = chunk_call(1)
        invoked = []

        with self.assertRaises(AdapterAuthorizationError):
            adapter.invoke(value, secret=SelectedSecret("only-this-secret"),
                           constructor=lambda *_: invoked.append(True), child_context=context(value))

        self.assertEqual(invoked, [])
        self.assertEqual((book.reserved, book.outstanding), (0, 0))

    def test_a_hold_beyond_the_budget_fails_closed_and_a_settlement_frees_it(self):
        _, book, adapter = wired(audio_seconds=200)
        first = run_chunk(adapter, chunk_call(1)).reservation
        second = chunk_call(2)

        with self.assertRaises(AdapterBudgetError):
            run_chunk(adapter, second)
        self.assertEqual(book.outstanding, MAX_CHUNK_SECONDS)

        adapter.settle(first, 40)
        self.assertEqual(run_chunk(adapter, second).reservation.reserved, MAX_CHUNK_SECONDS)
        self.assertEqual(book.settled + book.outstanding, 40 + MAX_CHUNK_SECONDS)

    def test_non_audio_budgets_keep_the_never_refunded_predebit(self):
        approved = claim(SCRIPT, maxima=OperationMaxima(attempts=2, tokens=3,
                                                        audio_seconds=MAX_TARGET_SECONDS,
                                                        concurrency=1))
        book = OperationLedger.for_claim(approved, clock=lambda: 100)
        adapter = ProviderAdapters(approved, ledger=book)
        value = call(SCRIPT, amount=2)

        def boom(*_):
            raise RuntimeError("transport failed")

        with self.assertRaises(RuntimeError):
            adapter.invoke(value, secret=SelectedSecret("only-this-secret"), constructor=boom,
                           child_context=context(value))

        # Stage-12: a spent attempt is never refunded, ledger or not.
        self.assertEqual(adapter.spent()["tokens"], 2)
        self.assertEqual((book.reserved, book.outstanding), (0, 0))
        with self.assertRaises(AdapterBudgetError):
            adapter.invoke(value, secret=SelectedSecret("only-this-secret"),
                           constructor=lambda *_: "client", child_context=context(value))
        self.assertEqual(adapter.spent()["tokens"], 2)

    def test_a_ledger_must_be_bound_to_exactly_the_approved_maximum(self):
        approved = audio_claim()
        for bad in (object(),
                    OperationLedger(1, resource="not_a_budget"),
                    OperationLedger(MAX_TARGET_SECONDS - 1)):
            with self.subTest(ledger=repr(bad)), self.assertRaises(AdapterAuthorizationError):
                ProviderAdapters(approved, ledger=bad)
        self.assertIs(ProviderAdapters(approved).ledger, None)
