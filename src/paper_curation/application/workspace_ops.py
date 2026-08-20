"""Use cases and ports for local, committed Core workspace operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class WorkspaceEntry:
    """A committed Core page included in the local site index."""

    label: str
    page_path: Path


@dataclass(frozen=True, slots=True)
class BuildWorkspaceResult:
    """The atomically published local site index."""

    index_path: Path
    entries: tuple[WorkspaceEntry, ...]


@dataclass(frozen=True, slots=True)
class WorkspaceIssue:
    """A read-only validation finding for one generated record."""

    path: Path
    message: str


@dataclass(frozen=True, slots=True)
class ValidateWorkspaceResult:
    """Validation findings; an empty tuple means every record is complete."""

    issues: tuple[WorkspaceIssue, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


@dataclass(frozen=True, slots=True)
class WorkspaceRepairAction:
    """One generated item that repair may remove or quarantine."""

    path: Path
    action: str
    reason: str


@dataclass(frozen=True, slots=True)
class RepairWorkspaceResult:
    """A repair preview and whether its listed actions were executed."""

    actions: tuple[WorkspaceRepairAction, ...]
    executed: bool


class WorkspaceBuilder(Protocol):
    def build(self) -> BuildWorkspaceResult: ...


class WorkspaceValidator(Protocol):
    def validate(self) -> ValidateWorkspaceResult: ...


class WorkspaceRepairer(Protocol):
    def repair(self, *, execute: bool) -> RepairWorkspaceResult: ...


@dataclass(frozen=True, slots=True)
class BuildWorkspace:
    """Build a local index exclusively from committed Core pages."""

    workspace: WorkspaceBuilder

    def __call__(self) -> BuildWorkspaceResult:
        return self.workspace.build()


@dataclass(frozen=True, slots=True)
class ValidateWorkspace:
    """Read-only integrity validation for committed Core records."""

    workspace: WorkspaceValidator

    def __call__(self) -> ValidateWorkspaceResult:
        return self.workspace.validate()


@dataclass(frozen=True, slots=True)
class RepairWorkspace:
    """Preview or explicitly execute local generated-workspace repair."""

    workspace: WorkspaceRepairer

    def __call__(self, *, execute: bool = False) -> RepairWorkspaceResult:
        return self.workspace.repair(execute=execute)
