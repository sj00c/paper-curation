import inspect
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import run_update_force as ruf  # noqa: E402


class ProductionAutoPublishCompatTests(unittest.TestCase):
    def test_ordinary_runner_contains_no_publish_adapter(self):
        source = inspect.getsource(ruf)
        self.assertNotIn("def _maybe_auto_deploy", source)
        self.assertNotIn("prepare_deploy.py", source)

    def test_no_deploy_contract_requires_exact_env_and_flag(self):
        for env_value, flag, accepted in (
            (None, False, False),
            (None, True, False),
            ("1", False, False),
            ("true", True, False),
            ("1", True, True),
        ):
            with self.subTest(env_value=env_value, flag=flag):
                env = {} if env_value is None else {"PAPER_CURATION_NO_DEPLOY": env_value}
                with patch.dict(os.environ, env, clear=True):
                    if accepted:
                        ruf._require_no_deploy_contract(SimpleNamespace(no_deploy=flag))
                    else:
                        with self.assertRaises(SystemExit):
                            ruf._require_no_deploy_contract(SimpleNamespace(no_deploy=flag))

    def test_direct_child_requires_both_authorities_before_main(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(ruf, "main") as main:
            with self.assertRaisesRegex(RuntimeError, "no_deploy=True"):
                ruf._run_curate("ai4s", no_deploy=True)
            main.assert_not_called()

        observed_argv = []
        def capture_main():
            observed_argv.extend(sys.argv)
        with patch.dict(os.environ, {"PAPER_CURATION_NO_DEPLOY": "1"}, clear=True), patch.object(ruf, "main", side_effect=capture_main):
            ruf._run_curate("ai4s", no_deploy=True)
        self.assertIn("--no-deploy", observed_argv)


if __name__ == "__main__":
    unittest.main()
