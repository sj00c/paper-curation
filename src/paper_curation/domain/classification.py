"""Canonical, provider-neutral classification artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ClassificationValidationError(ValueError):
    """Raised when a classification artifact violates its schema contract."""


@dataclass(frozen=True)
class ClassificationAssignment:
    """One paper's classification in the ``_new_classification.json`` schema."""

    slug: str
    primary_category: str
    all_categories: tuple[str, ...]
    sub_category: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "slug": self.slug,
            "primary_category": self.primary_category,
            "all_categories": list(self.all_categories),
            "sub_category": self.sub_category,
        }


@dataclass(frozen=True)
class ClassificationCategory:
    """A category represented by the historical artifact schema."""

    name: str

    def to_mapping(self) -> dict[str, str]:
        return {"name": self.name}


@dataclass(frozen=True)
class ClassificationResult:
    """The complete, JSON-compatible classification artifact."""

    categories: tuple[ClassificationCategory, ...]
    assignments: tuple[ClassificationAssignment, ...]

    def to_mapping(self) -> dict[str, object]:
        return {
            "categories": [category.to_mapping() for category in self.categories],
            "assignments": [assignment.to_mapping() for assignment in self.assignments],
        }


class ClassificationProvider(Protocol):
    """Supplies assignments for an explicit set of paper slugs."""

    def classify(self, slugs: tuple[str, ...]) -> ClassificationResult:
        """Classify exactly the requested paper slugs."""
