"""Focused tests for first-run doctor artifact reporting."""
import io
from contextlib import redirect_stdout

import sys
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import MagicMock, patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import doctor as doctor_module  # noqa: E402


class DoctorFirstRunTests(unittest.TestCase):
    def test_missing_topic_directory_is_warning_before_first_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            reporter = doctor_module.Reporter()
            output = io.StringIO()
            with (
                patch.object(doctor_module, "DOCS_DIR", root / "docs"),
                patch.object(
                    doctor_module,
                    "PAPERS_INDEX",
                    root / "docs" / "papers" / "_papers_index.json",
                ),
                redirect_stdout(output),
            ):
                doctor_module.check_topic(
                    reporter,
                    "ai4s",
                    {"zotero": {"collections": {"ai4s": "AI for Science"}}},
                    None,
                )

        self.assertEqual(reporter.fails, 0)
        self.assertEqual(reporter.warns, 1)
        self.assertIn("PAPER_CURATION_NO_DEPLOY=1", output.getvalue())
        self.assertIn("--no-deploy", output.getvalue())

    def test_missing_topic_directory_fails_after_index_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            papers_index = root / "docs" / "papers" / "_papers_index.json"
            papers_index.parent.mkdir(parents=True)
            papers_index.write_text("[]", encoding="utf-8")
            reporter = doctor_module.Reporter()
            output = io.StringIO()
            with (
                patch.object(doctor_module, "DOCS_DIR", root / "docs"),
                patch.object(doctor_module, "PAPERS_INDEX", papers_index),
                redirect_stdout(output),
            ):
                doctor_module.check_topic(
                    reporter,
                    "ai4s",
                    {"zotero": {"collections": {"ai4s": "AI for Science"}}},
                    [],
                )

        self.assertEqual(reporter.fails, 1)
        self.assertEqual(reporter.warns, 0)
        self.assertIn("PAPER_CURATION_NO_DEPLOY=1", output.getvalue())
        self.assertIn("--no-deploy", output.getvalue())

    def test_normal_doctor_does_not_run_anthropic_smoke(self):
        reporter = doctor_module.Reporter()
        status = SimpleNamespace(
            mode="api-key",
            source="env:ANTHROPIC_API_KEY",
            ready=True,
            detail="API key configured",
        )
        smoke = MagicMock(return_value={
            "mode": "api-key",
            "source": "env:ANTHROPIC_API_KEY",
            "ready": True,
            "detail": "API key configured",
            "smoke": "ok",
        })

        with (
            patch.object(doctor_module, "auth_status", return_value=status),
            patch.object(doctor_module, "run_structured_smoke", smoke),
        ):
            doctor_module.check_api_keys(
                reporter,
                {"google_api_key": "set", "anthropic_api_key": "set"},
                anthropic_smoke=False,
            )

        smoke.assert_not_called()

    def test_anthropic_smoke_opt_in_uses_selected_mode(self):
        reporter = doctor_module.Reporter()
        status = SimpleNamespace(
            mode="oauth",
            source="env:CLAUDE_CODE_OAUTH_TOKEN",
            ready=True,
            detail="long-lived OAuth token configured",
        )
        smoke = MagicMock(return_value={
            "mode": "oauth",
            "source": "env:CLAUDE_CODE_OAUTH_TOKEN",
            "ready": True,
            "detail": "long-lived OAuth token configured",
            "smoke": "ok",
        })

        with (
            patch.object(doctor_module, "auth_status", return_value=status),
            patch.object(doctor_module, "claude_version", return_value=doctor_module.MIN_CLAUDE_CODE_VERSION),
            patch.object(doctor_module, "run_structured_smoke", smoke),
        ):
            doctor_module.check_api_keys(
                reporter,
                {"google_api_key": "set", "anthropic_auth": {"mode": "oauth"}},
                anthropic_smoke=True,
            )

        smoke.assert_called_once_with("oauth")
        self.assertGreaterEqual(reporter.oks, 2)

    def test_anthropic_smoke_failure_is_required_failure(self):
        reporter = doctor_module.Reporter()
        secret = "sk-ant-secret-that-must-not-leak"
        status = SimpleNamespace(
            mode="api-key",
            source="env:ANTHROPIC_API_KEY",
            ready=True,
            detail="API key configured",
        )
        output = io.StringIO()

        with (
            patch.object(doctor_module, "auth_status", return_value=status),
            patch.object(doctor_module, "run_structured_smoke", return_value={
                "mode": "api-key",
                "source": "env:ANTHROPIC_API_KEY",
                "ready": True,
                "detail": "API key configured",
                "smoke": "failed",
                "error": f"metered call failed for {secret}",
            }),
            patch.dict(doctor_module.os.environ, {"ANTHROPIC_API_KEY": secret}),
            redirect_stdout(output),
        ):
            doctor_module.check_api_keys(
                reporter,
                {"google_api_key": "set", "anthropic_api_key": "set"},
                anthropic_smoke=True,
            )

        self.assertGreaterEqual(reporter.fails, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("<redacted:ANTHROPIC_API_KEY>", output.getvalue())


if __name__ == "__main__":
    unittest.main()
