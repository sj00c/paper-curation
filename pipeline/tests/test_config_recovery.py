"""Crash-safe setup config transaction contracts."""
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402
import setup as setup_cli  # noqa: E402


class SimulatedCrash(Exception):
    pass


class ConfigRecoveryTests(unittest.TestCase):
    def _config(self, directory, value="old"):
        path = Path(directory) / "config.json"
        path.write_text('{"value":"%s"}\n' % value, encoding="utf-8")
        os.chmod(path, 0o600)
        return path

    def test_every_crash_state_recovers_exactly(self):
        for state in ("PREPARED", "ORIGINAL_MOVED", "REPLACED", "COMMITTED"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                path = self._config(directory)

                def crash(edge):
                    if edge == state:
                        raise SimulatedCrash()

                with self.assertRaises(SimulatedCrash):
                    config_loader.write_config_transaction({"value": "new"}, path, crash)
                config_loader.recover_config_transaction(path)
                expected = "new" if state == "COMMITTED" else "old"
                self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"value": expected})
                self.assertFalse((Path(directory) / "config.json.receipt").exists())
                self.assertFalse((Path(directory) / "config.json.lock").exists())
                self.assertEqual(list(Path(directory).glob("config.json.tmp.*")), [])
                self.assertEqual(list(Path(directory).glob("config.json.legacy.*")), [])

    def test_outputs_are_private_and_no_replace_or_copy_is_used(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            with patch.object(os, "replace", side_effect=AssertionError("replace fallback")):
                config_loader.write_config_transaction({"value": "new"}, path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o600)
            self.assertEqual(os.lstat(path).st_nlink, 1)

    def test_untracked_or_unsafe_candidates_are_ambiguous_and_untouched(self):
        variants = ("config.json.backup", "config.json.tmp.hostile", "config.json.legacy.hostile")
        for name in variants:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                path = self._config(directory)
                candidate = Path(directory) / name
                candidate.write_text("secret", encoding="utf-8")
                os.chmod(candidate, 0o600)
                before = candidate.read_bytes()
                with self.assertRaisesRegex(config_loader.ConfigRecoveryError, "CONFIG_RECOVERY_AMBIGUOUS"):
                    config_loader.write_config_transaction({"value": "new"}, path)
                self.assertEqual(candidate.read_bytes(), before)
                self.assertEqual(path.read_text(encoding="utf-8"), '{"value":"old"}\n')

    def test_mode_owner_link_and_symlink_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            os.chmod(path, 0o644)
            with self.assertRaisesRegex(config_loader.ConfigRecoveryError, "CONFIG_RECOVERY_AMBIGUOUS"):
                config_loader.write_config_transaction({"value": "new"}, path)
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            link = Path(directory) / "config.json.backup"
            os.link(path, link)
            with self.assertRaisesRegex(config_loader.ConfigRecoveryError, "CONFIG_RECOVERY_AMBIGUOUS"):
                config_loader.write_config_transaction({"value": "new"}, path)
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            link = Path(directory) / "config.json.tmp.hostile"
            link.symlink_to(path)
            with self.assertRaisesRegex(config_loader.ConfigRecoveryError, "CONFIG_RECOVERY_AMBIGUOUS"):
                config_loader.write_config_transaction({"value": "new"}, path)

    def test_receipt_digest_mismatch_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._config(directory)
            def crash(edge):
                if edge == "ORIGINAL_MOVED":
                    raise SimulatedCrash()
            with self.assertRaises(SimulatedCrash):
                config_loader.write_config_transaction({"value": "new"}, path, crash)
            receipt = next(Path(directory).glob("config.json.receipt"))
            data = receipt.read_text(encoding="utf-8").replace("a", "b", 1)
            receipt.write_text(data, encoding="utf-8")
            os.chmod(receipt, 0o600)
            with self.assertRaisesRegex(config_loader.ConfigRecoveryError, "CONFIG_RECOVERY_AMBIGUOUS"):
                config_loader.recover_config_transaction(path)
            self.assertTrue(receipt.exists())

    def test_missing_gemini_is_not_a_core_setup_failure(self):
        self.assertEqual([item["env"] for item in setup_cli.REQUIRED_KEYS], ["ZOTERO_API_KEY", "GOOGLE_API_KEY"])
        with patch.dict(os.environ, {"ZOTERO_API_KEY": "", "GOOGLE_API_KEY": "", "GEMINI_API_KEY": ""}, clear=False):
            self.assertEqual(setup_cli.missing_required_keys({}), [setup_cli.REQUIRED_KEYS[0]])


if __name__ == "__main__":
    unittest.main()
