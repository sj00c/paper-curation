"""Immutable declarations for process orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from graphlib import TopologicalSorter
from types import MappingProxyType
from typing import Iterable, Mapping


class SideEffect(str, Enum):
    PURE = "pure"
    LOCAL_READ = "local-read"
    LOCAL_WRITE = "local-write"
    NETWORK_READ = "network-read"
    LOCAL_SERVICE = "local-service"
    EXTERNAL_MUTATION = "external-mutation"
    PUBLICATION = "publication"
    NOTIFICATION = "notification"


class FailurePolicy(str, Enum):
    CRITICAL = "critical"
    OPTIONAL = "optional"


class CostClass(str, Enum):
    LOCAL = "local"
    REMOTE_UNMETERED = "remote-unmetered"
    METERED = "metered"


class PlanValidationError(ValueError):
    """A declarative plan is internally inconsistent or unsafe."""


@dataclass(frozen=True, slots=True)
class Step:
    """One process invocation and the facts needed to safely schedule it."""

    name: str
    argv: tuple[str, ...]
    prerequisites: frozenset[str] = field(default_factory=frozenset)
    provides: frozenset[str] = field(default_factory=frozenset)
    capability_requirement: str | None = None
    provider_requirement: str | None = None
    cost_class: CostClass = CostClass.LOCAL
    side_effect: SideEffect = SideEffect.LOCAL_WRITE
    declared_effects: frozenset[SideEffect] = field(default_factory=frozenset)
    failure_policy: FailurePolicy = FailurePolicy.CRITICAL
    optional_absent_exit_codes: frozenset[int] = field(default_factory=frozenset)
    timeout: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "argv", tuple(str(arg) for arg in self.argv))
        object.__setattr__(self, "prerequisites", frozenset(self.prerequisites))
        object.__setattr__(self, "provides", frozenset(self.provides))
        object.__setattr__(self, "optional_absent_exit_codes", frozenset(self.optional_absent_exit_codes))
        object.__setattr__(self, "side_effect", SideEffect(self.side_effect))
        object.__setattr__(self, "cost_class", CostClass(self.cost_class))
        effects = frozenset(SideEffect(effect) for effect in self.declared_effects)
        object.__setattr__(
            self,
            "declared_effects",
            effects or frozenset({self.side_effect}),
        )
        object.__setattr__(self, "failure_policy", FailurePolicy(self.failure_policy))
        if not self.name:
            raise PlanValidationError("step names must be non-empty")
        if not self.argv:
            raise PlanValidationError(f"step '{self.name}' has an empty argv")
        if self.capability_requirement == "":
            raise PlanValidationError(f"step '{self.name}' capability requirement must be non-empty")
        if self.provider_requirement == "":
            raise PlanValidationError(f"step '{self.name}' provider requirement must be non-empty")
        if self.capability_requirement is not None and self.provider_requirement is None:
            raise PlanValidationError(
                f"step '{self.name}' capability requirement needs an exact provider requirement")
        if self.provider_requirement is not None and self.capability_requirement is None:
            raise PlanValidationError(
                f"step '{self.name}' provider requirement needs a capability requirement")
        if self.cost_class is CostClass.METERED and (
            self.capability_requirement is None or self.provider_requirement is None
        ):
            raise PlanValidationError(
                f"metered step '{self.name}' requires an exact capability and provider")
        if self.timeout is not None and self.timeout <= 0:
            raise PlanValidationError(f"step '{self.name}' timeout must be positive")



@dataclass(frozen=True, slots=True)
class Plan:
    """A validated, deterministic process graph."""

    name: str
    steps: tuple[Step, ...]
    local_only: bool = True
    selected_capabilities: frozenset[str] = field(default_factory=frozenset)
    selected_providers: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "steps", tuple(self.steps))
        capabilities = frozenset(self.selected_capabilities)
        providers = MappingProxyType(dict(self.selected_providers))
        object.__setattr__(self, "selected_capabilities", capabilities)
        object.__setattr__(self, "selected_providers", providers)
        if not self.name:
            raise PlanValidationError("plan name must be non-empty")
        if any(not capability for capability in capabilities):
            raise PlanValidationError("selected capabilities must be non-empty")
        if any(not capability or not provider for capability, provider in providers.items()):
            raise PlanValidationError("selected capability providers must be non-empty")
        if set(providers) != set(capabilities):
            raise PlanValidationError(
                "each selected capability must bind to exactly one selected provider")
        names = [step.name for step in self.steps]
        if len(names) != len(set(names)):
            raise PlanValidationError("step names must be unique")
        known = set(names)
        for step in self.steps:
            missing = step.prerequisites - known
            if missing:
                raise PlanValidationError(
                    f"step '{step.name}' has unknown prerequisites: {', '.join(sorted(missing))}")
            if step.name in step.prerequisites:
                raise PlanValidationError(f"step '{step.name}' cannot depend on itself")
            forbidden = step.declared_effects & {
                SideEffect.EXTERNAL_MUTATION,
                SideEffect.PUBLICATION,
                SideEffect.NOTIFICATION,
            }
            if self.local_only and forbidden:
                raise PlanValidationError(
                    f"local plan '{self.name}' cannot contain "
                    f"{', '.join(sorted(effect.value for effect in forbidden))}")
        try:
            tuple(TopologicalSorter({step.name: step.prerequisites for step in self.steps}).static_order())
        except Exception as exc:  # graphlib exposes a version-specific CycleError
            raise PlanValidationError(f"plan '{self.name}' has cyclic dependencies") from exc

    def topological_steps(self) -> tuple[Step, ...]:
        """Return steps in dependency order, retaining declaration order for ties."""
        by_name = {step.name: step for step in self.steps}
        remaining = {step.name: set(step.prerequisites) for step in self.steps}
        ordered: list[Step] = []
        while remaining:
            ready = [step.name for step in self.steps if step.name in remaining and not remaining[step.name]]
            if not ready:  # guarded in __post_init__, kept fail-closed for future mutation.
                raise PlanValidationError(f"plan '{self.name}' has cyclic dependencies")
            for name in ready:
                ordered.append(by_name[name])
                del remaining[name]
            completed = set(ready)
            for prerequisites in remaining.values():
                prerequisites.difference_update(completed)
        return tuple(ordered)


def plan_from_steps(
    name: str,
    steps: Iterable[Step],
    *,
    local_only: bool = True,
    selected_capabilities: frozenset[str] | set[str] = frozenset(),
    selected_providers: Mapping[str, str] | None = None,
) -> Plan:
    """Convenience constructor for callers holding an iterable."""
    return Plan(
        name=name,
        steps=tuple(steps),
        local_only=local_only,
        selected_capabilities=frozenset(selected_capabilities),
        selected_providers={} if selected_providers is None else selected_providers,
    )
