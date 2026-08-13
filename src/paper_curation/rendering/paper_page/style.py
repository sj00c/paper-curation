"""Pure renderer for the packaged paper-page stylesheet."""

from __future__ import annotations

from collections.abc import Mapping
from importlib.resources import files
import re


_THEME_PLACEHOLDERS = {
    "accent": "{{PAPER_CURATION_THEME__ACCENT__}}",
    "accent_dark": "{{PAPER_CURATION_THEME__ACCENT_DARK__}}",
    "accent_bg": "{{PAPER_CURATION_THEME__ACCENT_BG__}}",
    "essence_border": "{{PAPER_CURATION_THEME__ESSENCE_BORDER__}}",
    "essence_bg": "{{PAPER_CURATION_THEME__ESSENCE_BG__}}",
    "link_color": "{{PAPER_CURATION_THEME__LINK_COLOR__}}",
}
_UNRESOLVED_PLACEHOLDER = re.compile(r"\{\{PAPER_CURATION_THEME__[A-Z_]+__\}\}")
_CSS_COLOR = re.compile(
    r"(?:#[0-9A-Fa-f]{3,4}|#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{8}|[A-Za-z]+)"
)


def _load_template() -> str:
    return files(__package__).joinpath("style.css").read_text(encoding="utf-8")


def _safe_color(value: object, key: str) -> str:
    if not isinstance(value, str) or not _CSS_COLOR.fullmatch(value):
        raise ValueError(f"theme {key!r} must be a CSS-safe color")
    return value


def render_css(theme: Mapping[str, object]) -> str:
    """Render the stylesheet with validated theme colors and no leftover tokens."""
    stylesheet = _load_template()
    for key, placeholder in _THEME_PLACEHOLDERS.items():
        if placeholder not in stylesheet:
            raise ValueError(f"paper stylesheet is missing placeholder for {key!r}")
        try:
            value = theme[key]
        except KeyError as exc:
            raise ValueError(f"theme is missing {key!r}") from exc
        stylesheet = stylesheet.replace(placeholder, _safe_color(value, key))
    if _UNRESOLVED_PLACEHOLDER.search(stylesheet):
        raise ValueError("paper stylesheet contains unresolved theme placeholders")
    return stylesheet.rstrip("\r\n")
