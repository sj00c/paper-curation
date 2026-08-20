"""Contract tests for optional enhancements after a committed Core result."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.application.curate import CurationSuccess
from paper_curation.application.enhance import (
    EnhancePaper,
    EnhancementBlocked,
    EnhancementFailure,
    EnhancementRequest,
    EnhancementSuccess,
)
from paper_curation.domain.papers import ArtifactRef, Paper, StageEvidence


def artifact(name: str) -> ArtifactRef:
    return ArtifactRef(name, f"papers/arbitrary-paper/{name}", f"sha256:{name}")


def core_result(*, receipt: ArtifactRef | None = None) -> CurationSuccess:
    paper = Paper("source", "scope", "record", "Arbitrary topic paper")
    evidence = ()
    if receipt is not None:
        evidence = (StageEvidence("commit_receipt", (receipt,), receipt.fingerprint),)
    return CurationSuccess(paper, evidence)


class Verifier:
    def __init__(self, valid: bool = True) -> None:
        self.valid_result = valid
        self.receipts: list[ArtifactRef] = []

    def valid(self, receipt: ArtifactRef) -> bool:
        self.receipts.append(receipt)
        return self.valid_result


class Enhancement:
    def __init__(self, artifacts: tuple[ArtifactRef, ...] = ()) -> None:
        self.artifacts = artifacts
        self.calls: list[tuple[Paper, ArtifactRef, str, str]] = []

    def generate(
        self,
        paper: Paper,
        receipt: ArtifactRef,
        capability: str,
        provider_id: str,
    ) -> tuple[ArtifactRef, ...]:
        self.calls.append((paper, receipt, capability, provider_id))
        return self.artifacts


class FailingEnhancement(Enhancement):
    def generate(
        self,
        paper: Paper,
        receipt: ArtifactRef,
        capability: str,
        provider_id: str,
    ) -> tuple[ArtifactRef, ...]:
        self.calls.append((paper, receipt, capability, provider_id))
        raise RuntimeError("selected provider failed")


class EnhancementUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = artifact("receipt.json")
        self.core = core_result(receipt=self.receipt)
        self.request = EnhancementRequest("metrics", "selected-metrics-provider")

    def test_valid_receipt_runs_exact_request_and_records_provenance(self) -> None:
        verifier = Verifier()
        port = Enhancement((artifact("metrics.json"),))

        result = EnhancePaper(port, verifier).execute(self.request, self.core)

        self.assertIsInstance(result, EnhancementSuccess)
        assert isinstance(result, EnhancementSuccess)
        self.assertIs(result.core, self.core)
        self.assertEqual(result.capability, "metrics")
        self.assertEqual(result.provider_id, "selected-metrics-provider")
        self.assertEqual(result.artifacts, (artifact("metrics.json"),))
        self.assertEqual(verifier.receipts, [self.receipt])
        self.assertEqual(
            port.calls,
            [(self.core.paper, self.receipt, "metrics", "selected-metrics-provider")],
        )

    def test_missing_or_stale_receipt_blocks_without_calling_provider(self) -> None:
        for core, verifier, code in (
            (core_result(), Verifier(), "core_receipt_missing"),
            (self.core, Verifier(valid=False), "core_receipt_stale"),
        ):
            with self.subTest(code=code):
                port = Enhancement((artifact("metrics.json"),))

                result = EnhancePaper(port, verifier).execute(self.request, core)

                self.assertIsInstance(result, EnhancementBlocked)
                assert isinstance(result, EnhancementBlocked)
                self.assertIs(result.core, core)
                self.assertEqual(result.code, code)
                self.assertEqual(port.calls, [])

    def test_provider_failure_is_sanitized_and_not_retried(self) -> None:
        port = FailingEnhancement()

        result = EnhancePaper(port, Verifier()).execute(self.request, self.core)

        self.assertIsInstance(result, EnhancementFailure)
        assert isinstance(result, EnhancementFailure)
        self.assertIs(result.core, self.core)
        self.assertEqual(result.code, "enhancement_generation_failed")
        self.assertEqual(len(port.calls), 1)

    def test_empty_artifacts_fails_without_changing_baseline(self) -> None:
        port = Enhancement()

        result = EnhancePaper(port, Verifier()).execute(self.request, self.core)

        self.assertIsInstance(result, EnhancementFailure)
        assert isinstance(result, EnhancementFailure)
        self.assertIs(result.core, self.core)
        self.assertEqual(result.code, "enhancement_generation_failed")
        self.assertEqual(self.core.evidence, (StageEvidence("commit_receipt", (self.receipt,), self.receipt.fingerprint),))
        self.assertEqual(len(port.calls), 1)


if __name__ == "__main__":
    unittest.main()
