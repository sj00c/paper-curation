#!/usr/bin/env python3
"""Adversarial QA harness for G004 (one canonical Gemini key resolver + exit 5).

This file is deliberately not named ``test_*.py``: it is a red-team harness, not
part of the default suite.  Run it explicitly from the repository root::

    python3 pipeline/tests/qa_g004_adversarial.py

It never mutates the production modules.  Every "old behavior" variant is
materialized in a throwaway copy of the tree under a temporary directory, and
the shipped test files are executed verbatim against that copy so the tests
themselves are proven to be real discriminators.  Adversarial matrices run
in-process against the real modules with ``patch.dict``/``patch.object`` only.

No network call is ever made: the google-genai SDK is replaced by an in-memory
stub that records the api_key it was handed instead of contacting a provider.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
import types
from pathlib import Path
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[2]
PIPELINE = REPOSITORY / "pipeline"
for _entry in (str(REPOSITORY), str(PIPELINE)):
    if _entry not in sys.path:
        sys.path.insert(0, _entry)

import build_search_index  # noqa: E402
import config_loader  # noqa: E402
import doctor as doctor_module  # noqa: E402
import extract_insights  # noqa: E402
import run_update_force  # noqa: E402
import serve_local  # noqa: E402

RESOLVER_TESTS = "pipeline/tests/test_gemini_key_resolver.py"
EXIT_TESTS = "pipeline/tests/test_search_index_exit_codes.py"
HONESTY_TESTS = "pipeline/tests/test_gemini_call_site_honesty.py"
TLS_TESTS = "pipeline/tests/test_tls_security.py"

AGREEMENT = f"{RESOLVER_TESTS}::GeminiKeyResolverAgreementTests::test_every_call_site_resolves_identically"
DISABLE_SWITCH = f"{RESOLVER_TESTS}::GeminiKeyResolverAgreementTests::test_disable_switch_beats_a_configured_key_everywhere"
ONE_RESOLVER = f"{RESOLVER_TESTS}::GeminiKeyResolverAgreementTests::test_call_sites_share_one_resolver_object"
EXIT_FIVE = f"{EXIT_TESTS}::SearchIndexExitCodeTests::test_missing_key_exits_five_with_embeddings_unavailable"
EXIT_ONE = f"{EXIT_TESTS}::SearchIndexExitCodeTests::test_missing_google_genai_package_still_exits_one"

# A value no production string may echo back to an operator.
SENTINEL = "AIzaSyG004-QA-SENTINEL-do-not-log-8f3c1d"
WHITESPACE_KEY = "   "

# The contract suite: every shipped test module that imports one of the modules
# carrying a Gemini key-resolution call site.  A regression that this subset
# cannot see is a coverage gap, not a caught regression.
CONTRACT_MODULES = ("serve_local", "build_search_index", "config_loader", "doctor", "extract_insights")

RESULTS: list[dict] = []
COMMANDS: list[dict] = []
FINDINGS: list[dict] = []


# --------------------------------------------------------------------------
# reporting helpers
# --------------------------------------------------------------------------
def record(case: str, expected: str, observed: str, verdict: str) -> None:
    RESULTS.append({"case": case, "expected": expected, "observed": observed, "verdict": verdict})
    print(f"[{verdict.upper():>6}] {case}\n         observed: {observed}", flush=True)


def clip(value: str, limit: int) -> str:
    value = str(value).strip()
    return value if len(value) <= limit else value[:limit] + " …"


def tail(text: str, lines: int = 10) -> str:
    kept = [clip(line.rstrip(), 200) for line in str(text).strip().splitlines() if line.strip()]
    return clip(" | ".join(kept[-lines:]), 1_200)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"scratch build: expected exactly one occurrence of {label} ({text.count(old)} found)")
    return text.replace(old, new)


# --------------------------------------------------------------------------
# pre-retrofit source fragments (recovered from `git show HEAD:...`)
# --------------------------------------------------------------------------
NEW_SERVE_RESOLVE = "    return get_google_key().strip() or None\n"
OLD_SERVE_RESOLVE_ENV_ONLY = (
    '    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or ""\n'
    "    return key.strip() or None\n"
)
NEW_SERVE_AVAILABLE = "    return bool(resolve_google_key())\n"
OLD_SERVE_AVAILABLE_ENV_ONLY = (
    '    return bool(os.environ.get("GOOGLE_API_KEY", "").strip()\n'
    '                or os.environ.get("GEMINI_API_KEY", "").strip())\n'
)

NEW_RESOLVER_FLAG = (
    '    if os.environ.get("PAPER_CURATION_NO_GEMINI"):\n'
    '        return ""\n'
    "    cfg = load_config()\n"
)
OLD_RESOLVER_NO_FLAG = "    cfg = load_config()\n"

NEW_SEARCH_INDEX_REFUSAL = (
    "    api_key = get_google_key()\n"
    "    if not api_key:\n"
    '        print("ERROR: EMBEDDINGS_UNAVAILABLE — no Gemini API key resolved "\n'
    '              "(GOOGLE_API_KEY/GEMINI_API_KEY env, or config.json "\n'
    '              "gemini_api_key/google_api_key).")\n'
    '        print("       Dense retrieval is unavailable; search degrades to "\n'
    '              "lexical-only until a key is configured.")\n'
    '        print("       PAPER_CURATION_NO_GEMINI forces this refusal even when a "\n'
    '              "key is configured.")\n'
    "        sys.exit(EXIT_EMBEDDINGS_UNAVAILABLE)\n"
)
OLD_SEARCH_INDEX_REFUSAL = (
    '    api_key = (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")\n'
    "               or _load_gemini_key_from_config())\n"
    "    if not api_key:\n"
    '        print("ERROR: GOOGLE_API_KEY or GEMINI_API_KEY is not set.")\n'
    '        print("       Add it to .env or the process environment; legacy config.json '
    'keys are read only for compatibility.")\n'
    "        sys.exit(1)\n"
)
OLD_SEARCH_INDEX_HELPER = (
    "def _load_gemini_key_from_config() -> str:\n"
    '    """Compatibility fallback for legacy configs; environment variables take precedence."""\n'
    "    try:\n"
    '        cfg_path = Path(__file__).resolve().parents[1] / "config.json"\n'
    "        if cfg_path.exists():\n"
    '            with open(cfg_path, "r", encoding="utf-8") as f:\n'
    "                cfg = json.load(f)\n"
    '            return (cfg.get("gemini_api_key") or cfg.get("google_api_key") or "") or ""\n'
    "    except Exception:\n"
    "        pass\n"
    '    return ""\n'
    "\n\n"
    "def require_embedding_client():\n"
)
NEW_SEARCH_INDEX_ANCHOR = "def require_embedding_client():\n"

NEW_INSIGHTS_RESOLUTION = "    api_key = get_google_key()\n"
OLD_INSIGHTS_RESOLUTION = (
    '    api_key = (os.environ.get("GEMINI_API_KEY")\n'
    '               or os.environ.get("GOOGLE_API_KEY")\n'
    '               or load_config().get("gemini_api_key", "")\n'
    '               or load_config().get("google_api_key", ""))\n'
)

NEW_DOCTOR_HONESTY = (
    "    if found and not get_google_key():\n"
    "        rep.warn(\n"
    '            "Gemini optional capability disabled",\n'
    '            f"키는 {src} 에 있으나 PAPER_CURATION_NO_GEMINI 로 비활성화되어 "\n'
    '            "모든 실제 호출 지점이 Gemini 를 사용하지 않습니다.",\n'
    '            "다시 사용하려면 PAPER_CURATION_NO_GEMINI 를 해제하세요.",\n'
    "        )\n"
    "    elif found:\n"
)
OLD_DOCTOR_HONESTY = "    if found:\n"


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
    topics (docs/papers, docs/ai4s, the public PDFs) are never read by the suite.
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


def build_scratch(destination: Path, *, serve="new", resolver="new", search_index="new",
                  insights="new", doctor="new") -> Path:
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

    if serve != "new":
        path = destination / "pipeline" / "serve_local.py"
        source = path.read_text(encoding="utf-8")
        if serve == "env_only_resolver":
            source = replace_once(source, NEW_SERVE_RESOLVE, OLD_SERVE_RESOLVE_ENV_ONLY, "resolve_google_key body")
        elif serve == "env_only_available":
            source = replace_once(source, NEW_SERVE_AVAILABLE, OLD_SERVE_AVAILABLE_ENV_ONLY,
                                  "gemini_api_key_available body")
        else:
            raise SystemExit(f"unknown serve variant {serve}")
        path.write_text(source, encoding="utf-8")

    if resolver != "new":
        path = destination / "pipeline" / "config_loader.py"
        source = path.read_text(encoding="utf-8")
        source = replace_once(source, NEW_RESOLVER_FLAG, OLD_RESOLVER_NO_FLAG, "PAPER_CURATION_NO_GEMINI guard")
        path.write_text(source, encoding="utf-8")

    if search_index != "new":
        path = destination / "pipeline" / "build_search_index.py"
        source = path.read_text(encoding="utf-8")
        source = replace_once(source, NEW_SEARCH_INDEX_ANCHOR, OLD_SEARCH_INDEX_HELPER, "require_embedding_client def")
        source = replace_once(source, NEW_SEARCH_INDEX_REFUSAL, OLD_SEARCH_INDEX_REFUSAL, "exit-5 refusal block")
        path.write_text(source, encoding="utf-8")

    if insights != "new":
        path = destination / "pipeline" / "extract_insights.py"
        source = path.read_text(encoding="utf-8")
        source = replace_once(source, NEW_INSIGHTS_RESOLUTION, OLD_INSIGHTS_RESOLUTION, "_cc_gemini_call resolution")
        path.write_text(source, encoding="utf-8")

    if doctor != "new":
        path = destination / "pipeline" / "doctor.py"
        source = path.read_text(encoding="utf-8")
        source = replace_once(source, NEW_DOCTOR_HONESTY, OLD_DOCTOR_HONESTY, "doctor Gemini honesty branch")
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


def run_variant(label: str, node_ids: list[str], **variant: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="g004-qa-") as directory:
        scratch = build_scratch(Path(directory) / "tree", **variant)
        return run([sys.executable, "-m", "pytest", *node_ids, "-q", "--tb=line", "-p", "no:cacheprovider"],
                   cwd=scratch, label=label)


def contract_suite() -> list[str]:
    """Shipped test modules that import a module holding a key-resolution call site."""
    selected = []
    for path in sorted((PIPELINE / "tests").glob("test_*.py")):
        source = path.read_text(encoding="utf-8", errors="replace")
        if any(re.search(rf"^\s*import {module}\b|^\s*from {module} import", source, re.MULTILINE)
               for module in CONTRACT_MODULES):
            selected.append(f"pipeline/tests/{path.name}")
    return selected


def failing_nodes(output: str) -> set[str]:
    """Node ids from pytest's short summary, including pytest-subtests SUBFAILED lines."""
    nodes = set()
    for line in output.splitlines():
        match = re.search(r"(?:^FAILED|^ERROR|^SUBFAILED\([^)]*\))\s+(\S+::\S+)", line.strip())
        if match:
            nodes.add(match.group(1))
    return nodes


