"""Strict renderer for the packaged network presentation template."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from importlib.resources import files
import re


_PLACEHOLDER = re.compile(r"@@PAPER_CURATION_NETWORK_([A-Z0-9_]+)@@")
_EXPECTED_PLACEHOLDERS = (
    "TITLE_TOPIC",
    "HEADING_TOPIC",
    "YEAR_MIN_RANGE_MIN",
    "YEAR_MAX_RANGE_MIN",
    "YEAR_MIN_RANGE_VALUE",
    "YEAR_MIN_MAX_MIN",
    "YEAR_MAX_RANGE_MAX",
    "YEAR_MAX_RANGE_VALUE",
    "YEAR_MIN_LABEL",
    "YEAR_MAX_LABEL",
    "THREE_D_CONTROL",
    "NODES_JSON",
    "LINKS_JSON",
    "NODE_CONNECTIONS_JSON",
    "CATEGORY_COLORS_JSON",
    "CATEGORY_SHAPES_JSON",
    "CATEGORY_COUNTS_JSON",
    "SUBCATEGORY_COLORS_JSON",
    "SUBCATEGORY_COUNTS_JSON",
    "CATEGORY_SUBCATEGORIES_JSON",
    "RELATION_COLORS_JSON",
    "YEAR_MIN_INITIAL",
    "YEAR_MAX_INITIAL",
    "HAS_3D",
)


def _template() -> str:
    return files(__package__).joinpath("template.html").read_text(encoding="utf-8")


def render_network_template(context: Mapping[str, str]) -> str:
    """Render the template with exactly its declared, caller-escaped values."""
    expected = set(_EXPECTED_PLACEHOLDERS)
    provided = set(context)
    missing = expected - provided
    unexpected = provided - expected
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing context: {', '.join(sorted(missing))}")
        if unexpected:
            details.append(f"unexpected context: {', '.join(sorted(unexpected))}")
        raise ValueError("; ".join(details))
    non_text = sorted(name for name, value in context.items() if not isinstance(value, str))
    if non_text:
        raise TypeError(f"template values must be strings: {', '.join(non_text)}")

    template = _template()
    declared = _PLACEHOLDER.findall(template)
    if Counter(declared) != Counter(_EXPECTED_PLACEHOLDERS):
        raise ValueError("template placeholders do not match the renderer contract")
    return _PLACEHOLDER.sub(lambda match: context[match.group(1)], template)
