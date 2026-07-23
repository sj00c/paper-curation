import json
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PIPELINE = Path(__file__).resolve().parents[1]
ROOT = PIPELINE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))
from pipeline.lib import search_index_metadata as meta  # noqa: E402

import run_update_force as ruf  # noqa: E402


class RunUpdateForceSmokeTests(unittest.TestCase):
    def test_smoke_index_candidates_prefer_existing_index_pdf_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            papers = Path(temp_dir) / "papers"
            papers.mkdir()
            pdf = Path(temp_dir) / "paper.pdf"
            pdf.write_bytes(b"%PDF-1.4\n")
            (papers / "_papers_index.json").write_text(json.dumps([
                {
                    "slug": "000_Key_Only",
                    "title": "Key Only",
                    "topics": ["ai4s"],
                    "zotero_item_key": "KEYONLY",
                },
                {
                    "slug": "001_Test_Paper",
                    "title": "Test Paper",
                    "topics": ["ai4s"],
                    "zotero_item_key": "",
                    "pdf_path": str(pdf),
                },
            ]), encoding="utf-8")

            with patch.object(ruf, "PAPERS_DIR", str(papers)):
                candidates = ruf._smoke_candidates_from_index("ai4s", 1)

            self.assertEqual(len(candidates), 1)
            self.assertEqual(candidates[0][0]["pdf_path"], str(pdf))
            self.assertEqual(candidates[0][1], "001_Test_Paper")

    def test_zotero_smoke_sample_oversamples_past_untitled_first_records(self):
        payload = [
            {"data": {"key": "UNTITLED1", "itemType": "document", "title": ""}},
            {"data": {"key": "UNTITLED2", "itemType": "document"}},
            {
                "data": {
                    "key": "VALID1",
                    "itemType": "journalArticle",
                    "title": "Physical AI Later Paper",
                }
            },
        ]

        class FakeResponse(io.StringIO):
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(req, timeout=0, context=None):
            self.assertIn("limit=25", req.full_url)
            self.assertIn("start=0", req.full_url)
            return FakeResponse(json.dumps(payload))

        with patch.object(ruf.urllib.request, "urlopen", side_effect=fake_urlopen):
            items = ruf._fetch_zotero_items_sample("PHYSICALAI", 1)

        candidates, duplicates, skipped = ruf._map_items_to_slugs(items, [], {})
        self.assertEqual([item["key"] for item in items], ["VALID1"])
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0][0]["title"], "Physical AI Later Paper")
        self.assertEqual(duplicates, 0)
        self.assertEqual(skipped, 0)

    def test_smoke_writes_only_under_smoke_root_and_suppresses_deploy(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            production_papers = root / "docs" / "papers"
            production_papers.mkdir(parents=True)
            pdf = root / "paper.pdf"
            pdf.write_bytes(b"%PDF-1.4\n")
            (production_papers / "_papers_index.json").write_text(json.dumps([
                {
                    "slug": "001_Test_Paper",
                    "title": "Test Paper",
                    "topics": ["ai4s"],
                    "pdf_path": str(pdf),
                }
            ]), encoding="utf-8")
            smoke_base = root / "pipeline"
            smoke_base.mkdir()
            args = SimpleNamespace(topic="ai4s", smoke_limit=1)

            def fake_process(item, slug, cp):
                Path(ruf.PAPERS_DIR, slug).mkdir(parents=True)
                Path(ruf.PAPERS_DIR, slug, "review.md").write_text("ok", encoding="utf-8")
                cp["completed"].append(slug)
                ruf.save_checkpoint(cp)
                return "ok"

            with (
                patch.dict(os.environ, {}, clear=True),
                patch.object(ruf, "PAPERS_DIR", str(production_papers)),
                patch.object(ruf, "PIPELINE_DIR", smoke_base),
                patch.object(ruf, "_slug_to_zotero_key", {"existing": "KEY"}),
                patch.object(ruf, "_slug_to_pdf_path", {"existing": "/existing.pdf"}),
                patch.object(ruf, "process_paper", side_effect=fake_process),
                patch.object(ruf.subprocess, "run") as subprocess_run,
            ):
                ruf._run_smoke(args, SimpleNamespace(mode="oauth", source="saved:/login"))
                self.assertNotIn("PAPER_CURATION_NO_DEPLOY", os.environ)
                self.assertEqual(ruf._slug_to_zotero_key, {"existing": "KEY"})
                self.assertEqual(ruf._slug_to_pdf_path, {"existing": "/existing.pdf"})
                subprocess_run.assert_not_called()

            reports = list((smoke_base / "_smoke" / "ai4s").glob("*/report.json"))
            self.assertEqual(len(reports), 1)
            report = json.loads(reports[0].read_text(encoding="utf-8"))
            scratch_root = Path(report["scratch_root"])
            self.assertTrue((scratch_root / "papers" / "001_Test_Paper" / "review.md").exists())
            self.assertTrue((scratch_root / "checkpoint.json").exists())
            self.assertFalse((production_papers / "001_Test_Paper").exists())
            self.assertEqual(report["deploy"]["status"], "suppressed")
            self.assertEqual(report["auth"], {"mode": "oauth", "source": "saved:/login"})
            self.assertEqual(report["attempted"][0]["pdf"]["status"], "found")
            self.assertEqual(report["post_processing"]["status"], "skipped")

    def test_new_topic_smoke_scans_beyond_first_candidate_for_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            production_papers = root / "docs" / "papers"
            production_papers.mkdir(parents=True)
            (production_papers / "_papers_index.json").write_text("[]", encoding="utf-8")
            smoke_base = root / "pipeline"
            smoke_base.mkdir()
            pdf = root / "later.pdf"
            pdf.write_bytes(b"%PDF-1.4\n")
            args = SimpleNamespace(topic="robotics-lab", smoke_limit=1)
            items = [
                {"key": "NO_PDF", "title": "First Candidate", "itemType": "journalArticle"},
                {"key": "HAS_PDF", "title": "Later Candidate", "itemType": "journalArticle"},
            ]

            def fake_process(item, slug, cp):
                cp["completed"].append(slug)
                return "ok"

            with (
                patch.object(ruf, "PAPERS_DIR", str(production_papers)),
                patch.object(ruf, "PIPELINE_DIR", smoke_base),
                patch.object(ruf, "COLLECTIONS", {"robotics-lab": "COLLKEY"}),
                patch.object(ruf, "_fetch_zotero_items_sample", return_value=items) as fetch,
                patch.object(
                    ruf,
                    "find_pdf",
                    side_effect=[("", "no_match"), (str(pdf), "index_pdf_path")],
                ),
                patch.object(ruf, "process_paper", side_effect=fake_process),
            ):
                ruf._run_smoke(args, SimpleNamespace(mode="oauth", source="saved:/login"))

            fetch.assert_called_once_with("COLLKEY", 25)
            report_path = next(
                (smoke_base / "_smoke" / "robotics-lab").glob("*/report.json")
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "ok")
            self.assertEqual(report["candidate_count"], 2)
            self.assertEqual(report["candidate_attempt_limit"], 10)
            self.assertEqual([attempt["result"] for attempt in report["attempted"]], ["no_pdf", "ok"])



    def test_smoke_no_pdf_emits_nonzero_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            production_papers = root / "docs" / "papers"
            production_papers.mkdir(parents=True)
            (production_papers / "_papers_index.json").write_text(json.dumps([
                {"slug": "001_No_Pdf", "title": "No PDF", "topics": ["ai4s"], "zotero_item_key": "KEY"}
            ]), encoding="utf-8")
            smoke_base = root / "pipeline"
            smoke_base.mkdir()
            args = SimpleNamespace(topic="ai4s", smoke_limit=1)

            with (
                patch.object(ruf, "PAPERS_DIR", str(production_papers)),
                patch.object(ruf, "PIPELINE_DIR", smoke_base),
                patch.object(ruf, "find_pdf", return_value=("", "no_match")),
                patch.object(ruf, "MAX_RETRIES", 1),
            ):
                with self.assertRaises(SystemExit) as raised:
                    ruf._run_smoke(
                        args, SimpleNamespace(mode="oauth", source="saved:/login")
                    )

            self.assertEqual(raised.exception.code, 2)
            report_path = next((smoke_base / "_smoke" / "ai4s").glob("*/report.json"))
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "no_smokeable_pdf")
            self.assertIn("Attach at least one PDF", report["remediation"])


    def test_candidate_fetch_failure_writes_scratch_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            production_papers = root / "docs" / "papers"
            production_papers.mkdir(parents=True)
            (production_papers / "_papers_index.json").write_text(
                "[]", encoding="utf-8"
            )
            smoke_base = root / "pipeline"
            smoke_base.mkdir()
            args = SimpleNamespace(topic="ai4s", smoke_limit=1)

            with (
                patch.object(ruf, "PAPERS_DIR", str(production_papers)),
                patch.object(ruf, "PIPELINE_DIR", smoke_base),
                patch.object(ruf, "COLLECTIONS", {"ai4s": "COLLKEY"}),
                patch.object(
                    ruf,
                    "_fetch_zotero_items_sample",
                    side_effect=TimeoutError("network timeout"),
                ),
            ):
                with self.assertRaises(SystemExit) as raised:
                    ruf._run_smoke(
                        args, SimpleNamespace(mode="oauth", source="saved:/login")
                    )

            self.assertEqual(raised.exception.code, 2)
            report_path = next(
                (smoke_base / "_smoke" / "ai4s").glob("*/report.json")
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "candidate_fetch_failed")
            self.assertEqual(report["error_type"], "TimeoutError")
            self.assertEqual(report["deploy"]["status"], "suppressed")
            self.assertEqual(report["post_processing"]["status"], "skipped")

    def test_vector_rebuild_controls_report_mismatch_without_building(self):
        cases = [
            ("dry-run", SimpleNamespace(no_deploy=False, dry_run=True, mode="curate"), {}),
            ("smoke", SimpleNamespace(no_deploy=True, dry_run=False, mode="smoke"), {}),
            (
                "explicit env",
                SimpleNamespace(no_deploy=False, dry_run=False, mode="curate"),
                {"PAPER_CURATION_NO_VECTOR_REBUILD": "1"},
            ),
        ]
        for _label, args, env in cases:
            with self.subTest(_label), tempfile.TemporaryDirectory() as temp_dir:
                topic_dir = Path(temp_dir) / "topic"
                topic_dir.mkdir()
                (topic_dir / "_search_index.json").write_text(json.dumps({
                    **meta.current_index_metadata(),
                    "embedding_provider": "other",
                    "count": 0,
                    "papers": {},
                    "chunks": [],
                }), encoding="utf-8")
                calls = []

                with (
                    patch.dict(os.environ, env, clear=True),
                    patch.object(ruf, "get_topic_dir", return_value=topic_dir),
                    patch.object(ruf, "log") as log,
                ):
                    status = ruf._postprocess_search_index(
                        args,
                        "ai4s",
                        lambda *call: calls.append(call),
                    )

                self.assertEqual(status, "suppressed")
                self.assertEqual([call[0] for call in calls], ["cleanup"])
                self.assertTrue(any("metadata is incompatible" in call.args[0] for call in log.call_args_list))
                self.assertFalse(any("build_search_index" == call[0] for call in calls))

    def test_no_deploy_search_index_postprocess_still_builds_locally(self):
        cases = [
            (
                "flag",
                SimpleNamespace(no_deploy=True, dry_run=False, mode="curate"),
                {},
            ),
            (
                "env",
                SimpleNamespace(no_deploy=False, dry_run=False, mode="curate"),
                {"PAPER_CURATION_NO_DEPLOY": "1"},
            ),
        ]
        for _label, args, env in cases:
            with self.subTest(_label):
                calls = []

                with patch.dict(os.environ, env, clear=True):
                    status = ruf._postprocess_search_index(
                        args,
                        "ai4s",
                        lambda *call: calls.append(call),
                    )

                self.assertEqual(status, "built")
                self.assertEqual([call[0] for call in calls], ["cleanup", "build_search_index"])
                self.assertIn("pipeline/build_search_index.py", calls[1][1])

    def test_production_search_index_postprocess_remains_possible(self):
        cases = [
            ("default", {}),
            ("vector env disabled value", {"PAPER_CURATION_NO_VECTOR_REBUILD": "0"}),
        ]
        for _label, env in cases:
            with self.subTest(_label):
                calls = []

                with patch.dict(os.environ, env, clear=True):
                    status = ruf._postprocess_search_index(
                        SimpleNamespace(no_deploy=False),
                        "ai4s",
                        lambda *call: calls.append(call),
                    )

                self.assertEqual(status, "built")
                self.assertEqual([call[0] for call in calls], ["cleanup", "build_search_index"])
                self.assertIn("pipeline/build_search_index.py", calls[1][1])

    def test_dry_run_main_never_invokes_search_index_entrypoint(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            papers = Path(temp_dir) / "papers"
            papers.mkdir()
            argv = [
                "run_update_force.py",
                "--topic", "ai4s",
                "--mode", "curate",
                "--dry-run",
            ]
            with (
                patch.object(sys, "argv", argv),
                patch.object(ruf, "PAPERS_DIR", str(papers)),
                patch.object(ruf, "CHECKPOINT_FILE", str(Path(temp_dir) / "checkpoint.json")),
                patch.object(ruf, "COLLECTIONS", {"ai4s": "COLLKEY"}),
                patch.object(ruf, "fetch_zotero_items", return_value=[]),
                patch.object(ruf.subprocess, "run") as subprocess_run,
            ):
                ruf.main()

            subprocess_run.assert_not_called()

    def test_smoke_auth_failure_does_not_leak_no_deploy_env(self):
        argv = [
            "run_update_force.py",
            "--topic", "ai4s",
            "--mode", "smoke",
            "--skip-dedup",
        ]
        with (
            patch.dict(os.environ, {}, clear=True),
            patch.object(sys, "argv", argv),
            patch.object(
                ruf,
                "require_auth_ready",
                side_effect=ruf.AnthropicAuthError("not logged in"),
            ),
        ):
            with self.assertRaises(SystemExit):
                ruf.main()
            self.assertNotIn("PAPER_CURATION_NO_DEPLOY", os.environ)

if __name__ == "__main__":
    unittest.main()
