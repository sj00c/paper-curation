import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD_TOPIC_INDEX = ROOT / "pipeline" / "build_topic_index.py"
DASHBOARD_RUNTIME = ROOT / "docs" / "public" / "paper-curation-local.js"


class GeneratedDashboardSecurityTests(unittest.TestCase):
    """Contract checks for the local dashboard emitted by build_topic_index."""

    @classmethod
    def setUpClass(cls):
        cls.source = BUILD_TOPIC_INDEX.read_text(encoding="utf-8")
        cls.runtime = DASHBOARD_RUNTIME.read_text(encoding="utf-8")

    def test_generated_dashboard_has_no_browser_provider_or_secret_paths(self):
        source = (self.source + self.runtime).lower()
        forbidden = (
            "api.anthropic.com",
            "api.openai.com",
            "generativelanguage.googleapis.com",
            "anthropic-dangerous-direct-browser-access",
            "localstorage",
            "x-api-key",
            "authorization': 'bearer",
            "authorization\": \"bearer",
            "_gemini_key",
            "_anthropic_key",
            "_openai_key",
            "audio_modal",
            "audio_script",
        )
        for value in forbidden:
            self.assertNotIn(value, source)

    def test_actions_use_only_same_origin_authoritative_protocol(self):
        source = self.runtime
        for route in (
            "'/api/action/plan'",
            "'/api/action/approve'",
            "'/api/action/start'",
            "'/api/action/status?operation_id='",
            "'/api/action/final?operation_id='",
        ):
            self.assertIn(route, source)
        self.assertIn("credentials: 'same-origin'", source)
        self.assertIn("RETAINED_NO_EFFECT", source)
        self.assertIn("no browser fallback will run", source)

    def test_bootstrap_json_is_text_content_parsed_and_script_safe(self):
        source = self.source
        self.assertIn('type="application/json"', source)
        self.assertIn('JSON.parse(bootstrapEl.textContent)', self.runtime)
        for escaped in (r'replace("<", "\\u003c")', r'replace(">", "\\u003e")', r'replace("&", "\\u0026")'):
            self.assertIn(escaped, source)
        self.assertIn('replace("\\u2028", "\\\\u2028")', source)
        self.assertIn('replace("\\u2029", "\\\\u2029")', source)

    def test_audio_is_bootstrap_gated_without_affecting_local_search_and_cards(self):
        source = self.runtime
        self.assertIn('button.hidden = !enabled', source)
        self.assertIn('button.disabled = !enabled', source)
        self.assertIn("configureAudio(actionsAvailable ? ACTION.bootstrap.audio_capability : null)", source)
        self.assertIn("action_capability.state === 'AVAILABLE'", source)
        self.assertIn("button.disabled = !actionsAvailable", source)
        self.assertIn("actionJson('/api/bootstrap')", source)
        self.assertIn("function searchPapers(query)", source)
        self.assertIn("render_paper_card", self.source)


if __name__ == "__main__":
    unittest.main()