# --------------------------------------------------------------------------
# in-process probes: the fake SDK never contacts a provider
# --------------------------------------------------------------------------
class ProviderReached(RuntimeError):
    """Raised by the stub when a call site actually tries to generate content."""


class StubModels:
    def __init__(self, client): self.client = client

    def generate_content(self, **kwargs):
        raise ProviderReached(f"generate_content reached with api_key={self.client.api_key!r}")

    def embed_content(self, **kwargs):
        raise ProviderReached(f"embed_content reached with api_key={self.client.api_key!r}")


class StubClient:
    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        self.models = StubModels(self)


def stub_sdk() -> dict[str, types.ModuleType]:
    genai = types.ModuleType("google.genai")
    genai.Client = StubClient
    gtypes = types.ModuleType("google.genai.types")

    class _Config:
        def __init__(self, **kwargs): self.kwargs = kwargs

    class _Part:
        @staticmethod
        def from_bytes(**kwargs): return kwargs

    gtypes.GenerateContentConfig = _Config
    gtypes.EmbedContentConfig = _Config
    gtypes.Part = _Part
    genai.types = gtypes
    google = types.ModuleType("google")
    google.genai = genai
    return {"google": google, "google.genai": genai, "google.genai.types": gtypes}


def doctor_gemini_report(cfg: dict) -> str:
    """Run doctor's real Gemini branch; the unrelated Anthropic/TLS probes are stubbed out."""
    reporter = doctor_module.Reporter()
    buffer = io.StringIO()
    status = types.SimpleNamespace(ready=False, mode=None)
    with patch.object(doctor_module, "_check_secret_sources", lambda *a, **k: None), \
            patch.object(doctor_module, "_check_tls_status", lambda *a, **k: None), \
            patch.object(doctor_module, "_check_anthropic_auth", lambda *a, **k: status), \
            contextlib.redirect_stdout(buffer):
        doctor_module.check_api_keys(reporter, cfg)
    lines = [line for line in buffer.getvalue().splitlines() if "Gemini" in line or "GOOGLE_API_KEY" in line]
    return " | ".join(line.strip() for line in lines)


