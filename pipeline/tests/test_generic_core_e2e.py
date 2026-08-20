"""End-to-end proof for the generic local Core product path."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sqlite3
from urllib.request import urlopen

import fitz

from paper_curation.cli import main
from paper_curation.composition import CompositionDependencies
from paper_curation.domain.papers import ArtifactRef
from paper_curation.integrations.server import LocalStaticServer
from paper_curation.application.serve import ServeSite, ServeSiteRequest


_REVIEW = """# Review
## Summary
A source-grounded summary of the selected paper.
## Contributions
The paper contributes a synthetic method.
## Methods
The extracted text describes the method.
## Evidence and Findings
The extracted text reports quantum evidence.
## Limitations
The synthetic fixture states a limited scope.
## Source Grounding
The statements above are grounded in the extracted PDF text.
"""


class _ReviewProvider:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def write(self, paper, text) -> ArtifactRef:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / f"{paper.record_id}.md"
        path.write_text(_REVIEW, encoding="utf-8")
        return ArtifactRef("review.md", str(path), sha256(path.read_bytes()).hexdigest())


def _library(database: Path, pdf: Path) -> None:
    connection = sqlite3.connect(database)
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
        [(1, "journalArticle"), (2, "attachment")],
    )
    connection.execute("INSERT INTO collections VALUES (1, 1, 'SCOPE')")
    connection.executemany(
        "INSERT INTO items VALUES (?, 1, ?, ?)",
        [(1, "PAPER", 1), (2, "PDF", 2)],
    )
    connection.execute("INSERT INTO collectionItems VALUES (1, 1, 0)")
    connection.executemany(
        "INSERT INTO fields VALUES (?, ?)", [(1, "title"), (2, "abstractNote"), (3, "DOI")]
    )
    connection.executemany(
        "INSERT INTO itemDataValues VALUES (?, ?)",
        [(1, "Synthetic paper"), (2, "A domain-neutral fixture"), (3, "10.1000/synthetic")],
    )
    connection.executemany(
        "INSERT INTO itemData VALUES (1, ?, ?)", [(1, 1), (2, 2), (3, 3)]
    )
    connection.execute("INSERT INTO creators VALUES (1, 'Ada', 'Example', 0)")
    connection.execute("INSERT INTO itemCreators VALUES (1, 1, 0)")
    connection.execute(
        "INSERT INTO itemAttachments VALUES (2, 1, 'application/pdf', ?, 2)",
        (str(pdf),),
    )
    connection.commit()
    connection.close()


def test_generic_local_core_update_build_query_and_serve(tmp_path: Path, capsys) -> None:
    pdf = tmp_path / "paper.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Synthetic method reports quantum evidence with a deliberately limited scope.",
    )
    document.save(pdf)
    document.close()

    database = tmp_path / "zotero.sqlite"
    _library(database, pdf)
    workspace = tmp_path / "workspace"
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "workspace": {"root": str(workspace)},
                "source": {
                    "provider": "zotero",
                    "transport": "local-sqlite",
                    "sqlite_path": str(database),
                    "collections": {"synthetic-topic": "SCOPE"},
                },
                "core": {
                    "review": {
                        "provider": "local-model",
                        "model": "configured-model",
                        "local_endpoint": "http://127.0.0.1:11434",
                    }
                },
                "features": {},
                "publication": {"mode": "local", "base_url": ""},
            }
        ),
        encoding="utf-8",
    )
    dependencies = CompositionDependencies(
        local_review=lambda output_dir, endpoint, model, api_key="": _ReviewProvider(output_dir)
    )

    assert main(
        ["update", "--config", str(config), "--topic", "synthetic-topic"],
        composition_dependencies=dependencies,
        environment={},
    ) == 0
    update_output = capsys.readouterr().out
    assert "record=PAPER result=succeeded" in update_output
    assert "secret" not in update_output.casefold()

    assert main(["validate", "--config", str(config)]) == 0
    assert main(["build", "--config", str(config)]) == 0
    assert main(
        [
            "query",
            "--config",
            str(config),
            "--topic",
            "synthetic-topic",
            "--query",
            "quantum evidence",
        ]
    ) == 0
    assert "record=PAPER" in capsys.readouterr().out

    site = workspace / "site"
    handle = LocalStaticServer().start(
        ServeSite().plan(ServeSiteRequest(site, port=0))
    )
    try:
        index = urlopen(f"{handle.url}/", timeout=5).read().decode("utf-8")
        href = re.search(r'href="([^"]+)"', index)
        assert href is not None
        paper_page = urlopen(f"{handle.url}/{href.group(1)}", timeout=5).read().decode("utf-8")
        assert "Synthetic paper" in paper_page
        assert "source-grounded summary" in paper_page
    finally:
        handle.stop()
