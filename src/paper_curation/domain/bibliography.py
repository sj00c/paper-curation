"""Provider-neutral bibliography concepts."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Literal

EvidenceGrade = Literal["primary", "secondary", "derived"]


class BibliographyValidationError(ValueError):
    """A bibliography value does not satisfy the canonical contract."""


def canonical_doi(value: str) -> str:
    """Return a stable DOI identity without making a network request."""
    doi = value.strip()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    return doi.casefold()


def canonical_arxiv_id(value: str) -> str:
    """Return a stable arXiv identity without making a network request."""
    arxiv_id = value.strip()
    arxiv_id = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", arxiv_id,
                       flags=re.IGNORECASE)
    arxiv_id = re.sub(r"^arxiv:\s*", "", arxiv_id, flags=re.IGNORECASE)
    return arxiv_id.removesuffix(".pdf").casefold()


def canonical_title(value: str) -> str:
    """Return the conservative title identity used only as a last dedupe key."""
    return " ".join(value.casefold().split())


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


@dataclass(frozen=True, slots=True)
class BibliographyRecord:
    """Canonical, immutable metadata for one curated paper."""

    key: str
    title: str
    authors: tuple[str, ...] = ()
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

    @property
    def identity_keys(self) -> frozenset[str]:
        """Identifiers used to merge equivalent records from a selected source."""
        keys = {f"title:{canonical_title(self.title)}"}
        if self.doi:
            keys.add(f"doi:{self.doi}")
        if self.arxiv_id:
            keys.add(f"arxiv:{self.arxiv_id}")
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
