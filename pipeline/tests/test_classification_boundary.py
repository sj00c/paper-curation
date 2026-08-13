"""Contract tests for provider-neutral classification."""

from __future__ import annotations

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.classify import ClassifyPapers
from paper_curation.domain.classification import (
    ClassificationAssignment,
    ClassificationCategory,
    ClassificationResult,
    ClassificationValidationError,
)
from paper_curation.integrations.classification.providers import (
    HDBSCANClassificationProvider,
    ZoteroHierarchyClassificationProvider,
)


class ClassificationBoundaryTests(unittest.TestCase):
    def test_hdbscan_outlier_assignment_preserves_schema_for_arbitrary_topic(self) -> None:
        def assign(slug: str) -> ClassificationAssignment:
            self.assertEqual(slug, "outlier-paper")
            # The injected callable has already applied its centroid fallback.
            return ClassificationAssignment(
                slug=slug,
                primary_category="Applied Methods",
                all_categories=("Applied Methods", "Foundations"),
                sub_category="nearest-centroid",
            )

        result = ClassifyPapers(HDBSCANClassificationProvider(assign)).execute(
            ["outlier-paper"]
        )

        self.assertEqual(
            result.to_mapping(),
            {
                "categories": [{"name": "Applied Methods"}],
                "assignments": [
                    {
                        "slug": "outlier-paper",
                        "primary_category": "Applied Methods",
                        "all_categories": ["Applied Methods", "Foundations"],
                        "sub_category": "nearest-centroid",
                    }
                ],
            },
        )

    def test_zotero_hierarchy_preserves_multiple_categories(self) -> None:
        def assign(slug: str) -> ClassificationAssignment:
            return ClassificationAssignment(
                slug=slug,
                primary_category="Clinical Practice",
                all_categories=("Clinical Practice", "Data Methods"),
                sub_category="",
            )

        result = ClassifyPapers(ZoteroHierarchyClassificationProvider(assign)).execute(
            ["paper-b"]
        )

        self.assertEqual(
            result.to_mapping()["assignments"][0]["all_categories"],
            ["Clinical Practice", "Data Methods"],
        )

    def test_output_mapping_is_deterministic(self) -> None:
        def assign(slug: str) -> ClassificationAssignment:
            category = "Beta" if slug == "paper-b" else "Alpha"
            return ClassificationAssignment(slug, category, (category,), "")

        result = ClassifyPapers(HDBSCANClassificationProvider(assign)).execute(
            ["paper-b", "paper-a"]
        )

        self.assertEqual(
            result.to_mapping(),
            {
                "categories": [{"name": "Alpha"}, {"name": "Beta"}],
                "assignments": [
                    {
                        "slug": "paper-a",
                        "primary_category": "Alpha",
                        "all_categories": ["Alpha"],
                        "sub_category": "",
                    },
                    {
                        "slug": "paper-b",
                        "primary_category": "Beta",
                        "all_categories": ["Beta"],
                        "sub_category": "",
                    },
                ],
            },
        )

    def test_malformed_provider_assignment_fails_at_the_boundary(self) -> None:
        @dataclass(frozen=True)
        class MalformedProvider:
            def classify(self, slugs: tuple[str, ...]) -> ClassificationResult:
                return ClassificationResult(
                    categories=(ClassificationCategory("Methods"),),
                    assignments=(
                        ClassificationAssignment(
                            slug=slugs[0],
                            primary_category="Methods",
                            all_categories=("Other",),
                            sub_category="",
                        ),
                    ),
                )

        with self.assertRaises(ClassificationValidationError):
            ClassifyPapers(MalformedProvider()).execute(["paper-a"])


if __name__ == "__main__":
    unittest.main()
