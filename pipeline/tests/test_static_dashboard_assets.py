import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

from lib.static_assets import (  # noqa: E402
    LOCAL_DASHBOARD_ASSETS,
    local_asset_headers,
    manifest_records,
    verify_manifest_closure,
)


class StaticDashboardAssetTests(unittest.TestCase):
    def test_manifest_is_exact_and_content_addressed(self):
        verify_manifest_closure(ROOT)
        records = manifest_records()
        self.assertEqual([record["path"] for record in records], sorted(LOCAL_DASHBOARD_ASSETS))
        for record in records:
            content = (ROOT / record["path"]).read_bytes()
            self.assertEqual(record["byte_length"], len(content))
            self.assertEqual(record["sha256"], hashlib.sha256(content).hexdigest())
            self.assertEqual(record["spdx"], "MIT")
            self.assertEqual(record["source"], "owned-local-dashboard")

    def test_manifest_rejects_missing_extra_and_traversing_paths(self):
        expected = list(LOCAL_DASHBOARD_ASSETS)
        with self.assertRaisesRegex(ValueError, "missing"):
            verify_manifest_closure(ROOT, expected[:-1])
        with self.assertRaisesRegex(ValueError, "extra"):
            verify_manifest_closure(ROOT, expected + ["docs/public/untracked.js"])
        with self.assertRaises(ValueError):
            local_asset_headers("../docs/public/paper-curation-local.js")

    def test_manifest_rejects_symlinked_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in LOCAL_DASHBOARD_ASSETS:
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, destination)
            js_path = root / "docs/public/paper-curation-local.js"
            target = root / "owned.js"
            target.write_bytes(js_path.read_bytes())
            js_path.unlink()
            js_path.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "symlink"):
                verify_manifest_closure(root)

    def test_asset_headers_are_fixed_and_safe(self):
        for path in LOCAL_DASHBOARD_ASSETS:
            headers = local_asset_headers(path)
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
            self.assertTrue(headers["Content-Type"].startswith(("text/css", "text/javascript")))

    def test_local_assets_are_offline_and_only_use_local_action_endpoints(self):
        js = (ROOT / "docs/public/paper-curation-local.js").read_text(encoding="utf-8")
        css = (ROOT / "docs/public/paper-curation-local.css").read_text(encoding="utf-8")
        self.assertNotIn("http://", js + css)
        self.assertNotIn("https://", js + css)
        self.assertIn("AudioCapabilityV1", js)
        self.assertIn("/api/action/", js)
        self.assertNotIn("import ", css)
        self.assertNotIn("@import", css)

    def test_builder_only_emits_external_local_assets_and_safe_bootstrap_contract(self):
        source = (ROOT / "pipeline/build_topic_index.py").read_text(encoding="utf-8")
        js = (ROOT / "docs/public/paper-curation-local.js").read_text(encoding="utf-8")
        self.assertIn('href="../public/paper-curation-local.css"', source)
        self.assertIn('src="../public/paper-curation-local.js" defer', source)
        self.assertNotIn("<script>", source)
        self.assertNotIn("onclick=", source)
        self.assertNotIn("onload=", source)
        self.assertNotIn("cdn.jsdelivr.net", source)
        self.assertIn(r'replace("<", "\\u003c")', source)
        self.assertIn(r'replace("&", "\\u0026")', source)
        self.assertIn('replace("\\u2028", "\\\\u2028")', source)
        self.assertIn('replace("\\u2029", "\\\\u2029")', source)
        self.assertIn('"schema": "AudioCapabilityV1", "state": "UNAVAILABLE"', source)
        self.assertIn('id="deep-normal"', source)
        self.assertIn('id="deep-deeper"', source)
        self.assertIn("button.hidden = !enabled", js)


if __name__ == "__main__":
    unittest.main()
