"""Pure topic-index data to renderer-model transformation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from ..models import RenderLink, escaped, optional_text, paper_href, require_safe_source, safe_number, safe_segment, network_href


@dataclass(frozen=True, slots=True)
class TopicCardViewModel:
    slug: str
    title: str
    authors: str
    date: str
    journal: str
    essence: str
    score: float
    paper_link: RenderLink


@dataclass(frozen=True, slots=True)
class TopicCategoryViewModel:
    name: str
    description: str
    cards: tuple[TopicCardViewModel, ...]


@dataclass(frozen=True, slots=True)
class TopicPageViewModel:
    topic: str
    categories: tuple[TopicCategoryViewModel, ...]
    network_link: RenderLink


def _category_name(paper: Mapping[str, Any]) -> str:
    value = paper.get("category", paper.get("primary_category", "Other"))
    return optional_text({"category": value}, "category") or "Other"


def _card(paper: Mapping[str, Any]) -> tuple[str, TopicCardViewModel]:
    require_safe_source(paper)
    slug = safe_segment(paper.get("slug", paper.get("dir", "")), "slug")
    title = optional_text(paper, "title") or slug
    authors = paper.get("authors", "")
    if not isinstance(authors, str):
        try:
            authors = ", ".join(str(author).strip() for author in authors if str(author).strip())
        except TypeError as error:
            raise ValueError("authors must be text or an iterable") from error
    return _category_name(paper), TopicCardViewModel(
        slug=slug,
        title=escaped(title),
        authors=escaped(authors),
        date=escaped(optional_text(paper, "date")),
        journal=escaped(optional_text(paper, "journal")),
        essence=escaped(optional_text(paper, "essence")),
        score=safe_number(paper.get("score", paper.get("overall_score")), "score"),
        paper_link=paper_href(slug),
    )


def build_topic_page_view_model(
    topic: object,
    papers: Iterable[Mapping[str, Any]],
    categories: Iterable[Mapping[str, Any]] = (),
) -> TopicPageViewModel:
    """Produce stable, escaped category cards for a topic index page."""
    safe_topic = safe_segment(topic, "topic")
    grouped: dict[str, list[TopicCardViewModel]] = {}
    descriptions: dict[str, str] = {}
    for category in categories:
        require_safe_source(category)
        name = optional_text(category, "name") or optional_text(category, "category")
        if not name:
            raise ValueError("category name is required")
        description = escaped(optional_text(category, "description"))
        descriptions[name] = min(descriptions.get(name, description), description)
        grouped.setdefault(name, [])
    for paper in papers:
        name, card = _card(paper)
        grouped.setdefault(name, []).append(card)
    view_categories = tuple(
        TopicCategoryViewModel(
            name=escaped(name),
            description=descriptions.get(name, ""),
            cards=tuple(sorted(cards, key=lambda card: (-card.score, card.title.casefold(), card.slug))),
        )
        for name, cards in sorted(grouped.items(), key=lambda item: (item[0].casefold(), item[0]))
    )
    return TopicPageViewModel(safe_topic, view_categories, network_href())
