"""Connections live in the DB; the per-topic JSON is output, not the source.

They were stored as `docs/{topic}/_paper_connections.json`, one copy per topic
the two papers shared: 149,496 stored connections for 51,932 distinct claims,
79 pairs pointing at papers deleted long ago, and no way to ask "what connects
to X" without loading all nine files.

They are LLM claims, so these tests also pin the separation the registry
teardown taught: derived data must name its model and must never be gated as if
its content had been verified.
"""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

import build_bibliography_db as bib


class AuthorInstitutionTests(unittest.TestCase):
    """An author cannot sit where the paper is not linked."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "b.sqlite3"
        conn = sqlite3.connect(self.db)
        conn.executescript(bib.SCHEMA)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("INSERT INTO papers (paper_id,slug,title,review_dir)"
                     " VALUES (1,'a','A','docs/papers/a')")
        conn.execute("INSERT INTO authors (author_id,display_name,normalized_name)"
                     " VALUES (1,'Jun Lü','jun lu')")
        conn.execute("INSERT INTO institutions (institution_id,institution_name,"
                     "normalized_name,source) VALUES (1,'Nantong University','nantong university','pdf')")
        conn.commit()
        self.conn = conn
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(conn.close)

    def test_marker_and_order_are_recorded(self):
        self.conn.execute(
            "INSERT INTO paper_institutions (paper_id,institution_id,raw_name,source)"
            " VALUES (1,1,'1Dept, Nantong University','pdf')")
        self.conn.execute(
            "INSERT INTO paper_author_institutions (paper_id,author_id,"
            "institution_id,marker,author_order,source) VALUES (1,1,1,'3',3,'pdf.byline-marker')")
        self.conn.commit()
        row = self.conn.execute(
            "SELECT marker, author_order FROM paper_author_institutions").fetchone()
        self.assertEqual(row, ("3", 3))

    def test_a_link_without_a_paper_level_row_is_detectable(self):
        self.conn.execute(
            "INSERT INTO paper_author_institutions (paper_id,author_id,"
            "institution_id,marker,author_order,source) VALUES (1,1,1,'1',1,'x')")
        self.conn.commit()
        self.assertEqual(self.conn.execute(
            "SELECT COUNT(*) FROM paper_author_institutions pai WHERE NOT EXISTS("
            " SELECT 1 FROM paper_institutions pi WHERE pi.paper_id=pai.paper_id"
            " AND pi.institution_id=pai.institution_id)").fetchone()[0], 1)


class ByLineParserTests(unittest.TestCase):
    BYLINE = ("### Xi-Chen Wang1,2†, Di Zhu1,3†, Jun Lu1,3, Guan-Lan Guo1, "
              "Fan Fu1 and Wei-Guan Chen1,3*\n"
              "1Department of Rehabilitation Medicine, Nantong First People's "
              "Hospital, Nantong, China, 2Affiliated Teaching Hospital of Kangda "
              "College, Nanjing Medical University, Nanjing, China, 3Affiliated "
              "Nantong Clinical College of Nantong University, Nantong, China\n")

    def test_each_author_keeps_their_own_markers(self):
        got = bib.author_affiliation_markers(
            self.BYLINE, ["Xi-Chen Wang", "Di Zhu", "Guan-Lan Guo", "Fan Fu"])
        self.assertEqual(got["Xi-Chen Wang"], ["1", "2"])
        self.assertEqual(got["Di Zhu"], ["1", "3"])
        self.assertEqual(got["Guan-Lan Guo"], ["1"])

    def test_diacritics_do_not_lose_an_author(self):
        """Zotero has 'Jun Lü'; the PDF byline prints 'Jun Lu1,3'."""
        got = bib.author_affiliation_markers(self.BYLINE, ["Jun Lü"])
        self.assertEqual(got.get("Jun Lü"), ["1", "3"])

    def test_markers_resolve_to_affiliation_text(self):
        got = bib.marker_affiliations(self.BYLINE)
        self.assertIn("Nantong First People's Hospital", got["1"])
        self.assertIn("Nanjing Medical University", got["2"])
        self.assertIn("Nantong University", got["3"])


if __name__ == "__main__":
    unittest.main()
