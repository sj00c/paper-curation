"""Synthetic contract tests for the read-only local Zotero adapter."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.integrations.zotero.local import (
    ZoteroLocalAttachmentPort,
    ZoteroLocalSource,
)


class ZoteroLocalAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.database = root / "zotero.sqlite"
        self.storage = root / "storage"
        self.storage.mkdir()
        self.linked_pdf = root / "linked.pdf"
        self.linked_pdf.write_bytes(b"%PDF-linked")
        self._storage_file("STORAGEPDF", "stored.pdf", b"%PDF-stored")
        self._storage_file("NOTPDF", "not-pdf.pdf", b"not a PDF")
        self._create_library()
        self.source = ZoteroLocalSource(self.database)
        self.attachments = ZoteroLocalAttachmentPort(self.database, self.storage)

    def tearDown(self) -> None:
        self.attachments.close()
        self.source.close()
        self.temporary.cleanup()

    def _storage_file(self, attachment_id: str, filename: str, content: bytes) -> Path:
        directory = self.storage / attachment_id
        directory.mkdir()
        path = directory / filename
        path.write_bytes(content)
        return path

    def _create_library(self) -> None:
        connection = sqlite3.connect(self.database)
        connection.executescript(
            """
            CREATE TABLE collections (collectionID INTEGER PRIMARY KEY, libraryID INTEGER, key TEXT);
            CREATE TABLE collectionItems (collectionID INTEGER, itemID INTEGER, orderIndex INTEGER);
            CREATE TABLE items (itemID INTEGER PRIMARY KEY, libraryID INTEGER, key TEXT, itemTypeID INTEGER);
            CREATE TABLE itemTypes (itemTypeID INTEGER PRIMARY KEY, typeName TEXT);
            CREATE TABLE deletedCollections (collectionID INTEGER PRIMARY KEY);
            CREATE TABLE deletedItems (itemID INTEGER PRIMARY KEY);
            CREATE TABLE fields (fieldID INTEGER PRIMARY KEY, fieldName TEXT);
            CREATE TABLE itemDataValues (valueID INTEGER PRIMARY KEY, value TEXT);
            CREATE TABLE itemData (itemID INTEGER, fieldID INTEGER, valueID INTEGER);
            CREATE TABLE creators (creatorID INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, fieldMode INTEGER);
            CREATE TABLE itemCreators (itemID INTEGER, creatorID INTEGER, orderIndex INTEGER);
            CREATE TABLE tags (tagID INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE itemTags (itemID INTEGER, tagID INTEGER);
            CREATE TABLE itemAttachments (itemID INTEGER, parentItemID INTEGER, contentType TEXT, path TEXT, linkMode INTEGER);
            """
        )
        connection.executemany(
            "INSERT INTO itemTypes VALUES (?, ?)",
            [(1, "journalArticle"), (2, "attachment"), (3, "note")],
        )
        connection.executemany(
            "INSERT INTO collections VALUES (?, ?, ?)",
            [
                (1, 1, "COLLECTA"),
                (2, 2, "COLLECTB"),
                (3, 1, "DELETEDCOL"),
                (4, 1, "AMBIGUOUS"),
                (5, 2, "AMBIGUOUS"),
            ],
        )
        connection.execute("INSERT INTO deletedCollections VALUES (3)")
        connection.executemany(
            "INSERT INTO items VALUES (?, ?, ?, ?)",
            [
                (1, 1, "PAPERONE", 1),
                (2, 2, "PAPERONE", 1),
                (3, 1, "DELETED", 1),
                (10, 1, "LINKEDPDF", 2),
                (11, 1, "STORAGEPDF", 2),
                (12, 1, "MISSINGPDF", 2),
                (13, 1, "NOTPDF", 2),
                (14, 1, "SYMLINKPDF", 2),
                (15, 1, "LINKEDURL", 2),
                (17, 1, "NOTANATTACHMENT", 3),
                (20, 2, "STORAGEPDF", 2),
            ],
        )
        connection.execute("INSERT INTO deletedItems VALUES (3)")
        connection.executemany(
            "INSERT INTO collectionItems VALUES (?, ?, ?)",
            [(1, 1, 0), (1, 3, 1), (2, 2, 0), (3, 1, 0)],
        )
        fields = ("title", "abstractNote", "DOI", "date", "url")
        connection.executemany("INSERT INTO fields VALUES (?, ?)", enumerate(fields, start=1))
        values = [
            "First paper",
            "An abstract",
            "10.1000/example",
            "2025-02-03",
            "https://example.test/first",
            "Other library paper",
        ]
        connection.executemany("INSERT INTO itemDataValues VALUES (?, ?)", enumerate(values, start=1))
        connection.executemany(
            "INSERT INTO itemData VALUES (?, ?, ?)",
            [(1, field_id, field_id) for field_id in range(1, 6)] + [(2, 1, 6)],
        )
        connection.executemany(
            "INSERT INTO creators VALUES (?, ?, ?, ?)",
            [(1, "Ada", "Lovelace", 0), (2, "", "Research Group", 1), (3, "Mallory", "Other", 0)],
        )
        connection.executemany(
            "INSERT INTO itemCreators VALUES (?, ?, ?)",
            [(1, 2, 0), (1, 1, 1), (2, 3, 0)],
        )
        connection.executemany("INSERT INTO tags VALUES (?, ?)", [(1, "zeta"), (2, "alpha"), (3, "other")])
        connection.executemany("INSERT INTO itemTags VALUES (?, ?)", [(1, 1), (1, 2), (2, 3)])
        connection.executemany(
            "INSERT INTO itemAttachments VALUES (?, ?, ?, ?, ?)",
            [
                (10, 1, "application/pdf", str(self.linked_pdf), 2),
                (11, 1, "application/pdf", "storage:stored.pdf", 0),
                (12, 1, "application/pdf", "storage:missing.pdf", 0),
                (13, 1, "application/pdf", "storage:not-pdf.pdf", 0),
                (14, 1, "application/pdf", "storage:escaped.pdf", 0),
                (15, 1, "application/pdf", "https://example.invalid/paper.pdf", 3),
                (17, 1, "application/pdf", str(self.linked_pdf), 2),
                (20, 2, "application/pdf", "storage:other.pdf", 0),
            ],
        )
        connection.commit()
        connection.close()

    def test_current_schema_deleted_tables_and_library_scope_are_exact(self) -> None:
        papers = self.source.list_records("zotero", "COLLECTA")

        self.assertEqual(len(papers), 1)
        paper = papers[0]
        self.assertEqual(paper.record_id, "PAPERONE")
        self.assertEqual(paper.title, "First paper")
        self.assertEqual(paper.authors, ("Research Group", "Ada Lovelace"))
        self.assertEqual(paper.abstract, "An abstract")
        self.assertEqual(paper.doi, "10.1000/example")
        self.assertEqual(paper.published, "2025-02-03")
        self.assertEqual(paper.url, "https://example.test/first")
        self.assertEqual(paper.tags, ("alpha", "zeta"))
        self.assertEqual(
            [(item.scope_id, item.record_id, item.title) for item in self.source.list_records("zotero", "COLLECTB")],
            [("COLLECTB", "PAPERONE", "Other library paper")],
        )
        with self.assertRaises(ValueError):
            self.source.list_records("zotero", "DELETEDCOL")
        with self.assertRaises(ValueError):
            self.source.list_records("zotero", "AMBIGUOUS")

    def test_collection_and_attachment_queries_do_not_cross_libraries(self) -> None:
        paper = self.source.list_records("zotero", "COLLECTA")[0]
        attachments = self.source.list_attachments(paper)

        self.assertEqual(
            {attachment.attachment_id for attachment in attachments},
            {"LINKEDPDF", "STORAGEPDF", "MISSINGPDF", "NOTPDF", "SYMLINKPDF"},
        )
        self.assertNotIn("other.pdf", {attachment.filename for attachment in attachments})
        with self.assertRaises(ValueError):
            self.source.list_records("other", "COLLECTA")

    def test_linked_and_real_storage_layout_pdfs_materialize_with_sha256(self) -> None:
        paper = self.source.list_records("zotero", "COLLECTA")[0]
        attachments = self.source.list_attachments(paper)

        linked = next(item for item in attachments if item.attachment_id == "LINKEDPDF")
        stored = next(item for item in attachments if item.attachment_id == "STORAGEPDF")
        linked_artifact = self.attachments.materialize(paper, linked)
        stored_artifact = self.attachments.materialize(paper, stored)

        self.assertEqual(linked_artifact.path, str(self.linked_pdf.resolve()))
        self.assertEqual(linked_artifact.fingerprint, f"sha256:{hashlib.sha256(b'%PDF-linked').hexdigest()}")
        self.assertEqual(stored_artifact.path, str(self.storage / "STORAGEPDF" / "stored.pdf"))
        self.assertEqual(stored_artifact.fingerprint, f"sha256:{hashlib.sha256(b'%PDF-stored').hexdigest()}")

    def test_storage_symlink_escape_is_rejected(self) -> None:
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (outside / "escaped.pdf").write_bytes(b"%PDF-escaped")
        os.symlink(outside, self.storage / "SYMLINKPDF")
        paper = self.source.list_records("zotero", "COLLECTA")[0]
        escaped = next(item for item in self.source.list_attachments(paper) if item.attachment_id == "SYMLINKPDF")

        with self.assertRaises(ValueError):
            self.attachments.materialize(paper, escaped)

    def test_missing_attachment_path_is_rejected(self) -> None:
        paper = self.source.list_records("zotero", "COLLECTA")[0]
        missing = next(item for item in self.source.list_attachments(paper) if item.attachment_id == "MISSINGPDF")

        with self.assertRaises(FileNotFoundError):
            self.attachments.materialize(paper, missing)

    def test_non_pdf_content_is_rejected(self) -> None:
        paper = self.source.list_records("zotero", "COLLECTA")[0]
        non_pdf = next(item for item in self.source.list_attachments(paper) if item.attachment_id == "NOTPDF")

        with self.assertRaises(ValueError):
            self.attachments.materialize(paper, non_pdf)

    def test_snapshot_is_reused_and_cleaned_up_on_close(self) -> None:
        snapshot_path = self.source._snapshot_path
        attachment_snapshot_path = self.attachments._source._snapshot_path
        self.assertIsNotNone(snapshot_path)
        self.assertIsNotNone(attachment_snapshot_path)
        self.assertTrue(snapshot_path.is_file())
        self.assertTrue(attachment_snapshot_path.is_file())

        connection = sqlite3.connect(self.database)
        connection.execute("INSERT INTO items VALUES (?, ?, ?, ?)", (99, 1, "LATE", 1))
        connection.execute("INSERT INTO collectionItems VALUES (?, ?, ?)", (1, 99, 99))
        connection.commit()
        connection.close()

        self.assertEqual([paper.record_id for paper in self.source.list_records("zotero", "COLLECTA")], ["PAPERONE"])
        self.assertEqual(snapshot_path, self.source._snapshot_path)
        self.source.close()
        self.attachments.close()
        self.assertFalse(snapshot_path.exists())
        self.assertFalse(attachment_snapshot_path.exists())


if __name__ == "__main__":
    unittest.main()
