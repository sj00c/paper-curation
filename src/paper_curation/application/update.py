"""Deterministic batch orchestration for mandatory Core curation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from paper_curation.application.curate import (
    CuratePaper,
    CurationRequest,
    CurationResult,
    CurationSuccess,
)


class CoreUpdateStatus(StrEnum):
    SUCCEEDED = "succeeded"
    PARTIAL_FAILURE = "partial_failure"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CoreUpdateRequest:
    """Explicit Core selections for one deterministic batch."""

    selections: tuple[CurationRequest, ...]

    def __post_init__(self) -> None:
        selections = tuple(self.selections)
        identities = tuple(
            (selection.source_id, selection.scope_id, selection.record_id)
            for selection in selections
        )
        if not selections:
            raise ValueError("Core update requires at least one record selection")
        if len(identities) != len(set(identities)):
            raise ValueError("duplicate Core record selection")
        object.__setattr__(self, "selections", selections)


@dataclass(frozen=True, slots=True)
class CoreUpdateRecord:
    """One selected record and its independently retained Core outcome."""

    request: CurationRequest
    result: CurationResult

    @property
    def identity(self) -> tuple[str, str, str]:
        return (self.request.source_id, self.request.scope_id, self.request.record_id)

    @property
    def succeeded(self) -> bool:
        return isinstance(self.result, CurationSuccess)


@dataclass(frozen=True, slots=True)
class CoreUpdateResult:
    """Aggregate Core outcome; individual records remain in selection order."""

    records: tuple[CoreUpdateRecord, ...]

    def __post_init__(self) -> None:
        records = tuple(self.records)
        if not records:
            raise ValueError("Core update result requires at least one record")
        object.__setattr__(self, "records", records)

    @property
    def status(self) -> CoreUpdateStatus:
        if all(record.succeeded for record in self.records):
            return CoreUpdateStatus.SUCCEEDED
        if any(record.succeeded for record in self.records):
            return CoreUpdateStatus.PARTIAL_FAILURE
        return CoreUpdateStatus.FAILED

    @property
    def exit_code(self) -> int:
        return 0 if self.status == CoreUpdateStatus.SUCCEEDED else 1

    @property
    def succeeded(self) -> bool:
        return self.status == CoreUpdateStatus.SUCCEEDED


@dataclass(frozen=True, slots=True)
class UpdateCore:
    """Runs every selected Core curation sequentially without provider selection."""

    curate: CuratePaper

    def execute(self, request: CoreUpdateRequest) -> CoreUpdateResult:
        records: list[CoreUpdateRecord] = []
        for selection in request.selections:
            result = self.curate.execute(selection)
            records.append(CoreUpdateRecord(selection, result))
        return CoreUpdateResult(tuple(records))
