"""Explicit, side-effect-free paths for one local installation workspace."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Workspace:
    """Paths owned by a single installation.

    Constructing this object neither creates nor inspects any paths.
    """

    root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", Path(os.path.abspath(os.fspath(self.root))))

    @property
    def papers(self) -> Path:
        return self.root / "papers"

    @property
    def cache(self) -> Path:
        return self.root / ".cache"

    @property
    def staging(self) -> Path:
        return self.root / ".staging"

    @property
    def quarantine(self) -> Path:
        return self.root / ".quarantine"

    @property
    def site(self) -> Path:
        return self.root / "site"

    def within_root(self, *parts: str | Path) -> Path:
        """Join relative components under the checkout without allowing escapes."""
        result = self.root
        for part in parts:
            candidate = Path(part)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise ValueError("workspace paths must remain under the checkout root")
            result /= candidate
        return result
