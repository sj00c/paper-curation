"""Network-free compatibility contract for a configured synthetic corpus."""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).with_name("fixtures") / "generic_corpus"
sys.path.insert(0, str(PIPELINE))

import build_bibliography_db as bibliography  # noqa: E402
import build_papers_index as papers_index  # noqa: E402
import build_topic_index as topic_index  # noqa: E402
import config_loader as config  # noqa: E402
import review_to_html as review_html  # noqa: E402


TOPIC = "amber-field"
SLUG = "101_synthetic_record"
CATEGORY = "Synthetic Class"


class GenericCorpusContractTests(unittest.TestCase):
    def test_synthetic_configured_collection_renders_corpus_without_network(self):
        """The local corpus contract must not depend on a built-in collection."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            papers = docs / "papers"
            paper = papers / SLUG
            topic = docs / TOPIC
            paper.mkdir(parents=True)
            topic.mkdir()
            for name in ("review.md", "text.md", "bibliography.json"):
                shutil.copy2(FIXTURE / name, paper / name)
            shutil.copy2(FIXTURE / "config.json", root / "config.json")

            classification = {
                "primary_category": CATEGORY,
                "all_categories": [CATEGORY],
                "sub_category": "Synthetic Detail",
            }
            # The existing entry is the durable source of topic membership and
            # classification when the metadata index is regenerated.
            (papers / "_papers_index.json").write_text(json.dumps([{
                "slug": SLUG,
                "topics": [TOPIC],
                "primary_topic": TOPIC,
                "classifications": {TOPIC: classification},
            }]), encoding="utf-8")
            (topic / "_new_classification.json").write_text(json.dumps({
                "categories": [{"name": CATEGORY}],
                "assignments": [{
                    "slug": SLUG,
                    "primary_category": CATEGORY,
                    "all_categories": [CATEGORY],
                    "sub_category": "Synthetic Detail",
                }],
            }), encoding="utf-8")

            old_config = config.CONFIG_PATH, config.DOCS_DIR, config.PAPERS_DIR, config._config_cache
            old_index_dir = papers_index.PAPERS_DIR
            old_topic_dir, old_topic_docs = topic_index.PAPERS_DIR, topic_index.DOCS_DIR
            old_html_papers = review_html.PAPERS
            old_html_index, old_deploy_topics = review_html._PIDX, review_html._DEPLOY_TOPICS
            try:
                config.CONFIG_PATH = root / "config.json"
                config.DOCS_DIR = docs
                config.PAPERS_DIR = papers
                config._config_cache = None
                papers_index.PAPERS_DIR = str(papers)
                topic_index.PAPERS_DIR = str(papers)
                topic_index.DOCS_DIR = docs
                review_html.PAPERS = str(papers)
                review_html._PIDX = None
                review_html._DEPLOY_TOPICS = None

                with patch.dict(os.environ, {
                    "PAPER_CURATION_REFRESH_ZOTERO_CACHE": "",
                    "SKIP_ZOTERO_KEYS": "1",
                }), patch("urllib.request.urlopen", side_effect=AssertionError("network call")) as urlopen:
                    self.assertEqual(config.get_topic_names(), [TOPIC])
                    self.assertEqual(config.resolve_topic(script="synthetic"), TOPIC)
                    generated = papers_index._run_build_index(topic=TOPIC)
                    self.assertEqual(review_html._run_review_to_html(topic=TOPIC, slug=SLUG), {
                        "converted": 1, "skipped": 0,
                    })
                    topic_index._run_topic_index(topic=TOPIC)
                    self.assertEqual(urlopen.call_count, 0)

                self.assertEqual(len(generated), 1)
                entry = generated[0]
                self.assertTrue({
                    "slug", "title", "authors", "date", "doi", "topics",
                    "primary_topic", "classifications", "has_pdf", "has_figures",
                    "text_md_sha256", "doi_verified",
                } <= entry.keys())
                self.assertEqual(entry["slug"], SLUG)
                self.assertEqual(entry["topics"], [TOPIC])
                self.assertEqual(entry["primary_topic"], TOPIC)
                self.assertEqual(entry["classifications"], {TOPIC: classification})
                self.assertTrue(entry["has_pdf"])
                self.assertEqual(bibliography.load_sidecar(paper)["zotero"]["key"], "SYNTH001")

                paper_html = (paper / "index.html").read_text(encoding="utf-8")
                topic_html = (topic / "index.html").read_text(encoding="utf-8")
                self.assertIn("Synthetic Signal Study", paper_html)
                self.assertIn(f"../../{TOPIC}/index.html", paper_html)
                self.assertIn(f"../papers/{SLUG}/index.html", topic_html)
                self.assertIn("'../papers/' + slug + '/text.md'", topic_html)
                self.assertIn(CATEGORY, topic_html)
            finally:
                config.CONFIG_PATH, config.DOCS_DIR, config.PAPERS_DIR, config._config_cache = old_config
                papers_index.PAPERS_DIR = old_index_dir
                topic_index.PAPERS_DIR, topic_index.DOCS_DIR = old_topic_dir, old_topic_docs
                review_html.PAPERS = old_html_papers
                review_html._PIDX, review_html._DEPLOY_TOPICS = old_html_index, old_deploy_topics


if __name__ == "__main__":
    unittest.main()