def probe_call_sites(env: dict, config: dict) -> dict:
    """Every Gemini call site under one (env, config.json) matrix."""
    observed: dict[str, str] = {}
    present: dict[str, bool] = {}
    with patch.dict(os.environ, env, clear=False), \
            patch.object(config_loader, "load_config", return_value=config), \
            patch.dict(sys.modules, stub_sdk(), clear=False):
        resolved = config_loader.get_google_key()
        observed["config_loader.get_google_key"] = repr(resolved)
        present["config_loader.get_google_key"] = bool(resolved)

        value = serve_local.resolve_google_key()
        observed["serve_local.resolve_google_key"] = repr(value)
        present["serve_local.resolve_google_key"] = value is not None

        available = serve_local.gemini_api_key_available()
        observed["serve_local.gemini_api_key_available"] = str(available)
        present["serve_local.gemini_api_key_available"] = bool(available)

        state = serve_local.audio_capability()["state"]
        observed["serve_local.audio_capability"] = state
        present["serve_local.audio_capability"] = state == "AVAILABLE"

        gate = bool(run_update_force.get_google_key().strip())
        observed["run_update_force figure gate"] = str(gate)
        present["run_update_force figure gate"] = gate

        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                client = build_search_index.require_embedding_client()
            observed["build_search_index.require_embedding_client"] = f"client(api_key={client.api_key!r})"
            present["build_search_index.require_embedding_client"] = True
        except SystemExit as exit_error:
            observed["build_search_index.require_embedding_client"] = f"exit:{exit_error.code}"
            present["build_search_index.require_embedding_client"] = False

        try:
            extract_insights._cc_gemini_call("prompt", {"name": "x", "input_schema": {}})
            observed["extract_insights._cc_gemini_call"] = "returned without provider call"
            present["extract_insights._cc_gemini_call"] = True
        except ProviderReached as reached:
            observed["extract_insights._cc_gemini_call"] = clip(str(reached), 90)
            present["extract_insights._cc_gemini_call"] = True
        except RuntimeError as error:
            observed["extract_insights._cc_gemini_call"] = f"RuntimeError: {clip(str(error), 70)}"
            present["extract_insights._cc_gemini_call"] = "no Gemini API key" not in str(error)

        report = doctor_gemini_report(config)
        observed["doctor Gemini report"] = clip(report, 200)
        present["doctor Gemini report"] = "설정됨" in report

    return {"observed": observed, "present": present, "unanimous": len(set(present.values())) == 1}


def matrix_env(google="", gemini="", flag="") -> dict:
    return {"GOOGLE_API_KEY": google, "GEMINI_API_KEY": gemini, "PAPER_CURATION_NO_GEMINI": flag}


def summarize(probe: dict) -> str:
    disagreeing = sorted(name for name, value in probe["present"].items() if value)
    absent = sorted(name for name, value in probe["present"].items() if not value)
    return (f"present-at: {disagreeing or 'none'}; absent-at: {absent or 'none'}; "
            f"raw: {json.dumps(probe['observed'], ensure_ascii=False)}")


