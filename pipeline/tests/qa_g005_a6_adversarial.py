#!/usr/bin/env python3
"""Adversarial QA harness for G005 / A6 (discriminated Audio plan status).

This file is deliberately not named ``test_*.py``: it is a red-team harness, not
part of the default suite.  Run it explicitly from the repository root::

    python3 pipeline/tests/qa_g005_a6_adversarial.py

It never mutates the production modules.  Every "old behavior" variant is
materialized in a throwaway copy of the tree under a temporary directory, and
the shipped test files are executed verbatim against that copy so the tests
themselves are proven to be real discriminators.  Adversarial matrices run
in-process against the real modules with ``patch.dict``/``patch.object`` only.

No network call is ever made: an audit hook records every effectful CPython
audit event, the google-genai SDK is replaced by a stub that refuses to be
constructed, and ``socket``/``builtins.open`` are replaced by raising spies for
the purity probe.
"""
from __future__ import annotations

import argparse
import ast
import builtins
import http.client
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import types
from dataclasses import dataclass, fields
from pathlib import Path
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[2]
PIPELINE = REPOSITORY / "pipeline"
for _entry in (str(REPOSITORY), str(PIPELINE)):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import config_loader  # noqa: E402
import serve_local  # noqa: E402
from lib import audio_overview  # noqa: E402
from lib import operation_consent  # noqa: E402
from lib.audio_overview import AudioCapabilityV1  # noqa: E402

CONTRACT_TESTS = "pipeline/tests/test_audio_optional_capability.py"

# A value no production string may echo back to an operator.
SENTINEL = "AIzaSyG005-A6-QA-SENTINEL-do-not-log-4b7e2a"

# Cases that measure the shipped suite's sensitivity rather than the shipped behavior.
# A failed verdict here is a coverage gap, not a contract regression.
COVERAGE_PROBE_CASE = "coverage probe: does any shipped test guard the browser half of the discriminated pair?"
INFORMATIONAL_CASES = {COVERAGE_PROBE_CASE}

RESULTS: list[dict] = []
COMMANDS: list[dict] = []
FINDINGS: list[dict] = []


# --------------------------------------------------------------------------
# reporting helpers
# --------------------------------------------------------------------------
def record(case: str, expected: str, observed: str, verdict: str) -> None:
    RESULTS.append({"case": case, "expected": expected, "observed": observed, "verdict": verdict})
    print(f"[{verdict.upper():>6}] {case}\n         observed: {observed}", flush=True)


def finding(identifier: str, severity: str, statement: str, evidence: str, blocking: bool) -> None:
    FINDINGS.append({
        "id": identifier,
        "severity": severity,
        "statement": statement,
        "evidence": evidence,
        "blocking": blocking,
    })


def clip(value, limit: int = 400) -> str:
    text = str(value).strip()
    return text if len(text) <= limit else text[:limit] + " …"


def tail(text: str, lines: int = 6) -> str:
    kept = [clip(line.rstrip(), 200) for line in str(text).strip().splitlines() if line.strip()]
    return clip(" | ".join(kept[-lines:]), 1_200)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"scratch build: expected exactly one occurrence of {label} ({text.count(old)} found)")
    return text.replace(old, new)


# --------------------------------------------------------------------------
# audit hook: proves the contract function performs no effect at all
# --------------------------------------------------------------------------
_AUDIT_ON = [False]
_AUDIT_EVENTS: list[str] = []
_AUDIT_IGNORED = ("sys._getframe", "object.__getattr__", "builtins.id")


def _audit_hook(event, args):  # pragma: no cover - exercised by the purity probe
    if not _AUDIT_ON[0]:
        return
    if event in _AUDIT_IGNORED:
        return
    detail = ""
    if args:
        try:
            detail = repr(args[0])[:120]
        except Exception:
            detail = "<unrepresentable>"
    _AUDIT_EVENTS.append(f"{event}({detail})")


sys.addaudithook(_audit_hook)


class _Recording:
    """Enable audit recording for exactly one block."""

    def __enter__(self):
        _AUDIT_EVENTS.clear()
        _AUDIT_ON[0] = True
        return _AUDIT_EVENTS

    def __exit__(self, *exc):
        _AUDIT_ON[0] = False
        return False


# --------------------------------------------------------------------------
# pre-A6 source fragments (reconstructed; only ever written into a temp copy)
# --------------------------------------------------------------------------
NEW_PLAN_STATUS = (
    '    if capability.state == "AVAILABLE":\n'
    '        return {"schema": 1, "result": "PLANNED", "capability": capability.to_dict()}\n'
    '    return {"schema": 1, "result": "FEATURE_UNAVAILABLE", "capability": capability.to_dict()}\n'
)
OLD_PLAN_STATUS_UNTAGGED = (
    '    return {"schema": 1, "feature": capability.feature, "state": capability.state,\n'
    '            "reason": capability.reason, "mutated": False}\n'
)
PLAN_STATUS_AVAILABLE_UNTAGGED = (
    '    if capability.state == "AVAILABLE":\n'
    '        return {"schema": 1, "capability": capability.to_dict()}\n'
    '    return {"schema": 1, "result": "FEATURE_UNAVAILABLE", "capability": capability.to_dict()}\n'
)

NEW_SERVE_CAPABILITY = "    return _audio_capability_record().to_dict()\n"
OLD_SERVE_CAPABILITY_HANDBUILT = (
    "    key = resolve_google_key()\n"
    "    available = bool(key)\n"
    "    return {\n"
    '        "schema": "AudioCapabilityV1",\n'
    '        "feature": "audio_overview",\n'
    '        "provider": "gemini",\n'
    '        "state": "AVAILABLE" if available else "UNAVAILABLE",\n'
    '        "reason": "READY" if available else "GEMINI_AUTH_UNAVAILABLE",\n'
    '        "model": SCRIPT_MODEL if available else None,\n'
    '        "models": {"script": SCRIPT_MODEL, "tts": TTS_MODEL},\n'
    "    }\n"
)

NEW_AUDIO_JS_RESULT = (
    '    if (c.state !== "AVAILABLE") return {schema:1, result:"FEATURE_UNAVAILABLE", capability:c};\n'
    '    return {schema:1, result:"PLANNED", capability:c};\n'
)
OLD_AUDIO_JS_UNTAGGED = (
    '    return {schema:1, feature:c.feature, state:c.state, reason:c.reason, mutated:false};\n'
)


# --------------------------------------------------------------------------
# scratch tree
# --------------------------------------------------------------------------
SCRATCH_SKIP_TOP = {
    ".git", ".gjc", ".pytest_cache", "artifacts", "docs", "pdf_cache", "paperbanana",
    ".env", "pipeline", "node_modules", "__pycache__",
}
PIPELINE_IGNORE = shutil.ignore_patterns(
    "__pycache__", "_cache", "_logs", "_smoke", "_archive", "_state", ".pytest_cache",
    "*.pyc", "_update_force_checkpoint.json",
)


def _copy_docs_shell(destination: Path) -> None:
    """docs/ minus the multi-gigabyte generated content.

    serve_local refuses to bind without a docs directory and the dashboard tests
    read the two owned front-end assets, so the shell has to exist; the rendered
    topics are never read by the suite.
    """
    destination.mkdir(parents=True, exist_ok=True)
    source = REPOSITORY / "docs"
    if not source.is_dir():
        return
    for entry in source.iterdir():
        if entry.is_file():
            shutil.copy2(entry, destination / entry.name)
    public = source / "public"
    if public.is_dir():
        (destination / "public").mkdir(exist_ok=True)
        for entry in public.iterdir():
            if entry.is_file() and entry.suffix in {".css", ".js", ".json", ".svg"}:
                shutil.copy2(entry, destination / "public" / entry.name)


