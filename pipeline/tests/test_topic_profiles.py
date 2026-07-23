"""Focused tests for topic-profile and keyword config contracts."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402
import setup as setup_cli  # noqa: E402


class TopicProfileTests(unittest.TestCase):
    def _with_config(self, payload):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        config_path = root / "config.json"
        config_path.write_text(payload, encoding="utf-8")
        patcher = patch.object(config_loader, "CONFIG_PATH", config_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(temp_dir.cleanup)
        config_loader._config_cache = None
        self.addCleanup(setattr, config_loader, "_config_cache", None)
        return config_path

    def test_legacy_search_keywords_take_precedence_and_dedupe(self):
        self._with_config(
            '{"search_keywords":{"robotics":{"primary":["Robot Learning", " robot learning "],'
            '"secondary":["Embodied AI", "embodied ai"]}},'
            '"topic_profiles":{"robotics":{"search_keywords":{"primary":["ignored"],"secondary":["ignored"]}}}}'
        )
        self.assertEqual(
            config_loader.get_search_keywords("robotics"),
            {"primary": ["Robot Learning"], "secondary": ["Embodied AI"]},
        )

    def test_arbitrary_topic_falls_back_without_example_domain_injection(self):
        self._with_config("{}")
        keywords = config_loader.get_search_keywords("quantum-bio")
        self.assertEqual(keywords["primary"], ["quantum bio"])
        self.assertEqual(keywords["secondary"], ["quantum-bio", "quantum", "bio"])
        joined = " ".join(keywords["primary"] + keywords["secondary"]).casefold()
        self.assertNotIn("ai4s", joined)
        self.assertNotIn("scisci", joined)

    def test_topic_index_requires_explicit_topic_and_generic_unknown_theme(self):
        source = (PIPELINE / "build_topic_index.py").read_text(encoding="utf-8")
        self.assertNotIn('return "ai4s"', source)
        self.assertIn('raise SystemExit("Usage: PYTHONUTF8=1 python build_topic_index.py <topic>")', source)
        self.assertIn("topic_profile = get_topic_profile(TOPIC)", source)
        self.assertIn('"title": topic_label', source)
        self.assertNotIn("THEME = {", source)

    def test_topic_index_author_fallback_copy_is_domain_neutral(self):
        source = (PIPELINE / "build_topic_index.py").read_text(encoding="utf-8")
        self.assertIn("해당 저자가 포함된 다른 토픽에서 다시 시도해보세요", source)
        self.assertNotIn("다른 토픽(예: scisci)", source)

    def test_cjk_keywords_are_preserved_and_normalized(self):
        self._with_config(
            '{"topic_profiles":{"한국어-논문":{"label":"한국어  논문",'
            '"aliases":["한국어-논문"],"search_keywords":{"primary":["  생성형   과학  "],'
            '"secondary":["문헌  큐레이션"]}}}}'
        )
        keywords = config_loader.get_search_keywords("한국어-논문")
        self.assertIn("생성형 과학", keywords["primary"])
        self.assertIn("한국어 논문", keywords["primary"])
        self.assertIn("문헌 큐레이션", keywords["secondary"])

    def test_malformed_and_empty_profiles_report_paths_without_values(self):
        self._with_config('{"topic_profiles":{"broken":{"label":"Broken","search_keywords":{"primary":"SECRET_SENTINEL","secondary":[]}}}}')
        with self.assertRaisesRegex(ValueError, r"topic_profiles\.broken") as raised:
            config_loader.get_search_keywords("broken")
        self.assertNotIn("SECRET_SENTINEL", str(raised.exception))

        self._with_config('{"topic_profiles":{"broken":["not-object"]}}')
        with self.assertRaisesRegex(ValueError, r"topic_profiles\.broken"):
            config_loader.get_topic_profile("broken")

        for payload in (
            '{"topic_profiles":{"empty":{}}}',
            '{"topic_profiles":{"empty":{"label":""}}}',
        ):
            self._with_config(payload)
            with self.assertRaisesRegex(ValueError, r"topic_profiles\.empty\.label"):
                config_loader.get_search_keywords("empty")

    def test_one_and_multiple_collection_profiles_fill_keywords(self):
        one = setup_cli._topic_profiles({"robotics": "Robotics Papers"})
        self.assertEqual(one["robotics"]["search_keywords"]["primary"], ["Robotics Papers"])

        self._with_config(
            '{"zotero":{"collections":{"robotics":"Robotics Papers",'
            '"life-sciences":"Life Sciences"}}}'
        )
        self.assertEqual(config_loader.get_search_keywords("robotics")["primary"], ["Robotics Papers"])
        self.assertEqual(config_loader.get_search_keywords("life-sciences")["primary"], ["Life Sciences"])

    def test_zotero_collection_fallback_applies_only_without_explicit_profile(self):
        self._with_config(
            '{"zotero":{"collections":{"robotics":"Robotics Papers","fallback":"Fallback Papers"}},'
            '"topic_profiles":{"robotics":{"label":"Robotics Canonical"}}}'
        )
        self.assertEqual(config_loader.get_search_keywords("fallback")["primary"], ["Fallback Papers"])
        with patch.object(config_loader, "_resolve_collection_value", side_effect=lambda value: value):
            self.assertEqual(config_loader.get_collection_key("robotics"), "")

    def test_canonical_profiles_are_read_and_alias_only_profiles_are_rejected(self):
        self._with_config(
            '{"topic_profiles":{"robotics":{"label":"Robotics Papers",'
            '"collection_name":"Robotics Papers","collection_key":"ABCD1234",'
            '"aliases":["robotics"],"search_keywords":{"primary":["Robot Learning"],'
            '"secondary":["Embodied AI"]}}}}'
        )
        profile = config_loader.get_topic_profile("robotics")
        self.assertEqual(profile["label"], "Robotics Papers")
        self.assertEqual(profile["collection_name"], "Robotics Papers")
        self.assertEqual(profile["collection_key"], "ABCD1234")
        self.assertEqual(config_loader.get_collection_key("robotics"), "ABCD1234")
        self.assertIn("Robot Learning", config_loader.get_search_keywords("robotics")["primary"])

        for payload, path in (
            (
                '{"topic_profiles":{"legacy":{"collection":"Legacy Papers",'
                '"collection_label":"Legacy Papers","search_keywords":{"primary":["Legacy ML"],'
                '"secondary":["Legacy AI"]}}}}',
                r"topic_profiles\.legacy\.label",
            ),
            (
                '{"topic_profiles":{"legacy":{"collections":["Legacy Papers"]}}}',
                r"topic_profiles\.legacy\.label",
            ),
        ):
            self._with_config(payload)
            with self.assertRaisesRegex(ValueError, path) as raised:
                config_loader.get_topic_profile("legacy")
            self.assertNotIn("Legacy Papers", str(raised.exception))

    def test_setup_config_does_not_persist_sentinel_secrets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_path = root / "config.json"
            with (
                patch.object(setup_cli, "REPO", root),
                patch.object(setup_cli, "CONFIG_PATH", config_path),
                patch.dict(
                    os.environ,
                    {
                        "ZOTERO_API_KEY": "ZOTERO_SECRET_SENTINEL",
                        "GOOGLE_API_KEY": "GOOGLE_SECRET_SENTINEL",
                        "ANTHROPIC_API_KEY": "ANTHROPIC_SECRET_SENTINEL",
                        "RESEND_API_KEY": "RESEND_SECRET_SENTINEL",
                        "ZOTERO_COLLECTION_NAME": "Sentinel Papers",
                        "ZOTERO_TOPIC_ALIAS": "sentinel",
                        "ZOTERO_DIR": "",
                        "ZOTERO_EMAIL": "",
                        "UNPAYWALL_EMAIL": "",
                        "PAPERBANANA_DIR": "",
                        "GITHUB_REPO": "",
                    },
                    clear=False,
                ),
                patch("builtins.input", side_effect=AssertionError("unexpected prompt")),
            ):
                cfg = setup_cli.step_config()
                setup_cli.step_env_check(cfg, "api-key")

            contents = config_path.read_text(encoding="utf-8")
            self.assertIn("Sentinel Papers", contents)
            for sentinel in (
                "ZOTERO_SECRET_SENTINEL",
                "GOOGLE_SECRET_SENTINEL",
                "ANTHROPIC_SECRET_SENTINEL",
                "RESEND_SECRET_SENTINEL",
            ):
                self.assertNotIn(sentinel, contents)


if __name__ == "__main__":
    unittest.main()
