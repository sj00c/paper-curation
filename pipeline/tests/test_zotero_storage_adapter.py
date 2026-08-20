"""Synthetic HTTP tests for the read-only Zotero storage adapters."""

from __future__ import annotations

import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.integrations.zotero.api import (
    ZoteroStorageAttachmentPort,
    ZoteroStorageSource,
)


class _Response(io.BytesIO):
    def __init__(self, body: bytes, headers: dict[str, str] | None = None) -> None:
        super().__init__(body)
        self.headers = headers or {}


class _Http:
    def __init__(self, routes: dict[tuple[str, int | None], _Response | Exception]) -> None:
        self.routes = routes
        self.calls: list[str] = []
        self.timeouts: list[float] = []

    def __call__(self, request: object, timeout: float) -> _Response:
        url = getattr(request, "full_url")
        parts = urlsplit(url)
        start = int(parse_qs(parts.query).get("start", ["0"])[0])
        self.calls.append(parts.path)
        self.timeouts.append(timeout)
        route = self.routes[(parts.path, start if "start=" in parts.query else None)]
        if isinstance(route, Exception):
            raise route
        return _Response(route.getvalue(), dict(route.headers))


def _json(value: object, headers: dict[str, str] | None = None) -> _Response:
    import json

    return _Response(json.dumps(value).encode(), headers)


def _item(key: str, data: dict[str, object]) -> dict[str, object]:
    return {"key": key, "version": 7, "data": data}


PDF = b"%PDF-synthetic"


class ZoteroStorageAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.cache = Path(self.temp.name) / "cache"
        self.base = "https://zotero.invalid"
        self.routes: dict[tuple[str, int | None], _Response | Exception] = {
            ("/keys/current", None): _json({"userID": 42}),
            ("/users/42/collections/COLLECTA", None): _json({"key": "COLLECTA"}),
            (
                "/users/42/collections/COLLECTA/items",
                0,
            ): _json(
                [
                    _item(
                        "PAPERONE",
                        {
                            "itemType": "journalArticle",
                            "collections": ["COLLECTA"],
                            "title": "First paper",
                            "abstractNote": "Abstract",
                            "DOI": "10/example",
                            "date": "2025-02-03",
                            "url": "https://example.invalid/paper",
                            "creators": [
                                {"name": "Research Group"},
                                {"firstName": "Ada", "lastName": "Lovelace"},
                            ],
                            "tags": [{"tag": "zeta"}, {"tag": "alpha"}],
                        },
                    )
                ],
                {"Total-Results": "1"},
            ),
            ("/users/42/items/PAPERONE", None): _json(
                _item("PAPERONE", {"collections": ["COLLECTA"]})
            ),
            ("/users/42/items/PAPERONE/children", 0): _json(
                [
                    _item(
                        "PDFONE",
                        {
                            "itemType": "attachment",
                            "parentItem": "PAPERONE",
                            "contentType": "application/pdf",
                            "linkMode": "imported_file",
                            "filename": "paper.pdf",
                            "md5": hashlib.md5(PDF).hexdigest(),
                        },
                    ),
                ],
                {"Total-Results": "1"},
            ),
            ("/users/42/items/PDFONE/file", None): _Response(
                PDF,
                {
                    "Content-Type": "application/pdf",
                    "ETag": f'"{hashlib.md5(PDF).hexdigest()}"',
                },
            ),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_pagination_collection_isolation_and_metadata_mapping(self) -> None:
        second = _item(
            "PAPERTWO",
            {"itemType": "journalArticle", "collections": ["COLLECTA"], "title": "Second"},
        )
        self.routes[("/users/42/collections/COLLECTA/items", 0)] = _json(
            [
                _item(
                    "PAPERONE",
                    {
                        "itemType": "journalArticle",
                        "collections": ["COLLECTA"],
                        "title": "First paper",
                        "creators": [
                            {"name": "Research Group"},
                            {"firstName": "Ada", "lastName": "Lovelace"},
                        ],
                        "tags": [{"tag": "zeta"}, {"tag": "alpha"}],
                    },
                )
            ],
            {"Total-Results": "2"},
        )
        self.routes[("/users/42/collections/COLLECTA/items", 1)] = _json(
            [second], {"Total-Results": "2"}
        )
        client = _Http(self.routes)
        papers = ZoteroStorageSource("secret", client, self.base).list_records("zotero", "COLLECTA")

        self.assertEqual([paper.record_id for paper in papers], ["PAPERONE", "PAPERTWO"])
        self.assertEqual(papers[0].authors, ("Research Group", "Ada Lovelace"))
        self.assertEqual(papers[0].tags, ("zeta", "alpha"))
        self.assertNotIn("/users/42/collections/COLLECTB/items", client.calls)

    def test_exact_attachment_atomic_download_and_cached_fingerprint_reuse(self) -> None:
        client = _Http(self.routes)
        source = ZoteroStorageSource("secret", client, self.base)
        paper = source.list_records("zotero", "COLLECTA")[0]
        attachment = source.list_attachments(paper)[0]
        port = ZoteroStorageAttachmentPort("secret", self.cache, client, self.base)

        artifact = port.materialize(paper, attachment)
        self.assertEqual(
            artifact.fingerprint, f"sha256:{hashlib.sha256(b'%PDF-synthetic').hexdigest()}"
        )
        self.assertTrue(Path(artifact.path).is_file())
        self.assertEqual(list(self.cache.glob("*.partial")), [])
        client.calls.clear()
        self.assertEqual(port.materialize(paper, attachment).fingerprint, artifact.fingerprint)
        self.assertNotIn("/users/42/items/PDFONE/file", client.calls)

    def test_children_are_paginated_and_only_imported_pdf_files_are_exposed(self) -> None:
        self.routes[("/users/42/items/PAPERONE/children", 0)] = _json(
            [
                _item(
                    "LINKED",
                    {
                        "itemType": "attachment",
                        "parentItem": "PAPERONE",
                        "contentType": "application/pdf",
                        "linkMode": "linked_file",
                        "filename": "linked.pdf",
                        "md5": hashlib.md5(PDF).hexdigest(),
                    },
                )
            ],
            {"Total-Results": "2"},
        )
        self.routes[("/users/42/items/PAPERONE/children", 1)] = _json(
            [
                _item(
                    "PDFONE",
                    {
                        "itemType": "attachment",
                        "parentItem": "PAPERONE",
                        "contentType": "application/pdf",
                        "linkMode": "imported_url",
                        "filename": "paper.pdf",
                        "md5": hashlib.md5(PDF).hexdigest(),
                    },
                )
            ],
            {"Total-Results": "2"},
        )
        client = _Http(self.routes)
        paper = ZoteroStorageSource("secret", client, self.base).list_records("zotero", "COLLECTA")[0]

        attachments = ZoteroStorageSource("secret", client, self.base).list_attachments(paper)

        self.assertEqual([attachment.attachment_id for attachment in attachments], ["PDFONE"])
        self.assertEqual(attachments[0].checksum, f"md5:{hashlib.md5(PDF).hexdigest()}")
        self.assertTrue(
            Path(
                ZoteroStorageAttachmentPort("secret", self.cache, client, self.base).materialize(
                    paper, attachments[0]
                ).path
            ).is_file()
        )

    def test_pagination_no_progress_and_cache_symlink_fail_closed(self) -> None:
        client = _Http(self.routes)
        source = ZoteroStorageSource("secret", client, self.base)
        paper = source.list_records("zotero", "COLLECTA")[0]
        attachment = source.list_attachments(paper)[0]
        self.cache.mkdir()
        outside = Path(self.temp.name) / "outside.pdf"
        outside.write_bytes(PDF)
        (self.cache / "PDFONE-paper.pdf").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ZoteroStorageAttachmentPort(
                "secret", self.cache, client, self.base
            ).materialize(paper, attachment)
        self.assertEqual(outside.read_bytes(), PDF)

        self.routes[("/users/42/items/PAPERONE/children", 0)] = _json(
            [], {"Total-Results": "1"}
        )
        with self.assertRaisesRegex(ValueError, "no progress"):
            source.list_attachments(paper)

    def test_download_metadata_mismatches_are_rejected_before_replacement(self) -> None:
        client = _Http(self.routes)
        source = ZoteroStorageSource("secret", client, self.base)
        paper = source.list_records("zotero", "COLLECTA")[0]
        attachment = source.list_attachments(paper)[0]
        self.routes[("/users/42/items/PDFONE/file", None)] = _Response(
            PDF, {"Content-Type": "application/pdf", "ETag": '"different"'}
        )
        with self.assertRaisesRegex(ValueError, "ETag"):
            ZoteroStorageAttachmentPort("secret", self.cache, client, self.base).materialize(
                paper, attachment
            )
        self.assertEqual(list(self.cache.glob("*")), [])

        self.routes[("/users/42/items/PDFONE/file", None)] = _Response(
            b"%PDF-different", {"Content-Type": "application/pdf", "ETag": '"7"'}
        )
        with self.assertRaisesRegex(ValueError, "MD5"):
            ZoteroStorageAttachmentPort("secret", self.cache, client, self.base).materialize(
                paper, attachment
            )
        self.assertEqual(list(self.cache.glob("*")), [])

    def test_stale_cache_is_revalidated_and_replaced(self) -> None:
        client = _Http(self.routes)
        source = ZoteroStorageSource("secret", client, self.base)
        paper = source.list_records("zotero", "COLLECTA")[0]
        initial = source.list_attachments(paper)[0]
        port = ZoteroStorageAttachmentPort("secret", self.cache, client, self.base)
        port.materialize(paper, initial)
        replacement = b"%PDF-replacement"
        self.routes[("/users/42/items/PAPERONE/children", 0)] = _json(
            [
                _item(
                    "PDFONE",
                    {
                        "itemType": "attachment",
                        "parentItem": "PAPERONE",
                        "contentType": "application/pdf",
                        "linkMode": "imported_file",
                        "filename": "paper.pdf",
                        "md5": hashlib.md5(replacement).hexdigest(),
                    },
                )
            ],
            {"Total-Results": "1"},
        )
        self.routes[("/users/42/items/PDFONE/file", None)] = _Response(
            replacement,
            {
                "Content-Type": "application/pdf",
                "ETag": f'"{hashlib.md5(replacement).hexdigest()}"',
            },
        )
        refreshed = source.list_attachments(paper)[0]

        artifact = port.materialize(paper, refreshed)

        self.assertEqual(Path(artifact.path).read_bytes(), replacement)
        self.assertEqual(artifact.fingerprint, f"sha256:{hashlib.sha256(replacement).hexdigest()}")

    def test_malformed_non_pdf_and_http_errors_are_actionable_without_secret_leakage(self) -> None:
        self.routes[("/users/42/items/PDFONE/file", None)] = _Response(
            b"not a PDF", {"Content-Type": "application/pdf", "ETag": '"7"'}
        )
        client = _Http(self.routes)
        source = ZoteroStorageSource("secret-key", client, self.base)
        paper = source.list_records("zotero", "COLLECTA")[0]
        attachment = source.list_attachments(paper)[0]
        with self.assertRaisesRegex(ValueError, "not a PDF"):
            ZoteroStorageAttachmentPort("secret-key", self.cache, client, self.base).materialize(
                paper, attachment
            )
        self.assertEqual(list(self.cache.glob("*")), [])
        self.routes[("/keys/current", None)] = HTTPError(
            f"{self.base}/keys/current?token=secret-key", 401, "no", {}, None
        )
        with self.assertRaises(RuntimeError) as raised:
            ZoteroStorageSource("secret-key", _Http(self.routes), self.base).list_records(
                "zotero", "COLLECTA"
            )
        self.assertIn("401", str(raised.exception))
        self.assertNotIn("secret-key", str(raised.exception))

    def test_timeout_is_validated_propagated_and_never_leaked(self) -> None:
        client = _Http(self.routes)
        ZoteroStorageSource("secret-timeout", client, self.base, timeout=12.5).list_records(
            "zotero", "COLLECTA"
        )
        self.assertEqual(client.timeouts, [12.5, 12.5, 12.5])
        for timeout in (0, float("inf"), float("nan"), True):
            with self.assertRaisesRegex(ValueError, "timeout") as raised:
                ZoteroStorageSource("secret-timeout", client, self.base, timeout=timeout)
            self.assertNotIn("secret-timeout", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
