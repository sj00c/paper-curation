"""Embedding refusals stay distinguishable by exit code (no network, no real key)."""

import contextlib
import io
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


NO_KEY_ENV = {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""}
KEYED_ENV = {"GOOGLE_API_KEY": "test-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""}
# Nulling the parent package makes `from google import genai` raise ImportError
# without uninstalling anything.
NO_GENAI_MODULES = {"google": None, "google.genai": None}


class SearchIndexExitCodeTests(unittest.TestCase):
    def _refuse(self, env, config, modules=None):
        stdout = io.StringIO()
        with patch.dict(os.environ, env, clear=False), \
                patch.object(config_loader, "load_config", return_value=config), \
                patch.dict(sys.modules, modules or {}, clear=False):
            with contextlib.redirect_stdout(stdout):
                with self.assertRaises(SystemExit) as raised:
                    build_search_index.require_embedding_client()
        return raised.exception.code, stdout.getvalue()

    def test_missing_key_exits_five_with_embeddings_unavailable(self):
        code, out = self._refuse(NO_KEY_ENV, {})

        self.assertEqual(code, 5)
        self.assertIn("EMBEDDINGS_UNAVAILABLE", out)
        self.assertIn("Dense retrieval is unavailable", out)
        self.assertIn("lexical-only", out)

    def test_missing_google_genai_package_still_exits_one(self):
        code, out = self._refuse(
            KEYED_ENV, {"gemini_api_key": "config-key"}, modules=NO_GENAI_MODULES
        )

        self.assertEqual(code, 1)
        self.assertIn("google-genai package not installed", out)
        self.assertNotIn("EMBEDDINGS_UNAVAILABLE", out)

    def test_disable_switch_refuses_with_the_embedding_exit_code(self):
        code, out = self._refuse(
            {**KEYED_ENV, "PAPER_CURATION_NO_GEMINI": "1"}, {"gemini_api_key": "config-key"}
        )

        self.assertEqual(code, 5)
        self.assertIn("EMBEDDINGS_UNAVAILABLE", out)

    def test_missing_dependency_and_missing_key_are_never_the_same_code(self):
        self.assertEqual(build_search_index.EXIT_MISSING_GENAI_PACKAGE, 1)
        self.assertEqual(build_search_index.EXIT_EMBEDDINGS_UNAVAILABLE, 5)
        self.assertNotEqual(
            build_search_index.EXIT_MISSING_GENAI_PACKAGE,
            build_search_index.EXIT_EMBEDDINGS_UNAVAILABLE,
        )

    def test_dependency_check_precedes_key_resolution(self):
        # No key AND no package: the install problem is reported first, as before.
        code, out = self._refuse(NO_KEY_ENV, {}, modules=NO_GENAI_MODULES)

        self.assertEqual(code, 1)
        self.assertIn("google-genai package not installed", out)


if __name__ == "__main__":
    unittest.main()
