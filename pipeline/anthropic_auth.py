"""Anthropic API-key and Claude Code subscription OAuth client selection.

The pipeline historically instantiated ``anthropic.Anthropic`` directly.  That
forces Console API billing even when the operator already has a Claude Pro/Max,
Team, or Enterprise subscription.  This module keeps the SDK path intact and
adds a small compatibility client backed by the official ``claude -p`` command.

OAuth credentials are never treated as API keys.  In OAuth mode the child
process explicitly drops API-key credentials so Claude Code cannot silently
switch back to metered Console billing.
"""

from __future__ import annotations

import json
import base64
import os
import re
import signal
import shutil
import subprocess
import threading
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from config_loader import load_config

REPO = Path(__file__).resolve().parent.parent
_AUTH_ENV = "PAPER_CURATION_ANTHROPIC_AUTH"
_VALID_MODES = {"auto", "api-key", "oauth"}
MIN_CLAUDE_CODE_VERSION = (2, 1, 205)


class AnthropicAuthError(RuntimeError):
    """Raised when the selected Anthropic authentication path is unavailable."""


class ClaudeCodeUnsupportedContent(AnthropicAuthError):
    """Raised for content that the non-agentic CLI bridge cannot safely pass."""


@dataclass
class AnthropicAuthStatus:
    mode: str
    source: str
    ready: bool
    detail: str


def _config() -> dict[str, Any]:
    cfg = load_config() or {}
    return cfg if isinstance(cfg, dict) else {}


def _normalize_mode(value: str | None) -> str:
    mode = (value or "auto").strip().lower().replace("_", "-")
    aliases = {
        "api": "api-key",
        "apikey": "api-key",
        "claude-code": "oauth",
        "claude-code-oauth": "oauth",
        "subscription": "oauth",
    }
    mode = aliases.get(mode, mode)
    if mode not in _VALID_MODES:
        choices = ", ".join(sorted(_VALID_MODES))
        raise AnthropicAuthError(f"Invalid Anthropic auth mode {value!r}; choose {choices}")
    return mode


def configured_mode(explicit: str | None = None) -> str:
    """Resolve explicit/env/config auth mode without inspecting credentials."""
    cfg = _config()
    value = explicit or os.environ.get(_AUTH_ENV) or cfg.get("anthropic_auth") or "auto"
    if isinstance(value, dict):
        value = value.get("mode", "auto")
    return _normalize_mode(str(value))


def _api_key(explicit: str | None = None) -> tuple[str, str]:
    if explicit:
        return explicit.strip(), "argument"
    env_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if env_key:
        return env_key, "env:ANTHROPIC_API_KEY"
    cfg_key = str(_config().get("anthropic_api_key", "")).strip()
    if cfg_key:
        return cfg_key, "config:anthropic_api_key"
    return "", ""


def claude_version() -> tuple[int, ...]:
    claude = shutil.which("claude")
    if not claude:
        return ()
    try:
        proc = subprocess.run(
            [claude, "--version"], capture_output=True, text=True, timeout=10
        )
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", proc.stdout or proc.stderr)
        return tuple(int(part) for part in match.groups()) if match else ()
    except Exception:
        return ()


def _saved_oauth_status() -> tuple[bool, str]:
    claude = shutil.which("claude")
    if not claude:
        return False, "Claude Code CLI not found"
    try:
        child_env = os.environ.copy()
        child_env.pop("ANTHROPIC_API_KEY", None)
        child_env.pop("ANTHROPIC_AUTH_TOKEN", None)
        proc = subprocess.run(
            [claude, "auth", "status"],
            capture_output=True,
            text=True,
            timeout=15,
            env=child_env,
        )
        data = json.loads(proc.stdout or "{}")
        logged_in = proc.returncode == 0 and bool(data.get("loggedIn"))
        method = str(data.get("authMethod", "")).strip()
        provider = str(data.get("apiProvider", "")).strip()
        subscription = str(data.get("subscriptionType", "")).strip()
        is_subscription = logged_in and method == "claude.ai"
        detail = ", ".join(part for part in (method, provider, subscription) if part)
        return is_subscription, detail or "not logged in with a Claude subscription"
    except Exception as exc:
        return False, f"Claude auth status failed: {type(exc).__name__}"


