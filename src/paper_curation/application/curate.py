"""Application use case for curating one canonical paper.

Ports return artifact references rather than contents.  This keeps provider credentials and
paper full text out of application results and makes completed stages resumable.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, TypeAlias

from paper_curation.domain.papers import ArtifactRef, Attachment, Paper, StageEvidence


class CurationStage(StrEnum):
    IDENTITY = "identity"
    ATTACHMENT = "attachment"
    TEXT = "text"
    FIGURES = "figures"
    REVIEW = "review"
    SIDECAR = "sidecar"
    PAGE = "page"
    MUTATION = "mutation"


class CurationSource(Protocol):
    """Structural source contract satisfied by a Zotero gateway adapter."""

    def list_collection(self, collection_key: str) -> tuple[Paper, ...]: ...

    def list_attachments(self, paper_key: str) -> tuple[Attachment, ...]: ...


class CurationMutator(Protocol):
    """Separate opt-in mutation capability from the read source."""

    def mark_curated(self, paper_key: str) -> None: ...


class AttachmentPort(Protocol):
    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef: ...


class TextPort(Protocol):
    def extract(self, paper: Paper, source: ArtifactRef) -> ArtifactRef: ...


class FigurePort(Protocol):
    def extract(self, paper: Paper, text: ArtifactRef) -> tuple[ArtifactRef, ...]: ...


class ReviewPort(Protocol):
    def write(
        self, paper: Paper, text: ArtifactRef, figures: tuple[ArtifactRef, ...]
    ) -> ArtifactRef: ...


class SidecarPort(Protocol):
    """Writes the existing ``bibliography.json`` sidecar schema."""

    def write(self, paper: Paper, text: ArtifactRef, review: ArtifactRef) -> ArtifactRef: ...


class PagePort(Protocol):
    """Renders the existing ``review.md`` to ``index.html`` flow."""

    def render(self, paper: Paper, review: ArtifactRef, sidecar: ArtifactRef) -> ArtifactRef: ...


class EvidenceVerifier(Protocol):
    def valid(self, evidence: StageEvidence) -> bool: ...


@dataclass(frozen=True, slots=True)
class CurationRequest:
    collection_key: str
    paper_key: str
    resume: tuple[StageEvidence, ...] = ()
    request_external_mutation: bool = False

    def __post_init__(self) -> None:
        if not self.collection_key.strip() or not self.paper_key.strip():
            raise ValueError("collection key and paper key are required")
        object.__setattr__(self, "resume", tuple(self.resume))


@dataclass(frozen=True, slots=True)
class CurationSuccess:
    paper: Paper
    evidence: tuple[StageEvidence, ...]
    external_mutation_applied: bool

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
    """Orchestrates curation through injected adapters without performing I/O itself."""

    source: CurationSource
    attachments: AttachmentPort
    text: TextPort
    figures: FigurePort
    reviews: ReviewPort
    sidecars: SidecarPort
    pages: PagePort
    mutator: CurationMutator | None = None
    evidence_verifier: EvidenceVerifier | None = None

    def execute(self, request: CurationRequest) -> CurationResult:
        resumed = self._resumed(request.resume)
        if resumed is None:
            return CurationFailure(CurationStage.IDENTITY, "invalid_resume_evidence")
        if resumed and (
            self.evidence_verifier is None
            or not all(self.evidence_verifier.valid(item) for item in resumed.values())
        ):
            return CurationFailure(CurationStage.IDENTITY, "stale_resume_evidence")
        evidence = list(resumed.values())

        try:
            papers = self.source.list_collection(request.collection_key)
        except Exception:
            return CurationFailure(CurationStage.IDENTITY, "collection_read_failed", tuple(evidence))
        matches = tuple(
            paper for paper in papers
            if paper.key == request.paper_key and paper.collection_key == request.collection_key
        )
        if len(matches) != 1:
            return CurationFailure(CurationStage.IDENTITY, "paper_identity_not_unique", tuple(evidence))
        paper = matches[0]

        try:
            listed = self.source.list_attachments(paper.key)
        except Exception:
            return CurationFailure(CurationStage.ATTACHMENT, "attachment_read_failed", tuple(evidence))
        candidates = tuple(
            attachment for attachment in listed
            if attachment.paper_key == paper.key and attachment.media_type.lower() == "application/pdf"
        )
        if len(candidates) != 1:
            return CurationFailure(CurationStage.ATTACHMENT, "pdf_attachment_not_unique", tuple(evidence))

        attachment_evidence = self._stage(
            CurationStage.ATTACHMENT, resumed, evidence,
            lambda: (self.attachments.materialize(paper, candidates[0]),),
        )
        if isinstance(attachment_evidence, CurationFailure):
            return attachment_evidence
        source_artifact = attachment_evidence.artifacts[0]

        text_evidence = self._stage(
            CurationStage.TEXT, resumed, evidence,
            lambda: (self.text.extract(paper, source_artifact),),
        )
        if isinstance(text_evidence, CurationFailure):
            return text_evidence
        text_artifact = text_evidence.artifacts[0]

        figure_evidence = self._stage(
            CurationStage.FIGURES, resumed, evidence,
            lambda: self.figures.extract(paper, text_artifact),
        )
        if isinstance(figure_evidence, CurationFailure):
            return figure_evidence

        review_evidence = self._stage(
            CurationStage.REVIEW, resumed, evidence,
            lambda: (self.reviews.write(paper, text_artifact, figure_evidence.artifacts),),
        )
        if isinstance(review_evidence, CurationFailure):
            return review_evidence
        review_artifact = review_evidence.artifacts[0]

        sidecar_evidence = self._stage(
            CurationStage.SIDECAR, resumed, evidence,
            lambda: (self.sidecars.write(paper, text_artifact, review_artifact),),
        )
        if isinstance(sidecar_evidence, CurationFailure):
            return sidecar_evidence
        sidecar_artifact = sidecar_evidence.artifacts[0]

        page_evidence = self._stage(
            CurationStage.PAGE, resumed, evidence,
            lambda: (self.pages.render(paper, review_artifact, sidecar_artifact),),
        )
        if isinstance(page_evidence, CurationFailure):
            return page_evidence

        if request.request_external_mutation:
            if self.mutator is None:
                return CurationFailure(CurationStage.MUTATION, "mutation_not_configured", tuple(evidence))
            try:
                self.mutator.mark_curated(paper.key)
            except Exception:
                return CurationFailure(CurationStage.MUTATION, "explicit_mutation_failed", tuple(evidence))
        return CurationSuccess(paper, tuple(evidence), request.request_external_mutation)

    @staticmethod
    def _resumed(evidence: tuple[StageEvidence, ...]) -> dict[CurationStage, StageEvidence] | None:
        result: dict[CurationStage, StageEvidence] = {}
        ordered = (
            CurationStage.ATTACHMENT,
            CurationStage.TEXT,
            CurationStage.FIGURES,
            CurationStage.REVIEW,
            CurationStage.SIDECAR,
            CurationStage.PAGE,
        )
        for item in evidence:
            try:
                stage = CurationStage(item.stage)
            except ValueError:
                return None
            if stage in (CurationStage.IDENTITY, CurationStage.MUTATION) or stage in result:
                return None
            result[stage] = item
        completed = tuple(stage for stage in ordered if stage in result)
        if completed != ordered[:len(completed)]:
            return None
        return result

    @staticmethod
    def _stage(
        stage: CurationStage,
        resumed: dict[CurationStage, StageEvidence],
        evidence: list[StageEvidence],
        operation: Callable[[], tuple[ArtifactRef, ...]],
    ) -> StageEvidence | CurationFailure:
        existing = resumed.get(stage)
        if existing is not None:
            return existing
        try:
            artifacts = operation()
            normalized = tuple(artifacts)
            if not normalized and stage is not CurationStage.FIGURES:
                raise ValueError("stage produced no artifact")
            fingerprint = (
                "|".join(artifact.fingerprint for artifact in normalized)
                if normalized else "none"
            )
            created = StageEvidence(stage.value, normalized, fingerprint)
        except Exception:
            return CurationFailure(stage, "stage_failed", tuple(evidence))
        evidence.append(created)
        return created
