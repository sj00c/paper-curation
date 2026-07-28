"""Unit tests for the hold/settle duration ledger in the consent core."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from pipeline.lib.audio_operation import MAX_CHUNKS, MAX_CHUNK_SECONDS, MAX_TARGET_SECONDS
from pipeline.lib.operation_consent import (
    BILLED_USAGE_UNAVAILABLE,
    AuthMode,
    ConsentError,
    HoldState,
    LedgerBudgetError,
    LedgerInvariantError,
    LedgerOverspendError,
    LedgerState,
    LedgerStateError,
    OperationClaim,
    OperationHold,
    OperationLedger,
    OperationLedgerRecord,
    OperationMaxima,
    canonical_json_bytes,
    whole_units,
)


WORST_CASE = MAX_CHUNK_SECONDS
BUDGET = MAX_TARGET_SECONDS


def ledger(budget: int = BUDGET, *, now: float = 100.9) -> OperationLedger:
    return OperationLedger(budget, operation_id="audio-1", clock=lambda: now)


class HoldSettleLedgerTests(unittest.TestCase):
    def test_hold_reserves_without_debiting_and_settle_charges_actual(self):
        book = ledger()
        hold = book.hold(WORST_CASE, label="A02.tts.1")

        self.assertEqual(hold.state, HoldState.HELD)
        self.assertEqual((hold.reserved, hold.settled, hold.released), (WORST_CASE, 0, 0))
        self.assertEqual(hold.held_at, 100)
        # A hold is a reservation, not a debit: nothing is settled yet, but the
        # worst case is unavailable to any other hold while it is outstanding.
        self.assertEqual((book.settled, book.outstanding), (0, WORST_CASE))
        self.assertEqual(book.remaining, BUDGET - WORST_CASE)

        settled = book.settle(hold, 101)
        self.assertEqual(settled.state, HoldState.SETTLED)
        self.assertEqual((settled.settled, settled.released), (101, WORST_CASE - 101))
        self.assertEqual(settled.resolved_at, 100)
        self.assertEqual((book.settled, book.released, book.outstanding), (101, WORST_CASE - 101, 0))
        self.assertEqual(book.remaining, BUDGET - 101)

        record = book.complete()
        self.assertEqual(record.state, LedgerState.COMPLETED)
        self.assertEqual((record.reserved, record.settled, record.destroyed), (WORST_CASE, 101, 0))
        with self.assertRaises(FrozenInstanceError):
            record.settled = 0

    def test_settling_the_full_hold_releases_nothing(self):
        book = ledger()
        settled = book.settle(book.hold(WORST_CASE), WORST_CASE)
        self.assertEqual((settled.settled, settled.released), (WORST_CASE, 0))
        self.assertEqual(book.remaining, BUDGET - WORST_CASE)

    def test_reserved_always_covers_actual_and_the_invariant_is_a_real_check(self):
        book = ledger()
        holds = [book.hold(WORST_CASE, label=f"A02.tts.{ordinal}") for ordinal in range(1, 5)]
        book.assert_invariants()
        for index, hold in enumerate(holds):
            book.settle(hold, 90 + index)
            book.assert_invariants()
            record = book.record()
            self.assertGreaterEqual(record.reserved, record.actual)
            self.assertTrue(record.invariant_holds)
        self.assertEqual(book.record().actual, book.settled)

        # The assertion is not a tautology: a record whose settled usage exceeds
        # its budget is structurally representable and must be rejected.
        broken = OperationLedgerRecord(
            operation_id="audio-1", resource="audio_seconds", budget=10,
            reserved=20, outstanding=0, settled=20, released=0, destroyed=0,
        )
        self.assertFalse(broken.invariant_holds)
        with self.assertRaises(LedgerInvariantError):
            broken.assert_invariants()

    def test_actual_greater_than_hold_raises_and_never_clamps(self):
        book = ledger()
        hold = book.hold(WORST_CASE)
        before = canonical_json_bytes(book.record())

        with self.assertRaises(LedgerOverspendError) as caught:
            book.settle(hold, WORST_CASE + 1)
        self.assertIn(str(WORST_CASE + 1), str(caught.exception))
        self.assertIsInstance(caught.exception, ConsentError)

        # No silent clamp: the hold is untouched and still settleable.
        self.assertEqual(canonical_json_bytes(book.record()), before)
        self.assertEqual((book.settled, book.outstanding), (0, WORST_CASE))
        self.assertEqual(book.settle(hold, WORST_CASE).settled, WORST_CASE)

        with self.assertRaises(ConsentError):
            OperationHold("h", "h", 10, state=HoldState.SETTLED, settled=11, released=0)

    def test_billed_usage_is_unavailable_when_the_provider_reports_nothing(self):
        book = ledger()
        # Gemini returns token usageMetadata, not billed audio seconds, so the
        # sentinel is the normal case rather than an error path.
        settled = book.settle(book.hold(WORST_CASE), 100)
        self.assertIs(settled.billed, BILLED_USAGE_UNAVAILABLE)
        self.assertIs(book.record().billed, BILLED_USAGE_UNAVAILABLE)
        self.assertFalse(bool(BILLED_USAGE_UNAVAILABLE))
        self.assertEqual(repr(BILLED_USAGE_UNAVAILABLE), "BILLED_USAGE_UNAVAILABLE")
        self.assertIn(b'"billed":null', canonical_json_bytes(book.record()))

        explicit_none = ledger()
        self.assertIs(
            explicit_none.settle(explicit_none.hold(WORST_CASE), 100, billed=None).billed,
            BILLED_USAGE_UNAVAILABLE,
        )

        # Zero is a provider claim; the sentinel is the absence of one.
        zero = ledger()
        reported = zero.settle(zero.hold(WORST_CASE), 100, billed=0)
        self.assertEqual(reported.billed, 0)
        self.assertIsNot(reported.billed, BILLED_USAGE_UNAVAILABLE)
        self.assertIsNot(zero.record().billed, BILLED_USAGE_UNAVAILABLE)

    def test_billed_usage_is_advisory_and_never_gates_authorization(self):
        book = ledger()
        book.settle(book.hold(WORST_CASE), 100, billed=1_000_000)

        # Billed usage dwarfs the entire budget and still changes nothing.
        self.assertEqual(book.record().billed, 1_000_000)
        self.assertEqual(book.settled, 100)
        self.assertEqual(book.remaining, BUDGET - 100)
        for _ in range(MAX_CHUNKS - 1):
            book.settle(book.hold(WORST_CASE), 100, billed=1_000_000)
        record = book.complete()
        self.assertEqual(record.state, LedgerState.COMPLETED)
        self.assertEqual(record.settled, 100 * MAX_CHUNKS)
        self.assertEqual(record.billed, 1_000_000 * MAX_CHUNKS)
        self.assertGreater(record.billed, record.budget)
        self.assertGreaterEqual(record.remaining, 0)
        self.assertEqual(record.canonical_value()["billed"], 1_000_000 * MAX_CHUNKS)

    def test_partial_failure_keeps_settled_chunks_and_releases_the_outstanding_hold(self):
        book = ledger()
        settled_holds = [book.settle(book.hold(WORST_CASE, label=f"A02.tts.{n}"), 110) for n in (1, 2, 3)]
        malformed = book.hold(WORST_CASE, label="A02.tts.4")

        book.release(malformed)
        record = book.fail("A02.tts.4 returned malformed PCM")

        self.assertEqual(record.state, LedgerState.FAILED)
        self.assertEqual(record.reason, "A02.tts.4 returned malformed PCM")
        self.assertEqual(record.settled, 330)
        self.assertEqual(record.outstanding, 0)
        self.assertEqual(record.released, 3 * (WORST_CASE - 110) + WORST_CASE)
        self.assertEqual(record.reserved, 4 * WORST_CASE)
        # The spend really happened: settled chunks are never refunded, and the
        # paid-but-destroyed amount is surfaced rather than hidden.
        self.assertEqual(record.destroyed, 330)
        self.assertEqual(record.remaining, BUDGET - 330)
        self.assertTrue(all(hold.state is HoldState.SETTLED for hold in settled_holds))
        self.assertEqual(
            [hold.state for hold in record.holds][-1], HoldState.RELEASED,
        )
        record.assert_invariants()

        for call in (lambda: book.hold(WORST_CASE), lambda: book.settle(malformed, 1),
                     lambda: book.release(malformed), lambda: book.complete(),
                     lambda: book.cancel("late")):
            with self.assertRaises(LedgerStateError):
                call()

    def test_mid_stream_cancellation_releases_in_flight_holds_and_reports_destroyed(self):
        book = ledger()
        book.settle(book.hold(WORST_CASE, label="A02.tts.1"), 118)
        book.settle(book.hold(WORST_CASE, label="A02.tts.2"), 112)
        in_flight = book.hold(WORST_CASE, label="A02.tts.3")
        self.assertEqual(book.outstanding, WORST_CASE)

        record = book.cancel("cancelled mid-stream by the caller")

        self.assertEqual(record.state, LedgerState.CANCELLED)
        self.assertEqual(record.reason, "cancelled mid-stream by the caller")
        self.assertEqual(record.settled, 230)
        self.assertEqual(record.destroyed, 230)
        self.assertEqual(record.outstanding, 0)
        self.assertEqual(record.remaining, BUDGET - 230)
        self.assertEqual(record.holds[-1].hold_id, in_flight.hold_id)
        self.assertEqual(record.holds[-1].state, HoldState.RELEASED)
        self.assertEqual(record.holds[-1].released, WORST_CASE)
        self.assertTrue(all(hold.state is not HoldState.HELD for hold in record.holds))

    def test_double_settle_double_release_and_unknown_holds_raise_without_corruption(self):
        book = ledger()
        hold = book.hold(WORST_CASE)
        book.settle(hold, 100)
        after_settle = canonical_json_bytes(book.record())

        for call in (lambda: book.settle(hold, 1), lambda: book.release(hold),
                     lambda: book.settle("audio_seconds-99", 1),
                     lambda: book.release("audio_seconds-99"),
                     lambda: book.settle(OperationHold("ghost", "ghost", 5), 1)):
            with self.assertRaises(LedgerStateError):
                call()
            self.assertEqual(canonical_json_bytes(book.record()), after_settle)

        released_book = ledger()
        released = released_book.hold(WORST_CASE)
        released_book.release(released)
        after_release = canonical_json_bytes(released_book.record())
        for call in (lambda: released_book.release(released), lambda: released_book.settle(released, 1)):
            with self.assertRaises(LedgerStateError):
                call()
            self.assertEqual(canonical_json_bytes(released_book.record()), after_release)

    def test_thirty_two_chunks_settle_actual_without_exhausting_the_budget(self):
        book = ledger()
        actual_seconds = 100.4
        actual = whole_units(actual_seconds)
        window: list[OperationHold] = []
        peak = 0

        for ordinal in range(1, MAX_CHUNKS + 1):
            # Worst case is reserved immediately before construction, four
            # chunks may be in flight, and each response settles its actual.
            window.append(book.hold(WORST_CASE, label=f"A02.tts.{ordinal}"))
            if len(window) == 4:
                book.settle(window.pop(0), actual)
            book.assert_invariants()
            peak = max(peak, book.settled + book.outstanding)
        for hold in window:
            book.settle(hold, actual)

        record = book.complete()
        self.assertEqual(len(record.holds), MAX_CHUNKS)
        self.assertEqual(record.settled, MAX_CHUNKS * actual)
        self.assertEqual(record.reserved, MAX_CHUNKS * WORST_CASE)
        self.assertEqual(record.released, MAX_CHUNKS * (WORST_CASE - actual))
        self.assertEqual(record.outstanding, 0)
        # Total reservations (3840) exceed the 3600 budget, yet the legal run
        # never does: only actual usage is charged, so nothing double-counts.
        self.assertGreater(record.reserved, record.budget)
        self.assertLessEqual(peak, record.budget)
        self.assertLess(record.settled, record.budget)
        self.assertEqual(record.remaining, BUDGET - MAX_CHUNKS * actual)
        self.assertEqual(record.destroyed, 0)
        record.assert_invariants()

    def test_worst_case_only_accounting_would_exhaust_the_same_budget(self):
        # Control for the test above: holding worst case for every chunk without
        # ever settling and releasing runs out after 30 of the 32 chunks.
        book = ledger()
        for _ in range(BUDGET // WORST_CASE):
            book.hold(WORST_CASE)
        self.assertEqual(book.outstanding, BUDGET)
        with self.assertRaises(LedgerBudgetError):
            book.hold(WORST_CASE)
        self.assertEqual(book.outstanding, BUDGET)
        self.assertLess(BUDGET // WORST_CASE, MAX_CHUNKS)

    def test_ledger_binds_to_one_approved_claim_budget(self):
        claim = OperationClaim(
            1, "audio-1", "audio", "audio.overview", "topic", "retained-audio-source", "localhost",
            AuthMode.OAUTH, maxima=OperationMaxima(attempts=33, audio_seconds=BUDGET, concurrency=4),
            created_at=100, expires_at=1000,
        )
        book = OperationLedger.for_claim(claim, clock=lambda: 100)
        self.assertEqual(book.budget, BUDGET)
        self.assertEqual(book.resource, "audio_seconds")
        self.assertEqual(book.record().operation_id, "audio-1")
        with self.assertRaises(ConsentError):
            OperationLedger.for_claim(claim, resource="not_a_budget")
        with self.assertRaises(ConsentError):
            OperationLedger.for_claim(claim.maxima)

    def test_ledger_rejects_invalid_amounts_and_measurements(self):
        book = ledger()
        for amount in (0, -1, True, 1.5, "120", None):
            with self.assertRaises(ConsentError):
                book.hold(amount)
        hold = book.hold(WORST_CASE)
        for actual in (-1, True, 1.5, "100", None):
            with self.assertRaises(ConsentError):
                book.settle(hold, actual)
        with self.assertRaises(ConsentError):
            book.settle(hold, 100, billed=-1)
        with self.assertRaises(ConsentError):
            book.fail("")
        self.assertEqual(book.outstanding, WORST_CASE)
        with self.assertRaises(LedgerStateError):
            book.complete()

    def test_whole_units_rounds_measured_seconds_up(self):
        self.assertEqual(whole_units(0), 0)
        self.assertEqual(whole_units(100.4), 101)
        self.assertEqual(whole_units(119.999), 120)
        self.assertEqual(whole_units(float(MAX_CHUNK_SECONDS)), MAX_CHUNK_SECONDS)
        for value in (-0.1, float("nan"), float("inf"), True, "1", None):
            with self.assertRaises(ConsentError):
                whole_units(value)


if __name__ == "__main__":
    unittest.main()