def auth_status(explicit_mode: str | None = None) -> AnthropicAuthStatus:
    """Return a redacted status without performing an inference request."""
    mode = configured_mode(explicit_mode)
    key, key_source = _api_key()
    oauth_token = bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "").strip())

    if mode == "api-key":
        return AnthropicAuthStatus(mode, key_source, bool(key), "API key configured" if key else "API key missing")

    claude_found = bool(shutil.which("claude"))
    if mode == "oauth":
        if not claude_found:
            return AnthropicAuthStatus(mode, "", False, "Claude Code CLI not found")
        if oauth_token:
            return AnthropicAuthStatus(mode, "env:CLAUDE_CODE_OAUTH_TOKEN", True, "long-lived OAuth token configured")
        saved_oauth, saved_detail = _saved_oauth_status()
        return AnthropicAuthStatus(mode, "saved:/login" if saved_oauth else "", saved_oauth, saved_detail)

    # Auto mode is billing-safe: any explicit OAuth credential/login wins over
    # metered API credentials. API-key billing is selected only when OAuth is
    # unavailable (or when the caller explicitly requests api-key mode).
    if oauth_token:
        return AnthropicAuthStatus(
            "oauth",
            "env:CLAUDE_CODE_OAUTH_TOKEN",
            claude_found,
            "auto selected OAuth token" if claude_found else "Claude Code CLI not found",
        )
    saved_oauth, saved_detail = _saved_oauth_status() if claude_found else (False, "Claude Code CLI not found")
    if saved_oauth:
        return AnthropicAuthStatus("oauth", "saved:/login", True, f"auto selected saved OAuth ({saved_detail})")
    if key:
        return AnthropicAuthStatus("api-key", key_source, True, "auto selected API key")
    return AnthropicAuthStatus("oauth", "", False, saved_detail)


def require_auth_ready(explicit_mode: str | None = None) -> AnthropicAuthStatus:
    """Fail fast when the selected auth path cannot run the pipeline."""
    status = auth_status(explicit_mode)
    if not status.ready:
        raise AnthropicAuthError(
            f"Anthropic {status.mode} authentication is not ready: {status.detail}. "
            "For subscription OAuth, run `claude auth login`; for metered API billing, "
            "select api-key mode and set ANTHROPIC_API_KEY."
        )
    if status.mode == "oauth":
        version = claude_version()
        if version < MIN_CLAUDE_CODE_VERSION:
            installed = ".".join(str(part) for part in version) or "unknown"
            required = ".".join(str(part) for part in MIN_CLAUDE_CODE_VERSION)
            raise AnthropicAuthError(
                f"Claude Code >= {required} is required for OAuth structured output "
                f"(installed: {installed}); run `claude update`"
            )
    return status


def create_anthropic_client(
    *,
    auth_mode: str | None = None,
    api_key: str | None = None,
    timeout: float = 180.0,
    max_retries: int = 4,
    **kwargs: Any,
):
    """Create an Anthropic SDK client or a Claude Code OAuth compatibility client."""
    mode = configured_mode(auth_mode)
    key, _ = _api_key(api_key)
    if api_key is not None and auth_mode is None:
        # A caller-supplied SDK key is an explicit API-billing decision.
        mode = "api-key"
    if mode == "auto":
        mode = auth_status("auto").mode

    if mode == "api-key":
        if not key:
            raise AnthropicAuthError(
                "Anthropic API-key mode selected but ANTHROPIC_API_KEY/"
                "config.json(anthropic_api_key) is missing"
            )
        from anthropic import Anthropic

        return Anthropic(
            api_key=key, timeout=timeout, max_retries=max_retries, **kwargs
        )

    status = require_auth_ready(mode)
    if status.mode != "oauth":
        raise AnthropicAuthError(f"Unexpected Anthropic auth mode: {status.mode}")
    return ClaudeCodeClient(timeout=timeout, max_retries=max_retries)

