"""Fail-closed, read-only Zotero traversal and bounded PDF acquisition.

The transport is deliberately injected: callers can use the default urllib transport in
production and deterministic, network-free transports in tests.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import ssl
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Protocol


ZOTERO_ORIGIN = "https://api.zotero.org"
_PAGE_SIZE = 100
_MAX_PAGES = 10


class ZoteroBoundedError(RuntimeError):
    """A remote response or a requested effect exceeded the read-only contract."""


@dataclass(frozen=True)
class ZoteroBounds:
    max_attempts: int = 128
    max_redirects_per_request: int = 2
    max_redirects_total: int = 8
    max_response_bytes: int = 2 * 1024 * 1024
    max_metadata_bytes: int = 8 * 1024 * 1024
    max_pdf_bytes: int = 50 * 1024 * 1024
    max_parent_lookups: int = 100
    max_attachment_heads: int = 20
    connect_timeout: float = 5.0
    read_timeout: float = 15.0
    wall_timeout: float = 120.0


@dataclass(frozen=True)
class TransportResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes = b""


class ZoteroTransport(Protocol):
    def request(self, method: str, url: str, headers: Mapping[str, str], *,
                connect_timeout: float, read_timeout: float) -> TransportResponse: ...


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


class UrllibZoteroTransport:
    """The only built-in transport; it deliberately follows no redirects itself."""

    def __init__(self, ssl_context: ssl.SSLContext | None = None):
        handlers: list[Any] = [_NoRedirect()]
        if ssl_context is not None:
            handlers.append(urllib.request.HTTPSHandler(context=ssl_context))
        self._opener = urllib.request.build_opener(*handlers)

    def request(self, method: str, url: str, headers: Mapping[str, str], *,
                connect_timeout: float, read_timeout: float) -> TransportResponse:
        del read_timeout  # urllib exposes one timeout; the caller still records both bounds.
        request = urllib.request.Request(url, headers=dict(headers), method=method)
        try:
            with self._opener.open(request, timeout=connect_timeout) as response:
                return TransportResponse(response.status, dict(response.headers.items()), response.read())
        except urllib.error.HTTPError as error:
            return TransportResponse(error.code, dict(error.headers.items()), error.read())


def _header(headers: Mapping[str, str], name: str) -> str | None:
    name = name.lower()
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def _item_data(item: Mapping[str, Any]) -> Mapping[str, Any]:
    data = item.get("data", item)
    if not isinstance(data, Mapping):
        raise ZoteroBoundedError("invalid-item-data")
    return data


def _key(item: Mapping[str, Any]) -> str:
    key = _item_data(item).get("key") or item.get("key")
    if not isinstance(key, str) or not key:
        raise ZoteroBoundedError("missing-item-key")
    return key


def _date_added(item: Mapping[str, Any]) -> str:
    value = _item_data(item).get("dateAdded")
    if not isinstance(value, str) or not value:
        raise ZoteroBoundedError("missing-date-added")
    return value


class ZoteroBoundedReader:
    """A complete bounded collection reader.  It has no Zotero write operation."""

    def __init__(self, transport: ZoteroTransport, api_key: str, user_id: str,
                 *, origin: str = ZOTERO_ORIGIN, bounds: ZoteroBounds = ZoteroBounds(),
                 clock: Callable[[], float] = time.monotonic):
        parsed = urllib.parse.urlsplit(origin)
        if (parsed.scheme != "https" or parsed.netloc != "api.zotero.org" or
                parsed.path not in ("", "/") or parsed.query or parsed.fragment):
            raise ValueError("origin must be the exact HTTPS Zotero origin")
        self.transport = transport
        self.api_key = api_key
        self.user_id = str(user_id)
        self.origin = f"https://{parsed.netloc}"
        self.bounds = bounds
        self.clock = clock
        self._started = clock()
        self._attempts = 0
        self._redirects = 0
        self._metadata_bytes = 0
        self._parent_lookups = 0
        self._attachment_heads = 0

    def _wall_ok(self) -> None:
        if self.clock() - self._started >= self.bounds.wall_timeout:
            raise ZoteroBoundedError("wall-time-budget")

    def _request(self, method: str, path: str, *, pdf: bool = False) -> TransportResponse:
        if method not in {"GET", "HEAD"}:
            raise ZoteroBoundedError("read-only-method-required")
        url = urllib.parse.urljoin(self.origin + "/", path.lstrip("/"))
        redirects_here = 0
        while True:
            self._wall_ok()
            if self._attempts >= self.bounds.max_attempts:
                raise ZoteroBoundedError("attempt-budget")
            self._attempts += 1
            response = self.transport.request(
                method, url,
                {"Zotero-API-Key": self.api_key, "User-Agent": "paper-curation-bounded-reader"},
                connect_timeout=self.bounds.connect_timeout, read_timeout=self.bounds.read_timeout,
            )
            self._wall_ok()
            if response.status not in {301, 302, 303, 307, 308}:
                self._validate_response_size(response, pdf=pdf)
                if not pdf:
                    if self._metadata_bytes + len(response.body) > self.bounds.max_metadata_bytes:
                        raise ZoteroBoundedError("metadata-aggregate-budget")
                    self._metadata_bytes += len(response.body)
                return response
            location = _header(response.headers, "Location")
            if not location:
                raise ZoteroBoundedError("redirect-without-location")
            if redirects_here >= self.bounds.max_redirects_per_request:
                raise ZoteroBoundedError("redirect-request-budget")
            if self._redirects >= self.bounds.max_redirects_total:
                raise ZoteroBoundedError("redirect-total-budget")
            target = urllib.parse.urlsplit(urllib.parse.urljoin(url, location))
            if target.scheme != "https" or target.netloc != urllib.parse.urlsplit(self.origin).netloc:
                raise ZoteroBoundedError("unsafe-redirect-origin")
            redirects_here += 1
            self._redirects += 1
            url = target.geturl()

    def _validate_response_size(self, response: TransportResponse, *, pdf: bool) -> None:
        limit = self.bounds.max_pdf_bytes if pdf else self.bounds.max_response_bytes
        declared = _header(response.headers, "Content-Length")
        if declared is not None:
            try:
                if int(declared) > limit:
                    raise ZoteroBoundedError("pdf-response-budget" if pdf else "metadata-response-budget")
            except ValueError as exc:
                raise ZoteroBoundedError("invalid-content-length") from exc
        if len(response.body) > limit:
            raise ZoteroBoundedError("pdf-response-budget" if pdf else "metadata-response-budget")

    def _json(self, path: str) -> tuple[list[Mapping[str, Any]], TransportResponse]:
        response = self._request("GET", path)
        if response.status != 200:
            raise ZoteroBoundedError(f"unexpected-status-{response.status}")
        try:
            value = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ZoteroBoundedError("invalid-json") from exc
        if not isinstance(value, list):
            raise ZoteroBoundedError("expected-json-array")
        if not all(isinstance(item, Mapping) for item in value):
            raise ZoteroBoundedError("invalid-item")
        return value, response

    def collection_items(self, collection_key: str) -> list[Mapping[str, Any]]:
        """Read exactly the complete, version-pinned collection (at most 1000 items)."""
        all_items: list[Mapping[str, Any]] = []
        seen: set[str] = set()
        total: int | None = None
        version: str | None = None
        for page in range(_MAX_PAGES):
            start = page * _PAGE_SIZE
            path = (f"users/{urllib.parse.quote(self.user_id, safe='')}/collections/"
                    f"{urllib.parse.quote(collection_key, safe='')}/items/top?"
                    f"limit={_PAGE_SIZE}&start={start}&sort=dateAdded&direction=asc&format=json")
            batch, response = self._json(path)
            raw_total = _header(response.headers, "Total-Results")
            raw_version = _header(response.headers, "Last-Modified-Version")
            if raw_total is None or raw_version is None:
                raise ZoteroBoundedError("missing-pagination-pin")
            try:
                page_total = int(raw_total)
            except ValueError as exc:
                raise ZoteroBoundedError("invalid-total-results") from exc
            if page_total < 0 or page_total > _MAX_PAGES * _PAGE_SIZE:
                raise ZoteroBoundedError("total-results-budget")
            if total is None:
                total, version = page_total, raw_version
            elif total != page_total or version != raw_version:
                raise ZoteroBoundedError("pagination-drift")
            if len(batch) > _PAGE_SIZE:
                raise ZoteroBoundedError("page-size-budget")
            for item in batch:
                key = _key(item)
                _date_added(item)
                if key in seen:
                    raise ZoteroBoundedError("duplicate-item-key")
                seen.add(key)
                all_items.append(item)
            if len(all_items) == total:
                break
            if page == _MAX_PAGES - 1 and len(batch) == _PAGE_SIZE:
                raise ZoteroBoundedError("page-ten-more")
            if len(batch) < _PAGE_SIZE:
                break
        if total is None or len(all_items) != total:
            raise ZoteroBoundedError("total-results-mismatch")
        return sorted(all_items, key=lambda item: (_date_added(item), _key(item)))

    def children(self, parent: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        if self._parent_lookups >= self.bounds.max_parent_lookups:
            raise ZoteroBoundedError("parent-lookup-budget")
        self._parent_lookups += 1
        key = _key(parent)
        children, _ = self._json(
            f"users/{urllib.parse.quote(self.user_id, safe='')}/items/"
            f"{urllib.parse.quote(key, safe='')}/children?format=json"
        )
        return children

    def pdf_attachments(self, parents: list[Mapping[str, Any]]) -> list[tuple[Mapping[str, Any], Mapping[str, Any]]]:
        """Fetch children in canonical parent order and return de-duplicated PDF candidates."""
        candidates: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
        seen: set[str] = set()
        for parent in sorted(parents, key=lambda item: (_date_added(item), _key(item))):
            for attachment in self.children(parent):
                data = _item_data(attachment)
                key = _key(attachment)
                if key in seen:
                    continue
                seen.add(key)
                if data.get("itemType") != "attachment":
                    continue
                if str(data.get("contentType", "")).lower() != "application/pdf":
                    continue
                if data.get("parentItem") != _key(parent):
                    continue
                candidates.append((parent, attachment))
        return sorted(candidates, key=lambda pair: (_date_added(pair[0]), _key(pair[0]), _key(pair[1])))

    def first_complete_pdf(self, parents: list[Mapping[str, Any]]) -> tuple[Mapping[str, Any], Mapping[str, Any]] | None:
        for parent, attachment in self.pdf_attachments(parents):
            if self._attachment_heads >= self.bounds.max_attachment_heads:
                raise ZoteroBoundedError("attachment-head-budget")
            self._attachment_heads += 1
            response = self._request("HEAD", self._file_path(attachment), pdf=True)
            if response.status == 200:
                return parent, attachment
        return None

    def download_pdf(self, attachment: Mapping[str, Any]) -> bytes:
        response = self._request("GET", self._file_path(attachment), pdf=True)
        if response.status != 200:
            raise ZoteroBoundedError(f"unexpected-pdf-status-{response.status}")
        return response.body

    def _file_path(self, attachment: Mapping[str, Any]) -> str:
        return (f"users/{urllib.parse.quote(self.user_id, safe='')}/items/"
                f"{urllib.parse.quote(_key(attachment), safe='')}/file")


_TOKEN_RE = re.compile(r"\S+")


def validate_pdf_text(pdf: bytes, parser: Callable[[bytes], Mapping[str, Any] | str]) -> str:
    """Reject malformed/encrypted/low-text PDFs before a downstream paid operation."""
    if not pdf.startswith(b"%PDF-"):
        raise ZoteroBoundedError("invalid-pdf-signature")
    result = parser(pdf)
    if isinstance(result, str):
        text, encrypted = result, False
    elif isinstance(result, Mapping):
        text = result.get("text", "")
        encrypted = bool(result.get("encrypted", False))
    else:
        raise ZoteroBoundedError("invalid-parser-result")
    if encrypted:
        raise ZoteroBoundedError("encrypted-pdf")
    if not isinstance(text, str):
        raise ZoteroBoundedError("invalid-extracted-text")
    if len("".join(text.split())) < 500 or len(_TOKEN_RE.findall(text)) < 50:
        raise ZoteroBoundedError("insufficient-extracted-text")
    return text


@contextmanager
def bounded_scratch_pdf(pdf: bytes, scratch_dir: str | os.PathLike[str]) -> Iterator[Path]:
    """Hash then atomically materialize a 0600 PDF, always deleting it on exit."""
    if not pdf.startswith(b"%PDF-"):
        raise ZoteroBoundedError("invalid-pdf-signature")
    digest = hashlib.sha256(pdf).hexdigest()
    directory = Path(scratch_dir)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    target = directory / f"{digest}.pdf"
    fd, temporary = tempfile.mkstemp(prefix=f".{digest}.", suffix=".tmp", dir=directory)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(pdf)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        os.chmod(target, 0o600)
        yield target
    finally:
        for path in (temporary, target):
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass


def acquire_first_text_ready_pdf(reader: ZoteroBoundedReader, collection_key: str,
                                 scratch_dir: str | os.PathLike[str],
                                 parser: Callable[[bytes], Mapping[str, Any] | str]) -> tuple[Mapping[str, Any], Mapping[str, Any], str]:
    """Acquire only the deterministic first complete-set PDF and apply the cost gate.

    The scratch file is intentionally cleaned before return; downstream callers receive
    extracted text, not a retained local PDF.
    """
    parents = reader.collection_items(collection_key)
    chosen = reader.first_complete_pdf(parents)
    if chosen is None:
        raise ZoteroBoundedError("no-complete-pdf")
    parent, attachment = chosen
    pdf = reader.download_pdf(attachment)
    text = validate_pdf_text(pdf, parser)
    with bounded_scratch_pdf(pdf, scratch_dir):
        pass
    return parent, attachment, text
