"""Read-only Zotero Web API adapters using the ``zotero-storage`` transport."""

from __future__ import annotations

from hashlib import md5, sha256
import json
import math
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from paper_curation.domain.papers import ArtifactRef, Attachment, Paper


_ZOTERO_SOURCE_ID = "zotero"
_PDF_MEDIA_TYPE = "application/pdf"
_PAGE_SIZE = 100


class _Response(Protocol):
    headers: Any

    def read(self, size: int = -1) -> bytes: ...

    def close(self) -> None: ...


class _Opener(Protocol):
    def __call__(self, request: Request, timeout: float) -> _Response: ...


class _ZoteroApi:
    def __init__(
        self,
        api_key: str,
        opener: _Opener | Any | None,
        base_url: str,
        timeout: float,
    ) -> None:
        if not api_key.strip():
            raise ValueError("Zotero API key is required")
        if not base_url.strip():
            raise ValueError("Zotero API base URL is required")
        if isinstance(timeout, bool) or not isinstance(timeout, int | float) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("Zotero API timeout must be a positive finite number")
        self._api_key = api_key
        self._opener = opener or urlopen
        self._base_url = base_url.rstrip("/")
        self._timeout = float(timeout)
        self._owner_id: str | None = None

    def _owner(self) -> str:
        if self._owner_id is None:
            response = self._json("/keys/current")
            if not isinstance(response, dict):
                raise ValueError("Zotero API /keys/current response is malformed")
            owner_id = response.get("userID")
            if not isinstance(owner_id, int | str) or not str(owner_id).strip():
                raise ValueError("Zotero API /keys/current response has no userID")
            self._owner_id = str(owner_id)
        return self._owner_id

    def _path(self, suffix: str) -> str:
        return f"/users/{quote(self._owner(), safe='')}{suffix}"

    def _json(self, path: str, query: Mapping[str, str | int] | None = None) -> Any:
        response = self._request(path, query)
        try:
            payload = response.read()
        except Exception:
            try:
                response.close()
            except Exception:
                pass
            raise
        else:
            response.close()
        try:
            return json.loads(payload)
        except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Zotero API returned invalid JSON") from exc

    def _request(
        self, path: str, query: Mapping[str, str | int] | None = None
    ) -> _Response:
        url = f"{self._base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        request = Request(
            url,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Zotero-API-Version": "3",
            },
            method="GET",
        )
        open_request: Callable[[Request], _Response] = getattr(self._opener, "open", self._opener)
        try:
            return open_request(request, timeout=self._timeout)
        except HTTPError as exc:
            try:
                exc.close()
            except Exception:
                pass
            raise RuntimeError(
                f"Zotero API request failed with HTTP status {exc.code}"
            ) from exc
        except URLError as exc:
            raise RuntimeError("Zotero API request failed due to a network error") from exc
        except OSError as exc:
            raise RuntimeError("Zotero API request failed due to an I/O error") from exc
        except Exception as exc:
            raise RuntimeError("Zotero API request failed") from exc

    def _require_collection(self, scope_id: str) -> None:
        if not scope_id.strip():
            raise ValueError("scope_id must be an exact Zotero collection key")
        collection = self._json(
            self._path(f"/collections/{quote(scope_id, safe='')}")
        )
        if not isinstance(collection, dict) or collection.get("key") != scope_id:
            raise ValueError("Zotero API returned a collection with a different key")

    def _collection_items(self, scope_id: str) -> tuple[dict[str, Any], ...]:
        self._require_collection(scope_id)
        return self._paginated_items(
            self._path(f"/collections/{quote(scope_id, safe='')}/items")
        )

    def _paginated_items(self, path: str) -> tuple[dict[str, Any], ...]:
        start = 0
        results: list[dict[str, Any]] = []
        total: int | None = None
        while total is None or start < total:
            response = self._request(
                path,
                {"format": "json", "limit": _PAGE_SIZE, "start": start},
            )
            try:
                payload = response.read()
                header_total = _header(response.headers, "Total-Results")
            except Exception:
                try:
                    response.close()
                except Exception:
                    pass
                raise
            else:
                response.close()
            try:
                page = json.loads(payload)
            except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError("Zotero API returned invalid JSON") from exc
            if not isinstance(page, list) or not all(isinstance(item, dict) for item in page):
                raise ValueError("Zotero API collection items response is malformed")
            if header_total is not None:
                try:
                    total = int(header_total)
                except ValueError as exc:
                    raise ValueError("Zotero API returned an invalid Total-Results header") from exc
                if total < start + len(page):
                    raise ValueError("Zotero API collection pagination is inconsistent")
            results.extend(page)
            start += len(page)
            if not page:
                if total is not None and start < total:
                    raise ValueError("Zotero API pagination made no progress")
                break
            if total is None and len(page) < _PAGE_SIZE:
                break
        return tuple(results)

    @staticmethod
    def _validate_source(source_id: str) -> None:
        if source_id != _ZOTERO_SOURCE_ID:
            raise ValueError("Zotero storage source requires source_id 'zotero'")


