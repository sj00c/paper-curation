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
    Institution,
    SourceEvidence,
)

SIDECAR_SCHEMA = "bibliography-sidecar-1"
_SHA256_CHARACTERS = frozenset(string.hexdigits)


class BibliographyTransaction(Protocol):
    def upsert(self, record: BibliographyRecord) -> None: ...


class BibliographyRepository(Protocol):
    def transaction(self) -> ContextManager[BibliographyTransaction]: ...


@dataclass(frozen=True, slots=True)
class IngestedSidecars:
    """The records committed by a sidecar ingestion operation."""

    records: tuple[BibliographyRecord, ...]


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
        authors=_string_sequence(sidecar.get("authors"), "authors"),
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
        records: list[BibliographyRecord] = []
        keys: set[str] = set()
        for index, sidecar in enumerate(sidecars):
            zotero = _mapping(sidecar.get("zotero"), f"sidecars[{index}].zotero")
            key = _text(zotero.get("key"), f"sidecars[{index}].zotero.key", required=True)
            if key in keys:
                raise BibliographyValidationError(f"duplicate Zotero key {key}")
            if key not in text_by_zotero_key:
                raise BibliographyValidationError(f"missing text for Zotero key {key}")
            records.append(record_from_sidecar(sidecar, text_by_zotero_key[key]))
            keys.add(key)

        with self._repository.transaction() as transaction:
            for record in records:
                transaction.upsert(record)
        return IngestedSidecars(tuple(records))
