"""Pure application orchestration for one mandatory Core curation run."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, TypeAlias

from paper_curation.domain.papers import (
    ArtifactRef,
    Attachment,
    Paper,
    StageEvidence,
    paper_identity_fingerprint,
)


class CurationStage(StrEnum):
    IDENTIFY = "identify"
    MATERIALIZE_SOURCE = "materialize_source"
    EXTRACT_TEXT = "extract_text"
    GENERATE_REVIEW = "generate_review"
    WRITE_SIDECAR = "write_sidecar"
    RENDER_PAGE = "render_page"
    COMMIT_RECEIPT = "commit_receipt"


CORE_STAGES = tuple(CurationStage)


class CurationSource(Protocol):
    """Read-only source contract; concrete source adapters live outside application."""

    def list_records(self, source_id: str, scope_id: str) -> tuple[Paper, ...]: ...

    def list_attachments(self, paper: Paper) -> tuple[Attachment, ...]: ...


class AttachmentPort(Protocol):
    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef: ...


class TextPort(Protocol):
    def extract(self, paper: Paper, source: ArtifactRef) -> ArtifactRef: ...


class ReviewPort(Protocol):
    def write(self, paper: Paper, text: ArtifactRef) -> ArtifactRef: ...


class SidecarPort(Protocol):
    """Persists bibliography, text, review, provider, and evidence provenance."""

    def write(
        self,
        paper: Paper,
        text: ArtifactRef,
        review: ArtifactRef,
        review_provider_id: str,
        review_model_id: str,
    ) -> ArtifactRef: ...


class PagePort(Protocol):
    """Renders a local page from the review and sidecar artifacts."""

    def render(self, paper: Paper, review: ArtifactRef, sidecar: ArtifactRef) -> ArtifactRef: ...


class ReceiptPort(Protocol):
    """Atomically commits verified Core outputs and their receipt."""

    def commit(self, paper: Paper, evidence: tuple[StageEvidence, ...]) -> ArtifactRef: ...


class EvidenceVerifier(Protocol):
    def valid(self, paper: Paper, evidence: tuple[StageEvidence, ...]) -> bool: ...


@dataclass(frozen=True, slots=True)
class CurationRequest:
    source_id: str
    scope_id: str
    record_id: str
    attachment_id: str = ""
    resume: tuple[StageEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.scope_id.strip() or not self.record_id.strip():
            raise ValueError("source ID, scope ID, and record ID are required")
        object.__setattr__(self, "resume", tuple(self.resume))


@dataclass(frozen=True, slots=True)
class CurationSuccess:
    paper: Paper
    evidence: tuple[StageEvidence, ...]

    def _artifact(self, stage: CurationStage) -> ArtifactRef:
        evidence = next(item for item in self.evidence if item.stage == stage.value)
        return evidence.artifacts[0]

    @property
    def source_pdf(self) -> ArtifactRef:
        return self._artifact(CurationStage.MATERIALIZE_SOURCE)

    @property
    def extracted_text(self) -> ArtifactRef:
        return self._artifact(CurationStage.EXTRACT_TEXT)

    @property
    def review(self) -> ArtifactRef:
        return self._artifact(CurationStage.GENERATE_REVIEW)

    @property
    def sidecar(self) -> ArtifactRef:
        return self._artifact(CurationStage.WRITE_SIDECAR)

    @property
    def page(self) -> ArtifactRef:
        return self._artifact(CurationStage.RENDER_PAGE)

    @property
    def receipt(self) -> ArtifactRef:
        return self._artifact(CurationStage.COMMIT_RECEIPT)

    @property
    def review_provider_id(self) -> str:
        return next(
            item.provider_id
            for item in self.evidence
            if item.stage == CurationStage.GENERATE_REVIEW.value
        )

    @property
    def review_model_id(self) -> str:
        return next(
            item.model_id
            for item in self.evidence
            if item.stage == CurationStage.GENERATE_REVIEW.value
        )

    @property
    def artifact_paths(self) -> tuple[str, ...]:
        return tuple(artifact.path for stage in self.evidence for artifact in stage.artifacts)

    @property
    def artifact_fingerprints(self) -> tuple[str, ...]:
        return tuple(artifact.fingerprint for stage in self.evidence for artifact in stage.artifacts)


@dataclass(frozen=True, slots=True)
class CurationFailure:
    stage: CurationStage
    code: str
    evidence: tuple[StageEvidence, ...] = ()


CurationResult: TypeAlias = CurationSuccess | CurationFailure


@dataclass(frozen=True, slots=True)
class CuratePaper:
    """Orchestrates one selected review provider through injected ports only."""

    source: CurationSource
    attachments: AttachmentPort
    text: TextPort
    reviews: ReviewPort
    sidecars: SidecarPort
    pages: PagePort
    receipts: ReceiptPort
    review_provider_id: str
    review_model_id: str
    evidence_verifier: EvidenceVerifier

    def __post_init__(self) -> None:
        if not self.review_provider_id.strip():
            raise ValueError("review provider ID is required")
        if not self.review_model_id.strip():
            raise ValueError("review model ID is required")

    def execute(self, request: CurationRequest) -> CurationResult:
        resumed = self._resumed(request.resume)
        if resumed is None:
            return CurationFailure(CurationStage.IDENTIFY, "invalid_resume_evidence")
        if any(
            item.stage == CurationStage.GENERATE_REVIEW.value
            and item.provider_id != self.review_provider_id
            for item in resumed
        ):
            return CurationFailure(CurationStage.GENERATE_REVIEW, "review_provider_mismatch")
        if any(
            item.stage == CurationStage.GENERATE_REVIEW.value
            and item.model_id != self.review_model_id
            for item in resumed
        ):
            return CurationFailure(CurationStage.GENERATE_REVIEW, "review_model_mismatch")
        evidence = list(resumed)

        try:
            records = self.source.list_records(request.source_id, request.scope_id)
        except Exception:
            return CurationFailure(CurationStage.IDENTIFY, "identity_read_failed", tuple(evidence))
        matches = tuple(
            paper
            for paper in records
            if (
                paper.source_id == request.source_id
                and paper.scope_id == request.scope_id
                and paper.record_id == request.record_id
            )
        )
        if len(matches) != 1:
            return CurationFailure(CurationStage.IDENTIFY, "record_identity_not_unique", tuple(evidence))
        paper = matches[0]

        identity_evidence = self._identity_stage(paper, resumed, evidence)
        if isinstance(identity_evidence, CurationFailure):
            return identity_evidence
        if resumed and (
            self.evidence_verifier is None
            or not self.evidence_verifier.valid(paper, resumed)
        ):
            return CurationFailure(
                CurationStage.IDENTIFY, "stale_resume_evidence", tuple(evidence)
            )

        try:
            listed = self.source.list_attachments(paper)
        except Exception:
            return CurationFailure(
                CurationStage.MATERIALIZE_SOURCE, "attachment_read_failed", tuple(evidence)
            )
        candidates = tuple(
            attachment
            for attachment in listed
            if (
                attachment.source_id == paper.source_id
                and attachment.scope_id == paper.scope_id
                and attachment.record_id == paper.record_id
                and attachment.media_type.lower() == "application/pdf"
                and (not request.attachment_id or attachment.attachment_id == request.attachment_id)
            )
        )
        if not candidates:
            return CurationFailure(
                CurationStage.MATERIALIZE_SOURCE, "pdf_attachment_missing", tuple(evidence)
            )
        if len(candidates) != 1:
            return CurationFailure(
                CurationStage.MATERIALIZE_SOURCE, "pdf_attachment_ambiguous", tuple(evidence)
            )

        source_evidence = self._stage(
            CurationStage.MATERIALIZE_SOURCE,
            resumed,
            evidence,
            "attachment_materialize_failed",
            lambda: (self.attachments.materialize(paper, candidates[0]),),
            input_id=candidates[0].attachment_id,
        )
        if isinstance(source_evidence, CurationFailure):
            return source_evidence

        text_evidence = self._stage(
            CurationStage.EXTRACT_TEXT,
            resumed,
            evidence,
            "text_extraction_failed",
            lambda: (self.text.extract(paper, source_evidence.artifacts[0]),),
        )
        if isinstance(text_evidence, CurationFailure):
            return text_evidence

        review_evidence = self._stage(
            CurationStage.GENERATE_REVIEW,
            resumed,
            evidence,
            "review_generation_failed",
            lambda: (self.reviews.write(paper, text_evidence.artifacts[0]),),
            provider_id=self.review_provider_id,
            model_id=self.review_model_id,
        )
        if isinstance(review_evidence, CurationFailure):
            return review_evidence

        sidecar_evidence = self._stage(
            CurationStage.WRITE_SIDECAR,
            resumed,
            evidence,
            "sidecar_write_failed",
            lambda: (
                self.sidecars.write(
                    paper,
                    text_evidence.artifacts[0],
                    review_evidence.artifacts[0],
                    self.review_provider_id,
                    self.review_model_id,
                ),
            ),
        )
        if isinstance(sidecar_evidence, CurationFailure):
            return sidecar_evidence

        page_evidence = self._stage(
            CurationStage.RENDER_PAGE,
            resumed,
            evidence,
            "page_render_failed",
            lambda: (
                self.pages.render(paper, review_evidence.artifacts[0], sidecar_evidence.artifacts[0]),
            ),
        )
        if isinstance(page_evidence, CurationFailure):
            return page_evidence

        receipt_evidence = self._stage(
            CurationStage.COMMIT_RECEIPT,
            resumed,
            evidence,
            "receipt_commit_failed",
            lambda: (self.receipts.commit(paper, tuple(evidence)),),
        )
        if isinstance(receipt_evidence, CurationFailure):
            return receipt_evidence
        return CurationSuccess(paper, tuple(evidence))

    @staticmethod
    def _resumed(evidence: tuple[StageEvidence, ...]) -> tuple[StageEvidence, ...] | None:
        try:
            stages = tuple(CurationStage(item.stage) for item in evidence)
        except ValueError:
            return None
        if stages != CORE_STAGES[: len(stages)]:
            return None
        for stage, item in zip(stages, evidence, strict=True):
            expected_count = 0 if stage == CurationStage.IDENTIFY else 1
            if len(item.artifacts) != expected_count:
                return None
            if any(not isinstance(artifact, ArtifactRef) for artifact in item.artifacts):
                return None
            if item.artifacts and item.fingerprint != item.artifacts[0].fingerprint:
                return None
        if any(
            item.stage == CurationStage.GENERATE_REVIEW.value
            and (not item.provider_id.strip() or not item.model_id.strip())
            for item in evidence
        ):
            return None
        if any(
            item.stage == CurationStage.MATERIALIZE_SOURCE.value
            and not item.input_id.strip()
            for item in evidence
        ):
            return None
        return evidence

    @staticmethod
    def _identity_stage(
        paper: Paper,
        resumed: tuple[StageEvidence, ...],
        evidence: list[StageEvidence],
    ) -> StageEvidence | CurationFailure:
        expected = paper_identity_fingerprint(
            paper.source_id, paper.scope_id, paper.record_id
        )
        if resumed:
            if resumed[0].fingerprint != expected:
                return CurationFailure(
                    CurationStage.IDENTIFY, "resume_identity_mismatch", tuple(evidence)
                )
            return resumed[0]
        try:
            created = StageEvidence(
                CurationStage.IDENTIFY.value,
                fingerprint=expected,
            )
        except Exception:
            return CurationFailure(CurationStage.IDENTIFY, "identity_evidence_failed", tuple(evidence))
        evidence.append(created)
        return created

    @staticmethod
    def _stage(
        stage: CurationStage,
        resumed: tuple[StageEvidence, ...],
        evidence: list[StageEvidence],
        failure_code: str,
        operation: Callable[[], tuple[ArtifactRef, ...]],
        *,
        provider_id: str = "",
        input_id: str = "",
        model_id: str = "",
    ) -> StageEvidence | CurationFailure:
        completed = len(resumed)
        if CORE_STAGES.index(stage) < completed:
            existing = resumed[CORE_STAGES.index(stage)]
            if provider_id and existing.provider_id != provider_id:
                return CurationFailure(stage, "resume_provider_mismatch", tuple(evidence))
            if input_id and existing.input_id != input_id:
                return CurationFailure(stage, "resume_input_mismatch", tuple(evidence))
            if model_id and existing.model_id != model_id:
                return CurationFailure(stage, "resume_model_mismatch", tuple(evidence))
            return existing
        try:
            artifacts = tuple(operation())
            if not artifacts:
                raise ValueError("stage produced no artifact")
            created = StageEvidence(
                stage.value,
                artifacts,
                "|".join(artifact.fingerprint for artifact in artifacts),
                provider_id,
                input_id,
                model_id,
            )
        except Exception:
            return CurationFailure(stage, failure_code, tuple(evidence))
        evidence.append(created)
        return created
