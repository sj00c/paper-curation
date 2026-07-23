import io
import os
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import run_full  # noqa: E402


class RunFullSmokeTests(unittest.TestCase):
    def parse(self, argv):
        parser = run_full.build_parser()
        args = parser.parse_args(argv)
        run_full.validate_args(parser, args)
        return args

    def test_smoke_constructs_no_deploy_scratch_child_command(self):
        args = self.parse(["--topic", "ai4s", "--mode", "smoke", "--smoke-limit", "3"])
        cmd = run_full.build_update_force_cmd(args, run_full.resolve_images_default(args))

        self.assertIn("--mode", cmd)
        self.assertIn("smoke", cmd)
        self.assertIn("--smoke-limit", cmd)
        self.assertIn("3", cmd)
        self.assertIn("--no-deploy", cmd)
        self.assertIn("--skip-dedup", cmd)
        self.assertEqual(args.images, "skip")
        self.assertTrue(args.no_deploy)
        self.assertTrue(args.no_validate)

    def test_smoke_rejects_deploy_capable_options(self):
        with self.assertRaises(SystemExit):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.parse(["--topic", "ai4s", "--mode", "smoke", "--source", "web"])

        with self.assertRaises(SystemExit):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.parse(["--topic", "ai4s", "--mode", "smoke", "--dedup-execute"])

    def test_deploy_rejects_no_deploy(self):
        with self.assertRaises(SystemExit):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                self.parse([
                    "--topic", "ai4s", "--mode", "deploy", "--no-deploy",
                ])

    def test_production_curate_does_not_force_no_deploy(self):
        calls = []

        def fake_run(cmd, timeout=None, env=None):
            calls.append((cmd, env))
            return 0

        argv = [
            "run_full.py",
            "--topic", "ai4s",
            "--mode", "curate",
            "--source", "zotero",
            "--no-sync",
            "--no-validate",
        ]
        with (
            patch.dict(os.environ, {}, clear=True),
            patch.object(sys, "argv", argv),
            patch.object(run_full, "run", side_effect=fake_run),
            patch.object(run_full, "mark_running"),
            patch.object(run_full, "mark_finished"),
            redirect_stdout(io.StringIO()),
        ):
            run_full.main()

        self.assertEqual(len(calls), 1)
        self.assertIsNone(calls[0][1])
        self.assertNotIn("--no-deploy", calls[0][0])

    def test_no_deploy_sets_child_env_when_executing(self):
        calls = []

        def fake_run(cmd, timeout=None, env=None):
            calls.append((cmd, env))
            return 0

        argv = ["run_full.py", "--topic", "ai4s", "--mode", "smoke"]
        with (
            patch.object(sys, "argv", argv),
            patch.object(run_full, "run", side_effect=fake_run),
            patch.object(run_full, "mark_running") as mark_running,
            patch.object(run_full, "mark_finished") as mark_finished,
            redirect_stdout(io.StringIO()),
        ):
            run_full.main()

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["PAPER_CURATION_NO_DEPLOY"], "1")
        mark_running.assert_not_called()
        mark_finished.assert_not_called()

    def test_smoke_dry_run_does_not_execute_child_or_run_state(self):
        argv = ["run_full.py", "--topic", "ai4s", "--mode", "smoke", "--dry-run"]
        with (
            patch.object(sys, "argv", argv),
            patch.object(run_full, "run") as run,
            patch.object(run_full, "mark_running") as mark_running,
            patch.object(run_full, "mark_finished") as mark_finished,
            redirect_stdout(io.StringIO()),
        ):
            run_full.main()

        run.assert_not_called()
        mark_running.assert_not_called()
        mark_finished.assert_not_called()


if __name__ == "__main__":
    unittest.main()
