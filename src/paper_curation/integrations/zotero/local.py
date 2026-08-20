"""Read-only adapters for a local Zotero SQLite library."""

from __future__ import annotations

from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import os
import sqlite3
import stat
import tempfile
from typing import BinaryIO, Iterator

from paper_curation.domain.papers import ArtifactRef, Attachment, Paper


_ZOTERO_SOURCE_ID = "zotero"
_PDF_MEDIA_TYPE = "application/pdf"


class ZoteroLocalSource:
    """Expose one local Zotero library through the source-neutral curation port."""

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = Path(database_path)
        self._snapshot_path: Path | None = None
        self._connection: sqlite3.Connection | None = None
        self._create_snapshot()

    def __enter__(self) -> ZoteroLocalSource:
        return self

    def __exit__(self, exc_type: object, *_: object) -> None:
        if exc_type is None:
            self.close()
        else:
            try:
                self.close()
            except Exception:
                pass

    def close(self) -> None:
        """Close and remove this adapter's read snapshot."""
        connection, self._connection = self._connection, None
        snapshot_path, self._snapshot_path = self._snapshot_path, None
        first_error: Exception | None = None
        if connection is not None:
            try:
                connection.close()
            except Exception as error:
                first_error = error
        if snapshot_path is not None:
            try:
                snapshot_path.unlink(missing_ok=True)
            except Exception as error:
                if first_error is None:
                    first_error = error
        if first_error is not None:
            raise first_error

    def list_records(self, source_id: str, scope_id: str) -> tuple[Paper, ...]:
        self._validate_source(source_id)
        with self._snapshot() as connection:
            collection_id, library_id = self._require_collection(connection, scope_id)
            rows = connection.execute(
                """
                SELECT items.key AS record_id,
                       COALESCE((
                           SELECT itemDataValues.value
                           FROM itemData
                           JOIN itemDataValues USING (valueID)
                           JOIN fields USING (fieldID)
                           WHERE itemData.itemID = items.itemID AND fields.fieldName = 'title'
                       ), '') AS title,
                       COALESCE((
                           SELECT itemDataValues.value
                           FROM itemData
                           JOIN itemDataValues USING (valueID)
                           JOIN fields USING (fieldID)
                           WHERE itemData.itemID = items.itemID AND fields.fieldName = 'abstractNote'
                       ), '') AS abstract,
                       COALESCE((
                           SELECT itemDataValues.value
                           FROM itemData
                           JOIN itemDataValues USING (valueID)
                           JOIN fields USING (fieldID)
                           WHERE itemData.itemID = items.itemID AND fields.fieldName = 'DOI'
                       ), '') AS doi,
                       COALESCE((
                           SELECT itemDataValues.value
                           FROM itemData
                           JOIN itemDataValues USING (valueID)
                           JOIN fields USING (fieldID)
                           WHERE itemData.itemID = items.itemID AND fields.fieldName = 'date'
                       ), '') AS published,
                       COALESCE((
                           SELECT itemDataValues.value
                           FROM itemData
                           JOIN itemDataValues USING (valueID)
                           JOIN fields USING (fieldID)
                           WHERE itemData.itemID = items.itemID AND fields.fieldName = 'url'
                       ), '') AS url
                FROM collectionItems
                JOIN collections ON collections.collectionID = collectionItems.collectionID
                JOIN items ON items.itemID = collectionItems.itemID
                JOIN itemTypes ON itemTypes.itemTypeID = items.itemTypeID
                LEFT JOIN deletedItems ON deletedItems.itemID = items.itemID
                WHERE collections.collectionID = ?
                  AND collections.libraryID = ?
                  AND items.libraryID = ?
                  AND itemTypes.typeName NOT IN ('attachment', 'note', 'annotation')
                  AND deletedItems.itemID IS NULL
                ORDER BY collectionItems.orderIndex, items.key
                """,
                (collection_id, library_id, library_id),
            ).fetchall()
            return tuple(
                Paper(
                    source_id=_ZOTERO_SOURCE_ID,
                    scope_id=scope_id,
                    record_id=row["record_id"],
                    title=row["title"],
                    authors=self._creators(connection, row["record_id"], library_id),
                    abstract=row["abstract"],
                    doi=row["doi"],
                    published=row["published"],
                    url=row["url"],
                    tags=self._tags(connection, row["record_id"], library_id),
                )
                for row in rows
            )

    def list_attachments(self, paper: Paper) -> tuple[Attachment, ...]:
        self._validate_paper(paper)
        with self._snapshot() as connection:
            collection_id, library_id = self._require_collection(connection, paper.scope_id)
            rows = connection.execute(
                """
                SELECT attachment.key AS attachment_id, itemAttachments.path, itemAttachments.contentType
                FROM collectionItems
                JOIN collections ON collections.collectionID = collectionItems.collectionID
                JOIN items AS parent ON parent.itemID = collectionItems.itemID
                JOIN itemAttachments ON itemAttachments.parentItemID = parent.itemID
                JOIN items AS attachment ON attachment.itemID = itemAttachments.itemID
                JOIN itemTypes AS attachment_type ON attachment_type.itemTypeID = attachment.itemTypeID
                LEFT JOIN deletedItems AS deleted_parent ON deleted_parent.itemID = parent.itemID
                LEFT JOIN deletedItems AS deleted_attachment ON deleted_attachment.itemID = attachment.itemID
                WHERE collections.collectionID = ?
                  AND collections.libraryID = ?
                  AND parent.libraryID = ?
                  AND attachment.libraryID = ?
                  AND attachment_type.typeName = 'attachment'
                  AND parent.key = ?
                  AND deleted_parent.itemID IS NULL
                  AND deleted_attachment.itemID IS NULL
                  AND lower(itemAttachments.contentType) = ?
                  AND itemAttachments.linkMode IN (0, 1, 2)
                ORDER BY attachment.key
                """,
                (collection_id, library_id, library_id, library_id, paper.record_id, _PDF_MEDIA_TYPE),
            ).fetchall()
            return tuple(
                Attachment(
                    source_id=_ZOTERO_SOURCE_ID,
                    scope_id=paper.scope_id,
                    record_id=paper.record_id,
                    attachment_id=row["attachment_id"],
                    filename=self._filename(row["path"]),
                    media_type=row["contentType"],
                )
                for row in rows
            )

    @staticmethod
    def _validate_source(source_id: str) -> None:
        if source_id != _ZOTERO_SOURCE_ID:
            raise ValueError("Zotero local source requires source_id 'zotero'")

    def _validate_paper(self, paper: Paper) -> None:
        self._validate_source(paper.source_id)

    @staticmethod
    def _require_collection(connection: sqlite3.Connection, scope_id: str) -> tuple[int, int]:
        if not scope_id:
            raise ValueError("scope_id must be an existing exact Zotero collection key")
        rows = connection.execute(
            """
            SELECT DISTINCT collections.collectionID, collections.libraryID
            FROM collections
            LEFT JOIN deletedCollections
                ON deletedCollections.collectionID = collections.collectionID
            WHERE collections.key = ? AND deletedCollections.collectionID IS NULL
            """,
            (scope_id,),
        ).fetchall()
        if len(rows) != 1 or rows[0]["libraryID"] is None:
            raise ValueError("scope_id must identify one active Zotero collection in one library")
        return rows[0]["collectionID"], rows[0]["libraryID"]

    @staticmethod
    def _filename(path: str | None) -> str:
        if not path:
            raise ValueError("Zotero PDF attachment has no path")
        if path.startswith("storage:"):
            filename = path.removeprefix("storage:")
            if not filename or Path(filename).name != filename:
                raise ValueError("Zotero storage attachment path is invalid")
            return filename
        candidate = Path(path)
        if not candidate.is_absolute() or candidate.name in ("", ".", ".."):
            raise ValueError("Zotero linked attachment path must be absolute")
        return candidate.name

    @staticmethod
    def _creators(
        connection: sqlite3.Connection, record_id: str, library_id: int
    ) -> tuple[str, ...]:
        rows = connection.execute(
            """
            SELECT creators.firstName, creators.lastName, creators.fieldMode
            FROM items
            JOIN itemCreators USING (itemID)
            JOIN creators USING (creatorID)
            WHERE items.key = ? AND items.libraryID = ?
            ORDER BY itemCreators.orderIndex
            """,
            (record_id, library_id),
        ).fetchall()
        return tuple(
            name
            for row in rows
            if (name := (
                row["lastName"].strip()
                if row["fieldMode"]
                else " ".join(part for part in (row["firstName"], row["lastName"]) if part).strip()
            ))
        )

    @staticmethod
    def _tags(connection: sqlite3.Connection, record_id: str, library_id: int) -> tuple[str, ...]:
        rows = connection.execute(
            """
            SELECT tags.name
            FROM items
            JOIN itemTags USING (itemID)
            JOIN tags USING (tagID)
            WHERE items.key = ? AND items.libraryID = ?
            ORDER BY tags.name
            """,
            (record_id, library_id),
        ).fetchall()
        return tuple(row["name"] for row in rows if row["name"])

    def _create_snapshot(self) -> None:
        if not self._database_path.is_file():
            raise FileNotFoundError(f"Zotero database does not exist: {self._database_path}")
        descriptor, temporary_path = tempfile.mkstemp(prefix="paper-curation-zotero-", suffix=".sqlite")
        snapshot_path = Path(temporary_path)
        try:
            os.close(descriptor)
        except Exception:
            try:
                snapshot_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        source: sqlite3.Connection | None = None
        snapshot: sqlite3.Connection | None = None
        try:
            source = sqlite3.connect(f"{self._database_path.resolve().as_uri()}?mode=ro", uri=True)
            snapshot = sqlite3.connect(snapshot_path)
            source.backup(snapshot)
            snapshot.row_factory = sqlite3.Row
            self._snapshot_path = snapshot_path
            self._connection = snapshot
            snapshot = None
        finally:
            if snapshot is not None:
                try:
                    snapshot.close()
                except Exception:
                    pass
            if source is not None:
                try:
                    source.close()
                except Exception:
                    pass
            if self._connection is None:
                try:
                    snapshot_path.unlink(missing_ok=True)
                except OSError:
                    pass

    @contextmanager
    def _snapshot(self) -> Iterator[sqlite3.Connection]:
        if self._connection is None:
            raise RuntimeError("Zotero local source is closed")
        yield self._connection


