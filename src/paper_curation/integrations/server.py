"""Local-only static HTTP server adapter for a validated site plan."""

from __future__ import annotations

import mimetypes
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import ClassVar
from urllib.parse import unquote, urlsplit

from paper_curation.application.serve import ServeSite, ServeSitePlan, ServeSiteRequest

_CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".wasm": "application/wasm",
    ".xml": "application/xml; charset=utf-8",
}
_SENSITIVE_NAMES = frozenset({"_local_keys.json", "config.json", "credentials.json"})
_SENSITIVE_SUFFIXES = frozenset({".key", ".pem", ".p12", ".pfx"})


def _content_type(path: Path) -> str:
    known = _CONTENT_TYPES.get(path.suffix.casefold())
    if known:
        return known
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def _site_file(root: Path, request_path: str) -> Path | None:
    """Return a regular file under *root*, never a directory or escaped path."""
    try:
        decoded = unquote(urlsplit(request_path).path, encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        return None
    if "\\" in decoded:
        return None
    relative = decoded.lstrip("/")
    if not relative:
        relative = "index.html"
    candidate_path = PurePosixPath(relative)
    if candidate_path.is_absolute() or any(part in {"", ".", ".."} for part in candidate_path.parts):
        return None
    if any(part.startswith(".") for part in candidate_path.parts):
        return None
    if (
        candidate_path.name.casefold() in _SENSITIVE_NAMES
        or Path(candidate_path.name).suffix.casefold() in _SENSITIVE_SUFFIXES
    ):
        return None
    try:
        candidate = (root / Path(*candidate_path.parts)).resolve(strict=True)
        candidate.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def _handler_for(root: Path) -> type[BaseHTTPRequestHandler]:
    class StaticSiteHandler(BaseHTTPRequestHandler):
        site_root: ClassVar[Path] = root
        protocol_version = "HTTP/1.1"

        def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
            self._serve_file(include_body=True)

        def do_HEAD(self) -> None:  # noqa: N802 - stdlib callback name
            self._serve_file(include_body=False)

        def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
            self._method_not_allowed()

        def do_PUT(self) -> None:  # noqa: N802 - stdlib callback name
            self._method_not_allowed()

        def do_DELETE(self) -> None:  # noqa: N802 - stdlib callback name
            self._method_not_allowed()

        def do_PATCH(self) -> None:  # noqa: N802 - stdlib callback name
            self._method_not_allowed()

        def do_OPTIONS(self) -> None:  # noqa: N802 - stdlib callback name
            self._method_not_allowed()

        def log_message(self, _format: str, *_args: object) -> None:
            """Keep local serving quiet and avoid leaking request paths to logs."""

        def _method_not_allowed(self) -> None:
            self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
            self.send_header("Allow", "GET, HEAD")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def _serve_file(self, *, include_body: bool) -> None:
            path = _site_file(self.site_root, self.path)
            if path is None:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            try:
                content = path.read_bytes()
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", _content_type(path))
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if include_body:
                self.wfile.write(content)

    return StaticSiteHandler


@dataclass(slots=True)
class LocalStaticServerHandle:
    """A running local server with deterministic, idempotent shutdown."""

    _server: ThreadingHTTPServer
    _thread: threading.Thread

    @property
    def host(self) -> str:
        return str(self._server.server_address[0])

    @property
    def port(self) -> int:
        return int(self._server.server_address[1])

    @property
    def url(self) -> str:
        host = f"[{self.host}]" if ":" in self.host else self.host
        return f"http://{host}:{self.port}"

    @property
    def running(self) -> bool:
        return self._thread.is_alive()

    def wait(self) -> None:
        """Block until the server stops or the caller interrupts the wait."""
        self._thread.join()

    def stop(self) -> None:
        """Stop accepting requests and release the bound local socket."""
        if self._thread.is_alive():
            self._server.shutdown()
            self._thread.join()
        self._server.server_close()

    close = stop

    def __enter__(self) -> LocalStaticServerHandle:
        return self

    def __exit__(self, *_args: object) -> None:
        self.stop()


class LocalStaticServer:
    """Performs the sole serving side effect for a :class:`ServeSitePlan`."""

    def start(self, plan: ServeSitePlan) -> LocalStaticServerHandle:
        if not isinstance(plan, ServeSitePlan):
            raise TypeError("plan must be a ServeSitePlan")
        validated = ServeSite().plan(
            ServeSiteRequest(
                site_root=plan.site_root,
                host=plan.host,
                port=plan.port,
                allow_public_bind=plan.allow_public_bind,
            )
        )
        server = ThreadingHTTPServer(
            (validated.host, validated.port),
            _handler_for(validated.site_root),
        )
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, name="paper-curation-static-server", daemon=True)
        thread.start()
        return LocalStaticServerHandle(server, thread)
