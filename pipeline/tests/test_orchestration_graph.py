"""Contracts for the declarative orchestration graph."""

import subprocess
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from paper_curation.orchestration import (
    FailurePolicy,
    Plan,
    PlanValidationError,
    ReceiptStatus,
    SideEffect,
    Step,
    StepExecutionError,
    SubprocessRunner,
)
from paper_curation.orchestration.planner import Planner


class OrchestrationGraphTests(unittest.TestCase):
    def test_orders_named_prerequisites(self):
        plan = Plan("build", (
            Step("render", ("render",), prerequisites=frozenset({"extract"})),
            Step("extract", ("extract",)),
        ))
        self.assertEqual([step.name for step in plan.topological_steps()], ["extract", "render"])

    def test_local_plan_rejects_publication(self):
        with self.assertRaises(PlanValidationError):
            Plan("build", (Step("publish", ("publish",), side_effect=SideEffect.PUBLICATION),))

    def test_local_plan_rejects_hidden_publication_in_declared_effects(self):
        with self.assertRaises(PlanValidationError):
            Plan("build", (Step(
                "build", ("build",), side_effect=SideEffect.LOCAL_WRITE,
                declared_effects=frozenset({
                    SideEffect.LOCAL_WRITE, SideEffect.PUBLICATION,
                }),
            ),))

    def test_local_plan_rejects_external_mutation(self):
        with self.assertRaises(PlanValidationError):
            Plan("update", (Step(
                "dedup", ("dedup",),
                declared_effects=frozenset({SideEffect.EXTERNAL_MUTATION}),
            ),))

    def test_optional_absent_exit_skips(self):
        step = Step("search", ("search",), failure_policy=FailurePolicy.CRITICAL,
                    optional_absent_exit_codes=frozenset({5}))
        runner = SubprocessRunner(executor=lambda argv, **kwargs: subprocess.CompletedProcess(argv, 5))
        self.assertEqual(runner.run(step).status, ReceiptStatus.SKIPPED)

    def test_critical_failure_aborts(self):
        step = Step("index", ("index",))
        runner = SubprocessRunner(executor=lambda argv, **kwargs: subprocess.CompletedProcess(argv, 2))
        with self.assertRaises(StepExecutionError):
            runner.run(step)

    def test_build_and_update_preserve_the_friendly_cli_contract(self):
        planner = Planner(project_root=__import__("pathlib").Path("/checkout"), python="python")
        build_plan = planner.plan("build", topic="arbitrary-topic")
        update_plan = planner.plan("update", topic="arbitrary-topic")
        self.assertEqual(
            [step.name for step in build_plan.topological_steps()],
            ["inspect", "run-full"],
        )
        build = build_plan.steps[-1].argv
        update = update_plan.steps[-1].argv
        self.assertEqual(
            build,
            (
                "python", "-u", "/checkout/pipeline/run_full.py",
                "--topic", "arbitrary-topic", "--mode", "rebuild", "--yes",
            ),
        )
        self.assertEqual(
            update,
            (
                "python", "-u", "/checkout/pipeline/run_full.py",
                "--topic", "arbitrary-topic", "--mode", "curate",
                "--source", "zotero",
            ),
        )

    def test_installed_cli_discovers_the_checkout_from_cwd(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pipeline").mkdir()
            (root / "pipeline" / "run_full.py").write_text("", encoding="utf-8")
            with patch("paper_curation.orchestration.planner.Path.cwd", return_value=root):
                planner = Planner(python="python")
            self.assertEqual(planner.project_root, root.resolve())

    def test_query_and_legacy_effects_follow_effective_arguments(self):
        planner = Planner(project_root=Path("/checkout"), python="python")
        hybrid = planner.plan("query", topic="topic", query="q").steps[0]
        lexical = planner.plan(
            "query", topic="topic", query="q", legacy_args=("--mode", "bm25")
        ).steps[0]
        deploy = planner.plan(
            "legacy-run-full",
            topic="topic",
            legacy_args=("--mode", "deploy"),
        )
        self.assertIn(SideEffect.NETWORK_READ, hybrid.declared_effects)
        self.assertNotIn(SideEffect.NETWORK_READ, lexical.declared_effects)
        self.assertIn(SideEffect.PUBLICATION, deploy.steps[0].declared_effects)
        self.assertFalse(deploy.local_only)

    def test_friendly_commands_reject_axis_overrides(self):
        planner = Planner(project_root=Path("/checkout"), python="python")
        with self.assertRaises(ValueError):
            planner.plan(
                "update",
                topic="topic",
                legacy_args=("--mode", "deploy"),
            )
        with self.assertRaises(ValueError):
            planner.plan(
                "build",
                topic="topic",
                legacy_args=("--source=web",),
            )

    def test_effective_options_accept_equals_and_last_value_wins(self):
        planner = Planner(project_root=Path("/checkout"), python="python")
        lexical = planner.plan(
            "query",
            topic="topic",
            query="q",
            legacy_args=("--mode=hybrid", "--mode", "bm25"),
        )
        deploy = planner.plan(
            "legacy-run-full",
            topic="topic",
            legacy_args=("--mode=reclassify", "--mode=deploy"),
        )
        self.assertNotIn(SideEffect.NETWORK_READ, lexical.steps[0].declared_effects)
        self.assertIn(SideEffect.PUBLICATION, deploy.steps[0].declared_effects)


if __name__ == "__main__":
    unittest.main()