class ZoteroLocalAttachmentPort:
    """Materialize exact local Zotero PDF attachments without modifying the library."""

    def __init__(self, database_path: str | Path, storage_root: str | Path) -> None:
        self._source = ZoteroLocalSource(database_path)
        self._storage_root = Path(storage_root)

    def __enter__(self) -> ZoteroLocalAttachmentPort:
        return self

    def __exit__(self, exc_type: object, *_: object) -> None:
        if exc_type is None:
            self.close()
        else:
            try:
                self.close()
            except Exception:
                pass

    def close(self) -> None:
        self._source.close()

    def materialize(self, paper: Paper, attachment: Attachment) -> ArtifactRef:
        self._source._validate_paper(paper)
        if (
            attachment.source_id != paper.source_id
            or attachment.scope_id != paper.scope_id
            or attachment.record_id != paper.record_id
        ):
            raise ValueError("attachment does not belong to paper")
        with self._source._snapshot() as connection:
            collection_id, library_id = self._source._require_collection(connection, paper.scope_id)
            rows = connection.execute(
                """
                SELECT itemAttachments.path
                FROM collectionItems
                JOIN collections ON collections.collectionID = collectionItems.collectionID
                JOIN items AS parent ON parent.itemID = collectionItems.itemID
                JOIN itemAttachments ON itemAttachments.parentItemID = parent.itemID
                JOIN items AS child ON child.itemID = itemAttachments.itemID
                JOIN itemTypes AS child_type ON child_type.itemTypeID = child.itemTypeID
                LEFT JOIN deletedItems AS deleted_parent ON deleted_parent.itemID = parent.itemID
                LEFT JOIN deletedItems AS deleted_child ON deleted_child.itemID = child.itemID
                WHERE collections.collectionID = ?
                  AND collections.libraryID = ?
                  AND parent.libraryID = ?
                  AND child.libraryID = ?
                  AND child_type.typeName = 'attachment'
                  AND parent.key = ?
                  AND child.key = ?
                  AND deleted_parent.itemID IS NULL
                  AND deleted_child.itemID IS NULL
                  AND lower(itemAttachments.contentType) = ?
                  AND itemAttachments.linkMode IN (0, 1, 2)
                """,
                (
                    collection_id,
                    library_id,
                    library_id,
                    library_id,
                    paper.record_id,
                    attachment.attachment_id,
                    _PDF_MEDIA_TYPE,
                ),
            ).fetchall()
            if len(rows) != 1:
                raise ValueError("Zotero PDF attachment is missing or ambiguous")
            raw_path = rows[0]["path"]
            if attachment.filename != self._source._filename(raw_path):
                raise ValueError("attachment filename does not match Zotero metadata")
            if raw_path.startswith("storage:"):
                filename = self._source._filename(raw_path)
                with self._open_storage_attachment(attachment.attachment_id, filename) as (path, source):
                    digest = self._pdf_digest(source)
            else:
                path = self._resolve_linked_path(raw_path)
                with path.open("rb") as source:
                    digest = self._pdf_digest(source)
        return ArtifactRef(attachment.filename, str(path), f"sha256:{digest}")

    @staticmethod
    def _pdf_digest(source: BinaryIO) -> str:
        header = source.read(5)
        if header != b"%PDF-":
            raise ValueError("Zotero attachment is not a PDF")
        digest = sha256(header)
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _resolve_linked_path(raw_path: str | None) -> Path:
        if not raw_path:
            raise ValueError("Zotero PDF attachment has no path")
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            raise ValueError("Zotero linked attachment path must be absolute")
        candidate = candidate.resolve(strict=True)
        if not candidate.is_file():
            raise FileNotFoundError(f"Zotero attachment is not a file: {candidate}")
        return candidate

    @contextmanager
    def _open_storage_attachment(self, attachment_id: str, filename: str) -> Iterator[tuple[Path, BinaryIO]]:
        if Path(attachment_id).name != attachment_id or attachment_id in ("", ".", ".."):
            raise ValueError("Zotero attachment key is invalid")
        root = self._storage_root.absolute()
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        root_descriptor: int | None = None
        attachment_descriptor: int | None = None
        file_descriptor: int | None = None
        source: BinaryIO | None = None
        try:
            root_descriptor = os.open(root, flags)
            attachment_descriptor = os.open(attachment_id, flags, dir_fd=root_descriptor)
            file_descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=attachment_descriptor)
            if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
                raise ValueError("Zotero storage attachment is not a regular file")
            source = os.fdopen(file_descriptor, "rb")
            file_descriptor = None
            yield root / attachment_id / filename, source
        except FileNotFoundError:
            raise
        except OSError as error:
            raise ValueError("Zotero storage attachment path is unsafe") from error
        finally:
            if source is not None:
                try:
                    source.close()
                except Exception:
                    pass
            elif file_descriptor is not None:
                try:
                    os.close(file_descriptor)
                except OSError:
                    pass
            if attachment_descriptor is not None:
                try:
                    os.close(attachment_descriptor)
                except OSError:
                    pass
            if root_descriptor is not None:
                try:
                    os.close(root_descriptor)
                except OSError:
                    pass
