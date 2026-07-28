#!/usr/bin/env python3
"""Fail-closed loopback dashboard server and local operation-consent wire."""
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import secrets
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"
sys.path.insert(0, str(PIPELINE_DIR))

from lib.operation_consent import (  # noqa: E402
    APPROVAL_TTL_SECONDS,
    ApprovalRejectedError,
    AuthUnavailableError,
    OperationClaim,
    OperationConsent,
    OperationMaxima,
    PlanExpiredError,
    PlanScopeChangedError,
    ProviderTask,
    canonical_json_bytes,
    resolve_auth_mode,
    sha256_hex,
)
from lib import search_index_metadata as search_meta  # noqa: E402
from lib.audio_overview import (  # noqa: E402
    SCRIPT_MODEL,
    TTS_MODEL,
    AudioCapabilityV1,
    audio_plan_status,
    configured_audio_capability,
)
from tls import create_ssl_context  # noqa: E402
from config_loader import get_google_key  # noqa: E402

# Retained for the index metadata compatibility contract.  This server deliberately
# does not construct a Gemini client or proxy embedding requests.
GEMINI_MODEL = search_meta.EMBEDDING_MODEL
EMBED_PROVIDER = search_meta.EMBEDDING_PROVIDER
QUERY_TASK_TYPE = "RETRIEVAL_QUERY"
EMBED_DIM = search_meta.EMBEDDING_DIMENSION
_ssl_ctx = create_ssl_context(purpose="serve_local", config=None)

def resolve_google_key() -> str | None:
    """Canonical Gemini key seam: delegate to the one resolver, never probe.

    Returns the key config_loader.get_google_key() resolves (env
    GOOGLE_API_KEY/GEMINI_API_KEY → config.json, forced off by
    PAPER_CURATION_NO_GEMINI), or None when nothing resolves. This server still
    constructs no Gemini client and proxies no embedding request.
    """
    return get_google_key().strip() or None

API_SCHEMA = 1
MAX_JSON_BYTES = 64 * 1024
OPERATION_TTL_SECONDS = 10 * 60
CAPABILITY_TTL_SECONDS = 10 * 60
IDEMPOTENCY_RE = re.compile(r"^[0-9a-f]{64}$")
TOPIC_RE = re.compile(r"^[^/\\\x00]{1,128}$")


def oauth_available() -> bool:
    """Local credential presence only; never probes a provider or invokes a CLI."""
    return bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "").strip())


def api_key_available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def gemini_api_key_available() -> bool:
    # Canonical resolver only: env → config.json, forced off by
    # PAPER_CURATION_NO_GEMINI. An env-only chain here disagreed with
    # build_search_index and the Audio capability projection.
    return bool(resolve_google_key())


def audio_capability() -> dict[str, Any]:
    """Derive Gemini Audio availability from local configuration without probing.

    Delegates to lib.audio_overview so the server cannot drift from the library
    contract. Hand-building the dict here shipped an extra `models` key that
    AudioCapabilityV1 does not declare.

    Reachability is deliberately narrow and stated honestly: this helper
    synthesizes the model map from the same constants `derive_audio_capability`
    compares against, and passes the default `safe_root=True`, so from the
    server only GEMINI_AUTH_UNAVAILABLE and READY are reachable today.
    GEMINI_MODEL_UNAVAILABLE needs a real configured model map and
    AUDIO_TEMP_RECOVERY_AMBIGUOUS needs a real Audio-root probe; neither is
    supplied here yet, and both are covered by direct library tests.
    """
    return _audio_capability_record().to_dict()


def _audio_capability_record() -> AudioCapabilityV1:
    """The capability record itself, for callers that need the typed value."""
    return configured_audio_capability(
        config={"audio_overview": {"models": {"script": SCRIPT_MODEL, "tts": TTS_MODEL}}},
        auth=resolve_google_key() or "",
    )


class _WireState:
    def __init__(self) -> None:
        self.consent = OperationConsent()
        self.capabilities: dict[str, int] = {}
        self.lock = threading.RLock()

