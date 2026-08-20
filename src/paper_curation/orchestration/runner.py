"""No-shell process execution for declarative orchestration plans."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .model import FailurePolicy, Plan, Step


class ReceiptStatus(str, Enum):
    SUCCEEDED = "succeeded"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    FAILED = "failed"
    TIMED_OUT = "timed-out"


@dataclass(frozen=True, slots=True)
class RunReceipt:
    step: Step
    status: ReceiptStatus
    returncode: int | None
    stdout: str = ""
    stderr: str = ""
    detail: str = ""


class StepExecutionError(RuntimeError):
    """A critical step did not complete successfully."""

    def __init__(self, receipt: RunReceipt) -> None:
        self.receipt = receipt
        code = "timeout" if receipt.status is ReceiptStatus.TIMED_OUT else f"exit {receipt.returncode}"
        super().__init__(f"critical step '{receipt.step.name}' failed ({code})")


Executor = Callable[..., Any]


def _default_executor(argv: tuple[str, ...], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, shell=False, **kwargs)


class SubprocessRunner:
    """Execute exact argv vectors and return structured, credential-safe receipts."""

    def __init__(
        self,
        *,
        executor: Executor | None = None,
        environment: Mapping[str, str] | None = None,
        cwd: str | None = None,
        selected_capabilities: frozenset[str] | set[str] | None = None,
        selected_providers: Mapping[str, str] | None = None,
        capture_output: bool = True,
    ) -> None:
        self._executor = executor or _default_executor
        self._environment = dict(os.environ if environment is None else environment)
        self._cwd = cwd
        self._selected_capabilities = frozenset(selected_capabilities or ())
        self._selected_providers = dict(selected_providers or {})
        if set(self._selected_providers) != set(self._selected_capabilities):
            raise ValueError("each selected capability must bind to exactly one selected provider")
        self._capture_output = capture_output

    def run(self, step: Step) -> RunReceipt:
        """Run one step. Critical failures raise after a receipt is constructed."""
        return self._run(
            step,
            capabilities=self._selected_capabilities,
            providers=self._selected_providers,
        )

    def _run(
        self,
        step: Step,
        *,
        capabilities: frozenset[str],
        providers: Mapping[str, str],
    ) -> RunReceipt:
        if not self._is_selected(
            step,
            capabilities=capabilities,
            providers=providers,
        ):
            receipt = self._skipped_receipt(step)
            if step.failure_policy is FailurePolicy.CRITICAL:
                raise StepExecutionError(receipt)
            return receipt
        try:
            kwargs = {
                "cwd": self._cwd,
                "env": dict(self._environment),
                "text": True,
                "timeout": step.timeout,
            }
            if self._capture_output:
                kwargs["capture_output"] = True
            result = self._executor(step.argv, **kwargs)
        except subprocess.TimeoutExpired as exc:
            receipt = RunReceipt(
                step, ReceiptStatus.TIMED_OUT, 124,
                stdout=_as_text(exc.stdout), stderr=_as_text(exc.stderr),
                detail=f"timed out after {step.timeout}s",
            )
        except Exception as exc:
            receipt = RunReceipt(step, ReceiptStatus.FAILED, None, detail=f"{type(exc).__name__}: {exc}")
        else:
            returncode, stdout, stderr = _result_parts(result)
            if returncode == 0:
                return RunReceipt(step, ReceiptStatus.SUCCEEDED, 0, stdout, stderr)
            if returncode in step.optional_absent_exit_codes:
                return RunReceipt(
                    step, ReceiptStatus.SKIPPED, returncode, stdout, stderr,
                    detail=f"optional capability absent (exit {returncode})",
                )
            receipt = RunReceipt(step, ReceiptStatus.FAILED, returncode, stdout, stderr)
        if step.failure_policy is FailurePolicy.CRITICAL:
            raise StepExecutionError(receipt)
        return receipt

    def run_plan(self, plan: Plan) -> tuple[RunReceipt, ...]:
        """Run a plan, recording blocked dependents without invoking them."""
        receipts: dict[str, RunReceipt] = {}
        for step in plan.topological_steps():
            failed_prerequisites = [
                receipts[name]
                for name in step.prerequisites
                if receipts[name].status is not ReceiptStatus.SUCCEEDED
            ]
            if failed_prerequisites:
                receipts[step.name] = RunReceipt(
                    step,
                    ReceiptStatus.BLOCKED,
                    None,
                    detail="blocked by prerequisite: " + ", ".join(
                        f"{receipt.step.name} ({receipt.status.value})"
                        for receipt in sorted(failed_prerequisites, key=lambda receipt: receipt.step.name)
                    ),
                )
                continue
            if not self._is_selected(
                step,
                capabilities=plan.selected_capabilities,
                providers=plan.selected_providers,
            ):
                receipts[step.name] = self._skipped_receipt(step)
                continue
            try:
                receipts[step.name] = self._run(
                    step,
                    capabilities=plan.selected_capabilities,
                    providers=plan.selected_providers,
                )
            except StepExecutionError as exc:
                receipts[step.name] = exc.receipt
        return tuple(receipts[step.name] for step in plan.topological_steps())

    @staticmethod
    def _is_selected(
        step: Step,
        *,
        capabilities: frozenset[str],
        providers: Mapping[str, str],
    ) -> bool:
        if step.capability_requirement is None:
            return True
        return (
            step.capability_requirement in capabilities
            and step.provider_requirement is not None
            and providers.get(step.capability_requirement) == step.provider_requirement
        )

    @staticmethod
    def _skipped_receipt(step: Step) -> RunReceipt:
        if step.capability_requirement is None:
            detail = ""
        elif step.provider_requirement is None:
            detail = f"required capability unavailable: {step.capability_requirement}"
        else:
            detail = (
                "required capability/provider unavailable: "
                f"{step.capability_requirement}/{step.provider_requirement}"
            )
        return RunReceipt(step, ReceiptStatus.SKIPPED, None, detail=detail)


def _as_text(value: object) -> str:
    if value is None:
        return ""
    return value.decode() if isinstance(value, bytes) else str(value)


def _result_parts(result: Any) -> tuple[int, str, str]:
    if isinstance(result, int):
        return result, "", ""
    return int(result.returncode), _as_text(getattr(result, "stdout", "")), _as_text(getattr(result, "stderr", ""))
