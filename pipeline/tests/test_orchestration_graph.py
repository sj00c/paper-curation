"""Contracts for the declarative orchestration graph."""

import subprocess
import unittest

from paper_curation.orchestration import (
    CostClass,
    FailurePolicy,
    Plan,
    PlanValidationError,
    ReceiptStatus,
    SideEffect,
    Step,
    StepExecutionError,
    SubprocessRunner,
)


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

    def test_plan_requires_one_exact_provider_per_selected_capability(self):
        with self.assertRaises(PlanValidationError):
            Plan(
                "build",
                (Step("review", ("review",)),),
                selected_capabilities=frozenset({"review"}),
            )

    def test_unselected_provider_is_not_executed(self):
        calls = []
        plan = Plan(
            "build",
            (Step(
                "review", ("review",),
                capability_requirement="review",
                provider_requirement="selected",
            ),),
            selected_capabilities=frozenset({"review"}),
            selected_providers={"review": "other"},
        )
        runner = SubprocessRunner(executor=lambda argv, **kwargs: calls.append(argv))
        receipts = runner.run_plan(plan)
        self.assertEqual(receipts[0].status, ReceiptStatus.SKIPPED)
        self.assertEqual(calls, [])

    def test_metered_step_requires_an_exact_capability_provider_binding(self):
        with self.assertRaises(PlanValidationError):
            Step("review", ("review",), cost_class=CostClass.METERED)

    def test_optional_failure_blocks_dependent_without_executing_it(self):
        calls = []
        plan = Plan("build", (
            Step("optional", ("optional",), failure_policy=FailurePolicy.OPTIONAL),
            Step("dependent", ("dependent",), prerequisites=frozenset({"optional"})),
        ))
        runner = SubprocessRunner(
            executor=lambda argv, **kwargs: calls.append(argv) or subprocess.CompletedProcess(argv, 1)
        )
        receipts = runner.run_plan(plan)
        self.assertEqual([receipt.status for receipt in receipts], [
            ReceiptStatus.FAILED, ReceiptStatus.BLOCKED,
        ])
        self.assertEqual(calls, [("optional",)])
        self.assertIn("optional (failed)", receipts[1].detail)

    def test_plan_records_critical_failure_and_blocks_its_dependent(self):
        plan = Plan("build", (
            Step("critical", ("critical",)),
            Step("dependent", ("dependent",), prerequisites=frozenset({"critical"})),
        ))
        runner = SubprocessRunner(
            executor=lambda argv, **kwargs: subprocess.CompletedProcess(argv, 1)
        )
        receipts = runner.run_plan(plan)
        self.assertEqual([receipt.status for receipt in receipts], [
            ReceiptStatus.FAILED, ReceiptStatus.BLOCKED,
        ])

if __name__ == "__main__":
    unittest.main()
