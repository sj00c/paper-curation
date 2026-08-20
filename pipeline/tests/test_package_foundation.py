"""Contracts for the side-effect-free installable package foundation."""

from __future__ import annotations

import inspect
import json
import subprocess
import tempfile
import unittest
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.capabilities import detect_capabilities
from paper_curation.composition import CompositionDependencies, _selected_review_provider
from paper_curation.config.models import AppConfig
from paper_curation.domain.papers import ArtifactRef, Paper
from paper_curation.errors import ConfigError, ConfigValidationError
from paper_curation.integrations.providers.review import (
    AnthropicAPIReviewAdapter,
    ClaudeCodeOAuthReviewAdapter,
    LocalModelReviewAdapter,
)
from paper_curation.integrations.persistence.configuration import _encode_config
from paper_curation.workspace import Workspace


def config_for(alias: str = "any-topic") -> dict[str, object]:
    return {
        "workspace": {"root": "/workspace"},
        "source": {
            "provider": "zotero",
            "transport": "local-sqlite",
            "sqlite_path": "/workspace/zotero.sqlite",
            "collections": {alias: "Collection"},
        },
        "core": {"review": {"provider": "claude-code-oauth", "model": "configured-review-model"}},
        "features": {
            "dense_search": {"enabled": False},
            "figure_validation": {"enabled": False},
        },
        "search_keywords": {alias: {"primary": ["research"], "secondary": []}},
        "topic_profiles": {alias: {"title": "Research"}},
        "publication": {"mode": "local", "base_url": ""},
    }


