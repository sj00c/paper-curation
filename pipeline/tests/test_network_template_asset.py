"""Contracts for the packaged network presentation template."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "pipeline"))

import generate_network
from paper_curation.rendering.network import template


class NetworkTemplateAssetTests(unittest.TestCase):
    def test_renderer_requires_the_complete_context(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing context"):
            template.render_network_template({})

    def test_generated_page_escapes_unicode_topic_and_keeps_json_as_script_data(self) -> None:
        html = generate_network.generate_html(
            nodes=[{"id": "paper-1", "category": "AI", "title": "한글"}],
            links=[],
            cat_colors={"AI": "#fff"},
            cat_shapes={"AI": "circle"},
            sub_colors={},
            years=[2024],
            topic="연구-東京",
            node_conns={"paper-1": []},
        )

        self.assertIn("연구-東京", html)
        self.assertIn('const nodesRaw = [{"id": "paper-1", "category": "AI", "title": "한글"}]', html)
        self.assertNotIn("@@PAPER_CURATION_NETWORK_", html)

    def test_topic_alias_rejects_markup_and_traversal(self) -> None:
        with self.assertRaises(ValueError):
            generate_network.generate_html(
                [], [], {}, {}, {}, [], "<script>alert(1)</script>"
            )

    def test_generated_json_cannot_terminate_the_script(self) -> None:
        html = generate_network.generate_html(
            nodes=[{
                "id": "paper-1",
                "category": "AI",
                "title": "</script><img src=x onerror=alert(1)>",
            }],
            links=[],
            cat_colors={"AI": "#fff"},
            cat_shapes={"AI": "circle"},
            sub_colors={},
            years=[2024],
            topic="topic",
        )
        self.assertNotIn("</script><img", html)
        self.assertIn("\\u003c/script\\u003e", html)


if __name__ == "__main__":
    unittest.main()
