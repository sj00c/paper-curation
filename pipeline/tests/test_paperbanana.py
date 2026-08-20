import importlib
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.lib import paperbanana
from pipeline.lib.paperbanana import _resolve_output_path


class PaperBananaConfigurationTests(unittest.TestCase):
    def test_clean_import_does_not_probe_configuration(self):
        config_loader = types.ModuleType("config_loader")
        config_loader.get_paperbanana_dir = lambda: (_ for _ in ()).throw(
            AssertionError("configuration probed"))

        with patch.dict(sys.modules, {"config_loader": config_loader}):
            importlib.reload(paperbanana)

    def test_missing_configuration_fails_only_when_generating(self):
        config_loader = types.ModuleType("config_loader")
        config_loader.get_paperbanana_dir = lambda: ""

        with patch.dict(os.environ, {"PAPERBANANA_DIR": ""}, clear=False), \
             patch.dict(sys.modules, {"config_loader": config_loader}), \
             patch.object(paperbanana.logger, "exception"):
            with self.assertRaisesRegex(
                    ValueError, "PaperBanana generation requires PAPERBANANA_DIR"):
                paperbanana.generate_diagram("method", "caption")

    def test_configured_generation_uses_configured_checkout(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.dict(os.environ, {"PAPERBANANA_DIR": tmp}, clear=False), \
             patch.object(paperbanana, "_ensure_path",
                          side_effect=RuntimeError("stop after configuration")) as ensure, \
             patch.object(paperbanana.logger, "exception"):
            with self.assertRaisesRegex(RuntimeError, "stop after configuration"):
                paperbanana.generate_diagram("method", "caption")

        ensure.assert_called_once_with(Path(tmp).resolve())


class PaperBananaOutputPathTests(unittest.TestCase):
    def test_relative_output_is_resolved_before_workdir_change(self):
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                resolved = _resolve_output_path("artifacts/timeline.png")
            finally:
                os.chdir(original)

        self.assertEqual(
            resolved,
            Path(tmp).resolve() / "artifacts" / "timeline.png",
        )

    def test_none_output_stays_none(self):
        self.assertIsNone(_resolve_output_path(None))


if __name__ == "__main__":
    unittest.main()