def build_scratch(destination: Path, *, plan_status="new", serve="new", audio_js="new") -> Path:
    """Materialize a self-contained copy of the tree with the requested variant."""
    destination.mkdir(parents=True, exist_ok=True)
    for entry in REPOSITORY.iterdir():
        if entry.name in SCRATCH_SKIP_TOP:
            continue
        target = destination / entry.name
        if entry.is_dir():
            shutil.copytree(entry, target, ignore=PIPELINE_IGNORE, symlinks=True)
        else:
            shutil.copy2(entry, target)
    shutil.copytree(PIPELINE, destination / "pipeline", ignore=PIPELINE_IGNORE)
    _copy_docs_shell(destination / "docs")

    if plan_status != "new" or audio_js != "new":
        path = destination / "pipeline" / "lib" / "audio_overview.py"
        source = path.read_text(encoding="utf-8")
        if plan_status == "untagged":
            source = replace_once(source, NEW_PLAN_STATUS, OLD_PLAN_STATUS_UNTAGGED, "audio_plan_status body")
        elif plan_status == "available_missing_result":
            source = replace_once(source, NEW_PLAN_STATUS, PLAN_STATUS_AVAILABLE_UNTAGGED,
                                  "audio_plan_status body")
        elif plan_status != "new":
            raise SystemExit(f"unknown plan_status variant {plan_status}")
        if audio_js == "untagged":
            source = replace_once(source, NEW_AUDIO_JS_RESULT, OLD_AUDIO_JS_UNTAGGED, "AUDIO_JS openAudioModal body")
        elif audio_js != "new":
            raise SystemExit(f"unknown audio_js variant {audio_js}")
        path.write_text(source, encoding="utf-8")

    if serve != "new":
        path = destination / "pipeline" / "serve_local.py"
        source = path.read_text(encoding="utf-8")
        if serve == "handbuilt_models":
            source = replace_once(source, NEW_SERVE_CAPABILITY, OLD_SERVE_CAPABILITY_HANDBUILT,
                                  "audio_capability body")
        else:
            raise SystemExit(f"unknown serve variant {serve}")
        path.write_text(source, encoding="utf-8")

    return destination


def run(command: list[str], *, cwd: Path, label: str) -> tuple[int, str]:
    environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["NO_COLOR"] = "1"
    process = subprocess.run(command, cwd=cwd, env=environment, capture_output=True, text=True, timeout=900)
    output = (process.stdout or "") + (process.stderr or "")
    COMMANDS.append({
        "label": label,
        "command": " ".join(command),
        "cwd": "<scratch>" if cwd != REPOSITORY else ".",
        "exit_code": process.returncode,
    })
    return process.returncode, output


# The scratch copy is not a git working tree, so the two repository-inventory tests that shell out
# to `git ls-files` cannot run there. They are unrelated to A6 and are covered by the real-tree run.
SCRATCH_IGNORES = ["--ignore=pipeline/tests/test_no_personal_tooling.py"]


def run_variant(label: str, node_ids: list[str], **variant: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="g005-qa-") as directory:
        scratch = build_scratch(Path(directory) / "tree", **variant)
        return run([sys.executable, "-m", "pytest", *node_ids, *SCRATCH_IGNORES, "-q", "--tb=line",
                    "-p", "no:cacheprovider"],
                   cwd=scratch, label=label)


def failing_nodes(output: str) -> set[str]:
    """Node ids from pytest's short summary, including pytest-subtests SUBFAILED lines."""
    nodes = set()
    for line in output.splitlines():
        match = re.search(r"(?:^FAILED|^ERROR|^SUBFAILED\([^)]*\))\s+(\S+::\S+)", line.strip())
        if match:
            nodes.add(match.group(1))
    return nodes


# --------------------------------------------------------------------------
# 1. discriminator proofs
# --------------------------------------------------------------------------
def discriminator_proof() -> dict:
    proof: dict = {}

    code, output = run_variant("control: unmutated scratch copy", ["pipeline/tests"])
    control_nodes = failing_nodes(output)
    proof["control"] = {
        "variant": "unmutated copy of the working tree",
        "exitCode": code,
        "summary": tail(output, 2),
        "failingNodes": sorted(control_nodes),
        "ignoredInScratch": SCRATCH_IGNORES,
        "whyIgnored": "test_no_personal_tooling.py shells out to `git ls-files`; a temporary copy is "
                      "not a git working tree. Unrelated to A6 and still executed by the real-tree run.",
    }
    record(
        "control: the scratch copy of the tree is green before any mutation",
        "exit 0 so every later failure is attributable to the injected old behavior",
        f"exit {code}: {tail(output, 2)}",
        "passed" if code == 0 else "failed",
    )

    variants = [
        (
            "untagged",
            {"plan_status": "untagged"},
            'audio_plan_status returns the retired {schema, feature, state, reason, mutated:false}',
            {
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_missing_auth_is_informational_and_ui_is_disabled_without_provider_work",
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_plan_status_carries_the_result_discriminator_on_both_variants",
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_server_capability_and_route_use_the_library_contract",
            },
        ),
        (
            "availableMissingResult",
            {"plan_status": "available_missing_result"},
            "audio_plan_status omits `result` on the AVAILABLE branch only",
            {
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_plan_status_carries_the_result_discriminator_on_both_variants",
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_server_capability_and_route_use_the_library_contract",
            },
        ),
        (
            "serveHandBuiltModelsKey",
            {"serve": "handbuilt_models"},
            "serve_local.audio_capability() hand-builds the dict again and ships the stray `models` key",
            {
                f"{CONTRACT_TESTS}::AudioOptionalCapabilityTests::"
                "test_server_capability_and_route_use_the_library_contract",
            },
        ),
    ]

    for name, variant, description, expected_nodes in variants:
        code, output = run_variant(f"variant: {name}", ["pipeline/tests"], **variant)
        observed_nodes = failing_nodes(output) - control_nodes
        missed = sorted(expected_nodes - observed_nodes)
        proof[name] = {
            "variant": description,
            "mutation": variant,
            "exitCode": code,
            "summary": tail(output, 3),
            "newFailingNodes": sorted(observed_nodes),
            "expectedDiscriminators": sorted(expected_nodes),
            "expectedButPassing": missed,
        }
        record(
            f"discriminator: shipped tests fail against the old behavior — {description}",
            "exit != 0 and every named contract assertion fails (control-run failures subtracted)",
            f"exit {code}, {len(observed_nodes)} newly failing node(s) "
            + json.dumps(sorted(observed_nodes))
            + "; missed discriminators: " + (json.dumps(missed) if missed else "none"),
            "passed" if code != 0 and not missed else "failed",
        )

    # Coverage probe: is the browser half of the same contract actually guarded?
    code, output = run_variant("variant: audioJsUntagged", ["pipeline/tests"], audio_js="untagged")
    observed_nodes = failing_nodes(output) - control_nodes
    guarded = bool(observed_nodes)
    proof["audioJsUntagged"] = {
        "variant": "AUDIO_JS openAudioModal returns the retired untagged object in the browser",
        "mutation": {"audio_js": "untagged"},
        "exitCode": code,
        "summary": tail(output, 3),
        "newFailingNodes": sorted(observed_nodes),
        "shippedSuiteIsSensitive": guarded,
        "note": "recorded as a coverage probe, not as a regression: if the shipped suite has no "
                "assertion over the JS discriminator this mutation is invisible to it. The node "
                "parity case below covers the real asset out of band.",
    }
    record(
        COVERAGE_PROBE_CASE,
        "informational — a mutation of AUDIO_JS openAudioModal should ideally fail the shipped suite",
        f"exit {code}, {len(observed_nodes)} newly failing node(s) beyond the control: the shipped "
        "suite is " + ("sensitive" if guarded else "BLIND")
        + " to a retired-shape regression inside AUDIO_JS",
        "passed" if guarded else "failed",
    )
    if not guarded:
        finding(
            "A6-QA-1",
            "low",
            "No shipped test asserts the discriminated pair emitted by the browser asset "
            "`AUDIO_JS.openAudioModal`; reverting only that function to the retired untagged shape "
            "leaves `python3 -m pytest pipeline/tests -q` fully green.",
            f"scratch variant audio_js=untagged: full suite exit {code} with "
            f"{len(observed_nodes)} newly failing node(s) beyond the control. The Python half is well "
            "guarded (three discriminating tests in test_audio_optional_capability.py); only the JS "
            "half is unguarded. Remediation is one assertion in "
            "pipeline/tests/test_static_dashboard_assets.py or test_review_page_security.py: "
            "assertIn('result:\"FEATURE_UNAVAILABLE\"', audio_overview.AUDIO_JS) and "
            "assertIn('result:\"PLANNED\"', audio_overview.AUDIO_JS). Left unapplied on purpose: this "
            "lane does not modify the shipped suite the leader already recorded evidence against. "
            "The gap is covered out of band by this harness's node parity case, which evaluates the "
            "real asset and compares it to audio_plan_status for all four reason codes.",
            False,
        )
    return proof


