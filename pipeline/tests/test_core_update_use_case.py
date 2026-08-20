"""Synthetic contracts for deterministic batch Core updates."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.application.curate import (
    CurationFailure,
    CurationRequest,
    CurationStage,
    CurationSuccess,
)
from paper_curation.application.update import (
    CoreUpdateResult,
    CoreUpdateRequest,
    CoreUpdateStatus,
    UpdateCore,
)
from paper_curation.domain.papers import Paper


def selection(record_id: str) -> CurationRequest:
    return CurationRequest("synthetic-source", "synthetic-scope", record_id)


def success(request: CurationRequest) -> CurationSuccess:
    return CurationSuccess(
        Paper(request.source_id, request.scope_id, request.record_id, "Synthetic paper"), ()
    )


class FakeCurate:
    def __init__(self, outcomes: dict[str, object]) -> None:
        self.outcomes = outcomes
        self.calls: list[str] = []

    def execute(self, request: CurationRequest):
        self.calls.append(request.record_id)
        outcome = self.outcomes[request.record_id]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class CoreUpdateUseCaseTests(unittest.TestCase):
    def test_preserves_selection_order_and_stable_record_identity(self) -> None:
        selections = (selection("third"), selection("first"), selection("second"))
        curate = FakeCurate({item.record_id: success(item) for item in selections})

        result = UpdateCore(curate).execute(CoreUpdateRequest(selections))

        self.assertEqual(curate.calls, ["third", "first", "second"])
        self.assertEqual(
            [record.identity for record in result.records],
            [
                ("synthetic-source", "synthetic-scope", "third"),
                ("synthetic-source", "synthetic-scope", "first"),
                ("synthetic-source", "synthetic-scope", "second"),
            ],
        )

    def test_rejects_duplicate_source_scope_record_before_execution(self) -> None:
        duplicate = selection("same")

        with self.assertRaisesRegex(ValueError, "duplicate Core record selection"):
            CoreUpdateRequest((duplicate, selection("same")))

    def test_continues_after_per_record_failure(self) -> None:
        first, second, third = selection("first"), selection("second"), selection("third")
        curate = FakeCurate(
            {
                "first": success(first),
                "second": CurationFailure(CurationStage.GENERATE_REVIEW, "review_failed"),
                "third": CurationFailure(CurationStage.EXTRACT_TEXT, "text_failed"),
            }
        )

        result = UpdateCore(curate).execute(CoreUpdateRequest((first, second, third)))

        self.assertEqual(curate.calls, ["first", "second", "third"])
        self.assertTrue(result.records[0].succeeded)
        self.assertEqual(result.records[1].result.code, "review_failed")
        self.assertEqual(result.records[2].result.code, "text_failed")
        self.assertEqual(result.status, CoreUpdateStatus.PARTIAL_FAILURE)
        self.assertEqual(result.exit_code, 1)

    def test_rejects_empty_selection_and_surfaces_unexpected_defects(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            CoreUpdateRequest(())
        with self.assertRaisesRegex(ValueError, "at least one"):
            CoreUpdateResult(())
        request = selection("broken")
        curate = FakeCurate({"broken": RuntimeError("unexpected defect")})
        with self.assertRaisesRegex(RuntimeError, "unexpected defect"):
            UpdateCore(curate).execute(CoreUpdateRequest((request,)))

    def test_all_success_has_successful_aggregate_exit(self) -> None:
        first, second = selection("first"), selection("second")
        curate = FakeCurate({"first": success(first), "second": success(second)})

        result = UpdateCore(curate).execute(CoreUpdateRequest((first, second)))

        self.assertEqual(result.status, CoreUpdateStatus.SUCCEEDED)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(result.succeeded)

    def test_all_failures_have_failed_aggregate_exit(self) -> None:
        first, second = selection("first"), selection("second")
        curate = FakeCurate(
            {
                "first": CurationFailure(CurationStage.IDENTIFY, "identity_failed"),
                "second": CurationFailure(CurationStage.EXTRACT_TEXT, "text_failed"),
            }
        )

        result = UpdateCore(curate).execute(CoreUpdateRequest((first, second)))

        self.assertEqual(result.status, CoreUpdateStatus.FAILED)
        self.assertEqual(result.exit_code, 1)
        self.assertFalse(result.succeeded)


if __name__ == "__main__":
    unittest.main()
