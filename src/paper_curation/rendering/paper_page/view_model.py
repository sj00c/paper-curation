"""Pure paper-page data to renderer-model transformation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ..models import RenderLink, escaped, optional_text, require_safe_source, safe_number, safe_segment, topic_back_href


@dataclass(frozen=True, slots=True)
class PaperPageViewModel:
    topic: str
    slug: str
    title: str
    authors: tuple[str, ...]
    date: str
    journal: str
    doi: str
    essence: str
    score: float
    back_link: RenderLink


def build_paper_page_view_model(topic: object, paper: Mapping[str, Any]) -> PaperPageViewModel:
    """Transform canonical paper metadata without touching filesystem or configuration."""
    require_safe_source(paper)
    safe_topic = safe_segment(topic, "topic")
    slug = safe_segment(paper.get("slug", paper.get("dir", "")), "slug")
    raw_authors = paper.get("authors", ())
    if isinstance(raw_authors, str):
        authors = tuple(escaped(author.strip()) for author in raw_authors.split(",") if author.strip())
    elif isinstance(raw_authors, Sequence):
        authors = tuple(escaped(author) for author in raw_authors if str(author).strip())
    else:
        raise ValueError("authors must be a string or sequence")
    title = optional_text(paper, "title") or slug
    return PaperPageViewModel(
        topic=safe_topic,
        slug=slug,
        title=escaped(title),
        authors=authors,
        date=escaped(optional_text(paper, "date")),
        journal=escaped(optional_text(paper, "journal")),
        doi=escaped(optional_text(paper, "doi")),
        essence=escaped(optional_text(paper, "essence")),
        score=safe_number(paper.get("score", paper.get("overall_score")), "score"),
        back_link=topic_back_href(safe_topic),
    )