class PackageFoundationTests(unittest.TestCase):
    def test_review_model_is_required_and_secret_safe(self) -> None:
        config = config_for()
        del config["core"]["review"]["model"]
        with self.assertRaisesRegex(ConfigError, "core.review.model"):
            AppConfig.from_mapping(config)

        config = config_for()
        config["core"]["review"]["model"] = "   "
        config["credentials"] = {"anthropic_api_key": "super-secret"}
        with self.assertRaises(ConfigValidationError) as raised:
            AppConfig.from_mapping(config)
        self.assertIn("core.review.model", str(raised.exception))
        self.assertNotIn("super-secret", str(raised.exception))

    def test_review_model_round_trips_exactly(self) -> None:
        config = config_for()
        config["core"]["review"]["model"] = "  installation-selected-model  "
        parsed = AppConfig.from_mapping(config)
        self.assertEqual(parsed.core.review.model, "installation-selected-model")
        encoded = json.loads(_encode_config(parsed))
        self.assertEqual(encoded["core"]["review"]["model"], "installation-selected-model")
        self.assertEqual(AppConfig.from_mapping(encoded).core.review, parsed.core.review)

    def test_review_adapters_require_a_model_constructor_argument(self) -> None:
        for adapter in (
            ClaudeCodeOAuthReviewAdapter,
            AnthropicAPIReviewAdapter,
            LocalModelReviewAdapter,
        ):
            self.assertIs(inspect.signature(adapter).parameters["model"].default, inspect.Parameter.empty)

    def test_claude_code_receives_the_exact_configured_model(self) -> None:
        review = """# Review
## Summary
Summary.
## Contributions
Contributions.
## Methods
Methods.
## Evidence and Findings
Evidence.
## Limitations
Limitations.
## Source Grounding
Grounding.
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "paper.txt"
            source.write_text("source text", encoding="utf-8")
            text = ArtifactRef("text.txt", str(source), sha256(source.read_bytes()).hexdigest())
            paper = Paper("zotero", "topic", "item", "Paper", (), None, None)
            calls: list[tuple[str, ...]] = []

            def runner(command: tuple[str, ...], **_: object) -> subprocess.CompletedProcess[str]:
                calls.append(command)
                return subprocess.CompletedProcess(command, 0, review)

            ClaudeCodeOAuthReviewAdapter(root / "reviews", "model/from-installation", runner).write(
                paper, text
            )
        model_index = calls[0].index("--model")
        self.assertEqual(calls[0][model_index + 1], "model/from-installation")

    def test_composition_wires_only_the_configured_model_for_each_provider(self) -> None:
        calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

        def adapter(name: str):
            def construct(*args: object, **kwargs: object) -> object:
                calls.append((name, args, kwargs))
                return object()

            return construct

        dependencies = CompositionDependencies(
            claude_review=adapter("claude"),
            anthropic_review=adapter("anthropic"),
            local_review=adapter("local"),
            anthropic_client=lambda _: object(),
        )
        for provider, endpoint in (
            ("claude-code-oauth", ""),
            ("anthropic-api", ""),
            ("local-model", "http://127.0.0.1:8080"),
        ):
            config = config_for()
            config["core"]["review"] = {
                "provider": provider,
                "model": "provider-independent-model",
                "local_endpoint": endpoint,
            }
            _selected_review_provider(
                AppConfig.from_mapping(config),
                Path("/workspace"),
                {"ANTHROPIC_API_KEY": "credential-does-not-select-model"},
                dependencies,
            )

        self.assertEqual([name for name, _, _ in calls], ["claude", "anthropic", "local"])
        self.assertEqual(
            [kwargs["model"] for _, _, kwargs in calls],
            ["provider-independent-model"] * 3,
        )
        self.assertEqual(calls[-1][2]["api_key"], "")

    def test_local_model_endpoint_must_be_loopback(self) -> None:
        config = config_for()
        config["core"]["review"] = {
            "provider": "local-model",
            "model": "configured-model",
            "local_endpoint": "https://models.example.invalid/v1",
        }
        with self.assertRaisesRegex(ConfigValidationError, "loopback"):
            AppConfig.from_mapping(config)
        for suffix in ("?api_key=secret", "#credential", ";token=secret"):
            config["core"]["review"]["local_endpoint"] = (
                "http://127.0.0.1:8080/v1" + suffix
            )
            with self.assertRaisesRegex(ConfigValidationError, "loopback"):
                AppConfig.from_mapping(config)

    def test_arbitrary_configured_topic_is_valid(self) -> None:
        config = AppConfig.from_mapping(config_for("my-new-topic"))
        self.assertEqual(config.source.collections["my-new-topic"], "Collection")
        self.assertEqual(config.search_keywords["my-new-topic"].primary, ("research",))

    def test_two_domain_neutral_topic_configurations_need_no_code_change(self) -> None:
        climate = AppConfig.from_mapping(config_for("climate-methods"))
        linguistics = AppConfig.from_mapping(config_for("historical-linguistics"))
        self.assertEqual(climate.source.collections["climate-methods"], "Collection")
        self.assertEqual(linguistics.source.collections["historical-linguistics"], "Collection")

    def test_malformed_config_fails_without_echoing_values(self) -> None:
        config = config_for()
        config["search_keywords"] = {"any-topic": {"primary": "secret-value", "secondary": []}}
        with self.assertRaises(ConfigError) as raised:
            AppConfig.from_mapping(config)
        self.assertNotIn("secret-value", str(raised.exception))

    def test_public_publication_requires_url(self) -> None:
        config = config_for()
        config["publication"] = {
            "mode": "public",
            "provider": "cloudflare",
            "base_url": "",
            "config_path": "wrangler.toml",
        }
        with self.assertRaises(ConfigValidationError):
            AppConfig.from_mapping(config)

    def test_local_publication_defaults_have_no_deployment_target(self) -> None:
        config = config_for()
        config["publication"] = {"mode": "local", "base_url": ""}
        parsed = AppConfig.from_mapping(config)
        publication = parsed.publication
        self.assertEqual((publication.mode, publication.provider, publication.config_path), ("local", "", ""))
        self.assertEqual(
            json.loads(_encode_config(parsed))["publication"],
            {"mode": "local", "base_url": ""},
        )

    def test_public_publication_requires_provider_and_config_path(self) -> None:
        config = config_for()
        config["publication"] = {"mode": "public", "base_url": "https://papers.example.test"}
        with self.assertRaisesRegex(ConfigValidationError, "publication.provider"):
            AppConfig.from_mapping(config)
        config["publication"] = {
            "mode": "public",
            "provider": "cloudflare",
            "base_url": "https://papers.example.test",
        }
        with self.assertRaisesRegex(ConfigValidationError, "publication.config_path"):
            AppConfig.from_mapping(config)

    def test_public_publication_rejects_unsupported_provider_and_escaping_config(self) -> None:
        config = config_for()
        config["publication"] = {
            "mode": "public",
            "provider": "other",
            "base_url": "https://papers.example.test",
            "config_path": "wrangler.toml",
        }
        with self.assertRaisesRegex(ConfigValidationError, "publication.provider"):
            AppConfig.from_mapping(config)
        config["publication"]["provider"] = "cloudflare"
        for path in ("/tmp/wrangler.toml", r"C:\tmp\wrangler.toml", r"C:wrangler.toml", "../wrangler.toml"):
            config["publication"]["config_path"] = path
            with self.assertRaisesRegex(ConfigValidationError, "publication.config_path"):
                AppConfig.from_mapping(config)

    def test_publication_is_strict_and_serializes_selected_deployment(self) -> None:
        config = config_for()
        config["publication"] = {
            "mode": "public",
            "provider": "cloudflare",
            "base_url": "https://papers.example.test",
            "config_path": "deploy/wrangler.toml",
        }
        parsed = AppConfig.from_mapping(config)
        encoded = json.loads(_encode_config(parsed))
        self.assertEqual(encoded["publication"], config["publication"])
        self.assertEqual(AppConfig.from_mapping(encoded).publication, parsed.publication)
        encoded["publication"]["account_id"] = "not-allowed"
        with self.assertRaisesRegex(ConfigValidationError, "publication"):
            AppConfig.from_mapping(encoded)

    def test_cloudflare_url_or_credential_never_selects_a_provider(self) -> None:
        config = config_for()
        config["credentials"] = {"zotero_api_key": "token"}
        config["publication"] = {
            "mode": "public",
            "base_url": "https://site.pages.dev",
            "config_path": "wrangler.toml",
        }
        with self.assertRaisesRegex(ConfigValidationError, "publication.provider"):
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
                "GOOGLE_API_KEY": "token",
                "OPENAI_API_KEY": "token",
            },
            path_exists=lambda path: path == Path("/workspace/zotero.sqlite"),
            path_is_dir=lambda path: False,
        )
        self.assertEqual(
            enabled,
            type(enabled)(True, True, {"dense_search": False, "figure_validation": False}, False),
        )

    def test_unselected_credentials_enable_nothing(self) -> None:
        config = AppConfig.from_mapping(config_for())
        capabilities = detect_capabilities(
            config,
            {
                "CLAUDE_CODE_OAUTH_TOKEN": "token",
                "ZOTERO_API_KEY": "token",
                "GOOGLE_API_KEY": "token",
                "OPENAI_API_KEY": "token",
            },
            path_exists=lambda path: path == Path("/workspace/zotero.sqlite"),
            path_is_dir=lambda path: False,
        )
        self.assertEqual(dict(capabilities.features), {"dense_search": False, "figure_validation": False})

    def test_local_sqlite_does_not_require_zotero_api_key(self) -> None:
        config = AppConfig.from_mapping(config_for())
        capabilities = detect_capabilities(
            config,
            {"CLAUDE_CODE_OAUTH_TOKEN": "token"},
            path_exists=lambda path: path == Path("/workspace/zotero.sqlite"),
            path_is_dir=lambda path: False,
        )
        self.assertTrue(capabilities.source_ready)

    def test_selected_provider_without_credential_fails_clearly(self) -> None:
        config = config_for()
        config["core"] = {"review": {"provider": "anthropic-api", "model": "configured-review-model"}}
        with self.assertRaisesRegex(ConfigValidationError, "core.review.provider"):
            detect_capabilities(
                AppConfig.from_mapping(config),
                {},
                path_exists=lambda path: path == Path("/workspace/zotero.sqlite"),
                path_is_dir=lambda path: False,
            )

    def test_workspace_paths_cannot_escape_checkout(self) -> None:
        workspace = Workspace(ROOT)
        self.assertEqual(workspace.papers, ROOT / "papers")
        self.assertEqual(workspace.cache, ROOT / ".cache")
        self.assertEqual(workspace.site, ROOT / "site")
        with self.assertRaises(ValueError):
            workspace.within_root("docs", "..", "outside")

    def test_disabled_feature_cannot_select_provider(self) -> None:
        config = config_for()
        config["features"] = {"dense_search": {"enabled": False, "provider": "google"}}
        with self.assertRaisesRegex(ConfigValidationError, "features.dense_search.provider"):
            AppConfig.from_mapping(config)


if __name__ == "__main__":
    unittest.main()