class ZoteroStorageSource(_ZoteroApi):
    """Expose an exact Zotero Web API collection through the curation source port."""

    def __init__(
        self,
        api_key: str,
        opener: _Opener | Any | None = None,
        base_url: str = "https://api.zotero.org",
        timeout: float = 30.0,
    ) -> None:
        super().__init__(api_key, opener, base_url, timeout)

    def list_records(self, source_id: str, scope_id: str) -> tuple[Paper, ...]:
        self._validate_source(source_id)
        papers: list[Paper] = []
        for item in self._collection_items(scope_id):
            data = _item_data(item)
            if data.get("itemType") in {"attachment", "note", "annotation"}:
                continue
            if item.get("key") is None or not isinstance(item["key"], str):
                raise ValueError("Zotero API item has no exact item key")
            collections = data.get("collections")
            if not isinstance(collections, list) or scope_id not in collections:
                raise ValueError("Zotero API item does not belong to the requested collection")
            papers.append(
                Paper(
                    source_id=_ZOTERO_SOURCE_ID,
                    scope_id=scope_id,
                    record_id=item["key"],
                    title=_required_text(data, "title", "Zotero API item"),
                    authors=_creators(data),
                    abstract=_text(data, "abstractNote"),
                    doi=_text(data, "DOI"),
                    published=_text(data, "date"),
                    url=_text(data, "url"),
                    tags=_tags(data),
                )
            )
        return tuple(papers)

    def list_attachments(self, paper: Paper) -> tuple[Attachment, ...]:
        self._validate_paper(paper)
        children = self._children(paper.record_id)
        attachments: list[Attachment] = []
        for item in children:
            data = _item_data(item)
            if (
                data.get("itemType") != "attachment"
                or _text(data, "contentType").lower() != _PDF_MEDIA_TYPE
                or _text(data, "linkMode") not in {"imported_file", "imported_url"}
            ):
                continue
            if item.get("key") is None or not isinstance(item["key"], str):
                raise ValueError("Zotero API attachment has no exact item key")
            if data.get("parentItem") != paper.record_id:
                raise ValueError("Zotero API attachment does not belong to the requested paper")
            attachments.append(
                Attachment(
                    source_id=_ZOTERO_SOURCE_ID,
                    scope_id=paper.scope_id,
                    record_id=paper.record_id,
                    attachment_id=item["key"],
                    filename=_filename(data),
                    media_type=_PDF_MEDIA_TYPE,
                    checksum=_md5_checksum(data),
                )
            )
        return tuple(attachments)

    def _validate_paper(self, paper: Paper) -> None:
        self._validate_source(paper.source_id)
        self._require_collection(paper.scope_id)
        item = self._json(self._path(f"/items/{quote(paper.record_id, safe='')}"))
        data = _item_data(item)
        if item.get("key") != paper.record_id or paper.scope_id not in data.get("collections", []):
            raise ValueError("paper does not belong to the requested Zotero collection")

    def _children(self, record_id: str) -> tuple[dict[str, Any], ...]:
        return self._paginated_items(
            self._path(f"/items/{quote(record_id, safe='')}/children")
        )


