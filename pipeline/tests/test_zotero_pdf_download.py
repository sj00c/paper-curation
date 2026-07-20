"""Focused no-network tests for Zotero Storage PDF cache downloads."""

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402

with (
    patch.object(config_loader, "get_zotero_api_key", return_value="test-key"),
    patch.object(config_loader, "get_zotero_user_id", return_value="123"),
    patch.object(config_loader, "get_zotero_dir", return_value="/tmp/paper-curation-test-cache"),
    patch.object(config_loader, "get_collections", return_value={}),
):
    import run_update_force as update  # noqa: E402

download_zotero_attachment = getattr(update, "_download_zotero_attachment")
opendataloader_ready = getattr(update, "_opendataloader_ready")


class FakeResponse(io.BytesIO):
    pass


class ZoteroPdfDownloadTests(unittest.TestCase):
    def test_synced_attachment_downloads_into_generated_cache(self):
        pdf = b"%PDF-1.7\n" + (b"0" * 2048)
        child = {
            "key": "ATTACH01",
            "data": {
                "itemType": "attachment",
                "contentType": "application/pdf",
                "filename": "Paper.pdf",
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(update, "API_KEY", "zotero-key"),
                patch.object(update, "USER_ID", "123"),
                patch.object(update, "ZOTERO_DIR", temp_dir),
                patch.object(
                    update.urllib.request,
                    "urlopen",
                    return_value=FakeResponse(pdf),
                ) as urlopen,
            ):
                result = download_zotero_attachment(child, "Paper")

            output = Path(result)
            self.assertEqual(output.parent, Path(temp_dir))
            self.assertEqual(output.name, "Paper.pdf")
            self.assertEqual(output.read_bytes(), pdf)
            request = urlopen.call_args.args[0]
            self.assertEqual(
                request.full_url,
                "https://api.zotero.org/users/123/items/ATTACH01/file",
            )
            self.assertEqual(request.get_header("Zotero-api-key"), "zotero-key")

    def test_metadata_only_item_recovers_open_access_pdf(self):
        pdf = b"%PDF-1.7\n" + (b"0" * 2048)
        item = {
            "key": "ITEM01",
            "title": "Metadata-only scientific paper",
            "DOI": "10.1000/example",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "Recovered.pdf"

            def fake_download(received, destination):
                self.assertEqual(received, item)
                self.assertEqual(destination, temp_dir)
                output.write_bytes(pdf)
                return str(output), ""

            fake_register = SimpleNamespace(download_pdf=fake_download)
            with (
                patch.object(update, "ZOTERO_DIR", temp_dir),
                patch.object(
                    update.urllib.request,
                    "urlopen",
                    return_value=FakeResponse(b"[]"),
                ),
                patch.dict(sys.modules, {"register_zotero": fake_register}),
                patch.object(update, "_audit_append"),
            ):
                path, method = update.find_pdf(item)

        self.assertEqual(path, str(output))
        self.assertEqual(method, "metadata_oa_download")
    def test_title_addressed_oa_cache_precedes_network_lookup(self):
        item = {
            "key": "CACHED01",
            "title": "Cached scientific paper",
            "DOI": "10.1000/cached",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(update, "ZOTERO_DIR", temp_dir):
                from register_zotero import safe_filename

                cached = Path(temp_dir) / (
                    safe_filename(item["title"]) + ".pdf"
                )
                cached.write_bytes(b"%PDF-1.7\n" + (b"0" * 6000))
                with (
                    patch.object(
                        update.urllib.request,
                        "urlopen",
                        side_effect=AssertionError("network lookup was attempted"),
                    ),
                    patch.object(update, "_audit_append"),
                ):
                    path, method = update.find_pdf(item)

        self.assertEqual(path, str(cached))
        self.assertEqual(method, "metadata_oa_cache")

    def test_missing_pdf_does_not_create_empty_paper_directory(self):
        checkpoint = {"completed": [], "failed": []}
        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(update, "PAPERS_DIR", temp_dir),
                patch.object(update, "find_pdf", return_value=(None, "no_match")),
                patch.object(update, "save_checkpoint"),
            ):
                status = update.process_paper(
                    {"key": "ITEM02", "title": "Unavailable paper"},
                    "001_Unavailable_paper",
                    checkpoint,
                )

            self.assertEqual(status, "no_pdf")
            self.assertFalse((Path(temp_dir) / "001_Unavailable_paper").exists())
            self.assertEqual(
                checkpoint["failed"],
                [{
                    "key": "ITEM02",
                    "slug": "001_Unavailable_paper",
                    "reason": "no_pdf:no_match",
                }],
            )
    def test_pdf_lookup_uses_wall_clock_deadline(self):
        release = update.threading.Event()

        def stuck_lookup(_item):
            release.wait(2)
            return None, "late"

        try:
            with (
                patch.dict(
                    os.environ,
                    {"PAPER_CURATION_PDF_LOOKUP_TIMEOUT": "1"},
                ),
                patch.object(update, "find_pdf", side_effect=stuck_lookup),
                patch.object(update.time, "time", side_effect=[100.0, 200.0]),
                patch.object(update, "_audit_append") as audit,
            ):
                result = update._find_pdf_with_wall_deadline({
                    "key": "SUSPENDED",
                    "title": "Suspend-stale lookup",
                })
        finally:
            release.set()

        self.assertEqual(result, (None, "timeout"))
        self.assertEqual(
            audit.call_args.args[0]["method"],
            "metadata_pdf_lookup_timeout",
        )

    def test_terminal_failures_are_preserved_by_reason(self):
        self.assertTrue(update._is_terminal_failure({
            "reason": "no_pdf:no_match",
        }))
        self.assertTrue(update._is_terminal_failure({
            "reason": "sanity_mismatch:title_hits=1/4",
        }))
        self.assertFalse(update._is_terminal_failure({
            "reason": "oauth_timeout",
        }))

    def test_broken_macos_java_launcher_is_cached_as_unavailable(self):
        with (
            patch.object(update, "_OPENDATALOADER_READY", None),
            patch.object(update.shutil, "which", return_value="/usr/bin/java"),
            patch.object(
                update.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=1),
            ) as run,
            patch.object(update, "log"),
        ):
            self.assertFalse(opendataloader_ready())
            self.assertFalse(opendataloader_ready())

        run.assert_called_once()

    def test_sanity_check_scans_beyond_first_six_thousand_characters(self):
        item = {
            "title": "Modeling biomedical graduate student career development",
            "creators": [{"lastName": "Svenson"}],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            text_path = Path(temp_dir) / "text.md"
            text_path.write_text(
                ("unrelated proceedings content " * 300)
                + "\nModeling biomedical graduate student career development\n"
                + "Emma Svenson",
                encoding="utf-8",
            )

            passed, reason = update._zotero_text_sanity(item, str(text_path))

        self.assertTrue(passed, reason)
        self.assertIn("title 6/6", reason)

    def test_oauth_limit_preserves_pipeline_worker_concurrency(self):
        with (
            patch.dict(os.environ, {"PAPER_CURATION_OAUTH_CONCURRENCY": "3"}),
            patch.object(update.threading, "BoundedSemaphore") as semaphore,
            patch.object(update, "log") as log,
            patch.object(update, "_oauth_call_limiter", None),
        ):
            limit = update._configure_oauth_call_limiter("oauth", 16)

        self.assertEqual(limit, 3)
        semaphore.assert_called_once_with(3)
        self.assertIn("pipeline workers remain 16", log.call_args.args[0])

    def test_model_call_runs_inside_oauth_limiter(self):
        limiter = MagicMock()
        call = MagicMock(return_value="response")
        with patch.object(update, "_oauth_call_limiter", limiter):
            result = update._run_oauth_limited(call)

        self.assertEqual(result, "response")
        limiter.__enter__.assert_called_once_with()
        limiter.__exit__.assert_called_once()
        call.assert_called_once_with()

    def test_invalid_download_is_removed(self):
        child = {"key": "ATTACH02", "data": {"filename": "Bad.pdf"}}
        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(update, "API_KEY", "zotero-key"),
                patch.object(update, "USER_ID", "123"),
                patch.object(update, "ZOTERO_DIR", temp_dir),
                patch.object(
                    update.urllib.request,
                    "urlopen",
                    return_value=FakeResponse(b"not a pdf"),
                ),
                patch.object(update, "_audit_append"),
            ):
                result = download_zotero_attachment(child, "Bad")

            self.assertEqual(result, "")
            self.assertFalse((Path(temp_dir) / "Bad.pdf").exists())
            self.assertFalse((Path(temp_dir) / "Bad.pdf.part").exists())


if __name__ == "__main__":
    unittest.main()