# --------------------------------------------------------------------------
# 1. Discriminator proofs
# --------------------------------------------------------------------------
def discriminator_proof() -> dict:
    evidence: list[str] = []
    shipped = [RESOLVER_TESTS, EXIT_TESTS, HONESTY_TESTS, TLS_TESTS]

    control_code, control_output = run_variant("control scratch (verbatim copy)", shipped)
    record(
        "harness control: verbatim scratch copy runs the shipped resolver suites green",
        "exit 0 (the scratch harness itself introduces no failure)",
        f"exit {control_code}: {tail(control_output, 3)}",
        "passed" if control_code == 0 else "failed",
    )

    env_only_code, env_only_output = run_variant(
        "pre-change env-only serve_local.resolve_google_key", [AGREEMENT], serve="env_only_resolver")
    record(
        "discriminator A: old env-only serve_local chain vs test_every_call_site_resolves_identically",
        "test FAILS on the config-only matrix (env-only chain returns None where the resolver returns config-key)",
        f"exit {env_only_code}: {tail(env_only_output, 4)}",
        "passed" if env_only_code != 0 and "config-only" in env_only_output else "failed",
    )
    evidence.append(f"[env-only resolve_google_key / agreement] exit={env_only_code} :: {tail(env_only_output, 4)}")

    available_code, available_output = run_variant(
        "pre-change env-only gemini_api_key_available", [RESOLVER_TESTS, HONESTY_TESTS],
        serve="env_only_available")
    record(
        "discriminator A2: old env-only gemini_api_key_available() vs the capability-projection tests",
        "test FAILS: a config-only key must still report the Audio/Gemini capability as available",
        f"exit {available_code}: {tail(available_output, 5)}",
        "passed" if available_code != 0 else "failed",
    )
    evidence.append(f"[env-only gemini_api_key_available] exit={available_code} :: {tail(available_output, 5)}")

    flag_code, flag_output = run_variant(
        "pre-change resolver ignoring PAPER_CURATION_NO_GEMINI", [DISABLE_SWITCH], resolver="old_no_flag")
    record(
        "discriminator B: resolver without the PAPER_CURATION_NO_GEMINI guard vs test_disable_switch_beats_a_configured_key_everywhere",
        "test FAILS: every call site keeps resolving env-key while the disable switch is set",
        f"exit {flag_code}: {tail(flag_output, 4)}",
        "passed" if flag_code != 0 else "failed",
    )
    evidence.append(f"[resolver ignores the flag] exit={flag_code} :: {tail(flag_output, 4)}")

    site_flag_code, site_flag_output = run_variant(
        "one call site ignoring PAPER_CURATION_NO_GEMINI (env-only serve_local)", [DISABLE_SWITCH],
        serve="env_only_resolver")
    record(
        "discriminator B2: a single call site ignoring the disable switch vs test_disable_switch_beats_a_configured_key_everywhere",
        "test FAILS: serve_local reports env-key while the canonical resolver reports ''",
        f"exit {site_flag_code}: {tail(site_flag_output, 4)}",
        "passed" if site_flag_code != 0 else "failed",
    )
    evidence.append(f"[call site ignores the flag] exit={site_flag_code} :: {tail(site_flag_output, 4)}")

    exit_code_code, exit_code_output = run_variant(
        "pre-change build_search_index refusal (exit 1)", [EXIT_FIVE], search_index="old_exit1")
    record(
        "discriminator C: old exit-1 refusal vs test_missing_key_exits_five_with_embeddings_unavailable",
        "test FAILS with 1 != 5, so the new EMBEDDINGS_UNAVAILABLE code is genuinely asserted",
        f"exit {exit_code_code}: {tail(exit_code_output, 4)}",
        "passed" if exit_code_code != 0 else "failed",
    )
    evidence.append(f"[old exit-1 refusal] exit={exit_code_code} :: {tail(exit_code_output, 4)}")

    still_one_code, still_one_output = run_variant(
        "pre-change build_search_index refusal vs the dependency test", [EXIT_ONE], search_index="old_exit1")
    record(
        "discriminator C2: the exit-1 dependency test still passes against the old refusal",
        "exit 0 — the failure above is specifically 5-vs-1, not a blanket variant breakage",
        f"exit {still_one_code}: {tail(still_one_output, 3)}",
        "passed" if still_one_code == 0 else "failed",
    )
    evidence.append(f"[old refusal / dependency test] exit={still_one_code} :: {tail(still_one_output, 3)}")

    helper_code, helper_output = run_variant(
        "pre-change build_search_index local config chain", [ONE_RESOLVER], search_index="old_exit1")
    record(
        "discriminator C3: the reinstated _load_gemini_key_from_config helper vs test_call_sites_share_one_resolver_object",
        "test FAILS: a second key chain inside build_search_index is rejected by name",
        f"exit {helper_code}: {tail(helper_output, 4)}",
        "passed" if helper_code != 0 else "failed",
    )

    insights_code, insights_output = run_variant(
        "pre-change extract_insights local key chain", [HONESTY_TESTS], insights="old_local_chain")
    record(
        "discriminator D: old extract_insights local chain vs the call-site honesty tests",
        "test FAILS: _cc_gemini_call must resolve through the canonical resolver and honor the disable switch",
        f"exit {insights_code}: {tail(insights_output, 4)}",
        "passed" if insights_code != 0 else "failed",
    )
    evidence.append(f"[extract_insights local chain] exit={insights_code} :: {tail(insights_output, 4)}")

    doctor_code, doctor_output = run_variant(
        "pre-change doctor Gemini report", [HONESTY_TESTS], doctor="old_always_ok")
    record(
        "discriminator E: old doctor '설정됨' report vs the doctor honesty test",
        "test FAILS: doctor must not report Gemini as configured while the disable switch is set",
        f"exit {doctor_code}: {tail(doctor_output, 4)}",
        "passed" if doctor_code != 0 else "failed",
    )
    evidence.append(f"[doctor always-ok] exit={doctor_code} :: {tail(doctor_output, 4)}")

    return {
        "controlExitCode": control_code,
        "oldBehaviorFails": all(code != 0 for code in (
            env_only_code, available_code, flag_code, site_flag_code, exit_code_code,
            helper_code, insights_code, doctor_code)),
        "exitCodeDiscriminatorIsSpecific": exit_code_code != 0 and still_one_code == 0,
        "evidence": " || ".join(evidence),
    }


# --------------------------------------------------------------------------
# 2. Coverage probe: which regressions does the shipped contract suite see?
# --------------------------------------------------------------------------
def coverage_probe() -> dict:
    suite = contract_suite()
    control_code, control_output = run_variant("contract suite control (verbatim scratch)", suite)
    baseline = failing_nodes(control_output)
    record(
        "coverage baseline: the contract suite (every shipped module importing a call-site module) is green",
        "exit 0 with no failing node in a verbatim scratch copy",
        f"exit {control_code} over {len(suite)} modules: {tail(control_output, 2)}",
        "passed" if control_code == 0 and not baseline else "failed",
    )

    findings = []
    for label, variant, description in (
        ("env-only gemini_api_key_available", {"serve": "env_only_available"},
         "serve_local.gemini_api_key_available() regressed to an env-only chain"),
        ("extract_insights local key chain", {"insights": "old_local_chain"},
         "extract_insights._cc_gemini_call regressed to its own env→config chain"),
        ("doctor always reports 설정됨", {"doctor": "old_always_ok"},
         "doctor reports Gemini configured while PAPER_CURATION_NO_GEMINI is set"),
    ):
        code, output = run_variant(f"contract suite vs {label}", suite, **variant)
        new_failures = sorted(failing_nodes(output) - baseline)
        caught = code != 0 and bool(new_failures)
        findings.append({"regression": description, "caughtByContractSuite": caught,
                         "exitCode": code, "newFailures": new_failures[:8]})
        record(
            f"coverage probe: contract suite vs {label}",
            "the shipped contract suite FAILS with a new failing node (the regression is observable)",
            f"exit {code}; new failing nodes vs baseline: {new_failures[:8] or 'none'}",
            "passed" if caught else "failed",
        )
    # What the suite looked like before this QA lane added the call-site honesty module.
    inherited = [module for module in suite if not module.endswith("test_gemini_call_site_honesty.py")]
    gaps = []
    for label, variant, description in (
        ("env-only gemini_api_key_available", {"serve": "env_only_available"},
         "serve_local.gemini_api_key_available() / audio_capability() regressed to an env-only chain"),
        ("extract_insights local key chain", {"insights": "old_local_chain"},
         "extract_insights._cc_gemini_call regressed to its own env→config chain"),
        ("doctor always reports 설정됨", {"doctor": "old_always_ok"},
         "doctor reports Gemini configured while PAPER_CURATION_NO_GEMINI is set"),
    ):
        code, output = run_variant(f"inherited suite vs {label}", inherited, **variant)
        new_failures = sorted(failing_nodes(output) - baseline)
        invisible = code == 0 and not new_failures
        gaps.append({"regression": description, "invisibleToInheritedSuite": invisible, "exitCode": code,
                     "newFailures": new_failures[:8]})
        record(
            f"coverage gap (pre-lane): inherited suite vs {label}",
            "gap reproduced — the suite as inherited by this QA lane cannot observe the regression",
            f"exit {code}; new failing nodes: {new_failures[:8] or 'none'}",
            "passed" if invisible else "failed",
        )

    return {"contractSuite": suite, "baselineFailing": sorted(baseline), "regressions": findings,
            "inheritedSuite": inherited, "preexistingGaps": gaps,
            "gapClosedBy": "pipeline/tests/test_gemini_call_site_honesty.py (added by this QA lane; tests only)"}


