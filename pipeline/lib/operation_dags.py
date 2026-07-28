"""Pure immutable planners for the offline query operation contracts.

This module deliberately does not import provider or transport code.  Adapters issue
only the returned steps and feed their retained results back to these reducers.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Mapping
import json
import unicodedata

from pipeline.lib.operation_consent import canonical_json_bytes, sha256_hex

RRF_K = 60
NORMAL_DEADLINE_SECONDS = 10 * 60
DEEPER_DEADLINE_SECONDS = 30 * 60


class DagError(ValueError):
    pass


class DagBoundsError(DagError):
    pass


class DagStateError(DagError):
    pass


class DagAuthError(DagError):
    pass

def _freeze_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_value(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    return value


@dataclass(frozen=True)
class Step:
    id: str
    kind: str
    provider_required: bool = False
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id or not isinstance(self.kind, str) or not self.kind:
            raise DagBoundsError("step id and kind must be nonempty strings")
        if not isinstance(self.provider_required, bool):
            raise DagBoundsError("step provider_required must be boolean")
        if isinstance(self.dependencies, (str, bytes)):
            raise DagBoundsError("step dependencies must be an ordered sequence")
        dependencies = tuple(self.dependencies)
        if any(not isinstance(dependency, str) or not dependency for dependency in dependencies):
            raise DagBoundsError("step dependencies must contain nonempty ids")
        object.__setattr__(self, "dependencies", dependencies)


@dataclass(frozen=True)
class QueryDag:
    command: str
    query: str
    deadline_seconds: int
    concurrency: int
    max_attempts: int
    steps: tuple[Step, ...]
    config: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.command, str) or not self.command:
            raise DagBoundsError("command must be a nonempty string")
        _query(self.query)
        for name in ("deadline_seconds", "concurrency", "max_attempts"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise DagBoundsError(f"{name} must be a positive integer")
        if isinstance(self.steps, (str, bytes)):
            raise DagBoundsError("steps must be an ordered sequence")
        steps = tuple(self.steps)
        if not steps or not all(isinstance(step, Step) for step in steps):
            raise DagBoundsError("steps must contain Step values")
        if len({step.id for step in steps}) != len(steps):
            raise DagBoundsError("step ids must be unique")
        if not isinstance(self.config, Mapping):
            raise DagBoundsError("config must be an object")
        canonical_config = json.loads(canonical_json_bytes(self.config).decode("utf-8"))
        object.__setattr__(self, "steps", steps)
        object.__setattr__(self, "config", _freeze_value(canonical_config))

    def canonical_value(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "concurrency": self.concurrency,
            "config": self.config,
            "deadline_seconds": self.deadline_seconds,
            "max_attempts": self.max_attempts,
            "query": self.query,
            "steps": [
                {
                    "dependencies": list(step.dependencies),
                    "id": step.id,
                    "kind": step.kind,
                    "provider_required": step.provider_required,
                }
                for step in self.steps
            ],
        }

    @property
    def canonical_digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self.canonical_value()))


@dataclass(frozen=True)
class QueryState:
    dag: QueryDag
    ready: tuple[Step, ...]
    completed: tuple[tuple[str, Mapping[str, Any]], ...] = ()
    terminal: str | None = None
    final_artifact: Mapping[str, Any] | None = None


def _integer(value: Any, name: str, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise DagBoundsError(f"{name} must be an integer from {low} to {high}")
    return value


def _query(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise DagBoundsError("query must be a nonempty NFC string")
    if unicodedata.normalize("NFC", value) != value:
        raise DagBoundsError("query must already be NFC-normalized")
    return value


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DagBoundsError(f"{name} must be an object")
    return value


def _providers(value: Any, required: bool) -> tuple[str, ...]:
    if value is None:
        value = ()
    if isinstance(value, Mapping):
        value = tuple(value)
    if isinstance(value, (str, bytes)):
        raise DagBoundsError("providers must be an ordered sequence")
    try:
        providers = tuple(value)
    except TypeError as exc:
        raise DagBoundsError("providers must be an ordered sequence") from exc
    if any(not isinstance(item, str) or not item for item in providers):
        raise DagBoundsError("providers must contain nonempty names")
    if required and not providers:
        raise DagBoundsError("declared provider requirement is missing")
    return providers


def _retrieval(payload: Mapping[str, Any], ceiling: int) -> tuple[str, int, int, bool]:
    value = _mapping(payload.get("retrieval"), "retrieval")
    mode = value.get("mode", "hybrid")
    if mode not in ("lexical", "dense", "hybrid"):
        raise DagBoundsError("retrieval.mode must be lexical, dense, or hybrid")
    top = _integer(value.get("top_k"), "retrieval.top_k", 1, ceiling)
    candidates = _integer(value.get("candidate_k"), "retrieval.candidate_k", top, ceiling)
    if value.get("rrf_k", RRF_K) != RRF_K:
        raise DagBoundsError("retrieval.rrf_k must be 60")
    rerank = value.get("rerank", False)
    if not isinstance(rerank, bool):
        raise DagBoundsError("retrieval.rerank must be boolean")
    return mode, top, candidates, rerank


def plan_normal(payload: Mapping[str, Any]) -> QueryDag:
    payload = _mapping(payload, "payload")
    query = _query(payload.get("query"))
    mode, top, candidates, rerank = _retrieval(payload, 100)
    web = _mapping(payload.get("web", {}), "web")
    include_web = web.get("include", False)
    if not isinstance(include_web, bool):
        raise DagBoundsError("web.include must be boolean")
    searches = _integer(web.get("max_searches", 0), "web.max_searches", 0, 3)
    if include_web != (searches > 0):
        raise DagBoundsError("web include must be false iff max_searches is zero")
    providers = _providers(payload.get("providers"), mode != "lexical" or True)
    steps: list[Step] = []
    if mode in ("lexical", "hybrid"):
        steps.append(Step("N10", "lexical.local"))
    if mode in ("dense", "hybrid"):
        steps.extend((Step("N11", "embed.query", True), Step("N12", "retrieve.dense", False, ("N11",))))
    select_deps = ("N10", "N12") if mode == "hybrid" else (("N10",) if mode == "lexical" else ("N12",))
    steps.append(Step("N13", "fuse.rrf" if mode == "hybrid" else "select.local", False, select_deps))
    predecessor = "N13"
    if rerank:
        steps.append(Step("N14", "rerank", True, (predecessor,)))
        predecessor = "N14"
    for ordinal in range(1, searches + 1):
        step_id = f"N15.{ordinal}"
        steps.append(Step(step_id, "web.search", True, (predecessor,)))
        predecessor = step_id
    steps.append(Step("N20", "answer", True, (predecessor,)))
    return QueryDag("query.normal", query, NORMAL_DEADLINE_SECONDS, 1, 12, tuple(steps), {
        "mode": mode, "top_k": top, "candidate_k": candidates, "rerank": rerank,
        "web_searches": searches, "providers": providers,
    })


def plan_deeper(payload: Mapping[str, Any]) -> QueryDag:
    payload = _mapping(payload, "payload")
    query = _query(payload.get("query"))
    mode, top, candidates, rerank = _retrieval(payload, 50)
    deeper = _mapping(payload.get("deeper"), "deeper")
    aspects = _integer(
        deeper.get("aspects", deeper.get("max_aspects")),
        "deeper.aspects",
        3,
        6,
    )
    sections = _integer(
        deeper.get("sections", deeper.get("max_sections")),
        "deeper.sections",
        2,
        8,
    )
    web_total = _integer(
        deeper.get("max_web_searches", 0),
        "deeper.max_web_searches",
        0,
        12,
    )
    web_per_aspect = _integer(
        deeper.get("web_per_aspect", 0),
        "deeper.web_per_aspect",
        0,
        2,
    )
    if web_total > aspects * web_per_aspect:
        raise DagBoundsError("web total exceeds per-aspect bound")
    nodes = _integer(deeper.get("graph_max_nodes"), "deeper.graph_max_nodes", 1, 60)
    edges = _integer(deeper.get("graph_max_edges"), "deeper.graph_max_edges", 0, 120)
    hops = _integer(deeper.get("graph_max_hops"), "deeper.graph_max_hops", 0, 2)
    providers = _providers(payload.get("providers"), True)

    remaining_web = web_total
    web_by_aspect: list[int] = []
    for _aspect in range(aspects):
        count = min(web_per_aspect, remaining_web)
        web_by_aspect.append(count)
        remaining_web -= count

    # Include every possible provider and deterministic branch in the frozen plan.
    # The reducer activates alternatives conditionally; listing them here ensures
    # approval binds the complete authority surface rather than only D01.
    steps: list[Step] = [
        Step("D01", "investigation.plan.provider", True),
        Step("D02", "investigation.plan.deterministic"),
    ]
    for aspect in range(1, aspects + 1):
        suffix = str(aspect)
        if mode in ("lexical", "hybrid"):
            steps.append(Step(f"D10.{suffix}", "lexical.local"))
        if mode in ("dense", "hybrid"):
            steps.extend((
                Step(f"D11.{suffix}", "embed.query", True),
                Step(f"D12.{suffix}", "retrieve.dense", False, (f"D11.{suffix}",)),
            ))
        retrieval_dependencies = (
            (f"D10.{suffix}", f"D12.{suffix}")
            if mode == "hybrid"
            else ((f"D10.{suffix}",) if mode == "lexical" else (f"D12.{suffix}",))
        )
        steps.append(Step(
            f"D13.{suffix}",
            "fuse.rrf" if mode == "hybrid" else "select.local",
            False,
            retrieval_dependencies,
        ))
        predecessor = f"D13.{suffix}"
        if rerank:
            steps.append(Step(f"D14.{suffix}", "rerank", True, (predecessor,)))
            predecessor = f"D14.{suffix}"
        steps.append(Step(f"D15.{suffix}", "graph.expand.local", False, (predecessor,)))
        predecessor = f"D15.{suffix}"
        for ordinal in range(1, web_by_aspect[aspect - 1] + 1):
            step_id = f"D16.{suffix}.{ordinal}"
            steps.append(Step(step_id, "web.search", True, (predecessor,)))
            predecessor = step_id

    steps.extend((
        Step("D20", "report.plan.provider", True),
        Step("D21", "report.plan.deterministic"),
    ))
    for section in range(1, sections + 1):
        steps.extend((
            Step(f"D30.{section}", "section.writer", True),
            Step(f"D31.{section}", "section.deterministic"),
        ))
    steps.extend((
        Step("D35", "complete.draft.local"),
        Step("D40", "final.synthesis.provider", True),
        Step("D41", "final.complete-draft-fallback.local"),
        Step("D42", "final.citation-fallback.local"),
        Step("D49", "final.publish.local"),
    ))
    return QueryDag(
        "query.deeper",
        query,
        DEEPER_DEADLINE_SECONDS,
        4,
        64,
        tuple(steps),
        {
            "mode": mode,
            "top_k": top,
            "candidate_k": candidates,
            "rerank": rerank,
            "aspects": aspects,
            "sections": sections,
            "web_total": web_total,
            "web_per_aspect": web_per_aspect,
            "web_by_aspect": tuple(web_by_aspect),
            "graph": (nodes, edges, hops),
            "providers": providers,
        },
    )


def start(dag: QueryDag) -> QueryState:
    if not isinstance(dag, QueryDag):
        raise DagStateError("dag must be a QueryDag")
    if dag.command == "query.deeper":
        return QueryState(dag, (next(step for step in dag.steps if step.id == "D01"),))
    return QueryState(dag, tuple(step for step in dag.steps if not step.dependencies))


def _result(value: Any) -> Mapping[str, Any]:
    result = _mapping(value, "result")
    # This both validates canonical value types (including no floats/NaN) and copies it.
    return __import__("json").loads(canonical_json_bytes(result).decode("utf-8"))


def _completed(state: QueryState) -> dict[str, Mapping[str, Any]]:
    return dict(state.completed)


def _planned_step(dag: QueryDag, step_id: str) -> Step:
    try:
        return next(step for step in dag.steps if step.id == step_id)
    except StopIteration as exc:
        raise DagStateError(f"step {step_id} is absent from the frozen DAG") from exc


def _fallback(dag: QueryDag, step: Step, result: Mapping[str, Any]) -> Step | None:
    if result.get("status") != "failed":
        return None
    if result.get("failure") == "auth":
        raise DagAuthError(f"authentication failure at {step.id}")
    if step.id == "D01":
        return replace(_planned_step(dag, "D02"), dependencies=("D01",))
    if step.id == "D20":
        return replace(_planned_step(dag, "D21"), dependencies=("D20",))
    if step.id.startswith("D30."):
        return replace(
            _planned_step(dag, step.id.replace("D30.", "D31.")),
            dependencies=(step.id,),
        )
    if step.id == "D40":
        target = "D42" if result.get("failure") == "citation" else "D41"
        return replace(_planned_step(dag, target), dependencies=("D40",))
    return None


def _deeper_after_investigation(dag: QueryDag) -> tuple[Step, ...]:
    prefixes = ("D10.", "D11.")
    return tuple(step for step in dag.steps if step.id.startswith(prefixes))


def _final_artifact(state: QueryState, kind: str, output: Mapping[str, Any]) -> Mapping[str, Any]:
    for field in ("text", "citations", "references", "connections", "figures"):
        if field not in output:
            raise DagStateError(f"final output must retain {field}")
    payload = {"query": state.dag.query, "text": output["text"], "citations": output["citations"], "references": output["references"], "connections": output["connections"], "figures": output["figures"]}
    payload_bytes = canonical_json_bytes(payload)
    result_digest = sha256_hex(canonical_json_bytes(output))
    final_digest = sha256_hex(payload_bytes)
    transfer = {"source_kind": kind, "source_operation_id": output.get("operation_id", ""), "source_result_digest": result_digest, "final_artifact_digest": final_digest, "payload_digest": sha256_hex(payload_bytes), "expires_at": output.get("expires_at", 0)}
    transfer_digest = sha256_hex(b"pc-query-v1\0" + canonical_json_bytes(transfer))
    return {"kind": f"{kind}.{'answer' if kind == 'normal' else 'report'}.v1", "payload": payload, "payload_digest": sha256_hex(payload_bytes), "result_digest": result_digest, "transfer": transfer, "transfer_digest": transfer_digest}


def reduce(state: QueryState, step_id: str, value: Mapping[str, Any]) -> QueryState:
    if not isinstance(state, QueryState) or state.terminal:
        raise DagStateError("state is not running")
    if not isinstance(step_id, str):
        raise DagStateError("step id must be a string")
    ready = {step.id: step for step in state.ready}
    if step_id not in ready:
        raise DagStateError("result is undeclared, duplicate, or out of order")

    step = ready.pop(step_id)
    result = _result(value)
    done = _completed(state)
    done[step_id] = result
    completed_ids = set(done)
    fallback = _fallback(state.dag, step, result)

    if (step_id == "N13" or step_id.startswith("D13.")) and not result.get("evidence"):
        return replace(
            state,
            ready=(),
            completed=tuple(done.items()),
            terminal="FAILED_EMPTY_EVIDENCE",
        )
    if step_id == "D35":
        for field in ("text", "citations", "references", "connections", "figures"):
            if field not in result:
                raise DagStateError(f"complete draft must retain {field}")

    if fallback is not None:
        return replace(
            state,
            ready=tuple(ready.values()) + (fallback,),
            completed=tuple(done.items()),
        )

    continuable_failure = (
        step_id == "N14"
        or step_id.startswith("N15.")
        or step_id.startswith("D14.")
        or step_id.startswith("D16.")
    )
    if result.get("status") == "failed" and not continuable_failure:
        return replace(
            state,
            ready=(),
            completed=tuple(done.items()),
            terminal="FAILED",
        )

    additions: list[Step] = []
    queued = set(ready)

    def schedule(candidate_id: str, dependencies: tuple[str, ...] | None = None) -> None:
        if candidate_id not in completed_ids and candidate_id not in queued:
            candidate = _planned_step(state.dag, candidate_id)
            if dependencies is not None:
                candidate = replace(candidate, dependencies=dependencies)
            additions.append(candidate)
            queued.add(candidate_id)

    if state.dag.command == "query.deeper":
        if step_id in ("D01", "D02"):
            for candidate in _deeper_after_investigation(state.dag):
                schedule(candidate.id, (step_id,))
        elif step_id.startswith("D11."):
            schedule(step_id.replace("D11.", "D12."))
        elif step_id.startswith(("D10.", "D12.")):
            aspect = step_id.split(".", 1)[1]
            lexical_done = f"D10.{aspect}" in completed_ids
            dense_done = f"D12.{aspect}" in completed_ids
            retrieval_ready = (
                state.dag.config["mode"] == "hybrid" and lexical_done and dense_done
            ) or (
                state.dag.config["mode"] == "lexical" and lexical_done
            ) or (
                state.dag.config["mode"] == "dense" and dense_done
            )
            if retrieval_ready:
                schedule(f"D13.{aspect}")
        elif step_id.startswith("D13."):
            aspect = step_id.split(".", 1)[1]
            schedule(f"D14.{aspect}" if state.dag.config["rerank"] else f"D15.{aspect}")
        elif step_id.startswith("D14."):
            schedule(step_id.replace("D14.", "D15."))
        elif step_id.startswith("D15."):
            aspect = int(step_id.split(".", 1)[1])
            if state.dag.config["web_by_aspect"][aspect - 1]:
                schedule(f"D16.{aspect}.1")
        elif step_id.startswith("D16."):
            _prefix, aspect_text, ordinal_text = step_id.split(".")
            aspect = int(aspect_text)
            ordinal = int(ordinal_text)
            if ordinal < state.dag.config["web_by_aspect"][aspect - 1]:
                schedule(f"D16.{aspect}.{ordinal + 1}")

        aspect_terminals = set()
        for aspect in range(1, state.dag.config["aspects"] + 1):
            count = state.dag.config["web_by_aspect"][aspect - 1]
            aspect_terminals.add(
                f"D16.{aspect}.{count}" if count else f"D15.{aspect}"
            )
        if (
            aspect_terminals <= completed_ids
            and "D20" not in completed_ids
            and "D21" not in completed_ids
        ):
            schedule("D20", tuple(sorted(aspect_terminals)))

        if step_id in ("D20", "D21"):
            for section in range(1, state.dag.config["sections"] + 1):
                schedule(f"D30.{section}", (step_id,))

        section_predecessors = tuple(
            f"D30.{section}"
            if (
                f"D30.{section}" in done
                and done[f"D30.{section}"].get("status") != "failed"
            )
            else f"D31.{section}"
            for section in range(1, state.dag.config["sections"] + 1)
        )
        sections_complete = all(
            predecessor in completed_ids for predecessor in section_predecessors
        )
        if sections_complete:
            schedule("D35", section_predecessors)
        if step_id == "D35":
            schedule("D40", ("D35",))
        if step_id in ("D40", "D41", "D42"):
            schedule("D49", (step_id,))
    else:
        for candidate in state.dag.steps:
            if (
                candidate.id not in completed_ids
                and candidate.id not in ready
                and all(dependency in completed_ids for dependency in candidate.dependencies)
            ):
                additions.append(candidate)

    artifact = None
    terminal = None
    if step_id == "N20" and result.get("status") != "failed":
        artifact = _final_artifact(state, "normal", result)
        terminal = "COMPLETED"
    if step_id == "D49" and result.get("status") != "failed":
        selected = done.get("D41") or done.get("D42") or done.get("D40") or done.get("D35")
        artifact = _final_artifact(state, "deeper", selected)
        terminal = "COMPLETED"
    return replace(
        state,
        ready=tuple(ready.values()) + tuple(additions),
        completed=tuple(done.items()),
        terminal=terminal,
        final_artifact=artifact,
    )


# Explicit aliases keep adapter call sites descriptive without duplicating authority.
reduce_normal = reduce
reduce_deeper = reduce
normal_plan = plan_normal
deeper_plan = plan_deeper
