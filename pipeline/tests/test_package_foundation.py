"""Contracts for the side-effect-free installable package foundation."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.capabilities import detect_capabilities
from paper_curation.config.loader import load_config
from paper_curation.config.models import AppConfig
from paper_curation.errors import ConfigError, ConfigValidationError
from paper_curation.workspace import Workspace


def config_for(alias: str = "any-topic") -> dict[str, object]:
    return {
        "zotero": {"collections": {alias: "Collection"}},
        "search_keywords": {alias: {"primary": ["research"], "secondary": []}},
        "topic_profiles": {alias: {"title": "Research"}},
        "publication": {"mode": "local", "base_url": ""},
    }


class PackageFoundationTests(unittest.TestCase):
    def test_arbitrary_configured_topic_is_valid(self) -> None:
        config = AppConfig.from_mapping(config_for("my-new-topic"))
        self.assertEqual(config.zotero.collections["my-new-topic"], "Collection")
        self.assertEqual(config.search_keywords["my-new-topic"].primary, ("research",))

    def test_malformed_config_fails_without_echoing_values(self) -> None:
        config = config_for()
        config["search_keywords"] = {"any-topic": {"primary": "secret-value", "secondary": []}}
        with self.assertRaises(ConfigError) as raised:
            AppConfig.from_mapping(config)
        self.assertNotIn("secret-value", str(raised.exception))

    def test_public_publication_requires_url(self) -> None:
        config = config_for()
        config["publication"] = {"mode": "public", "base_url": ""}
        with self.assertRaises(ConfigValidationError):
            AppConfig.from_mapping(config)

    def test_existing_local_build_config_can_omit_web_search_and_profile(self) -> None:
        config = config_for()
        config.pop("search_keywords")
        config.pop("topic_profiles")
        parsed = AppConfig.from_mapping(config)
        self.assertEqual(parsed.search_keywords, {})
        self.assertEqual(parsed.topic_profiles, {})

    def test_capabilities_are_pure_facts(self) -> None:
        config = AppConfig.from_mapping(config_for())
        enabled = detect_capabilities(
            config,
            {
                "CLAUDE_CODE_OAUTH_TOKEN": "token",
                "ZOTERO_API_KEY": "token",
                "GOOGLE_API_KEY": "token",
                "OPENAI_API_KEY": "token",
                "PAPERBANANA_DIR": "/paperbanana",
            },
            path_exists=lambda path: False,
            path_is_dir=lambda path: path == Path("/paperbanana"),
        )
        self.assertEqual(
            enabled,
            type(enabled)(True, True, True, True, True, True, False),
        )

    def test_workspace_paths_cannot_escape_checkout(self) -> None:
        workspace = Workspace(ROOT)
        self.assertEqual(workspace.papers, ROOT / "docs" / "papers")
        with self.assertRaises(ValueError):
            workspace.topic("../outside")
        with self.assertRaises(ValueError):
            workspace.within_root("docs", "..", "outside")

    def test_current_config_example_is_compatible(self) -> None:
        config = load_config(ROOT / "config.example.json")
        self.assertIn("my_topic", config.topic_profiles)


if __name__ == "__main__":
    unittest.main()
