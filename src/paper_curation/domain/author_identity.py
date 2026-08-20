"""Pure author-name normalization and conservative identity decisions."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Literal

AuthorIdentityDecision = Literal["same", "conflict", "unresolved"]


def canonical_orcid(value: str) -> str:
    """Return a canonical ORCID, rejecting malformed values."""
    orcid = value.strip()
    orcid = re.sub(r"^https?://orcid\.org/", "", orcid, flags=re.IGNORECASE)
    orcid = orcid.replace("-", "").upper()
    if not orcid:
        return ""
    if not re.fullmatch(r"\d{15}[\dX]", orcid):
        raise ValueError("ORCID must contain 16 digits")
    total = 0
    for character in orcid[:15]:
        total = (total + int(character)) * 2
    check = (12 - total % 11) % 11
    expected = "X" if check == 10 else str(check)
    if orcid[-1] != expected:
        raise ValueError("ORCID checksum is invalid")
    return "-".join((orcid[:4], orcid[4:8], orcid[8:12], orcid[12:]))


def canonical_author_name(value: str) -> str:
    """Return a Unicode-preserving key while accepting family-name-first display."""
    display = unicodedata.normalize("NFC", value).strip()
    if not display:
        raise ValueError("author name must not be empty")
    parts = [" ".join(part.split()) for part in display.split(",")]
    if len(parts) == 2 and all(parts):
        display = f"{parts[1]} {parts[0]}"
    else:
        display = " ".join(display.split())
    return display.casefold()


def _names_agree(left: str, right: str) -> bool:
    """Return true only for an exact canonical name assertion."""
    return left == right


@dataclass(frozen=True, slots=True)
class Author:
    """An author with display text retained separately from its identity key."""

    display_name: str
    orcid: str = ""
    identity_key: str = ""

    def __post_init__(self) -> None:
        display_name = unicodedata.normalize("NFC", self.display_name).strip()
        if not display_name:
            raise ValueError("author name must not be empty")
        key = canonical_author_name(display_name)
        if self.identity_key and self.identity_key != key:
            raise ValueError("author identity key must match display name")
        object.__setattr__(self, "display_name", display_name)
        object.__setattr__(self, "identity_key", key)
        object.__setattr__(self, "orcid", canonical_orcid(self.orcid))


def decide_author_identity(left: Author, right: Author) -> AuthorIdentityDecision:
    """Decide identity only when assertions agree; conflicts never fall back to names."""
    if left.orcid and right.orcid:
        if left.orcid != right.orcid:
            return "conflict"
        return "same"
    if _names_agree(left.identity_key, right.identity_key):
        return "same"
    return "unresolved"