def _wire_state(server: ThreadingHTTPServer) -> _WireState:
    state = getattr(server, "operation_wire_state", None)
    if state is None:
        state = _WireState()
        server.operation_wire_state = state
    return state


def _error(code: str, message: str) -> dict[str, Any]:
    return {"schema": API_SCHEMA, "error": {"code": code, "message": message}}


def _canonical_digest(value: Any) -> str:
    return sha256_hex(canonical_json_bytes(value))


class LocalHandler(SimpleHTTPRequestHandler):
    """Exact-127.0.0.1 static server with a bounded, consent-gated API."""
    server_version = "PaperCurationLocal/1"
    sys_version = ""

    def log_message(self, _format: str, *args: Any) -> None:
        # Requests can carry credentials; the stdlib access log is not a safe sink.
        return

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; font-src 'self'; "
            "base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
        )
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        super().end_headers()

    def _expected_authority(self) -> str:
        return "127.0.0.1:%d" % self.server.server_address[1]

    def _header_values(self, name: str) -> list[str]:
        values = self.headers.get_all(name)
        return [] if values is None else values

    def _valid_authority(self) -> bool:
        # Do not accept proxy authority because a local capability must not be
        # transferable through aliases, forwarded headers, or a reverse proxy.
        if self.client_address[0] != "127.0.0.1":
            return False
        host_values = self._header_values("Host")
        if len(host_values) != 1 or host_values[0] != self._expected_authority():
            return False
        for name in self.headers.keys():
            lowered = name.lower()
            if lowered == "forwarded" or lowered.startswith("x-forwarded-"):
                return False
        return True

    def _valid_origin(self) -> bool:
        values = self._header_values("Origin")
        return len(values) == 1 and values[0] == "http://" + self._expected_authority()

    def _send_json(self, status: int, value: dict[str, Any], *, cookie: str | None = None) -> None:
        body = canonical_json_bytes(value)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if cookie is not None:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def _reject_authority(self) -> None:
        self._send_json(400, _error("INVALID_AUTHORITY", "request authority must be exact IPv4 loopback"))

    def _read_json(self) -> tuple[dict[str, Any] | None, tuple[int, dict[str, Any]] | None]:
        if self.headers.get("Transfer-Encoding"):
            return None, (400, _error("TRANSFER_ENCODING_FORBIDDEN", "chunked request bodies are not accepted"))
        content_types = self._header_values("Content-Type")
        if len(content_types) != 1 or content_types[0] != "application/json":
            return None, (415, _error("UNSUPPORTED_MEDIA_TYPE", "Content-Type must be application/json"))
        lengths = self._header_values("Content-Length")
        if len(lengths) != 1 or not lengths[0].isdigit():
            return None, (400, _error("INVALID_CONTENT_LENGTH", "Content-Length is required"))
        length = int(lengths[0])
        if length > MAX_JSON_BYTES:
            return None, (413, _error("BODY_TOO_LARGE", "JSON body exceeds the local wire limit"))
        raw = self.rfile.read(length)
        if len(raw) != length:
            return None, (400, _error("TRUNCATED_BODY", "request body was truncated"))
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, (400, _error("INVALID_JSON", "body must be UTF-8 JSON"))
        if not isinstance(value, dict):
            return None, (400, _error("INVALID_SCHEMA", "JSON body must be an object"))
        return value, None

    @staticmethod
    def _exact_keys(value: dict[str, Any], required: set[str], optional: set[str] = set()) -> bool:
        return set(value) == required or (required <= set(value) <= required | optional)

    def _capability(self) -> str | None:
        raw = self.headers.get("Cookie", "")
        tokens = [item.strip()[3:] for item in raw.split(";") if item.strip().startswith("pc=")]
        if len(tokens) != 1:
            return None
        state = _wire_state(self.server)
        return tokens[0] if state.capabilities.get(tokens[0], 0) > int(time.time()) else None

    def _require_capability(self) -> str | None:
        token = self._capability()
        if token is None:
            self._send_json(401, _error("CAPABILITY_REQUIRED", "bootstrap capability cookie is required"))
        return token
    def _auth_available(self, name: str, fallback: Any) -> bool:
        override = getattr(self.server, name, None)
        return bool(override() if callable(override) else override) if override is not None else bool(fallback())


    def do_GET(self) -> None:  # noqa: N802
        if not self._valid_authority():
            return self._reject_authority()
        route = self.path.split("?", 1)[0]
        if route == "/api/bootstrap":
            return self._bootstrap()
        if route == "/api/status":
            return self._status()
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        # Authority and Origin intentionally precede any body read.
        if not self._valid_authority():
            return self._reject_authority()
        if not self._valid_origin():
            return self._send_json(403, _error("INVALID_ORIGIN", "Origin must be exact loopback authority"))
        route = self.path.split("?", 1)[0]
        if route not in {"/api/action/plan", "/api/action/approve", "/api/action/start"}:
            return self._send_json(404, _error("NOT_FOUND", "route is not available"))
        body, failure = self._read_json()
        if failure:
            return self._send_json(*failure)
        if route == "/api/action/plan":
            return self._plan(body)
        if route == "/api/action/approve":
            return self._approve(body)
        return self._start(body)

    def _bootstrap_value(self) -> dict[str, Any]:
        return {
            "schema": API_SCHEMA,
            "status": "ok",
            "action_capability": {
                "schema": "ActionCapabilityV1",
                "state": "UNAVAILABLE",
                "reason": "DISPATCH_UNAVAILABLE",
            },
            "audio_capability": audio_capability(),
        }

    def _bootstrap(self) -> None:
        state = _wire_state(self.server)
        token = secrets.token_urlsafe(32)
        with state.lock:
            state.capabilities[token] = int(time.time()) + CAPABILITY_TTL_SECONDS
        cookie = "pc=%s; HttpOnly; SameSite=Strict; Path=/api; Max-Age=%d" % (token, CAPABILITY_TTL_SECONDS)
        self._send_json(200, self._bootstrap_value(), cookie=cookie)

    def _status(self) -> None:
        self._send_json(200, self._bootstrap_value())

    def _validate_plan(self, body: dict[str, Any]) -> tuple[dict[str, Any] | None, tuple[int, dict[str, Any]] | None]:
        required = {"schema", "command", "topic_alias", "input", "limits"}
        if set(body) != required or isinstance(body.get("schema"), bool) or body.get("schema") != API_SCHEMA:
            return None, (400, _error("INVALID_SCHEMA", "plan fields must exactly match schema 1"))
        command = body.get("command")
        topic = body.get("topic_alias")
        data = body.get("input")
        limits = body.get("limits")
        limit_maxima = {
            "top_k": 100,
            "candidate_k": 100,
            "web_searches": 12,
            "aspects": 6,
            "sections": 8,
            "concurrency": 4,
            "max_attempts": 64,
            "tokens": 200_000,
            "items": 100,
        }
        if command not in {"query.normal", "query.deeper", "audio.create"} or not isinstance(topic, str) or not TOPIC_RE.fullmatch(topic):
            return None, (400, _error("INVALID_SCHEMA", "invalid command or topic_alias"))
        if not isinstance(data, dict) or not isinstance(limits, dict) or any(
            key not in limit_maxima or isinstance(value, bool) or not isinstance(value, int)
            or value < 0 or value > limit_maxima[key] for key, value in limits.items()
        ):
            return None, (400, _error("INVALID_SCHEMA", "input and bounded integer limits are required"))
        if command.startswith("query."):
            if not self._exact_keys(data, {"auth_mode", "query"}, {"source"}) or not isinstance(data.get("query"), str) or not 0 < len(data["query"].encode("utf-8")) <= 120000:
                return None, (400, _error("INVALID_SCHEMA", "query input is invalid"))
        else:
            if not self._exact_keys(data, {"auth_mode", "requested_target_seconds"}, {"source"}) or not isinstance(data.get("requested_target_seconds"), int) or isinstance(data.get("requested_target_seconds"), bool) or not 30 <= data["requested_target_seconds"] <= 3600:
                return None, (400, _error("INVALID_SCHEMA", "audio input is invalid"))
        if "source" in data and (not isinstance(data["source"], str) or not 0 < len(data["source"].encode("utf-8")) <= 4096):
            return None, (400, _error("INVALID_SCHEMA", "source is invalid"))
        if data.get("auth_mode") not in {"auto", "oauth", "api-key"}:
            return None, (400, _error("INVALID_SCHEMA", "input.auth_mode is required"))
        return {"command": command, "topic": topic, "input": data, "limits": limits}, None

    def _plan(self, body: dict[str, Any]) -> None:
        capability = self._require_capability()
        if capability is None:
            return
        request, failure = self._validate_plan(body)
        if failure:
            return self._send_json(*failure)
        assert request is not None
        if request["command"] == "audio.create" and audio_capability()["state"] != "AVAILABLE":
            # Optional Audio is an informational, non-mutating capability state.
            # A6: the response carries the `result` discriminator on both
            # variants so clients switch on one tag instead of inferring intent
            # from an absent key. No operation, claim, or credential is created.
            return self._send_json(200, audio_plan_status(_audio_capability_record()))
        try:
            if request["command"] == "audio.create":
                resolved = resolve_auth_mode(
                    request["input"]["auth_mode"],
                    oauth_available=False,
                    api_key_available=self._auth_available(
                        "gemini_api_key_available",
                        gemini_api_key_available,
                    ),
                )
            else:
                resolved = resolve_auth_mode(
                    request["input"]["auth_mode"],
                    oauth_available=self._auth_available(
                        "oauth_available",
                        oauth_available,
                    ),
                    api_key_available=self._auth_available(
                        "api_key_available",
                        api_key_available,
                    ),
                )
        except AuthUnavailableError:
            return self._send_json(
                401,
                _error("AUTH_UNAVAILABLE", "requested auth mode is unavailable"),
            )
        now = int(time.time())
        operation_id = secrets.token_hex(16)
        input_digest = _canonical_digest(request["input"])
        resource_digest = _canonical_digest(request["limits"])
        if request["command"] == "audio.create":
            providers = (
                ProviderTask("gemini", SCRIPT_MODEL, "audio.script", ()),
                ProviderTask("gemini", TTS_MODEL, "audio.tts", ()),
            )
        else:
            query_provider = (
                "claude" if resolved.resolved.value == "oauth" else "anthropic"
            )
            query_model = os.environ.get(
                "PAPER_CURATION_QUERY_MODEL",
                "claude-sonnet-5",
            ).strip()
            if not query_model:
                return self._send_json(
                    400,
                    _error("INVALID_MODEL", "query model must be configured"),
                )
            providers = (
                ProviderTask(
                    query_provider,
                    query_model,
                    request["command"],
                    (),
                ),
            )
        default_attempts = {
            "query.normal": 12,
            "query.deeper": 64,
            "audio.create": 33,
        }[request["command"]]
        default_concurrency = 1 if request["command"] == "query.normal" else 4
        maxima = OperationMaxima(
            attempts=request["limits"].get("max_attempts", default_attempts),
            tokens=request["limits"].get("tokens", 120_000),
            items=request["limits"].get(
                "items",
                32 if request["command"] == "audio.create" else 100,
            ),
            searches=request["limits"].get("web_searches", 0),
            audio_seconds=(
                3600 if request["command"] == "audio.create" else 0
            ),
            recipients=0,
            concurrency=request["limits"].get(
                "concurrency",
                default_concurrency,
            ),
        )
        claim = OperationClaim(
            version=API_SCHEMA,
            operation_id=operation_id,
            task="local.action",
            command=request["command"],
            topic=request["topic"],
            source=str(request["input"].get("source", "local")),
            ingress="localhost",
            auth=resolved.resolved,
            providers=providers,
            maxima=maxima,
            input_digests=(input_digest,),
            resource_digests=(resource_digest,),
            created_at=now,
            expires_at=now + OPERATION_TTL_SECONDS,
        )
        state = _wire_state(self.server)
        with state.lock:
            plan = state.consent.create_plan(claim)
            state.consent.bind_plan(
                plan.operation_id,
                plan.plan_hash,
                _canonical_digest({
                    "dispatcher": "unavailable",
                    "request": request,
                }),
            )
        preview = claim.canonical_value()
        preview["requested_auth"] = request["input"]["auth_mode"]
        preview["resolved_auth"] = resolved.resolved.value
        preview["cost"] = "PRICE_UNAVAILABLE"
        preview["dispatch_state"] = "UNAVAILABLE"
        preview["expected_work"] = (
            ["A01.script", "A02.tts.1..32", "A03.assemble"]
            if request["command"] == "audio.create"
            else [request["command"]]
        )
        if request["command"] == "audio.create":
            preview["requested_target_seconds"] = request["input"][
                "requested_target_seconds"
            ]
            preview["hard_actual_maximum_seconds"] = 3600
        self._send_json(200, {"schema": API_SCHEMA, "operation_id": plan.operation_id, "plan_hash": plan.plan_hash, "preview": preview, "approval_expires_in_seconds": APPROVAL_TTL_SECONDS, "operation_expires_at": claim.expires_at})

    def _approve(self, body: dict[str, Any]) -> None:
        if self._require_capability() is None:
            return
        if set(body) != {"schema", "operation_id", "plan_hash", "decision"} or isinstance(body.get("schema"), bool) or body.get("schema") != API_SCHEMA or not all(isinstance(body.get(key), str) for key in ("operation_id", "plan_hash", "decision")):
            return self._send_json(400, _error("INVALID_SCHEMA", "approval fields must exactly match schema 1"))
        state = _wire_state(self.server)
        try:
            with state.lock:
                credential = state.consent.approve(body["operation_id"], body["plan_hash"], decision=body["decision"])
        except PlanScopeChangedError:
            return self._send_json(409, _error("PLAN_SCOPE_CHANGED", "approval does not match planned scope"))
        except PlanExpiredError:
            return self._send_json(410, _error("PLAN_EXPIRED", "operation plan has expired"))
        except ApprovalRejectedError:
            return self._send_json(403, _error("APPROVAL_REJECTED", "decision must be approve"))
        self._send_json(200, {"schema": API_SCHEMA, "operation_id": credential.operation_id, "plan_hash": credential.plan_hash, "redeem_credential": credential.token, "redeem_expires_in_seconds": APPROVAL_TTL_SECONDS})

    def _start(self, body: dict[str, Any]) -> None:
        capability = self._require_capability()
        if capability is None:
            return
        if set(body) != {"schema", "operation_id", "plan_hash"} or isinstance(body.get("schema"), bool) or body.get("schema") != API_SCHEMA or not all(isinstance(body.get(key), str) for key in ("operation_id", "plan_hash")):
            return self._send_json(400, _error("INVALID_SCHEMA", "start fields must exactly match schema 1"))
        keys = self._header_values("Idempotency-Key")
        redeem = self._header_values("X-PC-Redeem")
        if len(keys) != 1 or not IDEMPOTENCY_RE.fullmatch(keys[0]):
            return self._send_json(400, _error("INVALID_IDEMPOTENCY_KEY", "Idempotency-Key must be 64 lowercase hexadecimal characters"))
        if len(redeem) != 1 or len(redeem[0]) != 43:
            return self._send_json(401, _error("REDEEM_REQUIRED", "X-PC-Redeem is required"))
        self._send_json(503, _error("DISPATCH_UNAVAILABLE", "no trusted internal worker adapter is available"))


def main() -> None:
    parser = argparse.ArgumentParser(description="fail-closed local Paper Curation server")
    parser.add_argument("--port", type=int, default=8000, help="listener port")
    parser.add_argument("--host", default="127.0.0.1", help=argparse.SUPPRESS)
    parser.add_argument("--topic", default="", help="configured topic alias (display only)")
    args = parser.parse_args()
    if args.host != "127.0.0.1":
        parser.error("serve_local only binds exact IPv4 loopback 127.0.0.1")
    if not DOCS_DIR.exists():
        print(f"ERROR: docs directory not found: {DOCS_DIR}", file=sys.stderr)
        raise SystemExit(1)
    handler = functools.partial(LocalHandler, directory=str(DOCS_DIR))
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    port = httpd.server_address[1]
    print(f"bind: 127.0.0.1:{port}")
    print(f"open: http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
