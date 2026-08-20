"""Pure application contract for one optional post-Core enhancement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeAlias

from paper_curation.application.curate import CurationStage, CurationSuccess
from paper_curation.domain.papers import ArtifactRef, Paper, StageEvidence


class ReceiptVerifier(Protocol):
    """Validates the committed Core receipt artifact before enhancement work."""

    def valid(self, receipt: ArtifactRef) -> bool: ...


class EnhancementPort(Protocol):
    """Runs exactly the requested capability with exactly the requested provider."""

    def generate(
        self,
        paper: Paper,
        receipt: ArtifactRef,
        capability: str,
        provider_id: str,
    ) -> tuple[ArtifactRef, ...]: ...


@dataclass(frozen=True, slots=True)
class EnhancementRequest:
    capability: str
    provider_id: str

    def __post_init__(self) -> None:
        if not self.capability.strip() or not self.provider_id.strip():
            raise ValueError("capability and provider ID are required")


@dataclass(frozen=True, slots=True)
class EnhancementSuccess:
    core: CurationSuccess
    capability: str
    provider_id: str
    artifacts: tuple[ArtifactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "artifacts", tuple(self.artifacts))


@dataclass(frozen=True, slots=True)
class EnhancementFailure:
    core: CurationSuccess
    capability: str
    provider_id: str
    code: str


@dataclass(frozen=True, slots=True)
class EnhancementBlocked:
    core: CurationSuccess
    capability: str
    provider_id: str
    code: str


EnhancementResult: TypeAlias = EnhancementSuccess | EnhancementFailure | EnhancementBlocked


@dataclass(frozen=True, slots=True)
class EnhancePaper:
    """Runs an optional enhancement only after its Core receipt is verified."""

    enhancements: EnhancementPort
    receipt_verifier: ReceiptVerifier

    def execute(self, request: EnhancementRequest, core: CurationSuccess) -> EnhancementResult:
        receipt = self._receipt(core.evidence)
        if receipt is None:
            return EnhancementBlocked(core, request.capability, request.provider_id, "core_receipt_missing")
        try:
            receipt_valid = self.receipt_verifier.valid(receipt)
        except Exception:
            receipt_valid = False
        if not receipt_valid:
            return EnhancementBlocked(core, request.capability, request.provider_id, "core_receipt_stale")

        try:
            artifacts = tuple(
                self.enhancements.generate(
                    core.paper,
                    receipt,
                    request.capability,
                    request.provider_id,
                )
            )
            if not artifacts or not all(isinstance(item, ArtifactRef) for item in artifacts):
                raise ValueError("enhancement produced no artifact references")
        except Exception:
            return EnhancementFailure(
                core,
                request.capability,
                request.provider_id,
                "enhancement_generation_failed",
            )
        return EnhancementSuccess(core, request.capability, request.provider_id, artifacts)

    @staticmethod
    def _receipt(evidence: tuple[StageEvidence, ...]) -> ArtifactRef | None:
        receipts = tuple(
            item
            for item in evidence
            if item.stage == CurationStage.COMMIT_RECEIPT.value
        )
        if len(receipts) != 1 or len(receipts[0].artifacts) != 1:
            return None
        return receipts[0].artifacts[0]
