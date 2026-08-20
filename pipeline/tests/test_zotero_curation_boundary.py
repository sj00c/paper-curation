"""Contract tests for the source-neutral Core curation boundary."""

import sys
import unittest
from dataclasses import replace
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
from paper_curation.domain.papers import (
    ArtifactRef,
    Attachment,
    Paper,
    StageEvidence,
    paper_identity_fingerprint,
)


def artifact(name: str) -> ArtifactRef:
    return ArtifactRef(name, f"papers/arbitrary-paper/{name}", f"sha256:{name}")


class FakeSource:
    def __init__(self, papers: tuple[Paper, ...], attachments: tuple[Attachment, ...]):
        self.papers = papers
        self.attachments = attachments

    def list_records(self, source_id: str, scope_id: str) -> tuple[Paper, ...]:
        return tuple(
            paper
            for paper in self.papers
            if paper.source_id == source_id and paper.scope_id == scope_id
        )

    def list_attachments(self, paper: Paper) -> tuple[Attachment, ...]:
        return tuple(
            item
            for item in self.attachments
            if (
                item.source_id == paper.source_id
                and item.scope_id == paper.scope_id
                and item.record_id == paper.record_id
            )
        )


class FakePorts:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.receipt_evidence: tuple[StageEvidence, ...] = ()

    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef:
        self.calls.append("materialize_source")
        return artifact("source.pdf")

    def extract(self, paper: Paper, source: ArtifactRef) -> ArtifactRef:
        self.calls.append("extract_text")
        return artifact("text.md")

    def write(self, paper: Paper, text: ArtifactRef) -> ArtifactRef:
        self.calls.append("generate_review")
        return artifact("review.md")

    def write_sidecar(
        self,
        paper: Paper,
        text: ArtifactRef,
        review: ArtifactRef,
        review_provider_id: str,
        review_model_id: str,
    ) -> ArtifactRef:
        self.calls.append(f"write_sidecar:{review_provider_id}:{review_model_id}")
        return artifact("bibliography.json")

    def render(self, paper: Paper, review: ArtifactRef, sidecar: ArtifactRef) -> ArtifactRef:
        self.calls.append("render_page")
        return artifact("index.html")

    def commit(self, paper: Paper, evidence: tuple[StageEvidence, ...]) -> ArtifactRef:
        self.calls.append("commit_receipt")
        self.receipt_evidence = evidence
        return artifact("receipt.json")


class SidecarFake:
    def __init__(self, ports: FakePorts) -> None:
        self.ports = ports

    def write(self, paper, text, review, review_provider_id, review_model_id):
        return self.ports.write_sidecar(
            paper, text, review, review_provider_id, review_model_id
        )


class FailingReview:
    def __init__(self) -> None:
        self.calls = 0

    def write(self, paper: Paper, text: ArtifactRef) -> ArtifactRef:
        self.calls += 1
        raise RuntimeError("selected provider failed")


class AlternateReview:
    def __init__(self) -> None:
        self.calls = 0

    def write(self, paper: Paper, text: ArtifactRef) -> ArtifactRef:
        self.calls += 1
        return artifact("alternate-review.md")


def use_case(source: FakeSource, ports: FakePorts, reviews=None) -> CuratePaper:
    class Verifier:
        def valid(self, paper, evidence):
            return all(
                all(item.fingerprint for item in stage.artifacts)
                or stage.stage == "identify"
                for stage in evidence
            )

    return CuratePaper(
        source=source,
        attachments=ports,
        text=ports,
        reviews=reviews or ports,
        sidecars=SidecarFake(ports),
        pages=ports,
        receipts=ports,
        review_provider_id="selected-review-provider",
        review_model_id="selected-review-model",
        evidence_verifier=Verifier(),
    )


class CurationBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.paper = Paper(
            source_id="reference-library",
            scope_id="any-scope",
            record_id="record-1",
            title="Arbitrary topic paper",
        )
        self.source = FakeSource(
            (self.paper,),
            (
                Attachment(
                    source_id="reference-library",
                    scope_id="any-scope",
                    record_id="record-1",
                    attachment_id="pdf-1",
                    filename="paper.pdf",
                ),
            ),
        )
        self.ports = FakePorts()

    def request(self, **changes) -> CurationRequest:
        values = {
            "source_id": "reference-library",
            "scope_id": "any-scope",
            "record_id": "record-1",
        }
        values.update(changes)
        return CurationRequest(**values)

    def test_curates_the_mandatory_core_with_provider_provenance_and_receipt(self) -> None:
        result = use_case(self.source, self.ports).execute(self.request())

        self.assertIsInstance(result, CurationSuccess)
        assert isinstance(result, CurationSuccess)
        self.assertEqual(
            self.ports.calls,
            [
                "materialize_source",
                "extract_text",
                "generate_review",
                "write_sidecar:selected-review-provider:selected-review-model",
                "render_page",
                "commit_receipt",
            ],
        )
        self.assertEqual(
            [stage.stage for stage in result.evidence],
            [
                "identify",
                "materialize_source",
                "extract_text",
                "generate_review",
                "write_sidecar",
                "render_page",
                "commit_receipt",
            ],
        )
        self.assertNotIn("figures", [stage.stage for stage in result.evidence])
        self.assertEqual(result.review_provider_id, "selected-review-provider")
        self.assertEqual(self.ports.receipt_evidence, result.evidence[:-1])
        self.assertEqual(result.source_pdf.name, "source.pdf")
        self.assertEqual(result.extracted_text.name, "text.md")
        self.assertEqual(result.review.name, "review.md")
        self.assertEqual(result.sidecar.name, "bibliography.json")
        self.assertEqual(result.page.name, "index.html")
        self.assertEqual(result.receipt.name, "receipt.json")

    def test_identity_failure_is_strict(self) -> None:
        result = use_case(self.source, self.ports).execute(self.request(record_id="different-record"))

        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "record_identity_not_unique")
        self.assertEqual(self.ports.calls, [])

    def test_missing_and_ambiguous_pdf_attachments_have_distinct_codes(self) -> None:
        missing = use_case(FakeSource((self.paper,), ()), self.ports).execute(self.request())
        self.assertIsInstance(missing, CurationFailure)
        assert isinstance(missing, CurationFailure)
        self.assertEqual(missing.code, "pdf_attachment_missing")

        second = Attachment(
            "reference-library", "any-scope", "record-1", "pdf-2", "second.pdf"
        )
        ambiguous = use_case(
            FakeSource((self.paper,), (self.source.attachments[0], second)), self.ports
        ).execute(self.request())
        self.assertIsInstance(ambiguous, CurationFailure)
        assert isinstance(ambiguous, CurationFailure)
        self.assertEqual(ambiguous.code, "pdf_attachment_ambiguous")

    def test_explicit_attachment_selects_one_pdf(self) -> None:
        second = Attachment(
            "reference-library", "any-scope", "record-1", "pdf-2", "second.pdf"
        )
        result = use_case(
            FakeSource((self.paper,), (self.source.attachments[0], second)), self.ports
        ).execute(self.request(attachment_id="pdf-2"))
        self.assertIsInstance(result, CurationSuccess)

    def test_selected_review_provider_failure_never_calls_an_alternate(self) -> None:
        failing = FailingReview()
        alternate = AlternateReview()
        result = use_case(self.source, self.ports, reviews=failing).execute(self.request())

        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "review_generation_failed")
        self.assertEqual(failing.calls, 1)
        self.assertEqual(alternate.calls, 0)
        self.assertNotIn(
            "write_sidecar:selected-review-provider:selected-review-model",
            self.ports.calls,
        )
        self.assertNotIn("render_page", self.ports.calls)
        self.assertNotIn("commit_receipt", self.ports.calls)

    def test_complete_evidence_resumes_idempotently(self) -> None:
        first = use_case(self.source, self.ports).execute(self.request())
        assert isinstance(first, CurationSuccess)
        calls_before_resume = list(self.ports.calls)

        resumed = use_case(self.source, self.ports).execute(self.request(resume=first.evidence))
        self.assertIsInstance(resumed, CurationSuccess)
        self.assertEqual(self.ports.calls, calls_before_resume)

    def test_resume_is_bound_to_record_and_attachment_identity(self) -> None:
        first = use_case(self.source, self.ports).execute(self.request())
        assert isinstance(first, CurationSuccess)

        wrong_record = (
            replace(first.evidence[0], fingerprint="identity:reference-library:any-scope:other"),
            *first.evidence[1:],
        )
        result = use_case(self.source, self.ports).execute(
            self.request(resume=wrong_record)
        )
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "resume_identity_mismatch")

        wrong_attachment = (
            first.evidence[0],
            replace(first.evidence[1], input_id="pdf-other"),
            *first.evidence[2:],
        )
        result = use_case(self.source, self.ports).execute(
            self.request(attachment_id="pdf-1", resume=wrong_attachment)
        )
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "resume_input_mismatch")

        wrong_model = tuple(
            replace(stage, model_id="other-model")
            if stage.stage == "generate_review"
            else stage
            for stage in first.evidence
        )
        result = use_case(self.source, self.ports).execute(
            self.request(resume=wrong_model)
        )
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "review_model_mismatch")

    def test_resume_evidence_must_be_an_ordered_contiguous_core_prefix(self) -> None:
        stale_review = StageEvidence(
            "generate_review", (artifact("review.md"),), "sha256:review", "selected-review-provider"
        )
        result = use_case(self.source, self.ports).execute(self.request(resume=(stale_review,)))
        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "invalid_resume_evidence")
        empty_source = (
            StageEvidence(
                "identify",
                fingerprint=paper_identity_fingerprint(
                    self.paper.source_id,
                    self.paper.scope_id,
                    self.paper.record_id,
                ),
            ),
            StageEvidence(
                "materialize_source",
                fingerprint="missing-artifact",
                input_id="pdf-1",
            ),
        )
        result = use_case(self.source, self.ports).execute(
            self.request(resume=empty_source)
        )
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "invalid_resume_evidence")

    def test_resume_identity_has_no_delimiter_collision(self) -> None:
        first_paper = Paper("a", "b:c", "d", "First")
        second_paper = Paper("a:b", "c", "d", "Second")
        source = FakeSource(
            (first_paper, second_paper),
            (
                Attachment("a", "b:c", "d", "pdf-a", "a.pdf"),
                Attachment("a:b", "c", "d", "pdf-b", "b.pdf"),
            ),
        )
        first = use_case(source, self.ports).execute(CurationRequest("a", "b:c", "d"))
        assert isinstance(first, CurationSuccess)
        result = use_case(source, self.ports).execute(
            CurationRequest("a:b", "c", "d", resume=first.evidence)
        )
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "resume_identity_mismatch")

    def test_resume_requires_verified_artifacts(self) -> None:
        first = use_case(self.source, self.ports).execute(self.request())
        assert isinstance(first, CurationSuccess)

        class RejectingVerifier:
            def valid(self, paper, evidence):
                return False

        operation = CuratePaper(
            source=self.source,
            attachments=self.ports,
            text=self.ports,
            reviews=self.ports,
            sidecars=SidecarFake(self.ports),
            pages=self.ports,
            receipts=self.ports,
            review_provider_id="selected-review-provider",
            review_model_id="selected-review-model",
            evidence_verifier=RejectingVerifier(),
        )
        result = operation.execute(self.request(resume=first.evidence))
        self.assertIsInstance(result, CurationFailure)
        assert isinstance(result, CurationFailure)
        self.assertEqual(result.code, "stale_resume_evidence")


if __name__ == "__main__":
    unittest.main()
