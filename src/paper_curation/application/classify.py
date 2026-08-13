"""Application service for provider-neutral paper classification."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from paper_curation.domain.classification import (
    ClassificationAssignment,
    ClassificationCategory,
    ClassificationProvider,
    ClassificationResult,
    ClassificationValidationError,
)


@dataclass(frozen=True)
class ClassifyPapers:
    """Validate and normalize a provider result into the artifact contract."""

    provider: ClassificationProvider

    def execute(self, requested_slugs: Iterable[str]) -> ClassificationResult:
        slugs = tuple(requested_slugs)
        self._validate_requested_slugs(slugs)
        result = self.provider.classify(slugs)
        self._validate_result(result, slugs)
        return ClassificationResult(
            categories=tuple(sorted(result.categories, key=lambda category: category.name)),
            assignments=tuple(sorted(result.assignments, key=lambda assignment: assignment.slug)),
        )

    @staticmethod
    def _validate_requested_slugs(slugs: tuple[str, ...]) -> None:
        if any(not isinstance(slug, str) or not slug.strip() for slug in slugs):
            raise ClassificationValidationError("Requested slugs must be non-empty strings.")
        if len(set(slugs)) != len(slugs):
            raise ClassificationValidationError("Requested slugs must be unique.")

    @staticmethod
    def _validate_result(result: ClassificationResult, slugs: tuple[str, ...]) -> None:
        if not isinstance(result, ClassificationResult):
            raise ClassificationValidationError("Provider must return a ClassificationResult.")

        if any(not isinstance(category, ClassificationCategory) for category in result.categories):
            raise ClassificationValidationError("Provider categories must be ClassificationCategory values.")
        category_names = tuple(category.name for category in result.categories)
        if any(not isinstance(name, str) or not name.strip() for name in category_names):
            raise ClassificationValidationError("Category names must be non-empty strings.")
        if len(set(category_names)) != len(category_names):
            raise ClassificationValidationError("Category names must be unique.")

        if any(not isinstance(assignment, ClassificationAssignment) for assignment in result.assignments):
            raise ClassificationValidationError("Provider assignments must be ClassificationAssignment values.")
        assignment_slugs = tuple(assignment.slug for assignment in result.assignments)
        if len(set(assignment_slugs)) != len(assignment_slugs):
            raise ClassificationValidationError("Provider assignments must have unique slugs.")
        if set(assignment_slugs) != set(slugs):
            raise ClassificationValidationError("Provider assignments must match the requested slugs.")

        primary_names: set[str] = set()
        for assignment in result.assignments:
            if not isinstance(assignment.slug, str) or not assignment.slug.strip():
                raise ClassificationValidationError("Assignment slugs must be non-empty strings.")
            if not isinstance(assignment.primary_category, str) or not assignment.primary_category.strip():
                raise ClassificationValidationError("Primary categories must be non-empty strings.")
            if not isinstance(assignment.sub_category, str):
                raise ClassificationValidationError("Sub-categories must be strings.")
            if not assignment.all_categories:
                raise ClassificationValidationError("Assignments must include at least one category.")
            if any(not isinstance(name, str) or not name.strip() for name in assignment.all_categories):
                raise ClassificationValidationError("Assignment categories must be non-empty strings.")
            if len(set(assignment.all_categories)) != len(assignment.all_categories):
                raise ClassificationValidationError("Assignment categories must be unique.")
            if assignment.primary_category not in assignment.all_categories:
                raise ClassificationValidationError(
                    "The primary category must be included in all_categories."
                )
            primary_names.add(assignment.primary_category)

        if not primary_names.issubset(set(category_names)):
            raise ClassificationValidationError(
                "Every primary category must be declared in categories."
            )


def validate_classification_mapping(data: Mapping[str, object]) -> ClassificationResult:
    """Validate an existing artifact mapping at the production adapter boundary."""
    try:
        categories = tuple(
            ClassificationCategory(str(item["name"]))
            for item in data["categories"]  # type: ignore[index,union-attr]
        )
        assignments = tuple(
            ClassificationAssignment(
                slug=str(item["slug"]),
                primary_category=str(item["primary_category"]),
                all_categories=tuple(str(value) for value in item["all_categories"]),
                sub_category=str(item.get("sub_category", "")),
            )
            for item in data["assignments"]  # type: ignore[index,union-attr]
        )
    except (KeyError, TypeError) as exc:
        raise ClassificationValidationError("Malformed classification artifact mapping.") from exc

    class ExistingArtifactProvider:
        def classify(self, slugs: tuple[str, ...]) -> ClassificationResult:
            return ClassificationResult(categories, assignments)

    return ClassifyPapers(ExistingArtifactProvider()).execute(
        assignment.slug for assignment in assignments
    )
