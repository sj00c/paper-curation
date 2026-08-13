"""Contracts for the packaged paper-page stylesheet."""

from __future__ import annotations

import sys
import unittest
from importlib.resources import files
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.rendering.paper_page.style import render_css


THEME = {
    "accent": "#3B82F6",
    "accent_dark": "#2563EB",
    "accent_bg": "#EFF6FF",
    "essence_border": "#2563EB",
    "essence_bg": "#F8FAFD",
    "link_color": "#2563EB",
}


class PaperStyleAssetTests(unittest.TestCase):
    def test_packaged_resource_renders_configured_theme(self) -> None:
        resource = files("paper_curation.rendering.paper_page").joinpath("style.css")
        self.assertTrue(resource.is_file())
        css = render_css({key: "#123456" for key in THEME})
        self.assertIn("border-bottom: 3px solid #123456", css)
        self.assertIn("background: #123456", css)
        self.assertNotIn("{{PAPER_CURATION_THEME__", css)

    def test_named_css_color_is_accepted(self) -> None:
        css = render_css({key: "rebeccapurple" for key in THEME})
        self.assertIn("color: rebeccapurple", css)

    def test_malicious_theme_value_is_rejected(self) -> None:
        theme = dict(THEME, accent="#123456; background: url(https://attacker.invalid)")
        with self.assertRaises(ValueError):
            render_css(theme)

    def test_unresolved_placeholder_is_rejected(self) -> None:
        with patch(
            "paper_curation.rendering.paper_page.style._load_template",
            return_value="a { color: {{PAPER_CURATION_THEME__UNKNOWN__}}; }",
        ):
            with self.assertRaises(ValueError):
                render_css(THEME)

    def test_review_renderer_delegates_without_embedded_stylesheet(self) -> None:
        source = (ROOT / "pipeline" / "review_to_html.py").read_text(encoding="utf-8")
        self.assertIn("from paper_curation.rendering.paper_page.style import render_css", source)
        self.assertIn("def get_css(t):\n    return render_css(t)", source)
        self.assertNotIn("body {{ font-family: 'KoPub Dotum'", source)


if __name__ == "__main__":
    unittest.main()
