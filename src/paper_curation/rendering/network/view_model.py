"""Pure graph data to renderer-model transformation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from ..models import escaped, optional_text, require_safe_source, safe_number, safe_segment


@dataclass(frozen=True, slots=True)
class NetworkNodeViewModel:
    id: str
    title: str
    category: str
    year: str
    essence: str
    score: float


@dataclass(frozen=True, slots=True)
class NetworkEdgeViewModel:
    source: str
    target: str
    relation: str
    reason: str
    weight: float


@dataclass(frozen=True, slots=True)
class NetworkViewModel:
    topic: str
    nodes: tuple[NetworkNodeViewModel, ...]
    edges: tuple[NetworkEdgeViewModel, ...]


def build_network_view_model(
    topic: object,
    nodes: Iterable[Mapping[str, Any]],
    edges: Iterable[Mapping[str, Any]],
) -> NetworkViewModel:
    """Validate graph endpoints and return escaped, deterministically ordered data."""
    safe_topic = safe_segment(topic, "topic")
    by_id: dict[str, NetworkNodeViewModel] = {}
    for source in nodes:
        require_safe_source(source)
        node_id = safe_segment(source.get("id", source.get("slug", "")), "node id")
        if node_id in by_id:
            raise ValueError(f"duplicate node id: {node_id}")
        by_id[node_id] = NetworkNodeViewModel(
            id=node_id,
            title=escaped(optional_text(source, "title") or node_id),
            category=escaped(optional_text(source, "category") or "Other"),
            year=escaped(optional_text(source, "year")),
            essence=escaped(optional_text(source, "essence")),
            score=safe_number(source.get("score"), "score"),
        )
    rendered_edges: list[NetworkEdgeViewModel] = []
    for source in edges:
        require_safe_source(source)
        start = safe_segment(source.get("source", ""), "edge source")
        end = safe_segment(source.get("target", ""), "edge target")
        if start == end:
            raise ValueError(f"self-referential edge: {start}")
        if start not in by_id or end not in by_id:
            raise ValueError(f"edge endpoint is not a node: {start} -> {end}")
        rendered_edges.append(NetworkEdgeViewModel(
            source=start,
            target=end,
            relation=escaped(optional_text(source, "relation") or "alternative"),
            reason=escaped(optional_text(source, "reason")),
            weight=safe_number(source.get("weight"), "weight", 1.0),
        ))
    return NetworkViewModel(
        topic=safe_topic,
        nodes=tuple(by_id[node_id] for node_id in sorted(by_id)),
        edges=tuple(sorted(rendered_edges, key=lambda edge: (
            edge.source, edge.target, edge.relation.casefold(), edge.reason.casefold(), edge.weight,
        ))),
    )
