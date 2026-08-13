"""Pure primitives shared by renderer view-model transforms."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from html import escape
from math import isfinite
from typing import Any

_CREDENTIAL_FIELDS = frozenset({
    "api_key", "apikey", "token", "access_token", "authorization", "password",
    "secret", "credential", "credentials", "private_key", "client_secret",
})


@dataclass(frozen=True, slots=True)
class RenderLink:
    """A renderer-safe relative link."""

    href: str


def escaped(value: object) -> str:
    """Return text safe for insertion into HTML text or quoted attributes."""
    return escape("" if value is None else str(value), quote=True)


def required_text(source: Mapping[str, Any], field: str) -> str:
    value = source.get(field)
    if value is None or not str(value).strip():
        raise ValueError(f"{field} is required")
    return str(value).strip()


def optional_text(source: Mapping[str, Any], field: str) -> str:
    value = source.get(field, "")
    return "" if value is None else str(value).strip()


def safe_segment(value: object, field: str) -> str:
    segment = str(value).strip()
    if (
        not segment
        or segment in {".", ".."}
        or "/" in segment
        or "\\" in segment
        or any(ord(character) < 32 for character in segment)
    ):
        raise ValueError(f"invalid {field}: {value!r}")
    return segment


def require_safe_source(source: Mapping[str, Any]) -> None:
    """Reject credentials anywhere in input, including ignored renderer fields."""
    def visit(value: object) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                normalized = str(key).lower().replace("-", "_")
                if normalized in _CREDENTIAL_FIELDS:
                    raise ValueError(f"credential field is not accepted: {key}")
                visit(child)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            for child in value:
                visit(child)

    visit(source)


def safe_number(value: object, field: str, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"invalid {field}: {value!r}") from error
    if not isfinite(number):
        raise ValueError(f"invalid {field}: {value!r}")
    return number


def paper_href(slug: object) -> RenderLink:
    return RenderLink(f"../papers/{safe_segment(slug, 'slug')}/index.html")


def topic_back_href(topic: object) -> RenderLink:
    return RenderLink(f"../../{safe_segment(topic, 'topic')}/index.html")


def network_href() -> RenderLink:
    return RenderLink("network.html")