# --------------------------------------------------------------------------
# 2. adversarial cases (in-process, against the real modules)
# --------------------------------------------------------------------------
MODELS = {"script": audio_overview.SCRIPT_MODEL, "tts": audio_overview.TTS_MODEL}

REASON_MATRIX = (
    ("READY", {"auth": "configured", "models": MODELS, "safe_root": True}, "AVAILABLE", "PLANNED"),
    ("GEMINI_AUTH_UNAVAILABLE", {"auth": "", "models": MODELS, "safe_root": True},
     "UNAVAILABLE", "FEATURE_UNAVAILABLE"),
    ("GEMINI_MODEL_UNAVAILABLE", {"auth": "configured", "models": {}, "safe_root": True},
     "UNAVAILABLE", "FEATURE_UNAVAILABLE"),
    ("AUDIO_TEMP_RECOVERY_AMBIGUOUS", {"auth": "configured", "models": MODELS, "safe_root": False},
     "UNAVAILABLE", "FEATURE_UNAVAILABLE"),
)


def case_reason_to_result() -> dict:
    observed = {}
    mismatches = []
    for reason, kwargs, state, expected_result in REASON_MATRIX:
        capability = audio_overview.derive_audio_capability(**kwargs)
        status = audio_overview.audio_plan_status(capability)
        observed[reason] = {
            "state": capability.state,
            "reason": capability.reason,
            "result": status.get("result"),
            "resultKeyPresent": "result" in status,
        }
        if capability.reason != reason or capability.state != state or status.get("result") != expected_result:
            mismatches.append(reason)
        if "result" not in status:
            mismatches.append(reason + " (no discriminator)")

    # Exhaustive sweep: PLANNED must be produced by AVAILABLE and by nothing else.
    sweep = []
    disagreements = []
    for auth in (None, "", "   ", "\t\n", "configured", SENTINEL, 0, 1, [], {}):
        for models in (None, {}, {"script": audio_overview.SCRIPT_MODEL},
                       {"tts": audio_overview.TTS_MODEL}, MODELS,
                       {"script": "other", "tts": audio_overview.TTS_MODEL}):
            for safe_root in (True, False):
                capability = audio_overview.derive_audio_capability(
                    auth=auth, models=models, safe_root=safe_root)
                status = audio_overview.audio_plan_status(capability)
                sweep.append((capability.state, capability.reason, status.get("result")))
                planned = status.get("result") == "PLANNED"
                if planned is not (capability.state == "AVAILABLE"):
                    disagreements.append((capability.state, capability.reason, status.get("result")))
                if status.get("result") not in {"PLANNED", "FEATURE_UNAVAILABLE"}:
                    disagreements.append(("bad-tag", capability.reason, status.get("result")))

    pairs = sorted({tuple(item) for item in sweep})
    tags_per_state: dict[str, set] = {}
    for state, _reason, result in sweep:
        tags_per_state.setdefault(state, set()).add(result)
    ambiguous = {state: sorted(tags) for state, tags in tags_per_state.items() if len(tags) != 1}

    record(
        "every reachable capability state maps to exactly one `result` "
        "(READY / GEMINI_AUTH_UNAVAILABLE / GEMINI_MODEL_UNAVAILABLE / AUDIO_TEMP_RECOVERY_AMBIGUOUS)",
        "PLANNED only for state=AVAILABLE (READY); FEATURE_UNAVAILABLE for every UNAVAILABLE reason; "
        "`result` present on both variants",
        json.dumps(observed, ensure_ascii=False),
        "passed" if not mismatches else "failed",
    )
    record(
        "exhaustive derive_audio_capability sweep: no state ever produces two different tags",
        "120 auth x models x safe_root combinations collapse to exactly one tag per state and no "
        "tag outside {PLANNED, FEATURE_UNAVAILABLE}",
        f"{len(sweep)} combinations, {len(pairs)} distinct (state, reason, result) triples "
        f"{json.dumps(pairs, ensure_ascii=False)}; state->tags {json.dumps({k: sorted(v) for k, v in tags_per_state.items()})}; "
        f"disagreements: {json.dumps(disagreements) if disagreements else 'none'}",
        "passed" if not disagreements and not ambiguous else "failed",
    )
    return {"reasonMatrix": observed, "sweepCombinations": len(sweep),
            "distinctTriples": [list(item) for item in pairs],
            "stateToTags": {k: sorted(v) for k, v in tags_per_state.items()},
            "disagreements": [list(item) for item in disagreements],
            "mismatches": mismatches}


@dataclass(frozen=True)
class _CapabilityWithExtraKey(AudioCapabilityV1):
    """A capability that smuggles one extra key into the nested record."""

    models: dict | None = None


def case_key_set_exactness() -> dict:
    expected_top = {"schema", "result", "capability"}
    expected_nested = set(AudioCapabilityV1().to_dict())
    observations = {}
    failures = []
    for label, capability in (
        ("unavailable", audio_overview.derive_audio_capability(auth="", models=MODELS)),
        ("available", audio_overview.derive_audio_capability(auth="configured", models=MODELS)),
    ):
        status = audio_overview.audio_plan_status(capability)
        top = set(status)
        nested = set(status["capability"])
        observations[label] = {"top": sorted(top), "nested": sorted(nested),
                               "schema": status.get("schema"), "result": status.get("result")}
        if top != expected_top or nested != expected_nested or status.get("schema") != 1:
            failures.append(label)

    # The exactness assertion must be a real discriminator: one extra nested key fails loudly.
    smuggled = audio_overview.audio_plan_status(
        _CapabilityWithExtraKey(state="AVAILABLE", reason="READY", model=audio_overview.SCRIPT_MODEL,
                                models=dict(MODELS)))
    smuggled_nested = set(smuggled["capability"])
    caught = smuggled_nested != expected_nested and "models" in smuggled_nested
    observations["smuggledExtraKey"] = {"nested": sorted(smuggled_nested), "detected": caught}

    record(
        "key-set exactness: the payload is exactly {schema, result, capability} on both variants and the "
        "nested record is exactly AudioCapabilityV1().to_dict()",
        f"top-level == {sorted(expected_top)}, nested == {sorted(expected_nested)}, schema == 1",
        json.dumps(observations, ensure_ascii=False),
        "passed" if not failures else "failed",
    )
    record(
        "key-set exactness is a live discriminator: an added capability key fails loudly",
        "a frozen subclass that adds `models` is detected by the same set comparison the shipped test uses",
        f"nested key set became {sorted(smuggled_nested)}; detected={caught}",
        "passed" if caught else "failed",
    )
    return {"expectedTop": sorted(expected_top), "expectedNested": sorted(expected_nested),
            "observations": observations, "failures": failures}


