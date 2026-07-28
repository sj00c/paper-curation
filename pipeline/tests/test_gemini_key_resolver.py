"""One canonical Gemini key resolver: every call site must agree, matrix by matrix."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
ROOT = PIPELINE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import build_search_index  # noqa: E402
import config_loader  # noqa: E402
import run_update_force  # noqa: E402
import serve_local  # noqa: E402


# (name, environment, config.json payload, expected resolved key)
# An empty env value means "unset" for resolution purposes; PAPER_CURATION_NO_GEMINI
# is the explicit disable switch (set by reextract_figures.py's geometric-only mode).
KEY_MATRICES = (
    (
        "env-only",
        {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
        {},
        "env-key",
    ),
    (
        "env-alias-only",
        {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "alias-key", "PAPER_CURATION_NO_GEMINI": ""},
        {},
        "alias-key",
    ),
    (
        "config-only",
        {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
        {"gemini_api_key": "config-key"},
        "config-key",
    ),
    (
        "config-only-legacy-alias",
        {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
        {"google_api_key": "legacy-config-key"},
        "legacy-config-key",
    ),
    (
        "disabled-by-flag",
        {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "alias-key", "PAPER_CURATION_NO_GEMINI": "1"},
        {"gemini_api_key": "config-key"},
        "",
    ),
    (
        "nothing-configured",
        {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
        {},
        "",
    ),
)


class GeminiKeyResolverAgreementTests(unittest.TestCase):
    def _matrix(self, env, config):
        """Pin process env and config.json content; .env loading is bypassed."""
        return (
            patch.dict(os.environ, env, clear=False),
            patch.object(config_loader, "load_config", return_value=config),
        )

    def _resolved_by_call_site(self):
        return {
            "config_loader.get_google_key": config_loader.get_google_key(),
            "build_search_index (embedding pass)": build_search_index.get_google_key(),
            "run_update_force (figure validation)": run_update_force.get_google_key(),
            "serve_local.resolve_google_key": serve_local.resolve_google_key() or "",
        }

    def test_every_call_site_resolves_identically(self):
        for name, env, config, expected in KEY_MATRICES:
            with self.subTest(matrix=name):
                env_patch, config_patch = self._matrix(env, config)
                with env_patch, config_patch:
                    resolved = self._resolved_by_call_site()
                self.assertEqual(
                    set(resolved.values()), {expected},
                    f"call sites disagree on matrix {name}: {resolved}",
                )

    def test_call_sites_share_one_resolver_object(self):
        self.assertIs(build_search_index.get_google_key, config_loader.get_google_key)
        self.assertIs(run_update_force.get_google_key, config_loader.get_google_key)
        self.assertIs(serve_local.get_google_key, config_loader.get_google_key)
        self.assertFalse(hasattr(build_search_index, "_load_gemini_key_from_config"))

    def test_serve_local_returns_none_only_when_nothing_resolves(self):
        for name, env, config, expected in KEY_MATRICES:
            with self.subTest(matrix=name):
                env_patch, config_patch = self._matrix(env, config)
                with env_patch, config_patch:
                    value = serve_local.resolve_google_key()
                if expected:
                    self.assertEqual(value, expected)
                else:
                    self.assertIsNone(value)

    def test_figure_validation_gate_follows_the_shared_resolver(self):
        for name, env, config, expected in KEY_MATRICES:
            with self.subTest(matrix=name):
                env_patch, config_patch = self._matrix(env, config)
                with env_patch, config_patch:
                    # Mirrors run_update_force.extract_figures' have_gemini gate.
                    have_gemini = bool(run_update_force.get_google_key().strip())
                self.assertEqual(have_gemini, bool(expected))

    def test_disable_switch_beats_a_configured_key_everywhere(self):
        env = {
            "GOOGLE_API_KEY": "env-key",
            "GEMINI_API_KEY": "alias-key",
            "PAPER_CURATION_NO_GEMINI": "1",
        }
        env_patch, config_patch = self._matrix(env, {"gemini_api_key": "config-key"})
        with env_patch, config_patch:
            resolved = self._resolved_by_call_site()
            self.assertIsNone(serve_local.resolve_google_key())
        self.assertEqual(set(resolved.values()), {""}, resolved)

    def test_resolve_google_key_stays_a_patchable_module_attribute(self):
        # pipeline/tests/test_tls_security.py patches this exact seam.
        original = serve_local.resolve_google_key
        self.assertTrue(callable(original))
        with patch.object(serve_local, "resolve_google_key", return_value=None) as stub:
            self.assertIsNone(serve_local.resolve_google_key())
            self.assertEqual(stub.call_count, 1)
        self.assertIs(serve_local.resolve_google_key, original)

    def test_server_still_constructs_no_gemini_client(self):
        source = Path(serve_local.__file__).read_text(encoding="utf-8")
        self.assertNotIn("genai.Client", source)
        self.assertNotIn("embedContent", source)


if __name__ == "__main__":
    unittest.main()
