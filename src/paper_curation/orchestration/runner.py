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
        capabilities: frozenset[str] | set[str] | None = None,
        capture_output: bool = True,
    ) -> None:
        self._executor = executor or _default_executor
        self._environment = dict(os.environ if environment is None else environment)
        self._cwd = cwd
        self._capabilities = frozenset(capabilities or ())
        self._capture_output = capture_output

    def run(self, step: Step) -> RunReceipt:
        """Run one step. Critical failures raise after a receipt is constructed."""
        if step.capability_requirement and step.capability_requirement not in self._capabilities:
            receipt = RunReceipt(
                step, ReceiptStatus.SKIPPED, None,
                detail=f"required capability unavailable: {step.capability_requirement}",
            )
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
        """Run the plan in validated topological order, stopping on critical failure."""
        return tuple(self.run(step) for step in plan.topological_steps())


def _as_text(value: object) -> str:
    if value is None:
        return ""
    return value.decode() if isinstance(value, bytes) else str(value)


def _result_parts(result: Any) -> tuple[int, str, str]:
    if isinstance(result, int):
        return result, "", ""
    return int(result.returncode), _as_text(getattr(result, "stdout", "")), _as_text(getattr(result, "stderr", ""))