# --------------------------------------------------------------------------
# 3. Adversarial matrices
# --------------------------------------------------------------------------
def adversarial_cases() -> dict:
    notes: dict = {}

    # --- whitespace-only keys ------------------------------------------------
    split_surfaces = []
    for label, env, config in (
        ("env", matrix_env(google=WHITESPACE_KEY), {}),
        ("config.json", matrix_env(), {"gemini_api_key": WHITESPACE_KEY}),
    ):
        probe = probe_call_sites(env, config)
        agree = probe["unanimous"]
        none_present = not any(probe["present"].values())
        record(
            f"adversarial: whitespace-only key ('   ') in {label}",
            "every call site agrees, and none treats a blank key as a configured key",
            summarize(probe),
            "passed" if agree and none_present else "failed",
        )
        notes[f"whitespaceOnly_{label}"] = probe["observed"]
        if not (agree and none_present):
            split_surfaces.append({
                "surface": label,
                "treatsBlankAsConfigured": sorted(n for n, v in probe["present"].items() if v),
                "treatsBlankAsAbsent": sorted(n for n, v in probe["present"].items() if not v),
            })
    if split_surfaces:
        FINDINGS.append({
            "id": "G004-QA-1",
            "severity": "medium",
            "title": "a whitespace-only Gemini key ('   ') splits the call sites",
            "detail": (
                "config_loader.get_google_key() returns the raw value without stripping, so a blank key is "
                "truthy. Sites that strip (serve_local.resolve_google_key, the run_update_force figure gate, "
                "doctor._resolve_key) report 'no key'; sites that only test truthiness "
                "(build_search_index.require_embedding_client, extract_insights._cc_gemini_call) accept it "
                "and construct genai.Client(api_key='   '). The documented exit-5 EMBEDDINGS_UNAVAILABLE "
                "refusal is therefore skipped for a blank key: the run fails later with an opaque provider "
                "auth error instead of degrading to lexical-only."
            ),
            "surfaces": split_surfaces,
            "preExisting": ("yes — the pre-retrofit chains did not strip either, so the retrofit did not "
                            "introduce it; but the 'every call site agrees' contract does not hold for it"),
            "suggestedFix": ("return the stripped value from config_loader.get_google_key() (one line); "
                             "NOT applied here — this lane must not change production behavior"),
        })

    # --- disable-switch semantics -------------------------------------------
    semantics = {}
    for value, expected_disabled in (("1", True), ("0", True), ("false", True), ("", False), ("   ", True)):
        probe = probe_call_sites(matrix_env(google="env-key", flag=value), {"gemini_api_key": "config-key"})
        disabled = not any(probe["present"].values())
        semantics[repr(value)] = {
            "disabled": disabled,
            "unanimous": probe["unanimous"],
            "observed": probe["observed"],
        }
        record(
            f"adversarial: PAPER_CURATION_NO_GEMINI={value!r} with a key configured",
            ("every call site agrees; documented semantics: any non-empty value disables, "
             "the empty string does not"),
            f"disabled={disabled} unanimous={probe['unanimous']}; " + summarize(probe),
            "passed" if probe["unanimous"] and disabled == expected_disabled else "failed",
        )
    notes["disableSwitchSemantics"] = {
        "rule": "os.environ.get() truthiness — any non-empty string disables Gemini, including '0' and 'false'; "
                "an empty or unset value leaves Gemini enabled",
        "matrix": {key: value["disabled"] for key, value in semantics.items()},
    }

    # --- config-only key, empty env -----------------------------------------
    probe = probe_call_sites(matrix_env(), {"gemini_api_key": "config-key"})
    proceeds = probe["observed"]["build_search_index.require_embedding_client"].startswith("client(")
    record(
        "adversarial: key only in config.json with an empty environment",
        "build_search_index proceeds with the config key instead of exiting 5",
        summarize(probe),
        "passed" if proceeds and probe["unanimous"] else "failed",
    )

    # --- dependency + key both missing --------------------------------------
    missing_sdk = {"google": None, "google.genai": None, "google.genai.types": None}
    buffer = io.StringIO()
    with patch.dict(os.environ, matrix_env(), clear=False), \
            patch.object(config_loader, "load_config", return_value={}), \
            patch.dict(sys.modules, missing_sdk, clear=False):
        try:
            with contextlib.redirect_stdout(buffer):
                build_search_index.require_embedding_client()
            code = "no exit"
        except SystemExit as exit_error:
            code = exit_error.code
    text = buffer.getvalue()
    record(
        "adversarial: google-genai missing AND no key resolvable",
        "the dependency check fires first (exit 1), keeping 1 and 5 distinguishable",
        f"exit={code}; stdout={tail(text, 3)}",
        "passed" if code == 1 and "EMBEDDINGS_UNAVAILABLE" not in text else "failed",
    )

    # --- patch-seam survival -------------------------------------------------
    original = serve_local.resolve_google_key
    with patch.dict(os.environ, matrix_env(google="env-key"), clear=False), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": "config-key"}):
        with patch.object(serve_local, "resolve_google_key", return_value=None) as stub:
            seam = {
                "resolve_google_key": serve_local.resolve_google_key(),
                "gemini_api_key_available": serve_local.gemini_api_key_available(),
                "audio_capability": serve_local.audio_capability()["state"],
                "audio_reason": serve_local.audio_capability()["reason"],
                "stub_calls": stub.call_count,
            }
        restored = serve_local.resolve_google_key is original
        live = serve_local.gemini_api_key_available()
    forced_unavailable = (seam["resolve_google_key"] is None and seam["gemini_api_key_available"] is False
                          and seam["audio_capability"] == "UNAVAILABLE" and seam["stub_calls"] >= 3)
    record(
        "adversarial: patch.object(serve_local, 'resolve_google_key', return_value=None) still forces every dependent site off",
        "the module attribute stays patchable, all dependents report unavailable, and the original is restored",
        f"{json.dumps(seam, ensure_ascii=False)}; restored={restored}; live-after-restore={live}",
        "passed" if forced_unavailable and restored and live else "failed",
    )
    notes["patchSeam"] = seam

    # --- secret leakage ------------------------------------------------------
    leaks: dict[str, str] = {}
    with patch.dict(os.environ, matrix_env(google=SENTINEL), clear=False), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": SENTINEL}), \
            patch.dict(sys.modules, stub_sdk(), clear=False):
        leaks["audio_capability payload"] = json.dumps(serve_local.audio_capability(), ensure_ascii=False)
        leaks["doctor Gemini report"] = doctor_gemini_report({"gemini_api_key": SENTINEL})
    with patch.dict(os.environ, matrix_env(google=SENTINEL, flag="1"), clear=False), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": SENTINEL}), \
            patch.dict(sys.modules, stub_sdk(), clear=False):
        buffer = io.StringIO()
        with contextlib.suppress(SystemExit), contextlib.redirect_stdout(buffer):
            build_search_index.require_embedding_client()
        leaks["exit-5 refusal message"] = buffer.getvalue()
        leaks["doctor Gemini report (disabled)"] = doctor_gemini_report({"gemini_api_key": SENTINEL})
    leaking = sorted(name for name, text in leaks.items() if SENTINEL in text or SENTINEL[6:] in text)
    record(
        "adversarial: the resolved key value never reaches operator-visible output",
        "the sentinel key appears in none of the doctor report, the exit-5 message, or the capability payload",
        f"scanned {sorted(leaks)}; leaking: {leaking or 'none'}",
        "passed" if not leaking else "failed",
    )
    notes["leakScan"] = {"surfaces": sorted(leaks), "leaking": leaking}

    # --- doctor honesty ------------------------------------------------------
    disabled_report = None
    enabled_report = None
    with patch.dict(os.environ, matrix_env(google="env-key", flag="1"), clear=False), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": "config-key"}):
        disabled_report = doctor_gemini_report({"gemini_api_key": "config-key"})
    with patch.dict(os.environ, matrix_env(google="env-key"), clear=False), \
            patch.object(config_loader, "load_config", return_value={"gemini_api_key": "config-key"}):
        enabled_report = doctor_gemini_report({"gemini_api_key": "config-key"})
    honest = ("설정됨" not in disabled_report and "disabled" in disabled_report
              and "설정됨" in enabled_report)
    record(
        "adversarial: doctor honesty with PAPER_CURATION_NO_GEMINI=1 and a key present",
        "no '설정됨' configured-OK line for Gemini; a △ 'disabled' warning instead (and 설정됨 returns once re-enabled)",
        f"disabled: {clip(disabled_report, 220)} || enabled: {clip(enabled_report, 160)}",
        "passed" if honest else "failed",
    )
    notes["doctorReports"] = {"disabled": disabled_report, "enabled": enabled_report}

    # doctor's exit code is driven by rep.fails; the Gemini branch must never add one.
    fails = {}
    for label, env in (("disabled", matrix_env(google="env-key", flag="1")),
                       ("enabled", matrix_env(google="env-key")),
                       ("absent", matrix_env())):
        reporter = doctor_module.Reporter()
        buffer = io.StringIO()
        status = types.SimpleNamespace(ready=False, mode=None)
        with patch.dict(os.environ, env, clear=False), \
                patch.object(config_loader, "load_config", return_value={}), \
                patch.object(doctor_module, "_check_secret_sources", lambda *a, **k: None), \
                patch.object(doctor_module, "_check_tls_status", lambda *a, **k: None), \
                patch.object(doctor_module, "_check_anthropic_auth", lambda *a, **k: status), \
                contextlib.redirect_stdout(buffer):
            doctor_module.check_api_keys(reporter, {})
        fails[label] = reporter.fails
    record(
        "adversarial: the Gemini branch never contributes to doctor's non-zero exit code",
        "rep.fails is identical (and zero) whether Gemini is disabled, enabled, or absent → exit 0 from this section",
        f"fails per matrix: {fails}",
        "passed" if set(fails.values()) == {0} else "failed",
    )
    notes["doctorFailCounts"] = fails

    # --- real doctor CLI: exit code and leakage on the shipped binary ---------
    environment = dict(os.environ)
    environment.update({"GOOGLE_API_KEY": SENTINEL, "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": "1",
                        "NO_COLOR": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    process = subprocess.run([sys.executable, "pipeline/doctor.py"], cwd=REPOSITORY, env=environment,
                             capture_output=True, text=True, timeout=600)
    cli_output = (process.stdout or "") + (process.stderr or "")
    COMMANDS.append({"label": "real doctor CLI with PAPER_CURATION_NO_GEMINI=1 and a sentinel key",
                     "command": f"{sys.executable} pipeline/doctor.py", "cwd": ".",
                     "exit_code": process.returncode})
    gemini_lines = [line.strip() for line in cli_output.splitlines() if "Gemini" in line]
    gemini_ok_line = [line for line in gemini_lines if "설정됨" in line]
    failing_lines = [line.strip() for line in cli_output.splitlines() if "✗" in line]
    gemini_fail = [line for line in failing_lines if "Gemini" in line or "GOOGLE_API_KEY" in line]
    record(
        "adversarial: real `python3 pipeline/doctor.py` with the disable switch and a sentinel key",
        "no Gemini '설정됨' line, no sentinel in stdout, and the Gemini item contributes no ✗ (exit code unaffected)",
        f"exit {process.returncode}; gemini lines: {clip(' | '.join(gemini_lines), 260)}; "
        f"gemini ✗: {gemini_fail or 'none'}; unrelated ✗: {clip(' | '.join(failing_lines), 200) or 'none'}; "
        f"sentinel leaked: {SENTINEL in cli_output}",
        "passed" if not gemini_ok_line and not gemini_fail and SENTINEL not in cli_output else "failed",
    )
    notes["doctorCli"] = {
        "exitCode": process.returncode,
        "geminiLines": gemini_lines,
        "geminiFailures": gemini_fail,
        "unrelatedFailures": failing_lines,
        "sentinelLeaked": SENTINEL in cli_output,
    }
    return notes


# --------------------------------------------------------------------------
# 4. Bypass scan
# --------------------------------------------------------------------------
KEY_NAMES = ("GOOGLE_API_KEY", "GEMINI_API_KEY")
SCAN_ROOTS = ("pipeline", "bin", "scripts", "tests", "worker", "skills",
              "docs/setup-guide.md", "docs/operations.md", "docs/architecture.md",
              "docs/index.html", "CLAUDE.md", "README.md", "README.en.md", "SKILL.md",
              "SKILL.md.template", ".env.example", "config.example.json", "wrangler.toml",
              "package.json", "requirements.txt")
SCAN_SUFFIXES = {".py", ".mjs", ".js", ".sh", ".json", ".md", ".toml"}
SCAN_SKIP_DIRS = {"__pycache__", "_cache", "_logs", "_smoke", "_archive", "_state", "node_modules",
                  ".pytest_cache", "papers", "humanoid", "physical-ai"}

# Every hit that is legitimately allowed to name the raw environment variable.
# A hit that matches none of these rules is a real bypass.
ALLOWED = (
    ("pipeline/config_loader.py", "get_google_key",
     "the canonical resolver itself — the one place allowed to read the environment"),
    ("pipeline/reextract_figures.py", None,
     "deliberate disable trick: env pop plus PAPER_CURATION_NO_GEMINI=1 for the geometric-only bulk pass"),
    ("pipeline/doctor.py", None,
     "env-name enumeration for the presence/redaction report; the verdict itself calls get_google_key()"),
    ("pipeline/setup.py", None, "env-name enumeration for onboarding prompts"),
    ("worker/index.js", None,
     "Cloudflare Worker runtime binding (separate JS process, wrangler secret) — outside the Python resolver"),
    ("pipeline/tests/qa_g004_adversarial.py", None,
     "this red-team harness: builds throwaway pre-change variants, resolves nothing at runtime"),
    ("bin/paper-curation.mjs", None,
     "CLI help text (template literal) naming the env var for onboarding; the Node CLI resolves no key"),
    ("scripts/", None, "secret scanner / git hook name list"),
    ("tests/", None, "node test fixture"),
    ("pipeline/tests/", None, "test fixture / assertion"),
)

ENV_READ_RE = re.compile(
    r"""os\.(?:environ\.(?:get|pop)|getenv)\s*\(\s*["'](GOOGLE_API_KEY|GEMINI_API_KEY)["']"""
    r"""|os\.environ\s*\[\s*["'](GOOGLE_API_KEY|GEMINI_API_KEY)["']\s*\]"""
    r"""|env\.(GOOGLE_API_KEY|GEMINI_API_KEY)\b"""
)


def iter_scan_files():
    for root in SCAN_ROOTS:
        path = REPOSITORY / root
        if path.is_file():
            yield path
            continue
        if not path.is_dir():
            continue
        for candidate in sorted(path.rglob("*")):
            if not candidate.is_file() or candidate.suffix not in SCAN_SUFFIXES:
                continue
            if any(part in SCAN_SKIP_DIRS for part in candidate.relative_to(REPOSITORY).parts):
                continue
            yield candidate


def classify(relative: str, snippet: str) -> tuple[str, str]:
    for prefix, function, reason in ALLOWED:
        if relative.startswith(prefix):
            return "legitimate", reason
    return "bypass", "direct environment read outside the canonical resolver"


CODE_SUFFIXES = {".py", ".mjs", ".js", ".sh"}


def literal_spans(path: Path) -> dict[int, list[tuple[int, int]]]:
    """Column ranges covered by string literals and comments, per line.

    A name that only ever appears inside one of these ranges is prose or an
    operator-facing message, not a key lookup.
    """
    spans: dict[int, list[tuple[int, int]]] = {}
    try:
        with path.open("rb") as handle:
            for token in tokenize.tokenize(handle.readline):
                if token.type not in (tokenize.STRING, tokenize.COMMENT):
                    continue
                (start_row, start_col), (end_row, end_col) = token.start, token.end
                for row in range(start_row, end_row + 1):
                    low = start_col if row == start_row else 0
                    high = end_col if row == end_row else 10 ** 6
                    spans.setdefault(row, []).append((low, high))
    except Exception:
        return {}
    return spans


def mention_kind(relative: str, line: str, number: int,
                 spans: dict[int, list[tuple[int, int]]] | None) -> str:
    """Is this mention executable code, or text a human reads?"""
    suffix = Path(relative).suffix
    if suffix not in CODE_SUFFIXES:
        return "documentation"
    if spans is not None:
        covered = spans.get(number, [])
        positions = [match.start() for name in KEY_NAMES
                     for match in re.finditer(re.escape(name), line)]
        if positions and all(any(low <= position < high for low, high in covered) for position in positions):
            return "string-or-comment"
        return "code"
    stripped = line.strip()
    if stripped.startswith(("#", "//", "*")):
        return "comment"
    return "code"


def name_mentions() -> list[dict]:
    """Every mention of either environment-variable name, classified one by one.

    The direct-read regex only sees literal ``os.environ.get("GOOGLE_API_KEY")``.
    doctor/setup resolve through a *variable* name list, so a name-level pass is
    what actually proves nothing else resolves a key behind the resolver's back.
    """
    mentions = []
    for path in iter_scan_files():
        relative = str(path.relative_to(REPOSITORY))
        spans = literal_spans(path) if path.suffix == ".py" else None
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not any(name in line for name in KEY_NAMES):
                continue
            kind = mention_kind(relative, line, number, spans)
            verdict, reason = classify(relative, line)
            if kind != "code":
                verdict, reason = "legitimate", f"{kind}: names the variable for a human, resolves nothing"
            mentions.append({"file": relative, "line": number, "snippet": clip(line, 150),
                             "kind": kind, "classification": verdict, "reason": reason})
    return mentions


def indirect_readers() -> list[dict]:
    """Python functions that read os.environ through a *variable* name.

    doctor._resolve_key and setup._key_value never write "GOOGLE_API_KEY" next to
    os.environ.get, so the literal pass cannot see them.  Any such function whose
    module also carries one of the key names is a candidate key chain and has to be
    classified by hand.
    """
    readers = []
    for path in iter_scan_files():
        if path.suffix != ".py":
            continue
        relative = str(path.relative_to(REPOSITORY))
        text = path.read_text(encoding="utf-8", errors="replace")
        if not any(name in text for name in KEY_NAMES):
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                target = ast.unparse(node.func) if node.func else ""
                if target not in {"os.environ.get", "os.getenv", "os.environ.pop"}:
                    continue
                if not node.args or isinstance(node.args[0], ast.Constant):
                    continue  # literal reads are covered by the direct pass
                verdict, reason = classify(relative, "")
                readers.append({
                    "file": relative,
                    "line": node.lineno,
                    "function": function.name,
                    "expression": clip(ast.unparse(node), 120),
                    "classification": verdict,
                    "reason": reason,
                })
    return readers


def client_constructions() -> list[dict]:
    """Every genai.Client(...) in tracked Python, with the source of its api_key argument."""
    found = []
    for path in iter_scan_files():
        if path.suffix != ".py":
            continue
        relative = str(path.relative_to(REPOSITORY))
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "Client"):
                continue
            argument = next((kw.value for kw in node.keywords if kw.arg == "api_key"), None)
            expression = ast.unparse(argument) if argument is not None else "<positional/none>"
            source = expression
            if isinstance(argument, ast.Name):
                # Resolve the local binding inside the enclosing function.
                function = node
                while function in parents and not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    function = parents[function]
                if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for statement in ast.walk(function):
                        if (isinstance(statement, ast.Assign) and len(statement.targets) == 1
                                and isinstance(statement.targets[0], ast.Name)
                                and statement.targets[0].id == argument.id):
                            source = f"{argument.id} = {ast.unparse(statement.value)}"
            canonical = "get_google_key()" in source
            found.append({
                "file": relative,
                "line": node.lineno,
                "apiKeyExpression": clip(source, 160),
                "resolvesThroughCanonicalResolver": canonical,
            })
    return found


def bypass_scan() -> dict:
    hits = []
    for path in iter_scan_files():
        relative = str(path.relative_to(REPOSITORY))
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not ENV_READ_RE.search(line):
                continue
            verdict, reason = classify(relative, line)
            hits.append({"file": relative, "line": number, "snippet": clip(line, 160),
                         "classification": verdict, "reason": reason})
    real = [hit for hit in hits if hit["classification"] == "bypass"]
    record(
        "bypass scan: direct GOOGLE_API_KEY / GEMINI_API_KEY environment reads",
        "every remaining hit is the canonical resolver, an env-name enumeration, a deliberate disable trick, "
        "a worker binding, or a test fixture",
        f"{len(hits)} hits scanned; real bypasses: "
        + (json.dumps([hit["file"] + ":" + str(hit["line"]) for hit in real]) if real else "none"),
        "passed" if not real else "failed",
    )

    clients = client_constructions()
    stray = [client for client in clients if not client["resolvesThroughCanonicalResolver"]]
    record(
        "bypass scan: genai.Client(...) constructions",
        "every client is constructed from a value produced by config_loader.get_google_key()",
        f"{len(clients)} constructions: " + json.dumps(clients, ensure_ascii=False),
        "passed" if not stray else "failed",
    )

    mentions = name_mentions()
    unclassified = [item for item in mentions if item["classification"] != "legitimate"]
    by_kind: dict[str, int] = {}
    for item in mentions:
        by_kind[item["kind"]] = by_kind.get(item["kind"], 0) + 1
    record(
        "bypass scan: every mention of GOOGLE_API_KEY / GEMINI_API_KEY, name by name",
        "the name-level pass (which also sees doctor/setup's variable-driven lookups) leaves nothing "
        "unclassified",
        f"{len(mentions)} mentions by kind {by_kind}; unclassified: "
        + (json.dumps([item["file"] + ":" + str(item["line"]) for item in unclassified]) if unclassified else "none"),
        "passed" if not unclassified else "failed",
    )

    indirect = indirect_readers()
    indirect_bypasses = [item for item in indirect if item["classification"] != "legitimate"]
    record(
        "bypass scan: indirect os.environ reads driven by a key-name list",
        "every variable-driven environment lookup in a module that names a Gemini key is a documented "
        "presence report or onboarding prompt, never a functional key chain",
        f"{len(indirect)} indirect readers: "
        + json.dumps([f"{item['file']}:{item['function']}:{item['line']}" for item in indirect]),
        "passed" if not indirect_bypasses else "failed",
    )

    excluded = subprocess.run(["git", "check-ignore", "-v", "paperbanana/app.py"], cwd=REPOSITORY,
                              capture_output=True, text=True)
    return {
        "remainingHits": hits,
        "nameMentions": mentions,
        "unclassifiedMentions": unclassified,
        "indirectReaders": indirect,
        "indirectBypasses": indirect_bypasses,
        "realBypasses": ([f"{hit['file']}:{hit['line']}" for hit in real]
                         + [f"{item['file']}:{item['line']}" for item in unclassified]
                         + [f"{item['file']}:{item['line']}" for item in indirect_bypasses]
                         + [f"{item['file']}:{item['line']}" for item in stray]),
        "clientConstructions": clients,
        "strayClientConstructions": stray,
        "excludedTrees": [{
            "path": "paperbanana/",
            "reason": "gitignored vendored third-party app with its own configs/model_config.yaml key chain; "
                      "not part of the shipped package and never imported by pipeline/",
            "gitCheckIgnore": clip(excluded.stdout or excluded.stderr, 120),
        }],
        "scanRoots": list(SCAN_ROOTS),
    }


# --------------------------------------------------------------------------
# 5. Required suite
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
    parser = argparse.ArgumentParser(description="Adversarial QA harness for G004")
    parser.add_argument("--report", default="artifacts/g004-resolver-qa-report.json")
    arguments = parser.parse_args()

    proof = discriminator_proof()
    coverage = coverage_probe()
    adversarial = adversarial_cases()
    scan = bypass_scan()
    suite = required_suite()

    passed = sum(1 for item in RESULTS if item["verdict"] == "passed")
    failed = sum(1 for item in RESULTS if item["verdict"] == "failed")
    report = {
        "schemaVersion": 1,
        "kind": "package-test-report",
        "goal": "G004",
        "contract": "single canonical Gemini key resolver + EMBEDDINGS_UNAVAILABLE exit 5",
        "commands": COMMANDS,
        "results": RESULTS,
        "discriminatorProof": proof,
        "coverageProbe": coverage,
        "adversarialNotes": adversarial,
        "bypassScan": scan,
        "requiredSuite": suite,
        "findings": FINDINGS,
        "summary": {"passed": passed, "failed": failed, "findings": len(FINDINGS)},
    }

    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    # Fail closed rather than persist a real credential that a matrix may have touched.
    for name in KEY_NAMES:
        live = os.environ.get(name, "").strip()
        if live and live != SENTINEL and live in serialized:
            raise SystemExit(f"refusing to write the report: a live {name} value reached the payload")
    destination = Path(arguments.report)
    if not destination.is_absolute():
        destination = REPOSITORY / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(serialized, encoding="utf-8")
    print(f"\nwrote {destination} (passed={passed} failed={failed})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
