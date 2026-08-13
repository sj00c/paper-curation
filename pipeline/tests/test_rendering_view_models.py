"""Contracts for pure, safe renderer view-model transforms."""

from __future__ import annotations

import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.rendering.network.view_model import build_network_view_model
from paper_curation.rendering.paper_page.view_model import build_paper_page_view_model
from paper_curation.rendering.topic_page.view_model import build_topic_page_view_model


class RenderingViewModelTests(unittest.TestCase):
    def test_paper_page_preserves_arbitrary_safe_topic_back_route(self) -> None:
        model = build_paper_page_view_model("my_topic-2", {"slug": "paper_1", "title": "A"})
        self.assertEqual(model.back_link.href, "../../my_topic-2/index.html")
        with self.assertRaises(ValueError):
            build_paper_page_view_model("../outside", {"slug": "paper_1"})
        with self.assertRaises(ValueError):
            build_paper_page_view_model("topic", {"slug": "../paper"})

    def test_models_escape_html_and_are_immutable(self) -> None:
        model = build_paper_page_view_model("topic", {
            "slug": "paper_1", "title": '<script>alert("x")</script>',
            "authors": ["A & B"], "essence": "<b>summary</b>",
        })
        self.assertEqual(model.title, "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;")
        self.assertEqual(model.authors, ("A &amp; B",))
        self.assertEqual(model.essence, "&lt;b&gt;summary&lt;/b&gt;")
        with self.assertRaises(FrozenInstanceError):
            model.title = "changed"  # type: ignore[misc]

    def test_topic_cards_and_categories_have_stable_order_and_routes(self) -> None:
        model = build_topic_page_view_model("topic", [
            {"slug": "z", "title": "Zoo", "category": "Beta", "score": 1},
            {"slug": "a", "title": "Alpha", "category": "Alpha", "score": 2},
            {"slug": "b", "title": "Beta", "category": "Alpha", "score": 2},
        ], [{"name": "Empty"}])
        self.assertEqual([category.name for category in model.categories], ["Alpha", "Beta", "Empty"])
        self.assertEqual([card.slug for card in model.categories[0].cards], ["a", "b"])
        self.assertEqual(model.categories[0].cards[0].paper_link.href, "../papers/a/index.html")
        self.assertEqual(model.network_link.href, "network.html")

    def test_credentials_are_rejected_and_not_exposed(self) -> None:
        with self.assertRaisesRegex(ValueError, "credential field"):
            build_topic_page_view_model("topic", [{"slug": "a", "api_key": "secret"}])
        with self.assertRaisesRegex(ValueError, "credential field"):
            build_network_view_model("topic", [{"id": "a", "meta": {"token": "secret"}}], [])

    def test_network_orders_and_rejects_malformed_endpoints(self) -> None:
        model = build_network_view_model("topic", [
            {"id": "b", "title": "B"}, {"id": "a", "title": "<A>"},
        ], [{"source": "b", "target": "a", "relation": "<rel>"}])
        self.assertEqual([node.id for node in model.nodes], ["a", "b"])
        self.assertEqual(model.nodes[0].title, "&lt;A&gt;")
        self.assertEqual(model.edges[0].relation, "&lt;rel&gt;")
        with self.assertRaises(ValueError):
            build_network_view_model("topic", [{"id": "a"}], [{"source": "a", "target": "missing"}])


if __name__ == "__main__":
    unittest.main()
