"""Callable-backed adapters for classification implementations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from paper_curation.domain.classification import (
    ClassificationAssignment,
    ClassificationCategory,
    ClassificationResult,
)


AssignmentCallable = Callable[[str], ClassificationAssignment]


@dataclass(frozen=True)
class HDBSCANClassificationProvider:
    """Adapts an injected HDBSCAN assignment callable to the provider contract."""

    assign: AssignmentCallable

    def classify(self, slugs: tuple[str, ...]) -> ClassificationResult:
        assignments = tuple(self.assign(slug) for slug in slugs)
        return _result_for(assignments)


@dataclass(frozen=True)
class ZoteroHierarchyClassificationProvider:
    """Adapts an injected Zotero-hierarchy assignment callable to the provider contract."""

    assign: AssignmentCallable

    def classify(self, slugs: tuple[str, ...]) -> ClassificationResult:
        assignments = tuple(self.assign(slug) for slug in slugs)
        return _result_for(assignments)


def _result_for(assignments: tuple[ClassificationAssignment, ...]) -> ClassificationResult:
    """Build the legacy category list from primary assignments deterministically."""
    names = sorted(
        {
            assignment.primary_category
            for assignment in assignments
            if isinstance(assignment, ClassificationAssignment)
        }
    )
    return ClassificationResult(
        categories=tuple(ClassificationCategory(name) for name in names),
        assignments=assignments,
    )