class ZoteroStorageAttachmentPort(_ZoteroApi):
    """Download one exact Zotero PDF attachment into a local cache."""

    def __init__(
        self,
        api_key: str,
        cache_dir: str | Path,
        opener: _Opener | Any | None = None,
        base_url: str = "https://api.zotero.org",
        timeout: float = 30.0,
    ) -> None:
        super().__init__(api_key, opener, base_url, timeout)
        raw_cache = Path(cache_dir).expanduser()
        if raw_cache.is_symlink():
            raise ValueError("Zotero cache path must not be a symlink")
        self._cache_dir = raw_cache.resolve(strict=False)

    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef:
        self._validate_source(paper.source_id)
        if (
            attachment.source_id != paper.source_id
            or attachment.scope_id != paper.scope_id
            or attachment.record_id != paper.record_id
        ):
            raise ValueError("attachment does not belong to paper")
        remote = self._validate_attachment(paper, attachment)
        destination = self._destination(attachment)
        if destination.is_symlink():
            raise ValueError("Zotero cache entry must not be a symlink")
        if destination.is_file():
            try:
                return _artifact(destination, attachment.filename, attachment.checksum)
            except ValueError:
                destination.unlink()
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{attachment.attachment_id}-", suffix=".partial", dir=self._cache_dir
        )
        temporary = Path(temporary_name)
        try:
            response = self._request(
                self._path(f"/items/{quote(attachment.attachment_id, safe='')}/file")
            )
            try:
                digest, downloaded_md5, signature = _write_and_hash(response, descriptor)
                etag = _normalized_etag(_header(response.headers, "ETag"))
            except Exception:
                try:
                    response.close()
                except Exception:
                    pass
                raise
            else:
                response.close()
            if signature != b"%PDF-":
                raise ValueError("Zotero attachment download is not a PDF")
            _validate_checksum(attachment.checksum, downloaded_md5)
            expected_etag = _normalized_etag(
                attachment.checksum.removeprefix("md5:")
            )
            if etag != expected_etag:
                raise ValueError("Zotero attachment ETag does not match its metadata")
            os.replace(temporary, destination)
            return ArtifactRef(attachment.filename, str(destination), f"sha256:{digest}")
        except Exception:
            try:
                os.close(descriptor)
            except OSError:
                pass
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            raise

    def _validate_attachment(self, paper: Paper, attachment: Attachment) -> dict[str, Any]:
        parent = self._json(self._path(f"/items/{quote(paper.record_id, safe='')}"))
        parent_data = _item_data(parent)
        if parent.get("key") != paper.record_id or paper.scope_id not in parent_data.get("collections", []):
            raise ValueError("paper does not belong to the requested Zotero collection")
        children = self._paginated_items(
            self._path(f"/items/{quote(paper.record_id, safe='')}/children")
        )
        matches = [
            item
            for item in children
            if isinstance(item, dict) and item.get("key") == attachment.attachment_id
        ]
        if len(matches) != 1:
            raise ValueError("Zotero PDF attachment is missing or ambiguous")
        data = _item_data(matches[0])
        if (
            data.get("itemType") != "attachment"
            or data.get("parentItem") != paper.record_id
            or _text(data, "contentType").lower() != _PDF_MEDIA_TYPE
            or _text(data, "linkMode") not in {"imported_file", "imported_url"}
            or _filename(data) != attachment.filename
            or attachment.media_type.lower() != _PDF_MEDIA_TYPE
            or _md5_checksum(data) != attachment.checksum
        ):
            raise ValueError("attachment metadata does not match Zotero")
        version = matches[0].get("version")
        if isinstance(version, bool) or not isinstance(version, int | str) or not str(version).strip():
            raise ValueError("Zotero attachment has no version")
        return {"version": version}

    def _destination(self, attachment: Attachment) -> Path:
        filename = _filename({"filename": attachment.filename})
        if not attachment.attachment_id or Path(attachment.attachment_id).name != attachment.attachment_id:
            raise ValueError("Zotero attachment key is invalid")
        cache = self._cache_dir
        current = cache
        while True:
            if current.is_symlink():
                raise ValueError("Zotero cache path must not contain symlinks")
            if current == current.parent:
                break
            current = current.parent
        destination = cache / f"{attachment.attachment_id}-{filename}"
        if destination.parent != cache:
            raise ValueError("Zotero cache path escapes its root")
        return destination


