"""Contract tests for the provider-neutral Zotero curation boundary."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.application.curate import (
    CuratePaper,
    CurationFailure,
    CurationRequest,
    CurationSuccess,
)
from paper_curation.domain.papers import ArtifactRef, Attachment, Paper
from paper_curation.domain.papers import StageEvidence


def artifact(name: str) -> ArtifactRef:
    return ArtifactRef(name, f"papers/arbitrary-paper/{name}", f"sha256:{name}")


class FakeGateway:
    def __init__(self, papers: tuple[Paper, ...], attachments: tuple[Attachment, ...]):
        self.papers = papers
        self.attachments = attachments
        self.mutations: list[str] = []

    def list_collection(self, collection_key: str) -> tuple[Paper, ...]:
        return tuple(paper for paper in self.papers if paper.collection_key == collection_key)

    def list_attachments(self, paper_key: str) -> tuple[Attachment, ...]:
        return tuple(item for item in self.attachments if item.paper_key == paper_key)

    def mark_curated(self, paper_key: str) -> None:
        self.mutations.append(paper_key)


class FakePorts:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef:
        self.calls.append("attachment")
        return artifact("source.pdf")

    def extract(self, paper: Paper, source: ArtifactRef) -> ArtifactRef:
        self.calls.append("text")
        return artifact("text.md")

    def write(self, paper: Paper, text: ArtifactRef, review: ArtifactRef) -> ArtifactRef:
        self.calls.append("sidecar")
        return artifact("bibliography.json")

    def render(self, paper: Paper, review: ArtifactRef, sidecar: ArtifactRef) -> ArtifactRef:
        self.calls.append("page")
        return artifact("index.html")

    def extract_figures(self, paper: Paper, text: ArtifactRef) -> tuple[ArtifactRef, ...]:
        self.calls.append("figures")
        return (artifact("figures/figure-1.png"),)

    def write_review(
        self, paper: Paper, text: ArtifactRef, figures: tuple[ArtifactRef, ...]
    ) -> ArtifactRef:
        self.calls.append("review")
        return artifact("review.md")


class FigureFake:
    def __init__(self, ports: FakePorts) -> None:
        self.ports = ports

    def extract(self, paper: Paper, text: ArtifactRef) -> tuple[ArtifactRef, ...]:
        return self.ports.extract_figures(paper, text)


class ReviewFake:
    def __init__(self, ports: FakePorts) -> None:
        self.ports = ports

    def write(self, paper: Paper, text: ArtifactRef, figures: tuple[ArtifactRef, ...]) -> ArtifactRef:
        return self.ports.write_review(paper, text, figures)


def use_case(gateway: FakeGateway, ports: FakePorts) -> CuratePaper:
    class Verifier:
        def valid(self, evidence):
            return all(item.fingerprint.startswith("sha256:") for item in evidence.artifacts)

    return CuratePaper(
        source=gateway,
        attachments=ports,
        text=ports,
        figures=FigureFake(ports),
        reviews=ReviewFake(ports),
        sidecars=ports,
        pages=ports,
        mutator=gateway,
        evidence_verifier=Verifier(),
    )


class ZoteroCurationBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.paper = Paper("PAPER-1", "Arbitrary topic paper", "any-collection")
        self.gateway = FakeGateway(
            (self.paper,), (Attachment("PDF-1", "PAPER-1", "paper.pdf"),)
        )
        self.ports = FakePorts()

    def test_curates_an_arbitrary_collection_with_stage_evidence_without_mutation(self) -> None:
        result = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1")
        )

        self.assertIsInstance(result, CurationSuccess)
        assert isinstance(result, CurationSuccess)
        self.assertEqual(
            self.ports.calls, ["attachment", "text", "figures", "review", "sidecar", "page"]
        )
        self.assertEqual(self.gateway.mutations, [])
        self.assertEqual(
            [stage.stage for stage in result.evidence],
            ["attachment", "text", "figures", "review", "sidecar", "page"],
        )
        self.assertIn("papers/arbitrary-paper/review.md", result.artifact_paths)
        self.assertIn("sha256:bibliography.json", result.artifact_fingerprints)

    def test_identity_failure_is_strict(self) -> None:
        result = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "different-key")
        )

        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "paper_identity_not_unique")
        self.assertEqual(self.ports.calls, [])
        self.assertEqual(self.gateway.mutations, [])

    def test_complete_evidence_resumes_idempotently_and_mutation_is_opt_in(self) -> None:
        first = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1")
        )
        assert isinstance(first, CurationSuccess)
        calls_before_resume = list(self.ports.calls)

        resumed = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1", resume=first.evidence)
        )
        self.assertIsInstance(resumed, CurationSuccess)
        self.assertEqual(self.ports.calls, calls_before_resume)
        self.assertEqual(self.gateway.mutations, [])

        requested = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1", request_external_mutation=True)
        )
        self.assertIsInstance(requested, CurationSuccess)
        self.assertEqual(self.gateway.mutations, ["PAPER-1"])

    def test_resume_evidence_must_be_a_contiguous_stage_prefix(self) -> None:
        stale_review = StageEvidence("review", (artifact("review.md"),), "sha256:review")
        result = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1", resume=(stale_review,))
        )
        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "invalid_resume_evidence")

    def test_resume_requires_verified_artifacts(self) -> None:
        operation = use_case(self.gateway, self.ports)
        operation = CuratePaper(
            source=operation.source,
            attachments=operation.attachments,
            text=operation.text,
            figures=operation.figures,
            reviews=operation.reviews,
            sidecars=operation.sidecars,
            pages=operation.pages,
            mutator=operation.mutator,
        )
        first = use_case(self.gateway, self.ports).execute(
            CurationRequest("any-collection", "PAPER-1")
        )
        assert isinstance(first, CurationSuccess)
        result = operation.execute(
            CurationRequest("any-collection", "PAPER-1", resume=first.evidence)
        )
        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "stale_resume_evidence")

    def test_paper_without_figures_still_completes(self) -> None:
        class NoFigures(FigureFake):
            def extract(self, paper, text):
                self.ports.calls.append("figures")
                return ()

        operation = use_case(self.gateway, self.ports)
        operation = CuratePaper(
            source=operation.source,
            attachments=operation.attachments,
            text=operation.text,
            figures=NoFigures(self.ports),
            reviews=operation.reviews,
            sidecars=operation.sidecars,
            pages=operation.pages,
            mutator=operation.mutator,
        )
        result = operation.execute(CurationRequest("any-collection", "PAPER-1"))
        self.assertIsInstance(result, CurationSuccess)


if __name__ == "__main__":
    unittest.main()
