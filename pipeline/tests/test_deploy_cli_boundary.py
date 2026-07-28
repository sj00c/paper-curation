import hashlib
import inspect
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import prepare_deploy as deploy  # noqa: E402


class DeployCliBoundaryTests(unittest.TestCase):
    def _sealed_scope(self, root):
        stage = Path(root) / "stage"
        topic_dir = stage / "docs" / "ai4s"
        topic_dir.mkdir(parents=True)
        (topic_dir / "index.html").write_text("sealed", encoding="utf-8")
        target = stage / "wrangler.toml"
        target.write_text('[assets]\ndirectory = "./docs"\n', encoding="utf-8")
        files = {}
        for path in (topic_dir / "index.html", target):
            files[str(path.relative_to(stage))] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest = stage / "manifest.json"
        manifest.write_text(json.dumps({
            "topic": "ai4s", "pathspec": "docs/ai4s", "target": "wrangler.toml", "files": files,
        }), encoding="utf-8")
        return stage, manifest, target


    def test_dry_run_requires_only_an_exact_topic_scope(self):
        with patch.object(sys, "argv", ["prepare_deploy.py", "--topic", "ai4s", "--dry-run"]):
            deploy.main()
        with patch.object(sys, "argv", ["prepare_deploy.py", "--topic", "../all", "--dry-run"]):
            with self.assertRaises(SystemExit):
                deploy.main()

    def test_legacy_and_broad_grammar_is_rejected(self):
        with patch.object(sys, "argv", ["prepare_deploy.py", "--topic", "ai4s", "--push"]):
            with self.assertRaises(SystemExit):
                deploy.main()
        source = inspect.getsource(deploy)
        self.assertNotIn('["git"', source)
        self.assertNotIn("subprocess.run", source)
        self.assertNotIn("wrangler", source)

    def test_mutated_staging_fails_during_validation(self):
        with tempfile.TemporaryDirectory() as root:
            stage, manifest, target = self._sealed_scope(root)
            (stage / "docs" / "ai4s" / "index.html").write_text("mutated", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed"):
                deploy._load_sealed_scope("ai4s", stage, manifest, target, "docs/ai4s")

    def test_execute_grammar_is_rejected_without_any_effect_path(self):
        stderr = io.StringIO()
        argv = [
            "prepare_deploy.py",
            "--topic",
            "ai4s",
            "--execute",
            "--staging",
            "/tmp/stage",
            "--manifest",
            "/tmp/manifest.json",
            "--target",
            "/tmp/wrangler.toml",
            "--pathspec",
            "docs/ai4s",
        ]
        with patch.object(sys, "argv", argv), redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                deploy.main()
        self.assertIn("unrecognized arguments", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
