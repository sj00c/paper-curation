"""Conservative, document-local author-to-affiliation link extraction."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import re
import unicodedata

from paper_curation.domain.affiliations import match_affiliation
from paper_curation.domain.author_identity import Author
from paper_curation.domain.bibliography import AuthorInstitutionLink, Institution, SourceEvidence, stable_evidence_union

_SYMBOLS = "*†‡§¶#♣♢♡♠◊△▽○●□■◆★"
_SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


@dataclass(frozen=True, slots=True)
class MarkerAffiliation:
    """A printed marker and the affiliation text it declares."""

    marker: str
    affiliation: str


def _normal_marker(value: str) -> str:
    return value.translate(_SUPERSCRIPT_DIGITS).strip()


def infer_marker_alphabet(document: str) -> tuple[str, ...]:
    """Infer only markers actually used to introduce an affiliation in this document."""
    found: list[str] = []
    for line in document.splitlines():
        match = re.match(r"^\s*([0-9⁰¹²³⁴⁵⁶⁷⁸⁹]+|[" + re.escape(_SYMBOLS) + r"]+)\s*(\S)", line)
        if match and not unicodedata.category(match.group(2)[0]).startswith("L"):
            match = None
        if match:
            raw_marker = match.group(1)
            markers = (_normal_marker(raw_marker),) if raw_marker[0].isdigit() or raw_marker[0] in "⁰¹²³⁴⁵⁶⁷⁸⁹" else tuple(raw_marker)
            for marker in markers:
                if marker and marker not in found:
                    found.append(marker)
    return tuple(found)


def _author_pattern(author: Author) -> str:
    # The preceding Unicode-aware word boundary prevents a short author name
    # (Li) from matching within a longer one (Ali).  The caller requires a
    # marker suffix, which supplies the corresponding end-of-span boundary.
    name = r"\s+".join(re.escape(part) for part in author.display_name.split())
    return r"(?<!\w)" + name


def parse_author_markers(
    byline: str, authors: Sequence[Author], marker_alphabet: Sequence[str],
) -> dict[int, tuple[str, ...]]:
    """Read markers printed immediately after known author names, including wrapped bylines."""
    alphabet = {_normal_marker(marker) for marker in marker_alphabet}
    if not alphabet:
        return {}
    result: dict[int, tuple[str, ...]] = {}
    marker_chars = re.escape("".join(marker_alphabet) + "⁰¹²³⁴⁵⁶⁷⁸⁹")
    for index, author in enumerate(authors):
        match = re.search(
            _author_pattern(author) + r"[ \t]*([" + marker_chars + r"0-9,; \t]+)",
            byline,
            re.IGNORECASE,
        )
        if not match:
            continue
        suffix = match.group(1)
        values = re.findall(r"[0-9⁰¹²³⁴⁵⁶⁷⁸⁹]+|[" + marker_chars + r"]", suffix)
        markers: list[str] = []
        for value in values:
            marker = _normal_marker(value)
            if marker in alphabet and marker not in markers:
                markers.append(marker)
        if markers:
            result[index] = tuple(markers)
    return result


def parse_marker_affiliations(document: str, marker_alphabet: Sequence[str]) -> dict[str, tuple[str, ...]]:
    """Return affiliation declarations explicitly prefixed by inferred markers."""
    alphabet = {_normal_marker(marker) for marker in marker_alphabet}
    result: dict[str, list[str]] = {}
    for line in document.splitlines():
        match = re.match(r"^\s*([0-9⁰¹²³⁴⁵⁶⁷⁸⁹]+|[" + re.escape(_SYMBOLS) + r"]+)\s*(.+?)\s*$", line)
        if not match:
            continue
        raw_marker = match.group(1)
        affiliation = match.group(2).strip(" ,;:")
        markers = (_normal_marker(raw_marker),) if raw_marker[0].isdigit() or raw_marker[0] in "⁰¹²³⁴⁵⁶⁷⁸⁹" else tuple(raw_marker)
        if affiliation:
            for marker in markers:
                if marker in alphabet:
                    result.setdefault(marker, []).append(affiliation)
    return {marker: tuple(declarations) for marker, declarations in result.items()}


def _link(index: int, institution: int, evidence: tuple[SourceEvidence, ...]) -> AuthorInstitutionLink:
    return AuthorInstitutionLink(index, institution, evidence)


def _union_links(links: Sequence[AuthorInstitutionLink]) -> tuple[AuthorInstitutionLink, ...]:
    merged: dict[tuple[int, int], AuthorInstitutionLink] = {}
    for link in links:
        key = (link.author_index, link.institution_index)
        old = merged.get(key)
        merged[key] = link if old is None else _link(*key, stable_evidence_union(old.evidence, link.evidence))
    return tuple(merged.values())


def resolve_affiliation_links(
    authors: Sequence[Author],
    institutions: Sequence[Institution],
    *,
    author_markers: Mapping[int, Sequence[str]] = {},
    marker_affiliations: Mapping[str, str | Sequence[str]] = {},
    named_affiliations: Mapping[int, Sequence[str]] = {},
    shared_affiliations: Sequence[str] = (),
    evidence: tuple[SourceEvidence, ...] = (),
) -> tuple[AuthorInstitutionLink, ...]:
    """Resolve only explicit or unambiguous links; never manufacture a cartesian product.

    Explicit marker declarations win. Named/inline declarations fill authors not
    resolved by markers, then a single shared declaration, then a single paper
    institution. Equal links retain all supporting evidence.
    """
    resolved: set[int] = set()
    links: list[AuthorInstitutionLink] = []

    def add(index: int, text: str) -> bool:
        institution = match_affiliation(text, tuple(institutions))
        if institution is None:
            return False
        links.append(_link(index, tuple(institutions).index(institution), evidence))
        return True

    for index, markers in author_markers.items():
        if index < 0 or index >= len(authors):
            continue
        matched = False
        for marker in markers:
            declarations = marker_affiliations.get(_normal_marker(marker), ())
            texts = (declarations,) if isinstance(declarations, str) else tuple(declarations)
            normalized = {
                " ".join(unicodedata.normalize("NFC", text).casefold().split())
                for text in texts
                if isinstance(text, str) and text.strip()
            }
            if len(normalized) == 1 and texts and add(index, next(text for text in texts if isinstance(text, str) and text.strip())):
                matched = True
        if matched:
            resolved.add(index)

    for index, declarations in named_affiliations.items():
        if index < 0 or index >= len(authors) or index in resolved:
            continue
        matched = False
        for declaration in declarations:
            if add(index, declaration):
                matched = True
        if matched:
            resolved.add(index)

    if len(shared_affiliations) == 1:
        for index in range(len(authors)):
            if index not in resolved and add(index, shared_affiliations[0]):
                resolved.add(index)

    if len(institutions) == 1:
        for index in range(len(authors)):
            if index not in resolved:
                links.append(_link(index, 0, evidence))

    return _union_links(links)