def _run_claude_process(
    command: list[str],
    *,
    input: str,
    timeout: float,
    cwd: str,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    """Run Claude in its own process group and reap every child on timeout."""
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd,
        env=env,
        start_new_session=os.name != "nt",
    )
    timeout = max(0.1, float(timeout))
    timed_out = threading.Event()
    terminate_lock = threading.Lock()

    def terminate_process_tree() -> None:
        with terminate_lock:
            if timed_out.is_set():
                return
            timed_out.set()
            if os.name != "nt":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            try:
                process.kill()
            except ProcessLookupError:
                pass

    deadline = time.time() + timeout
    watchdog_stopped = threading.Event()

    def enforce_wall_clock_deadline() -> None:
        poll_interval = min(0.25, max(0.01, timeout))
        while not watchdog_stopped.wait(poll_interval):
            if time.time() >= deadline:
                terminate_process_tree()
                return

    watchdog = threading.Thread(
        target=enforce_wall_clock_deadline,
        name="claude-oauth-watchdog",
        daemon=True,
    )
    watchdog.start()
    try:
        stdout, stderr = process.communicate(input=input, timeout=timeout)
        if timed_out.is_set():
            raise subprocess.TimeoutExpired(command, timeout, output=stdout, stderr=stderr)
    except subprocess.TimeoutExpired as exc:
        terminate_process_tree()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except (subprocess.TimeoutExpired, OSError, ValueError):
            stdout = exc.output or ""
            stderr = exc.stderr or ""
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
        raise subprocess.TimeoutExpired(
            command,
            timeout,
            output=stdout if stdout is not None else exc.output,
            stderr=stderr if stderr is not None else exc.stderr,
        ) from exc
    except (OSError, ValueError) as exc:
        if not timed_out.is_set():
            raise
        raise subprocess.TimeoutExpired(command, timeout) from exc
    finally:
        watchdog_stopped.set()
        watchdog.join(timeout=1)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)



class ClaudeCodeClient:
    """Small synchronous subset of ``anthropic.Anthropic`` backed by ``claude -p``."""

    def __init__(self, *, timeout: float = 180.0, max_retries: int = 4):
        self.timeout = float(timeout)
        self.max_retries = int(max_retries)
        self.messages = _ClaudeCodeMessages(self)

    def with_options(
        self,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        **_: Any,
    ):
        return ClaudeCodeClient(
            timeout=self.timeout if timeout is None else timeout,
            max_retries=self.max_retries if max_retries is None else max_retries,
        )