def _header(headers: Any, name: str) -> str | None:
    if headers is None:
        return None
    if hasattr(headers, "get"):
        value = headers.get(name)
        if value is None:
            value = headers.get(name.lower())
        return str(value) if value is not None else None
    return None


def _item_data(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict) or not isinstance(item.get("data"), dict):
        raise ValueError("Zotero API item response is malformed")
    return item["data"]


def _text(data: Mapping[str, Any], field: str) -> str:
    value = data.get(field, "")
    return value.strip() if isinstance(value, str) else ""


def _required_text(data: Mapping[str, Any], field: str, context: str) -> str:
    value = _text(data, field)
    if not value:
        raise ValueError(f"{context} has no {field}")
    return value


def _creators(data: Mapping[str, Any]) -> tuple[str, ...]:
    creators = data.get("creators", [])
    if not isinstance(creators, list):
        raise ValueError("Zotero API item creators are malformed")
    names: list[str] = []
    for creator in creators:
        if not isinstance(creator, dict):
            raise ValueError("Zotero API item creator is malformed")
        name = _text(creator, "name") or " ".join(
            part for part in (_text(creator, "firstName"), _text(creator, "lastName")) if part
        )
        if name:
            names.append(name)
    return tuple(names)


def _tags(data: Mapping[str, Any]) -> tuple[str, ...]:
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        raise ValueError("Zotero API item tags are malformed")
    return tuple(
        tag["tag"].strip()
        for tag in tags
        if isinstance(tag, dict) and isinstance(tag.get("tag"), str) and tag["tag"].strip()
    )


def _filename(data: Mapping[str, Any]) -> str:
    filename = _required_text(data, "filename", "Zotero API attachment")
    if Path(filename).name != filename:
        raise ValueError("Zotero API attachment filename is invalid")
    return filename


def _md5_checksum(data: Mapping[str, Any]) -> str:
    value = _required_text(data, "md5", "Zotero API attachment").lower()
    if len(value) != 32 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError("Zotero API attachment md5 is invalid")
    return f"md5:{value}"


def _normalized_etag(value: str | None) -> str:
    if value is None:
        raise ValueError("Zotero attachment response has no ETag")
    normalized = value.strip()
    if normalized.startswith("W/"):
        normalized = normalized[2:].strip()
    if len(normalized) >= 2 and normalized[0] == normalized[-1] == '"':
        normalized = normalized[1:-1]
    if not normalized:
        raise ValueError("Zotero attachment ETag is invalid")
    return normalized


def _write_and_hash(response: _Response, descriptor: int) -> tuple[str, str, bytes]:
    sha256_digest = sha256()
    md5_digest = md5()
    signature = b""
    with os.fdopen(descriptor, "wb") as output:
        while chunk := response.read(1024 * 1024):
            if not signature:
                signature = chunk[:5]
            sha256_digest.update(chunk)
            md5_digest.update(chunk)
            output.write(chunk)
    return sha256_digest.hexdigest(), md5_digest.hexdigest(), signature


def _artifact(path: Path, name: str, expected_checksum: str) -> ArtifactRef:
    sha256_digest = sha256()
    md5_digest = md5()
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        source = os.fdopen(descriptor, "rb")
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise
    with source:
        signature = source.read(5)
        if signature != b"%PDF-":
            raise ValueError("cached Zotero attachment is not a PDF")
        sha256_digest.update(signature)
        md5_digest.update(signature)
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            sha256_digest.update(chunk)
            md5_digest.update(chunk)
    _validate_checksum(expected_checksum, md5_digest.hexdigest())
    return ArtifactRef(name, str(path), f"sha256:{sha256_digest.hexdigest()}")


def _validate_checksum(expected: str, actual: str) -> None:
    if not expected.startswith("md5:"):
        raise ValueError("attachment checksum must be an MD5 digest")
    normalized = expected.removeprefix("md5:").lower()
    if len(normalized) != 32 or any(character not in "0123456789abcdef" for character in normalized):
        raise ValueError("attachment checksum must be an MD5 digest")
    if normalized != actual:
        raise ValueError("Zotero attachment MD5 does not match its metadata")