class ProviderReached(RuntimeError):
    """Raised by the stub when something actually constructs a provider client."""


class _StubModels:
    def generate_content(self, **kwargs):
        raise ProviderReached("generate_content reached")

    def embed_content(self, **kwargs):
        raise ProviderReached("embed_content reached")


class _StubClient:
    constructions = 0

    def __init__(self, *args, **kwargs):
        type(self).constructions += 1
        raise ProviderReached("a Gemini client was constructed")


def _stub_sdk() -> dict:
    genai = types.ModuleType("google.genai")
    genai.Client = _StubClient
    genai_types = types.ModuleType("google.genai.types")
    genai.types = genai_types
    google = types.ModuleType("google")
    google.genai = genai
    return {"google": google, "google.genai": genai, "google.genai.types": genai_types}


class _RefusingSocket:
    def __init__(self, *args, **kwargs):
        raise ProviderReached("a socket was created")


def _refuse(*args, **kwargs):
    raise ProviderReached(f"an I/O call was attempted: {args[:1]}")


def case_purity() -> dict:
    """audio_plan_status must do no I/O, build no client, and mint no consent object."""
    source = Path(audio_overview.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(node for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef) and node.name == "audio_plan_status")
    calls = sorted({ast.unparse(node.func) for node in ast.walk(function) if isinstance(node, ast.Call)})
    module_imports = sorted({
        (node.module or "") if isinstance(node, ast.ImportFrom) else alias.name
        for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    })
    forbidden_imports = sorted(name for name in module_imports if re.search(
        r"genai|socket|urllib|http|requests|subprocess|operation_consent|secrets|sqlite|shutil", name))

    _StubClient.constructions = 0
    consent_calls: list[str] = []

    def _spy(name):
        def _inner(*args, **kwargs):
            consent_calls.append(name)
            raise ProviderReached(f"consent.{name} was called")
        return _inner

    payloads = []
    audit_events: list[str] = []
    errors = []
    with patch.dict(sys.modules, _stub_sdk(), clear=False), \
            patch.object(socket, "socket", _RefusingSocket), \
            patch.object(socket, "create_connection", _refuse), \
            patch.object(socket, "getaddrinfo", _refuse), \
            patch.object(builtins, "open", _refuse), \
            patch.object(secrets, "token_bytes", _refuse), \
            patch.object(secrets, "token_hex", _refuse), \
            patch.object(secrets, "token_urlsafe", _refuse), \
            patch.object(operation_consent.OperationConsent, "create_plan", _spy("create_plan")), \
            patch.object(operation_consent.OperationConsent, "bind_plan", _spy("bind_plan")), \
            patch.object(operation_consent.OperationConsent, "approve", _spy("approve")), \
            patch.object(operation_consent.OperationConsent, "redeem", _spy("redeem")):
        capabilities = [audio_overview.derive_audio_capability(**kwargs) for _r, kwargs, _s, _e in REASON_MATRIX]
        try:
            with _Recording() as events:
                for capability in capabilities:
                    payloads.append(audio_overview.audio_plan_status(capability))
                audit_events = list(events)
        except Exception as error:  # pragma: no cover - a failure here is the finding
            errors.append(f"{type(error).__name__}: {error}")

    # Positive control: the audit hook must actually be able to see an effect, otherwise
    # "zero audit events" would be an unfalsifiable claim.
    with _Recording() as events:
        with open(os.devnull, "rb") as handle:
            handle.read(1)
        control_events = list(events)
    record(
        "purity harness self-check: the audit hook records a real effect",
        "opening os.devnull inside the recorder yields at least one audit event",
        f"controlEvents={control_events[:4] or 'none'} ({len(control_events)} total)",
        "passed" if control_events else "failed",
    )

    clean = (not errors and not audit_events and _StubClient.constructions == 0
             and not consent_calls and len(payloads) == 4)
    record(
        "purity: audio_plan_status performs no I/O, constructs no provider client, and creates no "
        "operation / claim / credential",
        "zero CPython audit events, zero Gemini client constructions, zero OperationConsent calls, "
        "zero secrets.token_* calls, and four payloads still returned while open/socket/genai all refuse",
        f"payloads={len(payloads)}, auditEvents={audit_events or 'none'}, "
        f"clientConstructions={_StubClient.constructions}, consentCalls={consent_calls or 'none'}, "
        f"errors={errors or 'none'}",
        "passed" if clean else "failed",
    )
    record(
        "purity (static): audio_plan_status calls nothing but capability.to_dict(), and its module "
        "imports no provider / socket / consent surface",
        "the only call inside the function is capability.to_dict; lib.audio_overview imports nothing "
        "that could reach a provider, a socket, or the consent store",
        f"calls={calls}; module imports={module_imports}; forbidden={forbidden_imports or 'none'}",
        "passed" if calls == ["capability.to_dict"] and not forbidden_imports else "failed",
    )
    return {
        "auditEvents": audit_events,
        "auditHookControlEvents": control_events[:6],
        "auditHookControlEventCount": len(control_events),
        "clientConstructions": _StubClient.constructions,
        "consentCalls": consent_calls,
        "errors": errors,
        "callsInsideFunction": calls,
        "moduleImports": module_imports,
        "forbiddenImports": forbidden_imports,
        "payloadCount": len(payloads),
    }


def _matrix_env(**overrides) -> dict:
    environment = {key: value for key, value in os.environ.items()}
    for name in ("GOOGLE_API_KEY", "GEMINI_API_KEY", "PAPER_CURATION_NO_GEMINI"):
        environment.pop(name, None)
    environment.update({key: value for key, value in overrides.items() if value is not None})
    return environment


def case_secret_safety() -> dict:
    surfaces: dict[str, str] = {}
    with patch.dict(os.environ, _matrix_env(GOOGLE_API_KEY=SENTINEL), clear=True), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": SENTINEL}):
        record_value = serve_local._audio_capability_record()
        surfaces["serve_local._audio_capability_record().to_dict()"] = json.dumps(
            record_value.to_dict(), ensure_ascii=False)
        surfaces["serve_local.audio_capability()"] = json.dumps(
            serve_local.audio_capability(), ensure_ascii=False)
        surfaces["audio_plan_status(record)"] = json.dumps(
            audio_overview.audio_plan_status(record_value), ensure_ascii=False)
        surfaces["repr(record)"] = repr(record_value)
        surfaces["audio_script_block(capability=record)"] = audio_overview.audio_script_block(
            capability=record_value)
        surfaces["audio_script_block() default"] = audio_overview.audio_script_block()
        surfaces["audio_script_block(legacy positional key)"] = audio_overview.audio_script_block(
            SENTINEL, capability=record_value)
        # The legacy first positional parameter used to be the baked browser key.
        available = audio_overview.configured_audio_capability(
            config={"audio_overview": {"models": MODELS}}, auth=SENTINEL)
        surfaces["configured_audio_capability(auth=SENTINEL)"] = json.dumps(
            audio_overview.audio_plan_status(available), ensure_ascii=False)

    leaks = sorted(name for name, value in surfaces.items() if SENTINEL in value)
    # A partial leak matters too: any 12+ char run of the sentinel is a leak.
    fragments = {SENTINEL[index:index + 14] for index in range(0, len(SENTINEL) - 14)}
    partial = sorted(name for name, value in surfaces.items()
                     if name not in leaks and any(fragment in value for fragment in fragments))
    record(
        "secret safety: a configured sentinel key never reaches the plan payload, the server capability "
        "dict, or the rendered audio_script_block HTML",
        "the sentinel (and every 14-character fragment of it) is absent from all eight rendered surfaces, "
        "including the legacy positional key parameter",
        f"{len(surfaces)} surfaces checked, sizes "
        + json.dumps({name: len(value) for name, value in surfaces.items()})
        + f"; leaks={leaks or 'none'}; partialLeaks={partial or 'none'}",
        "passed" if not leaks and not partial else "failed",
    )
    return {"surfacesChecked": sorted(surfaces), "leaks": leaks, "partialLeaks": partial,
            "sentinelIsFake": True}


