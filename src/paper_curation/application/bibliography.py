"""Sidecar ingestion into the bibliography repository boundary."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import hashlib
import string

from typing import ContextManager, Protocol
from paper_curation.domain.bibliography import (
    BibliographyRecord,
    BibliographyValidationError,
    BibliographyField,
    FieldEvidence,
    Institution,
    MetadataConflict,
    MergedBibliography,
    SourceEvidence,
    canonical_arxiv_id,
    canonical_doi,
    canonical_title,
    merge_field_evidence,
    stable_evidence_union,
)
from paper_curation.domain.author_identity import Author, decide_author_identity

SIDECAR_SCHEMA = "bibliography-sidecar-1"
_SHA256_CHARACTERS = frozenset(string.hexdigits)


class BibliographyTransaction(Protocol):
    def upsert(self, bibliography: MergedBibliography) -> None: ...


class BibliographyRepository(Protocol):
    def transaction(self) -> ContextManager[BibliographyTransaction]: ...


@dataclass(frozen=True, slots=True)
class IngestedSidecars:
    """The complete merged aggregates committed by a sidecar ingestion."""

    bibliographies: tuple[MergedBibliography, ...]


@dataclass(frozen=True, slots=True)
class BibliographyCandidate:
    """One provider-neutral assertion about a record.

    Higher priorities win disagreements; lower priorities can only supply a
    missing value.  Exact assertions always retain evidence from every source.
    """

    record: BibliographyRecord
    priority: int
    field_evidence: tuple[FieldEvidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "field_evidence",
            merge_field_evidence(*self.field_evidence, *field_evidence_from_record(self.record)),
        )


def _mapping(value: object, path: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise BibliographyValidationError(f"{path} must be a mapping")
    return value


def _text(value: object, path: str, *, required: bool = False) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise BibliographyValidationError(f"{path} must be text")
    result = value.strip()
    if required and not result:
        raise BibliographyValidationError(f"{path} must not be empty")
    return result


def _string_sequence(value: object, path: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise BibliographyValidationError(f"{path} must be a sequence")
    values: list[str] = []
    for index, item in enumerate(value):
        text = _text(item, f"{path}[{index}]", required=True)
        values.append(text)
    return tuple(values)


def _authors(value: object) -> tuple[Author, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise BibliographyValidationError("authors must be a sequence")
    authors: list[Author] = []
    for index, item in enumerate(value):
        mapping = _mapping(item, f"authors[{index}]")
        try:
            authors.append(
                Author(
                    _text(mapping.get("display_name", mapping.get("name")), f"authors[{index}].display_name", required=True),
                    _text(mapping.get("orcid"), f"authors[{index}].orcid"),
                )
            )
        except ValueError as error:
            raise BibliographyValidationError(f"authors[{index}] is invalid: {error}") from error
    return tuple(authors)


def _sidecar_hash(value: object) -> str:
    digest = _text(value, "text_md_sha256", required=True).casefold()
    if len(digest) != 64 or any(character not in _SHA256_CHARACTERS for character in digest):
        raise BibliographyValidationError("text_md_sha256 must be a SHA-256 hex digest")
    return digest


def _institution(value: object, index: int, key: str) -> Institution:
    if isinstance(value, str):
        return Institution(
            name=_text(value, f"affiliations[{index}]", required=True),
            evidence=(SourceEvidence("bibliography-sidecar", "primary", key),),
        )
    mapping = _mapping(value, f"affiliations[{index}]")
    name = mapping.get("name", mapping.get("institution", mapping.get("display_name")))
    source = _text(mapping.get("source"), f"affiliations[{index}].source") or "bibliography-sidecar"
    grade = _text(mapping.get("evidence_grade"), f"affiliations[{index}].evidence_grade") or "primary"
    return Institution(
        name=_text(name, f"affiliations[{index}].name", required=True),
        country=_text(mapping.get("country", mapping.get("country_name")), f"affiliations[{index}].country"),
        ror_id=_text(mapping.get("ror_id"), f"affiliations[{index}].ror_id"),
        parent_name=_text(mapping.get("parent_name"), f"affiliations[{index}].parent_name"),
        evidence=(SourceEvidence(source, grade, key),),  # type: ignore[arg-type]
    )


def field_evidence_from_record(record: BibliographyRecord) -> tuple[FieldEvidence, ...]:
    """Build direct field assertions from supplied record values only."""
    values = (
        ("title", record.title),
        ("doi", record.doi),
        ("arxiv_id", record.arxiv_id),
        ("publication_title", record.publication_title),
        ("publication_date", record.publication_date),
    )
    return tuple(
        FieldEvidence(BibliographyField(name, value), record.evidence)
        for name, value in values
        if value
    )


def titles_compatible(left: str, right: str) -> bool:
    """Titles identify the same candidate only when their canonical text agrees."""
    return canonical_title(left) == canonical_title(right)


def _merge_institutions(
    primary: tuple[Institution, ...], secondary: tuple[Institution, ...],
) -> tuple[Institution, ...]:
    result = list(primary)
    positions = {
        (item.name, item.country, item.ror_id, item.parent_name): index
        for index, item in enumerate(result)
    }
    for item in secondary:
        key = (item.name, item.country, item.ror_id, item.parent_name)
        position = positions.get(key)
        if position is None:
            positions[key] = len(result)
            result.append(item)
        else:
            existing = result[position]
            result[position] = Institution(
                existing.name, existing.country, existing.ror_id, existing.parent_name,
                stable_evidence_union(existing.evidence, item.evidence),
            )
    return tuple(result)


def merge_bibliography_candidates(candidates: Iterable[BibliographyCandidate]) -> MergedBibliography:
    """Merge assertions for one record without guessing through identity conflicts."""
    ordered = sorted(
        tuple(candidates),
        key=lambda candidate: (
            -candidate.priority,
            candidate.record.title.casefold(),
            candidate.record.doi,
            candidate.record.arxiv_id,
            candidate.record.publication_title.casefold(),
            candidate.record.publication_date,
            candidate.record.text_sha256,
        ),
    )
    if not ordered:
        raise BibliographyValidationError("at least one bibliography candidate is required")
    first = ordered[0]
    if any(candidate.record.key != first.record.key for candidate in ordered[1:]):
        raise BibliographyValidationError("bibliography candidates must have the same record key")
    if any(not titles_compatible(first.record.title, candidate.record.title) for candidate in ordered[1:]):
        raise BibliographyValidationError("title identity conflict")
    for name, message in (("doi", "DOI identity conflict"), ("arxiv_id", "arXiv identity conflict")):
        normalize = canonical_doi if name == "doi" else canonical_arxiv_id
        values = {
            normalize(assertion.field.value)
            for candidate in ordered
            for assertion in candidate.field_evidence
            if assertion.field.name == name and assertion.field.value
        }
        if len(values) > 1:
            raise BibliographyValidationError(message)

    author_sets = [candidate.record.authors for candidate in ordered]
    if any(not authors for authors in author_sets):
        if any(authors for authors in author_sets):
            raise BibliographyValidationError("author identity unresolved")
    elif any(len(authors) != len(author_sets[0]) for authors in author_sets[1:]):
        raise BibliographyValidationError("author identity conflict")
    elif author_sets:
        for candidate_authors in author_sets[1:]:
            for left, right in zip(author_sets[0], candidate_authors):
                decision = decide_author_identity(left, right)
                if decision != "same":
                    raise BibliographyValidationError(f"author identity {decision}")

    def select(name: str, *, required: bool = False) -> str:
        populated = [
            candidate for candidate in ordered
            if (value := getattr(candidate.record, name))
        ]
        if not populated:
            return ""
        priority = populated[0].priority
        values = {getattr(candidate.record, name) for candidate in populated if candidate.priority == priority}
        if len(values) == 1:
            return next(iter(values))
        # No equal-priority assertion is privileged by input order.  Title is
        # required by the record contract; compatible titles use a stable
        # lexical representation rather than treating an input position as a
        # source of authority.
        return min(values, key=str.casefold) if required else ""

    authors = author_sets[0] if author_sets else ()
    institutions = _merge_institutions(
        next((candidate.record.institutions for candidate in ordered if candidate.record.institutions), ()),
        tuple(
            institution
            for candidate in ordered
            for institution in candidate.record.institutions
        ),
    )
    record = BibliographyRecord(
        key=first.record.key,
        title=select("title", required=True),
        authors=authors,
        doi=select("doi"),
        arxiv_id=select("arxiv_id"),
        publication_title=select("publication_title"),
        publication_date=select("publication_date"),
        institutions=institutions,
        evidence=stable_evidence_union(*(candidate.record.evidence for candidate in ordered)),
        text_sha256=select("text_sha256"),
    )
    assertions = merge_field_evidence(
        *(assertion for candidate in ordered for assertion in candidate.field_evidence)
    )
    conflict_names = {assertion.field.name for assertion in assertions}
    conflicts = tuple(
        MetadataConflict(
            name,
            tuple(assertion for assertion in assertions if assertion.field.name == name),
        )
        for name in sorted(conflict_names)
        if len({assertion.field.value for assertion in assertions if assertion.field.name == name}) > 1
    )
    return MergedBibliography(record, assertions, conflicts)


def record_from_sidecar(sidecar: Mapping[str, object], text: str | bytes) -> BibliographyRecord:
    """Validate one review-time sidecar and convert it to canonical metadata."""
    if _text(sidecar.get("schema"), "schema", required=True) != SIDECAR_SCHEMA:
        raise BibliographyValidationError("unsupported bibliography sidecar schema")
    zotero = _mapping(sidecar.get("zotero"), "zotero")
    bibliography = _mapping(sidecar.get("bibliography", {}), "bibliography")
    key = _text(zotero.get("key"), "zotero.key", required=True)
    digest = _sidecar_hash(sidecar.get("text_md_sha256"))
    raw_text = text.encode("utf-8") if isinstance(text, str) else text
    if not isinstance(raw_text, bytes):
        raise BibliographyValidationError("sidecar text must be text or bytes")
    if hashlib.sha256(raw_text).hexdigest() != digest:
        raise BibliographyValidationError(f"stale sidecar for Zotero key {key}")

    affiliations = sidecar.get("affiliations", ())
    if not isinstance(affiliations, (list, tuple)):
        raise BibliographyValidationError("affiliations must be a sequence")
    return BibliographyRecord(
        key=key,
        title=_text(
            zotero.get("title", bibliography.get("title")),
            "zotero.title",
            required=True,
        ),
        authors=_authors(sidecar.get("authors")),
        doi=_text(zotero.get("DOI", bibliography.get("doi")), "zotero.DOI"),
        arxiv_id=_text(zotero.get("archiveID"), "zotero.archiveID"),
        publication_title=_text(zotero.get("publicationTitle"), "zotero.publicationTitle"),
        publication_date=_text(zotero.get("date"), "zotero.date"),
        institutions=tuple(_institution(value, index, key) for index, value in enumerate(affiliations)),
        evidence=(SourceEvidence("bibliography-sidecar", "primary", key),),
        text_sha256=digest,
    )


class IngestBibliographySidecars:
    """Validate all sidecars before committing them in one repository transaction."""

    def __init__(self, repository: BibliographyRepository) -> None:
        self._repository = repository

    def ingest(
        self,
        sidecars: Iterable[Mapping[str, object]],
        *,
        text_by_zotero_key: Mapping[str, str | bytes],
    ) -> IngestedSidecars:
        candidates: list[BibliographyCandidate] = []
        keys: set[str] = set()
        for index, sidecar in enumerate(sidecars):
            zotero = _mapping(sidecar.get("zotero"), f"sidecars[{index}].zotero")
            key = _text(zotero.get("key"), f"sidecars[{index}].zotero.key", required=True)
            if key in keys:
                raise BibliographyValidationError(f"duplicate Zotero key {key}")
            if key not in text_by_zotero_key:
                raise BibliographyValidationError(f"missing text for Zotero key {key}")
            candidates.append(BibliographyCandidate(record_from_sidecar(sidecar, text_by_zotero_key[key]), 0))
            keys.add(key)
        return self.ingest_candidates(candidates)

    def ingest_candidates(self, candidates: Iterable[BibliographyCandidate]) -> IngestedSidecars:
        """Validate identity and merge every candidate before opening a transaction."""
        groups: dict[str, list[BibliographyCandidate]] = {}
        for candidate in candidates:
            groups.setdefault(candidate.record.key, []).append(candidate)
        merged = tuple(merge_bibliography_candidates(group) for group in groups.values())
        with self._repository.transaction() as transaction:
            for bibliography in merged:
                transaction.upsert(bibliography)
        return IngestedSidecars(merged)
