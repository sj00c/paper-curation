import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import prepare_deploy  # noqa: E402


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PrepareDeployScopeTests(unittest.TestCase):
    def make_scope(self, root, *, include_extra=False):
        topic = "robotics-lab"
        topic_dir = root / "docs" / topic
        topic_dir.mkdir(parents=True)
        index = topic_dir / "index.html"
        index.write_text("ok", encoding="utf-8")
        target = root / "wrangler.toml"
        target.write_text("name='synthetic'", encoding="utf-8")
        files = {
            "docs/robotics-lab/index.html": digest(index),
            "wrangler.toml": digest(target),
        }
        if include_extra:
            extra = root / "docs" / "historical-local" / "index.html"
            extra.parent.mkdir(parents=True)
            extra.write_text("unexpected", encoding="utf-8")
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({
            "topic": topic,
            "pathspec": "docs/robotics-lab",
            "target": "wrangler.toml",
            "files": files,
        }), encoding="utf-8")
        return topic, manifest, target

    def test_unrequested_topic_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            topic, manifest, target = self.make_scope(root, include_extra=True)
            with self.assertRaisesRegex(ValueError, "file set mismatch"):
                prepare_deploy._load_sealed_scope(
                    topic, root, manifest, target, "docs/robotics-lab"
                )

    def test_manifest_cannot_authorize_files_outside_exact_topic_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            topic, manifest, target = self.make_scope(root)
            outside = root / "docs" / "other-topic" / "index.html"
            outside.parent.mkdir(parents=True)
            outside.write_text("not authorized", encoding="utf-8")
            document = json.loads(manifest.read_text(encoding="utf-8"))
            document["files"]["docs/other-topic/index.html"] = digest(outside)
            manifest.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside the exact topic"):
                prepare_deploy._load_sealed_scope(
                    topic, root, manifest, target, "docs/robotics-lab"
                )
    def test_exact_manifest_file_set_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            topic, manifest, target = self.make_scope(root)
            staging, sealed_manifest, sealed_target, document = prepare_deploy._load_sealed_scope(
                topic, root, manifest, target, "docs/robotics-lab"
            )
            self.assertEqual(staging, root.resolve())
            self.assertEqual(sealed_manifest, manifest.resolve())
            self.assertEqual(sealed_target, target.resolve())
            self.assertEqual(document["topic"], topic)


if __name__ == "__main__":
    unittest.main()