def _serve_local_capability_sites() -> dict:
    """Static shape of every capability construction site inside serve_local."""
    tree = ast.parse(Path(serve_local.__file__).read_text(encoding="utf-8"))
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if name in {"configured_audio_capability", "derive_audio_capability", "AudioCapabilityV1"}:
                sites.append({
                    "call": name,
                    "line": node.lineno,
                    "keywords": sorted(keyword.arg for keyword in node.keywords if keyword.arg),
                    "source": ast.unparse(node),
                })
    callers = sorted({
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and any(isinstance(inner, ast.Call) and ast.unparse(inner.func) == "configured_audio_capability"
                for inner in ast.walk(node))
    })
    return {"sites": sites, "enclosingFunctions": callers}


def case_docstring_accuracy() -> dict:
    """The serve_local.audio_capability docstring claims a narrow reachability. Verify it exactly."""
    claims: dict[str, dict] = {}
    docstring = serve_local.audio_capability.__doc__ or ""

    # (1) Server sweep over everything resolve_google_key can return.
    server_reasons: dict[str, str] = {}
    for label, value in (("None", None), ("empty", ""), ("whitespace", "   "),
                         ("tab-newline", "\t\n"), ("configured", "configured"), ("sentinel", SENTINEL)):
        with patch.object(serve_local, "resolve_google_key", return_value=value):
            server_reasons[f"resolve_google_key()={label}"] = serve_local.audio_capability()["reason"]

    # (2) Server sweep over the real env / config chain (no seam patched below config_loader).
    matrices = (
        ("no key anywhere", _matrix_env(), {}),
        ("env GOOGLE_API_KEY", _matrix_env(GOOGLE_API_KEY=SENTINEL), {}),
        ("env GEMINI_API_KEY", _matrix_env(GEMINI_API_KEY=SENTINEL), {}),
        ("config gemini_api_key", _matrix_env(), {"gemini_api_key": SENTINEL}),
        ("config google_api_key", _matrix_env(), {"google_api_key": SENTINEL}),
        ("whitespace-only env key", _matrix_env(GOOGLE_API_KEY="   "), {}),
        ("disable switch beats a configured key",
         _matrix_env(GOOGLE_API_KEY=SENTINEL, PAPER_CURATION_NO_GEMINI="1"), {"gemini_api_key": SENTINEL}),
    )
    for label, environment, config in matrices:
        with patch.dict(os.environ, environment, clear=True), \
                patch.object(config_loader, "load_config", return_value=config):
            server_reasons[f"env/config matrix: {label}"] = serve_local.audio_capability()["reason"]

    reachable = sorted(set(server_reasons.values()))
    claims["serverReachableReasons"] = {
        "claim": "from the server only GEMINI_AUTH_UNAVAILABLE and READY are reachable today",
        "observed": server_reasons,
        "reachableSet": reachable,
        "holds": reachable == ["GEMINI_AUTH_UNAVAILABLE", "READY"],
    }

    # (3) The structural reason the other two are unreachable.
    static = _serve_local_capability_sites()
    single_site = (len(static["sites"]) == 1
                   and static["sites"][0]["call"] == "configured_audio_capability"
                   and static["enclosingFunctions"] == ["_audio_capability_record"]
                   and "safe_root" not in static["sites"][0]["keywords"])
    same_constants = (serve_local.SCRIPT_MODEL is audio_overview.SCRIPT_MODEL
                      and serve_local.TTS_MODEL is audio_overview.TTS_MODEL)
    claims["structuralCause"] = {
        "claim": "the helper synthesizes the model map from the same constants derive_audio_capability "
                 "compares against, and passes the default safe_root=True",
        "singleConstructionSite": single_site,
        "sites": static["sites"],
        "enclosingFunctions": static["enclosingFunctions"],
        "serveConstantsAreTheLibraryConstants": same_constants,
        "holds": bool(single_site and same_constants),
    }

    # (4) A capability-state consumer sees the same narrow set through every server entry point.
    entry_reasons = {}
    for label, value in (("no key", None), ("configured", "configured")):
        with patch.object(serve_local, "resolve_google_key", return_value=value):
            handler_free_bootstrap = serve_local.LocalHandler._bootstrap_value(
                types.SimpleNamespace(server=None))
            entry_reasons[f"_bootstrap_value ({label})"] = handler_free_bootstrap["audio_capability"]["reason"]
            entry_reasons[f"audio_capability() ({label})"] = serve_local.audio_capability()["reason"]
            entry_reasons[f"_audio_capability_record() ({label})"] = \
                serve_local._audio_capability_record().reason
            entry_reasons[f"audio.create plan branch ({label})"] = audio_overview.audio_plan_status(
                serve_local._audio_capability_record())["capability"]["reason"]
    claims["entryPointReasons"] = {
        "observed": entry_reasons,
        "reachableSet": sorted(set(entry_reasons.values())),
        "holds": sorted(set(entry_reasons.values())) == ["GEMINI_AUTH_UNAVAILABLE", "READY"],
    }

    # (5) The library really does reach the other two directly.
    direct = {
        "GEMINI_MODEL_UNAVAILABLE": audio_overview.derive_audio_capability(
            auth="configured", models={}).reason,
        "AUDIO_TEMP_RECOVERY_AMBIGUOUS": audio_overview.derive_audio_capability(
            auth="configured", models=MODELS, safe_root=False).reason,
    }
    claims["libraryReachesBoth"] = {
        "claim": "both are covered by direct library tests",
        "observed": direct,
        "holds": all(key == value for key, value in direct.items()),
    }

    # (6) The docstring also claims those two are covered by *shipped* tests.
    shipped = {}
    for reason in ("GEMINI_MODEL_UNAVAILABLE", "AUDIO_TEMP_RECOVERY_AMBIGUOUS"):
        hits = []
        for path in sorted((PIPELINE / "tests").glob("test_*.py")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for number, line in enumerate(text.splitlines(), 1):
                if reason in line:
                    hits.append(f"pipeline/tests/{path.name}:{number}")
        shipped[reason] = hits
    claims["shippedTestCoverage"] = {
        "claim": "neither is supplied here yet, and both are covered by direct library tests",
        "observed": shipped,
        "holds": all(bool(hits) for hits in shipped.values()),
    }

    # (7) The docstring's stray-key claim.
    declared = sorted(field.name for field in fields(AudioCapabilityV1))
    claims["strayModelsKey"] = {
        "claim": "hand-building the dict here shipped an extra `models` key that AudioCapabilityV1 "
                 "does not declare",
        "declaredFields": declared,
        "holds": "models" not in declared and "model" in declared,
    }

    # (8) The unreachability rests on constant identity, not on structure: show it is falsifiable.
    with patch.object(serve_local, "resolve_google_key", return_value="configured"), \
            patch.object(serve_local, "SCRIPT_MODEL", "some-other-model"):
        rebound = serve_local.audio_capability()["reason"]
    claims["falsifiability"] = {
        "note": "rebinding serve_local.SCRIPT_MODEL makes GEMINI_MODEL_UNAVAILABLE reachable, which "
                "confirms the docstring's 'today' scope is a statement about the constants, not about "
                "a structural impossibility",
        "observedWhenRebound": rebound,
        "holds": rebound == "GEMINI_MODEL_UNAVAILABLE",
    }

    understated = [name for name, claim in claims.items() if not claim.get("holds", True)]
    overstated = []
    if claims["serverReachableReasons"]["reachableSet"] != ["GEMINI_AUTH_UNAVAILABLE", "READY"]:
        overstated.append("a third reason is reachable from the server, or one of the two named is not")
    accurate = not understated and not overstated

    record(
        "docstring accuracy: serve_local.audio_capability() claims only GEMINI_AUTH_UNAVAILABLE and "
        "READY are reachable from the server, and that the other two are library-only",
        "every sub-claim holds in both directions: no third reason is reachable from any server entry "
        "point, both named reasons ARE reachable, the library reaches the other two directly, shipped "
        "tests cover them, and `models` is not a declared field",
        f"reachable from server = {claims['serverReachableReasons']['reachableSet']} across "
        f"{len(server_reasons)} probes; entry points = {claims['entryPointReasons']['reachableSet']}; "
        f"library direct = {direct}; shipped coverage = "
        + json.dumps({key: len(value) for key, value in shipped.items()})
        + f"; declared fields = {declared}; failed sub-claims = {understated or 'none'}",
        "passed" if accurate else "failed",
    )
    if not accurate:
        finding(
            "A6-QA-DOCSTRING",
            "medium",
            "The serve_local.audio_capability() docstring is inaccurate.",
            json.dumps({"failedSubClaims": understated, "overstated": overstated}, ensure_ascii=False),
            True,
        )
    return {"docstring": docstring.strip(), "claims": claims, "failedSubClaims": understated,
            "overstated": overstated, "accurate": accurate}


NODE_PARITY = r"""
import fs from 'node:fs';
const payload = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const results = {};
for (const [label, capability] of Object.entries(payload.capabilities)) {
  const doc = {
    readyState: 'complete',
    getElementById: () => null,
    addEventListener: () => {},
  };
  globalThis.document = doc;
  globalThis.window = globalThis;
  globalThis._AUDIO_CAPABILITY = capability === null ? undefined : capability;
  (0, eval)(payload.js);
  results[label] = globalThis.openAudioModal();
}
process.stdout.write(JSON.stringify(results));
"""


def case_browser_parity() -> dict:
    """The browser half of the contract must emit byte-identical discriminated pairs."""
    capabilities = {
        "unavailable": audio_overview.derive_audio_capability(auth="", models=MODELS).to_dict(),
        "available": audio_overview.derive_audio_capability(auth="configured", models=MODELS).to_dict(),
        "modelUnavailable": audio_overview.derive_audio_capability(auth="c", models={}).to_dict(),
        "ambiguousRoot": audio_overview.derive_audio_capability(
            auth="c", models=MODELS, safe_root=False).to_dict(),
        "missingBootstrap": None,
    }
    with tempfile.TemporaryDirectory(prefix="g005-parity-") as directory:
        root = Path(directory)
        (root / "payload.json").write_text(json.dumps(
            {"js": audio_overview.AUDIO_JS, "capabilities": capabilities}, ensure_ascii=False), encoding="utf-8")
        (root / "parity.mjs").write_text(NODE_PARITY, encoding="utf-8")
        code, output = run(["node", str(root / "parity.mjs"), str(root / "payload.json")],
                           cwd=REPOSITORY, label="node AUDIO_JS openAudioModal parity")
    if code != 0:
        record("browser parity: AUDIO_JS openAudioModal returns the same discriminated pair as Python",
               "node evaluates the shipped asset and reproduces the Python payload exactly",
               f"node exited {code}: {tail(output)}", "failed")
        return {"exitCode": code, "output": tail(output)}

    observed = json.loads(output)
    mismatches = {}
    for label, capability in capabilities.items():
        if capability is None:
            continue
        expected = audio_overview.audio_plan_status(
            AudioCapabilityV1(**capability))
        if observed.get(label) != expected:
            mismatches[label] = {"python": expected, "javascript": observed.get(label)}
    fallback = observed.get("missingBootstrap")
    fallback_ok = (isinstance(fallback, dict) and fallback.get("schema") == 1
                   and fallback.get("result") == "FEATURE_UNAVAILABLE"
                   and set(fallback) == {"schema", "result", "capability"})

    record(
        "browser parity: AUDIO_JS openAudioModal emits exactly the Python discriminated pair",
        "for all four reason codes the JS object deep-equals audio_plan_status(...) including key order-"
        "insensitive key sets, and a missing bootstrap still yields a tagged FEATURE_UNAVAILABLE",
        f"4 capabilities compared, mismatches={json.dumps(mismatches, ensure_ascii=False) if mismatches else 'none'}; "
        f"missing-bootstrap fallback={json.dumps(fallback, ensure_ascii=False)}",
        "passed" if not mismatches and fallback_ok else "failed",
    )
    return {"exitCode": code, "observed": observed, "mismatches": mismatches,
            "missingBootstrapFallback": fallback, "fallbackTagged": fallback_ok}


class _LiveServer:
    def __init__(self):
        self.server = serve_local.ThreadingHTTPServer(("127.0.0.1", 0), serve_local.LocalHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        raw = response.read()
        head = {key.lower(): value for key, value in response.getheaders()}
        connection.close()
        return response.status, head, json.loads(raw)


def case_wire_e2e() -> dict:
    """Drive the real loopback route end to end and prove the branch is non-mutating."""
    live = _LiveServer()
    try:
        authority = "127.0.0.1:%d" % live.port
        with patch.object(serve_local, "resolve_google_key", return_value=None):
            status, headers, bootstrap = live.request("GET", "/api/bootstrap", headers={"Host": authority})
            cookie = headers["set-cookie"].split(";", 1)[0]
            body = json.dumps({
                "schema": 1, "command": "audio.create", "topic_alias": "qa-topic",
                "input": {"auth_mode": "auto", "requested_target_seconds": 300},
                "limits": {},
            }).encode("utf-8")
            plan_status, _plan_headers, plan = live.request("POST", "/api/action/plan", body, {
                "Host": authority, "Origin": "http://" + authority,
                "Content-Type": "application/json", "Content-Length": str(len(body)),
                "Cookie": cookie,
            })
            expected = audio_overview.audio_plan_status(serve_local._audio_capability_record())
        state = serve_local._wire_state(live.server)
        plans = dict(state.consent._plans)
        approvals = dict(state.consent._approvals)
        capabilities = len(state.capabilities)
    finally:
        live.close()

    exact = plan == expected
    keys_exact = set(plan) == {"schema", "result", "capability"}
    tagged = plan.get("result") == "FEATURE_UNAVAILABLE"
    retired_absent = not ({"mutated", "feature", "state", "reason"} & set(plan))
    non_mutating = not plans and not approvals and capabilities == 1
    no_operation = "operation_id" not in plan and "plan_hash" not in plan

    record(
        "wire e2e: POST /api/action/plan {command: audio.create} on a real loopback server returns the "
        "discriminated unavailable pair and creates nothing",
        "200 with a payload byte-identical to audio_plan_status(_audio_capability_record()), key set "
        "exactly {schema, result, capability}, no retired top-level key, and zero plans / approvals / "
        "extra capabilities in the consent store",
        f"status={plan_status}, payload={json.dumps(plan, ensure_ascii=False)}, matchesLibrary={exact}, "
        f"plans={len(plans)}, approvals={len(approvals)}, capabilityTokens={capabilities}",
        "passed" if (plan_status == 200 and exact and keys_exact and tagged and retired_absent
                     and non_mutating and no_operation) else "failed",
    )
    record(
        "wire e2e: /api/bootstrap still publishes the capability record under its own top-level key",
        "bootstrap.audio_capability is the AudioCapabilityV1 record (the browser reads this key), and it "
        "is not the discriminated plan payload",
        f"status={status}, bootstrap.audio_capability="
        + json.dumps(bootstrap.get("audio_capability"), ensure_ascii=False)
        + f", top-level keys={sorted(bootstrap)}",
        "passed" if (status == 200
                     and set(bootstrap.get("audio_capability", {})) == set(AudioCapabilityV1().to_dict())
                     and "result" not in bootstrap) else "failed",
    )
    return {
        "planStatusCode": plan_status,
        "planPayload": plan,
        "matchesLibraryPayload": exact,
        "keySetExact": keys_exact,
        "retiredKeysAbsent": retired_absent,
        "consentPlansCreated": len(plans),
        "approvalsCreated": len(approvals),
        "capabilityTokens": capabilities,
        "bootstrapAudioCapability": bootstrap.get("audio_capability"),
        "bootstrapTopLevelKeys": sorted(bootstrap),
    }


def adversarial_cases() -> dict:
    return {
        "reasonToResult": case_reason_to_result(),
        "keySetExactness": case_key_set_exactness(),
        "purity": case_purity(),
        "secretSafety": case_secret_safety(),
        "docstringAccuracy": case_docstring_accuracy(),
        "browserParity": case_browser_parity(),
        "wireEndToEnd": case_wire_e2e(),
    }


# --------------------------------------------------------------------------
# 3. stale reader scan
# --------------------------------------------------------------------------
SCAN_DIRECTORIES = ("pipeline", "docs/public", "bin", "scripts", "tests", "worker", "skills")
SCAN_ROOT_GLOBS = ("*.md", "*.json", "*.mjs", "*.js", "*.toml", "*.txt")
SCAN_SUFFIXES = {".py", ".js", ".mjs", ".json", ".md", ".html", ".css", ".toml", ".txt", ".sh", ".template"}
SCAN_EXCLUDE_PARTS = {
    "__pycache__", "_cache", "_logs", "_smoke", "_archive", "_state", ".pytest_cache",
    "node_modules", ".git", ".gjc", "vendor", "artifacts",
}
RETIRED_KEY_RE = re.compile(r"\bmutated\b")
AUDIO_CAPABILITY_RE = re.compile(r"\baudio_capability\b")
GENERATED_TREES = ("pipeline/_smoke", "pipeline/_archive", "pipeline/_logs")


def _scan_files():
    seen = set()
    for directory in SCAN_DIRECTORIES:
        base = REPOSITORY / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            if SCAN_EXCLUDE_PARTS & set(path.relative_to(REPOSITORY).parts):
                continue
            if path.resolve() not in seen:
                seen.add(path.resolve())
                yield path
    for pattern in SCAN_ROOT_GLOBS:
        for path in sorted(REPOSITORY.glob(pattern)):
            if path.name.startswith("config.json"):
                continue
            if path.is_file() and path.resolve() not in seen:
                seen.add(path.resolve())
                yield path


def _classify_mutated(relative: str, line: str) -> tuple[str, str]:
    if relative.startswith("pipeline/tests/qa_g00") and relative.endswith("_adversarial.py"):
        return ("qa-harness", "this red-team harness names the retired key in its own assertions, "
                              "scanner rules, and scratch-copy fragments; it is not production code")
    if relative == "pipeline/tests/test_audio_optional_capability.py":
        return ("negative-assertion", "asserts the retired `mutated` key is ABSENT from the payload; this "
                                      "is the guard, not a reader")
    if relative.startswith("pipeline/tests/test_child_context_transport.py"):
        return ("unrelated-identifier", "local helper `_mutated_frame` for the child-context transport "
                                        "tamper tests; nothing to do with the audio plan payload")
    if relative.startswith("pipeline/tests/test_deploy_cli_boundary.py"):
        return ("unrelated-identifier", "deploy staging tamper test name/fixture text; unrelated to the "
                                        "audio plan payload")
    return ("UNCLASSIFIED", "no rule matched")


def _classify_audio_capability(relative: str, line: str) -> tuple[str, str]:
    stripped = line.strip()
    if relative == "pipeline/serve_local.py":
        if "_audio_capability_record" in stripped or "def audio_capability" in stripped:
            return ("producer", "the single server-side capability producer / its typed variant")
        if '"audio_capability": audio_capability()' in stripped:
            return ("bootstrap-producer", "publishes the AudioCapabilityV1 record under the bootstrap "
                                          "top-level key; unaffected by the plan payload shape")
        if 'audio_capability()["state"]' in stripped:
            return ("producer", "gate on the produced capability state before the discriminated branch")
        return ("producer", "server-side capability production or its docstring")
    if relative in {"pipeline/build_topic_index.py", "pipeline/review_to_html.py"}:
        return ("page-context-embed", "bakes a static UNAVAILABLE AudioCapabilityV1 into the page "
                                      "bootstrap JSON; it is a capability record, not a plan response")
    if relative == "docs/public/paper-curation-local.js":
        return ("bootstrap-response-reader", "reads ACTION.bootstrap.audio_capability, i.e. the "
                                             "/api/bootstrap response, NOT the /api/action/plan response; "
                                             "unaffected by the A6 payload change")
    if relative.startswith("pipeline/tests/qa_g00") and relative.endswith("_adversarial.py"):
        return ("qa-harness", "red-team harness probing the produced capability record out of band; "
                              "not production code and not a wire client")
    if relative.startswith("pipeline/tests/") or relative.startswith("pipeline/lib/"):
        return ("test-or-library", "test/library reference to the capability record surface, all of "
                                   "which read the bootstrap-style record and never the plan response")
    if relative == "pipeline/generate_workflow.py":
        return ("documentation", "generated operator documentation describing the bootstrap capability")
    return ("UNCLASSIFIED", "no rule matched")


def stale_reader_scan() -> dict:
    mutated_hits, capability_hits = [], []
    for path in _scan_files():
        relative = str(path.relative_to(REPOSITORY))
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            if RETIRED_KEY_RE.search(line):
                kind, why = _classify_mutated(relative, line)
                mutated_hits.append({"file": relative, "line": number, "text": clip(line.strip(), 200),
                                     "classification": kind, "why": why})
            if AUDIO_CAPABILITY_RE.search(line):
                kind, why = _classify_audio_capability(relative, line)
                capability_hits.append({"file": relative, "line": number, "text": clip(line.strip(), 200),
                                        "classification": kind, "why": why})

    # Which properties does the owned browser asset actually read off a plan response?
    asset = (REPOSITORY / "docs/public/paper-curation-local.js").read_text(encoding="utf-8")
    plan_reads = sorted(set(re.findall(r"\bplan\.([A-Za-z_][A-Za-z0-9_]*)", asset)))
    reads_retired = sorted(set(plan_reads) & {"mutated", "feature", "state", "reason", "audio_capability"})
    reads_discriminator = "result" in plan_reads

    # Python readers of an audio_plan_status(...) payload.
    python_readers = []
    for path in sorted(PIPELINE.rglob("*.py")):
        if SCAN_EXCLUDE_PARTS & set(path.relative_to(REPOSITORY).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            if "audio_plan_status(" in line:
                python_readers.append({
                    "file": str(path.relative_to(REPOSITORY)), "line": number,
                    "text": clip(line.strip(), 200),
                    "subscripts": sorted(set(re.findall(r'audio_plan_status\([^)]*\)\["([a-z_]+)"\]', line))),
                })

    # Gitignored generated trees still holding the pre-retrofit browser modal.
    generated = []
    for tree in GENERATED_TREES:
        base = REPOSITORY / tree
        if not base.is_dir():
            continue
        matches = [str(item.relative_to(REPOSITORY)) for item in base.rglob("*.html")
                   if "openAudioModal" in item.read_text(encoding="utf-8", errors="replace")]
        ignored = subprocess.run(["git", "check-ignore", "-v", tree], cwd=REPOSITORY,
                                 capture_output=True, text=True)
        generated.append({
            "tree": tree,
            "htmlFilesWithLegacyModal": len(matches),
            "examples": matches[:3],
            "gitCheckIgnore": clip((ignored.stdout or ignored.stderr), 120),
            "classification": "non-shipped generated artifact",
            "why": "gitignored smoke/archive output from a pre-retrofit run; never imported, never "
                   "deployed, and regenerated by the next pipeline run",
        })

    unclassified = [hit for hit in mutated_hits + capability_hits if hit["classification"] == "UNCLASSIFIED"]
    breaking = [hit for hit in capability_hits if hit["classification"] == "plan-response-reader"]

    record(
        "stale-reader scan: no surviving reader of the retired `mutated` key",
        "every `mutated` occurrence in the shipped tree is either the negative assertion that guards the "
        "removal or an unrelated identifier",
        f"{len(mutated_hits)} hit(s): "
        + json.dumps([f"{hit['file']}:{hit['line']} [{hit['classification']}]" for hit in mutated_hits]),
        "passed" if not any(hit["classification"] == "UNCLASSIFIED" for hit in mutated_hits) else "failed",
    )
    record(
        "stale-reader scan: no reader treats `audio_capability` as a top-level key of the PLAN response",
        "every `audio_capability` occurrence is a producer, a page-context embed, a /api/bootstrap "
        "response reader, or a test; none reads it off /api/action/plan",
        f"{len(capability_hits)} hit(s) across "
        + json.dumps(sorted({hit['file'] for hit in capability_hits}))
        + f"; breaking={breaking or 'none'}; unclassified="
        + (json.dumps([f"{hit['file']}:{hit['line']}" for hit in unclassified]) if unclassified else "none"),
        "passed" if not breaking and not unclassified else "failed",
    )
    record(
        "stale-reader scan: the owned browser asset's plan-response property reads survive the new shape",
        "docs/public/paper-curation-local.js reads only {operation_id, plan_hash, preview} off the plan "
        "response, so the discriminated payload degrades to its explicit unavailable message",
        f"plan.* reads = {plan_reads}; retired-key reads = {reads_retired or 'none'}; "
        f"switches on the new `result` discriminator = {reads_discriminator}",
        "passed" if not reads_retired else "failed",
    )
    if not reads_discriminator:
        finding(
            "A6-QA-2",
            "low",
            "The owned browser asset does not yet switch on the new `result` discriminator: it still "
            "infers unavailability from the ABSENCE of `operation_id`/`plan_hash`, which is the exact "
            "inference pattern A6 set out to remove.",
            "docs/public/paper-curation-local.js runLocalAction(): "
            "`if (!plan.operation_id || !plan.plan_hash) { actionStatus('This action is unavailable …') }`. "
            "Not a regression — the retired shape also lacked those keys, so behavior is unchanged and "
            "the wire e2e confirms the user-visible outcome is correct. Adoption of `result` on the "
            "client is follow-up work, not an A6 defect.",
            False,
        )

    return {
        "scannedDirectories": list(SCAN_DIRECTORIES),
        "excludedPathParts": sorted(SCAN_EXCLUDE_PARTS),
        "mutatedKeyHits": mutated_hits,
        "audioCapabilityHits": capability_hits,
        "planResponsePropertyReadsInOwnedAsset": plan_reads,
        "retiredKeyReadsInOwnedAsset": reads_retired,
        "assetSwitchesOnResult": reads_discriminator,
        "pythonPlanStatusReaders": python_readers,
        "generatedArtifactTrees": generated,
        "unclassified": unclassified,
        "breakingReaders": breaking,
        "conclusion": (
            "No surviving reader of the retired payload exists in the shipped tree. "
            f"{len(mutated_hits)} `mutated` hit(s) are the negative guard plus unrelated identifiers; "
            f"{len(capability_hits)} `audio_capability` hit(s) are producers, page-context embeds, or "
            "readers of the /api/bootstrap response — a different payload that A6 did not change. "
            "The only `audio_capability` consumer in JavaScript reads ACTION.bootstrap.audio_capability, "
            "never the plan response."
        ),
    }


# --------------------------------------------------------------------------
# 4. required suite
# --------------------------------------------------------------------------
def required_suite() -> dict:
    code, output = run([sys.executable, "-m", "pytest", "pipeline/tests", "-q", "-p", "no:cacheprovider"],
                       cwd=REPOSITORY, label="full python suite")
    summary = tail(output, 2)
    record(
        "suite: python3 -m pytest pipeline/tests -q",
        "exit 0, every test passes",
        f"exit {code}: {summary}",
        "passed" if code == 0 else "failed",
    )
    return {"exitCode": code, "summary": summary}


def main() -> int:
    parser = argparse.ArgumentParser(description="Adversarial QA harness for G005 / A6")
    parser.add_argument("--report", default="artifacts/g005-a6-qa-report.json")
    arguments = parser.parse_args()

    proof = discriminator_proof()
    adversarial = adversarial_cases()
    scan = stale_reader_scan()
    suite = required_suite()

    passed = sum(1 for item in RESULTS if item["verdict"] == "passed")
    failed = sum(1 for item in RESULTS if item["verdict"] == "failed")
    contract_failures = [item["case"] for item in RESULTS
                         if item["verdict"] == "failed" and item["case"] not in INFORMATIONAL_CASES]
    informational_failures = [item["case"] for item in RESULTS
                              if item["verdict"] == "failed" and item["case"] in INFORMATIONAL_CASES]
    report = {
        "schemaVersion": 1,
        "kind": "package-test-report",
        "goal": "G005",
        "contract": "A6 discriminated audio plan status",
        "surface": "Python package (pipeline/) plus its owned browser asset",
        "verdict": {
            "contract": "UPHELD" if not contract_failures else "BROKEN",
            "contractFailures": contract_failures,
            "informationalFailures": informational_failures,
            "note": "`summary.failed` counts every case with a failed verdict, including the "
                    "informational coverage probe. A coverage probe failure means the shipped suite "
                    "would not catch a regression in that surface; it is NOT a regression in the "
                    "shipped behavior, which the browser-parity and wire e2e cases prove correct.",
        },
        "commands": COMMANDS,
        "results": RESULTS,
        "discriminatorProof": proof,
        "adversarialCases": adversarial,
        "staleReaderScan": scan,
        "requiredSuite": suite,
        "findings": FINDINGS,
        "summary": {"passed": passed, "failed": failed},
    }

    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    # Fail closed rather than persist a real credential that a matrix may have touched.
    for name in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        live = os.environ.get(name, "").strip()
        if live and live != SENTINEL and live in serialized:
            raise SystemExit(f"refusing to write the report: a live {name} value reached the payload")
    destination = Path(arguments.report)
    if not destination.is_absolute():
        destination = REPOSITORY / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(serialized, encoding="utf-8")
    print(f"\nwrote {destination} (passed={passed} failed={failed} findings={len(FINDINGS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
