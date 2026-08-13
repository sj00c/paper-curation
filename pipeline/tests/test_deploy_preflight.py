"""Contracts for fail-closed read-only deployment preflight."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))
import inspect_deploy
import prepare_deploy


class DeployPreflightTests(unittest.TestCase):
    def test_missing_publication_credentials_and_assets_fail(self):
        with tempfile.TemporaryDirectory() as temporary, \
             patch.object(inspect_deploy, "ROOT", Path(temporary)), \
             patch.dict("os.environ", {}, clear=True), \
             patch("inspect_deploy.shutil.which", return_value=None):
            failures = inspect_deploy.inspect_deploy("topic")
        self.assertTrue(any("publication.mode" in item for item in failures))
        self.assertTrue(any("Cloudflare API token" in item for item in failures))
        self.assertTrue(any("required deploy asset" in item for item in failures))

    def test_complete_public_installation_passes_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs" / "papers").mkdir(parents=True)
            (root / "docs" / "topic").mkdir(parents=True)
            (root / "docs" / "papers" / "_papers_index.json").write_text(
                '[{"slug": "001_example"}]'
            )
            (root / "docs" / "topic" / "index.html").write_text("ok")
            (root / "docs" / "topic" / "_new_classification.json").write_text(
                '{"categories": [], "assignments": []}'
            )
            (root / "docs" / "topic" / "_search_index.json").write_text("{}")
            (root / "docs" / "topic" / "index.html").write_text("ok")
            (root / "wrangler.toml").write_text("name='test'")
            (root / "config.json").write_text(json.dumps({
                "publication": {"mode": "public", "base_url": "https://example.test"}
            }))
            before = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            with patch.object(inspect_deploy, "ROOT", root), patch.dict(
                "os.environ",
                {"CF_API_TOKEN": "secret", "CLOUDFLARE_ACCOUNT_ID": "account"},
                clear=True,
            ), patch("inspect_deploy.shutil.which", return_value="/usr/bin/npx"):
                self.assertEqual(inspect_deploy.inspect_deploy("topic"), ())
            after = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            self.assertEqual(before, after)

    def test_prepare_deploy_runs_preflight_before_any_mutation(self):
        with patch("inspect_deploy.inspect_deploy", return_value=("blocked",)), \
             patch.object(prepare_deploy, "ensure_gitignore",
                          side_effect=AssertionError("mutation must not run")):
            with self.assertRaises(SystemExit):
                prepare_deploy._run_deploy("topic", push=True)


if __name__ == "__main__":
    unittest.main()
