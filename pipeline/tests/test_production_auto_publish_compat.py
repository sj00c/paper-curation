import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import run_full  # noqa: E402
import run_update_force as ruf  # noqa: E402


class ProductionAutoPublishCompatTests(unittest.TestCase):
    def test_curate_dry_run_still_allows_child_auto_publish(self):
        argv = ["run_full.py", "--topic", "ai4s", "--mode", "curate", "--dry-run", "--no-sync"]
        out = io.StringIO()
        with patch.object(sys, "argv", argv), redirect_stdout(out):
            run_full.main()

        text = out.getvalue()
        self.assertIn("AUTO-PUBLISH-POSSIBLE", text)
        self.assertIn("deploy_state=AUTO-PUBLISH-POSSIBLE", text)
        self.assertIn("run_update_force.py", text)
        self.assertNotIn("--no-deploy", text)
        self.assertNotIn("PAPER_CURATION_NO_DEPLOY", text)

    def test_production_branch_invokes_prepare_deploy_push(self):
        completed = SimpleNamespace(returncode=0, stderr="")
        env = {
            "CLOUDFLARE_API_TOKEN": "test-token",
            "CLOUDFLARE_ACCOUNT_ID": "test-account",
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(ruf.subprocess, "run", return_value=completed) as run,
        ):
            status = ruf._maybe_auto_deploy(
                SimpleNamespace(no_deploy=False), "ai4s"
            )

        self.assertEqual(status, "deployed")
        command = run.call_args.args[0]
        self.assertEqual(
            command,
            ["python", "pipeline/prepare_deploy.py", "--topic", "ai4s", "--push"],
        )

    def test_production_deploy_failure_is_not_masked(self):
        completed = SimpleNamespace(returncode=7, stderr="deploy failed")
        env = {
            "CLOUDFLARE_API_TOKEN": "test-token",
            "CLOUDFLARE_ACCOUNT_ID": "test-account",
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(ruf.subprocess, "run", return_value=completed),
        ):
            with self.assertRaisesRegex(RuntimeError, "exit 7"):
                ruf._maybe_auto_deploy(
                    SimpleNamespace(no_deploy=False), "ai4s"
                )

    def test_deploy_suppression_blocks_publish_even_with_credentials(self):
        cases = [
            (
                "flag",
                SimpleNamespace(no_deploy=True),
                {
                    "CLOUDFLARE_API_TOKEN": "test-token",
                    "CLOUDFLARE_ACCOUNT_ID": "test-account",
                },
            ),
            (
                "env",
                SimpleNamespace(no_deploy=False),
                {
                    "CLOUDFLARE_API_TOKEN": "test-token",
                    "CLOUDFLARE_ACCOUNT_ID": "test-account",
                    "PAPER_CURATION_NO_DEPLOY": "1",
                },
            ),
        ]
        for _label, args, env in cases:
            with self.subTest(_label):
                with (
                    patch.dict(os.environ, env, clear=True),
                    patch.object(ruf.subprocess, "run") as run,
                ):
                    status = ruf._maybe_auto_deploy(args, "ai4s")

                self.assertEqual(status, "suppressed")
                run.assert_not_called()

    def test_explicit_deploy_mode_still_invokes_prepare_deploy_push(self):
        argv = ["run_full.py", "--topic", "ai4s", "--mode", "deploy", "--dry-run"]
        out = io.StringIO()
        with patch.object(sys, "argv", argv), redirect_stdout(out):
            run_full.main()

        text = out.getvalue()
        self.assertIn("prepare_deploy.py", text)
        self.assertIn("--push", text)
        self.assertIn("deploy_state=EXPLICIT-DEPLOY", text)
        self.assertNotIn("AUTO-PUBLISH-POSSIBLE", text)

    def test_deploy_mode_rejects_no_deploy_suppression(self):
        argv = ["run_full.py", "--topic", "ai4s", "--mode", "deploy", "--no-deploy"]
        with patch.object(sys, "argv", argv):
            with self.assertRaises(SystemExit):
                run_full.main()


if __name__ == "__main__":
    unittest.main()
