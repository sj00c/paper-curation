"""Data-free affiliation comparison for record-local assertions."""

from __future__ import annotations

import re
import unicodedata
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .bibliography import Institution


_GENERIC_AFFILIATION_TOKENS = frozenset({
    "academy",
    "center",
    "centre",
    "college",
    "department",
    "faculty",
    "hospital",
    "institute",
    "laboratory",
    "school",
    "university",
    "a",
    "an",
    "and",
    "at",
    "de",
    "del",
    "der",
    "des",
    "di",
    "du",
    "for",
    "in",
    "la",
    "le",
    "of",
    "the",
})
_SUBUNIT_TOKENS = frozenset(
    {
        "center",
        "centre",
        "department",
        "faculty",
        "laboratory",
        "school",
    }
)


def canonical_affiliation(value: str) -> str:
    """Return a Unicode-preserving comparison key, not an external identifier."""
    value = unicodedata.normalize("NFC", value).strip()
    if not value:
        raise ValueError("affiliation must not be empty")
    return " ".join(re.findall(r"[^\W_]+", value.casefold(), flags=re.UNICODE))


def _discriminative_tokens(value: str) -> set[str]:
    return set(canonical_affiliation(value).split()) - _GENERIC_AFFILIATION_TOKENS


def affiliation_score(left: str, right: str) -> float:
    """Score discriminative lexical agreement without institution data."""
    left_tokens, right_tokens = _discriminative_tokens(left), _discriminative_tokens(right)
    if left_tokens == right_tokens and left_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def affiliations_contradict(left: Institution, right: Institution) -> bool:
    """Return true only for explicit, incompatible asserted identifiers."""
    return bool(
        (left.ror_id and right.ror_id and left.ror_id.casefold() != right.ror_id.casefold())
        or (left.country and right.country and left.country.casefold() != right.country.casefold())
    )


def match_affiliation(
    asserted_name: str,
    candidates: Iterable[Institution],
    *,
    minimum_score: float = 0.5,
) -> Institution | None:
    """Return a unique match with substantial discriminative lexical agreement."""
    if not 0.0 <= minimum_score <= 1.0:
        raise ValueError("minimum score must be between zero and one")
    asserted_tokens = _discriminative_tokens(asserted_name)
    asserted_canonical = canonical_affiliation(asserted_name)
    asserted_all_tokens = set(asserted_canonical.split())
    scored: list[tuple[float, Institution]] = []
    for candidate in candidates:
        candidate_canonical = canonical_affiliation(candidate.name)
        candidate_tokens = _discriminative_tokens(candidate.name)
        has_subunit = bool(
            (asserted_all_tokens | set(candidate_canonical.split()))
            & _SUBUNIT_TOKENS
        )
        exact = asserted_canonical == candidate_canonical
        if has_subunit and not exact:
            continue
        if len(asserted_tokens & candidate_tokens) >= 2 or (
            exact and bool(asserted_tokens)
        ):
            scored.append((affiliation_score(asserted_name, candidate.name), candidate))
    if not scored:
        return None
    best_score = max(score for score, _ in scored)
    if best_score < minimum_score:
        return None
    winners = [candidate for score, candidate in scored if score == best_score]
    return winners[0] if len(winners) == 1 else None
