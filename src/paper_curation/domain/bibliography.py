"""Provider-neutral bibliography concepts."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Literal
import unicodedata

from .author_identity import Author

EvidenceGrade = Literal["primary", "secondary", "derived"]


class BibliographyValidationError(ValueError):
    """A bibliography value does not satisfy the canonical contract."""


def canonical_doi(value: str) -> str:
    """Return a stable DOI identity without making a network request."""
    doi = value.strip()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = doi.casefold()
    if not doi:
        return ""
    if (
        not re.fullmatch(r"10\.\d+/\S+", doi)
        or any(marker in doi for marker in ("xxxx", "your-doi", "insert-doi", "placeholder", "{", "}", "<", ">"))
    ):
        raise BibliographyValidationError("DOI is invalid or a placeholder")
    return doi


def canonical_arxiv_id(value: str) -> str:
    """Return a stable arXiv identity without making a network request."""
    arxiv_id = value.strip()
    arxiv_id = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", arxiv_id,
                       flags=re.IGNORECASE)
    arxiv_id = re.sub(r"^arxiv:\s*", "", arxiv_id, flags=re.IGNORECASE)
    return arxiv_id.removesuffix(".pdf").casefold()


def canonical_title(value: str) -> str:
    """Return the conservative title identity used only as a last dedupe key."""
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    """The source and confidence grade for a bibliographic assertion."""

    source: str
    grade: EvidenceGrade
    locator: str = ""

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise BibliographyValidationError("evidence source must not be empty")
        if self.grade not in ("primary", "secondary", "derived"):
            raise BibliographyValidationError("evidence grade is invalid")


def stable_evidence_union(*evidence_groups: tuple[SourceEvidence, ...]) -> tuple[SourceEvidence, ...]:
    """Deduplicate exact evidence while retaining the first asserted order."""
    result: list[SourceEvidence] = []
    seen: set[SourceEvidence] = set()
    for evidence_group in evidence_groups:
        for evidence in evidence_group:
            if evidence not in seen:
                result.append(evidence)
                seen.add(evidence)
    return tuple(result)


@dataclass(frozen=True, slots=True)
class Institution:
    """An institution asserted for a bibliography record."""

    name: str
    country: str = ""
    ror_id: str = ""
    parent_name: str = ""
    evidence: tuple[SourceEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise BibliographyValidationError("institution name must not be empty")
        object.__setattr__(self, "evidence", stable_evidence_union(self.evidence))


@dataclass(frozen=True, slots=True)
class BibliographyField:
    """One named metadata assertion, retaining its display value."""

    name: str
    value: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.value.strip():
            raise BibliographyValidationError("bibliography field name and value must not be empty")


@dataclass(frozen=True, slots=True)
class FieldEvidence:
    """Evidence supporting one field assertion."""

    field: BibliographyField
    evidence: tuple[SourceEvidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", stable_evidence_union(self.evidence))


def merge_field_evidence(*assertions: FieldEvidence) -> tuple[FieldEvidence, ...]:
    """Union exact duplicate assertions without selecting between different values."""
    positions: dict[BibliographyField, int] = {}
    merged: list[FieldEvidence] = []
    for assertion in assertions:
        position = positions.get(assertion.field)
        if position is None:
            positions[assertion.field] = len(merged)
            merged.append(assertion)
            continue
        current = merged[position]
        merged[position] = FieldEvidence(
            field=current.field,
            evidence=stable_evidence_union(current.evidence, assertion.evidence),
        )
    return tuple(merged)


@dataclass(frozen=True, slots=True)
class MetadataConflict:
    """Incompatible assertions for one field; no winner is inferred."""

    field_name: str
    assertions: tuple[FieldEvidence, ...]

    def __post_init__(self) -> None:
        if not self.field_name.strip() or len(self.assertions) < 2:
            raise BibliographyValidationError("metadata conflicts require a field and two assertions")
        if any(assertion.field.name != self.field_name for assertion in self.assertions):
            raise BibliographyValidationError("conflict assertions must name the conflicted field")
        if len({assertion.field.value for assertion in self.assertions}) != len(self.assertions):
            raise BibliographyValidationError("conflict assertions must have distinct values")


@dataclass(frozen=True, slots=True)
class AuthorInstitutionLink:
    """A record-local author-to-institution assertion using positional indices."""

    author_index: int
    institution_index: int
    evidence: tuple[SourceEvidence, ...] = ()

    def __post_init__(self) -> None:
        if self.author_index < 0 or self.institution_index < 0:
            raise BibliographyValidationError("author and institution indices must not be negative")
        object.__setattr__(self, "evidence", stable_evidence_union(self.evidence))


@dataclass(frozen=True, slots=True)
class BibliographyRecord:
    """Canonical, immutable metadata for one curated paper."""

    key: str
    title: str
    authors: tuple[Author, ...] = ()
    doi: str = ""
    arxiv_id: str = ""
    publication_title: str = ""
    publication_date: str = ""
    institutions: tuple[Institution, ...] = ()
    evidence: tuple[SourceEvidence, ...] = ()
    text_sha256: str = ""

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise BibliographyValidationError("record key must not be empty")
        if not self.title.strip():
            raise BibliographyValidationError("record title must not be empty")
        object.__setattr__(self, "doi", canonical_doi(self.doi))
        object.__setattr__(self, "arxiv_id", canonical_arxiv_id(self.arxiv_id))
        if any(not isinstance(author, Author) for author in self.authors):
            raise BibliographyValidationError("record authors must be Author values")
        object.__setattr__(self, "authors", tuple(self.authors))
        object.__setattr__(self, "institutions", tuple(self.institutions))
        object.__setattr__(self, "evidence", stable_evidence_union(self.evidence))

    @property
    def identity_keys(self) -> frozenset[str]:
        """Identifiers used to merge equivalent bibliography records."""
        keys = set()
        if self.doi:
            keys.add(f"doi:{self.doi}")
        if self.arxiv_id:
            keys.add(f"arxiv:{self.arxiv_id}")
        if not keys:
            keys.add(f"title:{canonical_title(self.title)}")
        return frozenset(keys)


@dataclass(frozen=True, slots=True)
class MergedBibliography:
    """A record with retained field assertions, conflicts, and local author links."""

    record: BibliographyRecord
    field_evidence: tuple[FieldEvidence, ...] = ()
    conflicts: tuple[MetadataConflict, ...] = ()
    author_institution_links: tuple[AuthorInstitutionLink, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "field_evidence", merge_field_evidence(*self.field_evidence))
        object.__setattr__(self, "conflicts", tuple(self.conflicts))
        links = tuple(self.author_institution_links)
        for link in links:
            if link.author_index >= len(self.record.authors):
                raise BibliographyValidationError("author link index is outside the record")
            if link.institution_index >= len(self.record.institutions):
                raise BibliographyValidationError("institution link index is outside the record")
        object.__setattr__(self, "author_institution_links", links)


@dataclass(frozen=True, slots=True)
class CitingPaper:
    """A paper that cites a bibliography record, with retained provenance."""

    title: str
    doi: str = ""
    arxiv_id: str = ""
    evidence: tuple[SourceEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise BibliographyValidationError("citing paper title must not be empty")
        object.__setattr__(self, "doi", canonical_doi(self.doi))
        object.__setattr__(self, "arxiv_id", canonical_arxiv_id(self.arxiv_id))
        object.__setattr__(self, "evidence", stable_evidence_union(self.evidence))

    @property
    def identity_keys(self) -> frozenset[str]:
        """Identifiers used to merge equivalent records from a selected source."""
        keys = set()
        if self.doi:
            keys.add(f"doi:{self.doi}")
        if self.arxiv_id:
            keys.add(f"arxiv:{self.arxiv_id}")
        if not keys:
            keys.add(f"title:{canonical_title(self.title)}")
        return frozenset(keys)


@dataclass(frozen=True, slots=True)
class CitedByResult:
    """The provider-neutral outcome of one cited-by analysis."""

    target: BibliographyRecord
    topic: str
    source: str
    citing_papers: tuple[CitingPaper, ...]
    analysis: object = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.topic.strip():
            raise BibliographyValidationError("topic must not be empty")
        if not self.source.strip():
            raise BibliographyValidationError("citing source must not be empty")
