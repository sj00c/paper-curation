"""Pure setup planning with an injected configuration writer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from paper_curation.config.models import AppConfig
from paper_curation.workspace import Workspace


@dataclass(frozen=True, slots=True)
class SetupPlan:
    """A side-effect-free description of a local installation setup."""

    target_path: Path
    workspace_directories: tuple[Path, ...]
    config: AppConfig = field(repr=False)
    replace: bool = False

    @property
    def backup_path(self) -> Path | None:
        if not self.replace:
            return None
        return self.target_path.with_name(f"{self.target_path.name}.pre-setup.bak")


@dataclass(frozen=True, slots=True)
class SetupResult:
    """The non-sensitive outcome of applying a setup plan."""

    target_path: Path
    workspace_directories: tuple[Path, ...]
    backup_path: Path | None = None


class ConfigWriter(Protocol):
    """Outer boundary for persisting an already planned local configuration."""

    def write(self, plan: SetupPlan) -> SetupResult:
        """Create the planned workspace and persist its configuration."""


def plan_setup(config: AppConfig, target_path: str | Path, *, replace: bool = False) -> SetupPlan:
    """Plan setup without inspecting or modifying the filesystem."""

    if not isinstance(config, AppConfig):
        raise TypeError("config must be an AppConfig")
    if not isinstance(replace, bool):
        raise TypeError("replace must be a boolean")

    workspace = Workspace(Path(config.workspace.root).expanduser())
    directories = (workspace.root, workspace.papers, workspace.cache)
    return SetupPlan(Path(target_path).expanduser(), directories, config, replace)


class SetupUseCase:
    """Plans setup independently from the filesystem adapter that executes it."""

    def __init__(self, writer: ConfigWriter) -> None:
        self._writer = writer

    def preview(self, config: AppConfig, target_path: str | Path, *, replace: bool = False) -> SetupPlan:
        return plan_setup(config, target_path, replace=replace)

    def execute(self, plan: SetupPlan) -> SetupResult:
        if not isinstance(plan, SetupPlan):
            raise TypeError("plan must be a SetupPlan")
        return self._writer.write(plan)
