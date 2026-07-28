import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import review_to_html as R  # noqa: E402


class GeneratedReviewPageSecurityTests(unittest.TestCase):
    """Contract checks for the secret-free, localhost-owned review page boundary."""

    @classmethod
    def setUpClass(cls):
        cls.html = cls._render_review()
        cls.runtime = (ROOT / "docs" / "public" / "paper-curation-local.js").read_text(
            encoding="utf-8"
        )

    @staticmethod
    def _render_review():
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            papers = docs / "papers"
            slug = "001_Test_Paper"
            paper_dir = papers / slug
            paper_dir.mkdir(parents=True)
            figures = paper_dir / "figures"
            figures.mkdir()
            (figures / "fig1.png").write_bytes(b"\x89PNG\r\n\x1a\nsynthetic")
            (paper_dir / "review.md").write_text(
                """# Safe Review
> **저자**: Test Author

## Essence
A concise summary.

## Background
Prior work context.

## Method
The proposed method.

## Results
![Figure one](figures/fig1.png)

## Evaluation
| Novelty | 4/5 |
| --- | --- |
| Technical Soundness | 4/5 |

## Implications
Useful follow-up notes.
""",
                encoding="utf-8",
            )
            topic_dir = docs / "safe-topic"
            topic_dir.mkdir()
            (topic_dir / "_paper_connections.json").write_text(
                json.dumps({slug: [{"slug": "002_Related", "relation": "extension", "reason": "Extends [001]."}]}),
                encoding="utf-8",
            )
            (papers / "_papers_index.json").write_text(
                json.dumps([
                    {"slug": slug, "title": "Safe Review", "date": "2026-01-01", "doi": ""},
                    {"slug": "002_Related", "title": "Related Paper", "date": "2026-01-02", "doi": ""},
                ]),
                encoding="utf-8",
            )
            old_papers, old_connections, old_bsi = R.PAPERS, R._connections_cache, R._BSI
            try:
                R.PAPERS = str(papers)
                R._connections_cache = {}
                R._BSI = None
                return R.convert_review(str(paper_dir / "review.md"), "safe-topic", str(paper_dir))
            finally:
                R.PAPERS, R._connections_cache, R._BSI = old_papers, old_connections, old_bsi

    def test_generated_page_has_no_browser_secret_or_provider_path(self):
        lower = self.html.lower()
        for forbidden in (
            "gemini_api_key",
            "google_api_key",
            "paper_curation_local_emails",
            "config.json",
            "localstorage",
            "generativelanguage.googleapis.com",
            "api.anthropic.com",
            "api.openai.com",
            "/api/audio-email",
            "resend",
            "browser fallback",
        ):
            self.assertNotIn(forbidden, lower)
        self.assertNotRegex(self.html, r"\son[a-z]+\s*=")

    def test_generated_page_uses_owned_assets_and_safe_action_bootstrap(self):
        self.assertIn('href="../../public/paper-curation-local.css"', self.html)
        self.assertIn('src="../../public/paper-curation-local.js" defer', self.html)
        bootstrap = re.search(
            r'<script id="dashboard-bootstrap" type="application/json">(.*?)</script>',
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(bootstrap)
        payload = json.loads(bootstrap.group(1))
        self.assertEqual(payload["schema"], 1)
        self.assertEqual(payload["audio_capability"], {
            "schema": "AudioCapabilityV1",
            "state": "UNAVAILABLE",
        })
        self.assertIn("'/api/action/plan'", self.runtime)
        self.assertIn("'/api/action/approve'", self.runtime)
        self.assertIn("credentials: 'same-origin'", self.runtime)

    def test_audio_is_the_only_capability_gated_surface(self):
        self.assertIn('id="deep-audio" type="button" hidden disabled aria-disabled="true"', self.html)
        self.assertIn("button.hidden = !enabled", self.runtime)
        self.assertIn("button.disabled = !enabled", self.runtime)
        self.assertIn("AudioCapabilityV1", self.runtime)
        disabled_buttons = re.findall(r'<button[^>]*disabled[^>]*>', self.html)
        self.assertEqual(len(disabled_buttons), 1)
        self.assertIn('id="deep-audio"', disabled_buttons[0])

    def test_inline_links_escape_attribute_and_text_injection(self):
        rendered = R._inline(
            '[bad" onclick="alert(1)](https://example.test/" onmouseover="alert(2))'
        )
        self.assertNotIn(' onclick="', rendered)
        self.assertNotIn(' onmouseover="', rendered)
        self.assertIn("&quot;", rendered)
        self.assertNotIn("<a ", rendered)
        safe = R._inline("[safe](https://example.test/paper)")
        self.assertIn('rel="noopener noreferrer"', safe)
    def test_review_content_sections_figures_and_connections_remain(self):
        for section in ("Essence", "Background", "Method", "Results", "Evaluation", "Implications"):
            self.assertIn(f"<h2>{section}</h2>", self.html)
        self.assertIn('src="figures/fig1.png"', self.html)
        self.assertIn("같이 보면 좋은 논문", self.html)
        self.assertIn("Related Paper", self.html)


if __name__ == "__main__":
    unittest.main()
