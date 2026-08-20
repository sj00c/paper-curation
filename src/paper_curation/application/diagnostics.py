"""Read-only installation inspection and readiness use cases."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from paper_curation.config.models import AppConfig, FeatureConfig


class DiagnosticSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A stable, secret-free diagnostic item."""

    code: str
    severity: DiagnosticSeverity
    message: str
    capability: str = "core"


@dataclass(frozen=True, slots=True)
class InspectionResult:
    """Configuration facts suitable for presentation without credential values."""

    diagnostics: tuple[Diagnostic, ...]
    source_transport: str
    configured_scopes: tuple[str, ...]
    core_review_provider: str
    core_review_cost_class: str
    enabled_capabilities: tuple[tuple[str, str], ...]
    workspace_location: str
    output_location: str
    publication_mode: str


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """The result of one read-only adapter probe."""

    ready: bool
    message: str = "ready"


class DiagnosticsProbes(Protocol):
    """Outer-adapter probes; implementations must not modify the installation."""

    def python_312(self) -> ProbeResult: ...

    def workspace_readable(self, location: str) -> ProbeResult: ...

    def workspace_writable(self, location: str) -> ProbeResult: ...

    def source_ready(self, transport: str, *, network: bool) -> ProbeResult: ...

    def core_provider_ready(self, provider: str, *, network: bool) -> ProbeResult: ...

    def required_dependencies(self) -> Iterable[tuple[str, ProbeResult]]: ...

    def enhancement_ready(
        self, capability: str, feature: FeatureConfig, *, network: bool
    ) -> ProbeResult: ...


@dataclass(frozen=True, slots=True)
class DoctorRequest:
    network: bool = False


@dataclass(frozen=True, slots=True)
class DoctorResult:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def core_healthy(self) -> bool:
        return not any(
            diagnostic.capability == "core" and diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    @property
    def exit_code(self) -> int:
        return 0 if self.core_healthy else 1


def review_cost_class(provider: str) -> str:
    """Classify the selected Core review provider's cost (single source of truth)."""
    return {
        "claude-code-oauth": "remote-unmetered",
        "anthropic-api": "metered",
        "local-model": "local",
    }[provider]


@dataclass(frozen=True, slots=True)
class InspectInstallation:
    """Project a configured installation into secret-free operational facts."""

    config: AppConfig
    output_directory: str | None = None

    def execute(self) -> InspectionResult:
        enabled = tuple(
            (name, feature.provider)
            for name, feature in self.config.features.items()
            if feature.enabled
        )
        scopes = tuple(self.config.source.collections)
        workspace = self.config.workspace.root
        output = self.output_directory if self.output_directory is not None else f"{workspace}/site"
        diagnostics = (
            Diagnostic("inspect.source_transport", DiagnosticSeverity.INFO, self.config.source.transport),
            Diagnostic("inspect.configured_scopes", DiagnosticSeverity.INFO, ",".join(scopes)),
            Diagnostic("inspect.core_review_provider", DiagnosticSeverity.INFO, self.config.core.review.provider),
            Diagnostic(
                "inspect.core_review_cost_class",
                DiagnosticSeverity.INFO,
                review_cost_class(self.config.core.review.provider),
            ),
            *(
                Diagnostic("inspect.enabled_capability", DiagnosticSeverity.INFO, f"{name}:{provider}", name)
                for name, provider in enabled
            ),
            Diagnostic("inspect.workspace_location", DiagnosticSeverity.INFO, workspace),
            Diagnostic("inspect.output_location", DiagnosticSeverity.INFO, output),
            Diagnostic("inspect.publication_mode", DiagnosticSeverity.INFO, self.config.publication.mode),
        )
        return InspectionResult(
            diagnostics=diagnostics,
            source_transport=self.config.source.transport,
            configured_scopes=scopes,
            core_review_provider=self.config.core.review.provider,
            core_review_cost_class=review_cost_class(self.config.core.review.provider),
            enabled_capabilities=enabled,
            workspace_location=workspace,
            output_location=output,
            publication_mode=self.config.publication.mode,
        )


@dataclass(frozen=True, slots=True)
class DoctorInstallation:
    """Check the selected Core path and enabled enhancements without writing."""

    config: AppConfig
    probes: DiagnosticsProbes

    def execute(self, request: DoctorRequest = DoctorRequest()) -> DoctorResult:
        diagnostics: list[Diagnostic] = []

        def core(code: str, result: ProbeResult) -> None:
            diagnostics.append(Diagnostic(
                code,
                DiagnosticSeverity.INFO if result.ready else DiagnosticSeverity.ERROR,
                result.message,
            ))

        core("core.python312", self.probes.python_312())
        core("core.workspace_readable", self.probes.workspace_readable(self.config.workspace.root))
        core("core.workspace_writable", self.probes.workspace_writable(self.config.workspace.root))
        core("core.source", self.probes.source_ready(self.config.source.transport, network=request.network))
        core(
            "core.review_provider",
            self.probes.core_provider_ready(self.config.core.review.provider, network=request.network),
        )
        for requirement, result in self.probes.required_dependencies():
            core(f"core.requirement.{requirement}", result)

        for capability, feature in self.config.features.items():
            if not feature.enabled:
                continue
            result = self.probes.enhancement_ready(capability, feature, network=request.network)
            diagnostics.append(Diagnostic(
                f"enhancement.{capability}",
                DiagnosticSeverity.INFO if result.ready else DiagnosticSeverity.WARNING,
                result.message,
                capability,
            ))
        return DoctorResult(tuple(diagnostics))
