"""Explicit, side-effect-free paths for a checkout."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Workspace:
    """Paths owned by a single checkout.

    Constructing this object neither creates nor inspects any paths.
    """

    root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", Path(os.path.abspath(os.fspath(self.root))))

    @property
    def docs(self) -> Path:
        return self.root / "docs"

    @property
    def papers(self) -> Path:
        return self.docs / "papers"

    @property
    def cache(self) -> Path:
        return self.root / "cache"

    def topic(self, alias: str) -> Path:
        """Return a topic directory while rejecting paths outside ``docs``."""
        if not isinstance(alias, str) or not alias or alias in {".", ".."}:
            raise ValueError("topic alias must be a non-empty directory name")
        candidate = Path(alias)
        if candidate.is_absolute() or len(candidate.parts) != 1:
            raise ValueError("topic alias must be a single directory name")
        return self.docs / candidate

    def within_root(self, *parts: str | Path) -> Path:
        """Join relative components under the checkout without allowing escapes."""
        result = self.root
        for part in parts:
            candidate = Path(part)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise ValueError("workspace paths must remain under the checkout root")
            result /= candidate
        return result