class _ClaudeCodeMessages:
    def __init__(self, client: ClaudeCodeClient):
        self._client = client

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: dict[str, Any] | None = None,
        **_: Any,
    ):
        temp_images = tempfile.TemporaryDirectory(prefix="paper-curation-vision-") if _has_images(messages) else None
        try:
            image_dir = Path(temp_images.name) if temp_images else None
            prompt = _render_messages(messages, image_dir=image_dir)
            schema = None
            tool_name = None
            if tools:
                tool_name = str((tool_choice or {}).get("name") or tools[0].get("name") or "structured_output")
                selected = next((tool for tool in tools if tool.get("name") == tool_name), tools[0])
                schema = selected.get("input_schema")

            result = self._run(
                prompt=prompt,
                model=model,
                system=system,
                schema=schema,
                working_dir=image_dir or REPO,
                allow_read=bool(image_dir),
            )
            if schema is not None:
                return SimpleNamespace(
                    content=[SimpleNamespace(type="tool_use", name=tool_name, input=result)]
                )
            return SimpleNamespace(content=[SimpleNamespace(type="text", text=str(result))])
        finally:
            if temp_images:
                temp_images.cleanup()

    def stream(self, **kwargs: Any):
        response = self.create(**kwargs)
        text = "".join(
            str(block.text)
            for block in response.content
            if getattr(block, "type", "") == "text"
        )
        return _ClaudeCodeStream(text)

    def count_tokens(self, *, messages: list[dict[str, Any]], **_: Any):
        # Claude Code has no local count-only command.  This conservative estimate
        # is used only for prompt chunking; inference still enforces model limits.
        text = _render_messages(messages)
        return SimpleNamespace(input_tokens=max(1, (len(text) + 2) // 3))

    def _run(
        self,
        *,
        prompt: str,
        model: str,
        system: str | None,
        schema: dict[str, Any] | None,
        working_dir: Path,
        allow_read: bool,
    ) -> str | dict[str, Any] | list[Any]:
        claude = shutil.which("claude")
        if not claude:
            raise AnthropicAuthError("Claude Code CLI disappeared during execution")

        system_prompt = system or "You are a precise research assistant. Follow the user's requested output format exactly."
        effective_prompt = prompt
        command = [
            claude,
            "-p",
            "--safe-mode",
            "--tools",
            "Read" if allow_read else "",
            *(["--allowedTools", "Read"] if allow_read else []),
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--output-format",
            "json",
            "--model",
            model,
            "--system-prompt",
            system_prompt,
        ]

        if schema:
            version = claude_version()
            if version < MIN_CLAUDE_CODE_VERSION:
                installed = ".".join(str(part) for part in version) or "unknown"
                required = ".".join(str(part) for part in MIN_CLAUDE_CODE_VERSION)
                raise AnthropicAuthError(
                    "Structured OAuth calls require Claude Code "
                    f">= {required} (installed: {installed}); run `claude update`"
                )
            compact_schema = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
            command.extend(["--json-schema", compact_schema])

        # OAuth must remain distinct from Console API billing.  Claude Code's
        # documented precedence puts API credentials ahead of subscription OAuth.
        child_env = os.environ.copy()
        child_env.pop("ANTHROPIC_API_KEY", None)
        child_env.pop("ANTHROPIC_AUTH_TOKEN", None)
        child_env["CLAUDE_CODE_SKIP_PROMPT_HISTORY"] = "1"

        last_error = ""
        attempts = max(1, self._client.max_retries + 1)
        for attempt in range(attempts):
            try:
                proc = _run_claude_process(
                    command,
                    input=effective_prompt,
                    timeout=self._client.timeout,
                    cwd=str(working_dir),
                    env=child_env,
                )
                payload = _decode_cli_payload(proc.stdout)
                if proc.returncode != 0 or payload.get("is_error"):
                    detail = payload.get("result") or proc.stderr.strip() or f"exit {proc.returncode}"
                    raise AnthropicAuthError(f"Claude Code OAuth call failed: {detail}")
                if schema:
                    structured = payload.get("structured_output")
                    if structured is not None:
                        return structured
                    return _extract_json(str(payload.get("result", "")))
                return str(payload.get("result", "")).strip()
            except (subprocess.TimeoutExpired, AnthropicAuthError, ValueError) as exc:
                last_error = str(exc)
                fatal_auth_error = any(
                    marker in last_error.lower()
                    for marker in (
                        "not logged in",
                        "login expired",
                        "authentication",
                        "invalid oauth",
                    )
                )
                if fatal_auth_error:
                    break
                if attempt + 1 >= attempts:
                    break
        raise AnthropicAuthError(last_error or "Claude Code OAuth call failed")


class _ClaudeCodeStream:
    def __init__(self, text: str):
        self.text_stream = iter((text,))

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _tb):
        return False


def _has_images(messages: list[dict[str, Any]]) -> bool:
    return any(
        isinstance(block, dict) and block.get("type") == "image"
        for message in messages
        if isinstance(message.get("content"), list)
        for block in message["content"]
    )


def _render_messages(messages: list[dict[str, Any]], image_dir: Path | None = None) -> str:
    rendered: list[str] = []
    image_index = 0
    for message in messages:
        role = str(message.get("role", "user")).upper()
        content = message.get("content", "")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if not isinstance(block, dict):
                    parts.append(str(block))
                elif block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
                elif block.get("type") == "image":
                    if image_dir is None:
                        raise ClaudeCodeUnsupportedContent(
                            "Image content requires an isolated image working directory"
                        )
                    source = block.get("source", {})
                    if source.get("type") != "base64" or not source.get("data"):
                        raise ClaudeCodeUnsupportedContent(
                            "Claude Code OAuth bridge supports base64 image sources only"
                        )
                    image_index += 1
                    media_type = str(source.get("media_type", "image/png"))
                    extension = {
                        "image/png": "png",
                        "image/jpeg": "jpg",
                        "image/gif": "gif",
                        "image/webp": "webp",
                    }.get(media_type, "img")
                    image_path = image_dir / f"input-image-{image_index}.{extension}"
                    try:
                        image_path.write_bytes(base64.b64decode(source["data"], validate=True))
                    except Exception as exc:
                        raise ClaudeCodeUnsupportedContent(
                            f"Invalid base64 image content: {type(exc).__name__}"
                        ) from exc
                    parts.append(
                        f"[IMAGE {image_index}] Use the Read tool to inspect `{image_path.name}`."
                    )
            text = "\n".join(part for part in parts if part)
        else:
            text = str(content)
        rendered.append(f"[{role}]\n{text}")
    return "\n\n".join(rendered)


def _decode_cli_payload(stdout: str) -> dict[str, Any]:
    try:
        payload = json.loads((stdout or "").strip())
    except json.JSONDecodeError as exc:
        raise AnthropicAuthError(f"Claude Code returned invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise AnthropicAuthError("Claude Code returned a non-object result envelope")
    return payload


def _extract_json(text: str) -> dict[str, Any] | list[Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        value = json.loads(stripped)
        if isinstance(value, (dict, list)):
            return value
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(stripped[index:])
            if isinstance(value, (dict, list)):
                return value
        except json.JSONDecodeError:
            continue
    raise AnthropicAuthError("Claude Code response did not contain valid structured JSON")
