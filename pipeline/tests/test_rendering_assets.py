"""Contracts for packaged static topic-page assets."""

from __future__ import annotations

import re
import sys
import unittest
from importlib.resources import files
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.rendering.assets import load_text_asset


class TopicPageAssetTests(unittest.TestCase):
    def test_packaged_resource_loads_and_contains_page_functions(self) -> None:
        resource = files("paper_curation.rendering.topic_page").joinpath("app.js")
        self.assertTrue(resource.is_file())
        javascript = load_text_asset()
        self.assertEqual(javascript, resource.read_text(encoding="utf-8"))
        self.assertIn("function toggleTopic(id)", javascript)
        self.assertIn("async function runDeepResearch", javascript)

    def test_synthetic_page_script_keeps_characteristic_functions(self) -> None:
        script = (
            "let _ANTHROPIC_KEY = '';\n"
            "let _OPENAI_KEY = '';\n"
            "let _LLM_KEY = '';\n"
            "window._PC_CROSS = false;\n"
            + load_text_asset()
        )
        self.assertIn("function sortCards(key, order)", script)
        self.assertIn("function toggleInsights()", script)
        self.assertIn("async function runDeepResearch", script)

    def test_asset_contains_no_credential_or_browser_storage_persistence(self) -> None:
        javascript = load_text_asset()
        self.assertNotIn("localStorage", javascript)
        self.assertNotIn("sessionStorage", javascript)
        self.assertIsNone(re.search(r"sk-(?:ant|proj)-[A-Za-z0-9_-]{20,}", javascript))
        self.assertIsNone(re.search(r"AIza[A-Za-z0-9_-]{20,}", javascript))

    def test_answer_markup_passes_through_a_strict_dom_sanitizer(self) -> None:
        javascript = load_text_asset()
        self.assertIn("function sanitizeMarkup(", javascript)
        self.assertIn("new DOMParser()", javascript)
        self.assertIn("allowed.has(node.tagName)", javascript)
        self.assertIn("node.removeAttribute", javascript)

    def test_builder_uses_packaged_asset_instead_of_embedded_javascript(self) -> None:
        builder = (ROOT / "pipeline" / "build_topic_index.py").read_text(encoding="utf-8")
        self.assertIn("from paper_curation.rendering import load_text_asset", builder)
        self.assertIn("+ load_text_asset())", builder)
        self.assertNotIn('JS = """function toggleTopic(id)', builder)


if __name__ == "__main__":
    unittest.main()
