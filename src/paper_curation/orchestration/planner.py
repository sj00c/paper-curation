"""Translate explicit operator intents into immutable process plans."""

from __future__ import annotations

import sys
import os
from pathlib import Path

from .model import FailurePolicy, Plan, SideEffect, Step


class Planner:
    """Build plans without probing configuration, credentials, or the filesystem."""

    def __init__(self, project_root: Path | None = None, *, python: str | None = None) -> None:
        self.project_root = project_root or self._discover_project_root()
        self.pipeline = self.project_root / "pipeline"
        self.python = python or sys.executable

    @staticmethod
    def _discover_project_root() -> Path:
        configured = os.environ.get("PAPER_CURATION_ROOT", "").strip()
        candidates = [Path(configured)] if configured else []
        candidates.extend((Path.cwd(), Path(__file__).resolve().parents[3]))
        for candidate in candidates:
            root = candidate.expanduser().resolve()
            if (root / "pipeline" / "run_full.py").is_file():
                return root
        raise RuntimeError(
            "paper-curation checkout not found; run from the checkout or set "
            "PAPER_CURATION_ROOT"
        )

    def plan(self, command: str, *, topic: str | None = None, execute: bool = False,
             query: str | None = None, config_path: str | None = None,
             legacy_args: tuple[str, ...] = ()) -> Plan:
        if command == "migrate":
            argv = [self.python, "-m", "paper_curation.cli", "migrate"]
            if config_path:
                argv.extend(("--config", config_path))
            if execute:
                argv.append("--execute")
            return self._plan(
                "migrate",
                "migrate",
                argv,
                SideEffect.LOCAL_WRITE if execute else SideEffect.LOCAL_READ,
            )
        if command == "build":
            self._reject_axis_overrides(legacy_args)
            return self._run_full(
                "build", topic, "rebuild", ("--yes", *legacy_args)
            )
        if command == "setup":
            return self._single("setup", "setup.py", None, None, legacy_args,
                                effect=SideEffect.LOCAL_WRITE,
                                effects={SideEffect.LOCAL_WRITE, SideEffect.NETWORK_READ})
        if command == "inspect":
            return self._single("inspect", "inspect_installation.py", None, None, legacy_args,
                                effect=SideEffect.LOCAL_READ)
        if command == "doctor":
            effects = {SideEffect.LOCAL_READ}
            if "--network" in legacy_args:
                effects.add(SideEffect.NETWORK_READ)
            return self._single("doctor", "doctor.py", None, None, legacy_args,
                                effect=SideEffect.LOCAL_READ, effects=effects)
        if command == "update":
            self._reject_axis_overrides(legacy_args)
            return self._run_full(
                "update", topic, "curate", ("--source", "zotero", *legacy_args)
            )
        if command == "serve":
            return self._single("serve", "serve_local.py", topic, None, legacy_args,
                                effect=SideEffect.LOCAL_READ,
                                effects={
                                    SideEffect.LOCAL_READ,
                                    SideEffect.NETWORK_READ,
                                    SideEffect.LOCAL_SERVICE,
                                })
        if command == "query":
            argv = self._base("query_search_index.py", topic)
            if not query:
                raise ValueError("query requires --query")
            argv.extend(("--query", query))
            argv.extend(legacy_args)
            lexical_only = self._effective_option(legacy_args, "--mode") == "bm25"
            effects = {SideEffect.LOCAL_READ}
            if not lexical_only:
                effects.add(SideEffect.NETWORK_READ)
            return self._plan(
                "query", "query", argv, SideEffect.LOCAL_READ, effects=effects
            )
        if command == "validate":
            return self._single("validate", "validate_papers.py", topic, None, legacy_args,
                                effect=SideEffect.LOCAL_READ)
        if command == "repair":
            argv = self._base("auto_recover.py", topic)
            if execute:
                argv.append("--execute")
            argv.extend(legacy_args)
            return self._plan("repair", "repair", argv,
                              SideEffect.LOCAL_WRITE if execute else SideEffect.LOCAL_READ)
        if command == "deploy":
            argv = self._base("prepare_deploy.py", topic)
            argv.append("--push")
            argv.extend(legacy_args)
            preflight = Step(
                "deploy-preflight", tuple(self._base("inspect_deploy.py", topic)),
                side_effect=SideEffect.LOCAL_READ,
                declared_effects=frozenset({
                    SideEffect.LOCAL_READ, SideEffect.NETWORK_READ,
                }),
                provides=frozenset({"deployment-ready"}),
            )
            publish = Step(
                "deploy", tuple(argv),
                prerequisites=frozenset({"deploy-preflight"}),
                side_effect=SideEffect.PUBLICATION,
                declared_effects=frozenset({
                    SideEffect.LOCAL_READ,
                    SideEffect.LOCAL_WRITE,
                    SideEffect.NETWORK_READ,
                    SideEffect.PUBLICATION,
                }),
            )
            return Plan("deploy", (preflight, publish), local_only=False)
        if command == "legacy-run-full":
            mode = self._effective_option(legacy_args, "--mode")
            source = self._effective_option(legacy_args, "--source")
            effects = {
                SideEffect.LOCAL_READ,
                SideEffect.LOCAL_WRITE,
                SideEffect.NETWORK_READ,
            }
            if source == "web" or "--dedup-execute" in legacy_args:
                effects.add(SideEffect.EXTERNAL_MUTATION)
            if mode == "deploy":
                effects.add(SideEffect.PUBLICATION)
            argv = self._base("run_full.py", topic)
            argv.extend(legacy_args)
            return Plan(
                "legacy-run-full",
                (Step(
                    "run-full", tuple(argv), side_effect=SideEffect.LOCAL_WRITE,
                    declared_effects=frozenset(effects),
                ),),
                local_only=not bool(
                    effects & {SideEffect.EXTERNAL_MUTATION, SideEffect.PUBLICATION}
                ),
            )
        raise ValueError(f"unknown orchestration command: {command}")

    def _run_full(self, name: str, topic: str | None, mode: str | None,
                  extra: tuple[str, ...]) -> Plan:
        argv = self._base("run_full.py", topic)
        if mode:
            argv.extend(("--mode", mode))
        argv.extend(extra)
        preflight = Step(
            "inspect",
            tuple(self._base("inspect_installation.py", None)),
            side_effect=SideEffect.LOCAL_READ,
            provides=frozenset({"installation-inspected"}),
        )
        operation = Step(
            "run-full",
            tuple(argv),
            prerequisites=frozenset({"inspect"}),
            side_effect=SideEffect.LOCAL_WRITE,
            declared_effects=frozenset({
                SideEffect.LOCAL_READ,
                SideEffect.LOCAL_WRITE,
                SideEffect.NETWORK_READ,
            }),
        )
        explicit_external_mutation = "--dedup-execute" in extra
        if explicit_external_mutation:
            operation = Step(
                operation.name,
                operation.argv,
                prerequisites=operation.prerequisites,
                side_effect=operation.side_effect,
                declared_effects=operation.declared_effects
                | {SideEffect.EXTERNAL_MUTATION},
            )
        return Plan(
            name,
            (preflight, operation),
            local_only=not explicit_external_mutation,
        )

    def _single(self, name: str, script: str, topic: str | None, mode: str | None,
                extra: tuple[str, ...], *, effect: SideEffect = SideEffect.LOCAL_WRITE,
                effects: set[SideEffect] | None = None) -> Plan:
        argv = self._base(script, topic)
        if mode:
            argv.extend(("--mode", mode))
        argv.extend(extra)
        return self._plan(name, name, argv, effect, effects=effects)

    def _base(self, script: str, topic: str | None) -> list[str]:
        argv = [self.python, "-u", str(self.pipeline / script)]
        if topic:
            argv.extend(("--topic", topic))
        return argv

    @staticmethod
    def _effective_option(arguments: tuple[str, ...], flag: str) -> str | None:
        value = None
        for index, argument in enumerate(arguments):
            if argument.startswith(flag + "="):
                value = argument.split("=", 1)[1]
            elif argument == flag and index + 1 < len(arguments):
                value = arguments[index + 1]
        return value

    @staticmethod
    def _reject_axis_overrides(arguments: tuple[str, ...]) -> None:
        forbidden = ("--mode", "--source")
        used = {
            flag
            for flag in forbidden
            if any(argument == flag or argument.startswith(flag + "=")
                   for argument in arguments)
        }
        if used:
            raise ValueError(
                "friendly commands do not accept axis overrides: "
                + ", ".join(sorted(used))
                + "; use legacy-run-full explicitly"
            )

    @staticmethod
    def _plan(
        name: str,
        step_name: str,
        argv: list[str],
        effect: SideEffect,
        *,
        effects: set[SideEffect] | None = None,
    ) -> Plan:
        declared = effects or {effect}
        if name in {"build", "update", "legacy-run-full"}:
            declared = {
                SideEffect.LOCAL_READ,
                SideEffect.LOCAL_WRITE,
                SideEffect.NETWORK_READ,
            }
        return Plan(name, (Step(step_name, tuple(argv), side_effect=effect,
                                declared_effects=frozenset(declared),
                                failure_policy=FailurePolicy.CRITICAL),))
