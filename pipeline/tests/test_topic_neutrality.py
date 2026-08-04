"""토픽 중립성 고정 — ai4s 가 없는 설치에서도 논문 페이지가 옳게 렌더되게.

배경. review_to_html 은 미등록 토픽을 만나면 `THEMES.get(topic, THEMES["ai4s"])`
로 ai4s 테마를 씌웠다. physical-ai 설치에서 실제로 두 가지가 깨졌다.

  1. accent 불일치 — build_topic_index 는 미지 토픽에 중립 파랑(#3B82F6)을 주는데
     논문 페이지만 ai4s 빨강(#D63423)으로 떴다. 같은 사이트 안에서 색이 갈렸다.
  2. 죽은 링크 — back_href 가 ../../ai4s/index.html 로 굳어, ai4s 디렉토리가 없는
     설치에서는 '목록으로 돌아가기' 가 404 였다.

detect_topic 도 같은 뿌리로 'ai4s' 를 반환해, 인덱스가 토픽을 말해주지 않는 논문이
남의 토픽으로 렌더됐다.

여기서 고정하는 계약:
  - 알려진 토픽(ai4s/scisci)의 테마는 그대로다. 기존 사이트가 바뀌면 안 된다.
  - 미등록 토픽은 중립 테마를 받고, back_href 는 언제나 자기 토픽을 가리킨다.
  - detect_topic 의 폴백은 설정에서 유도한다. 토픽이 유일하면 그것, 아니면 눈에
    띄는 'unknown' — 존재하지 않는 남의 페이지로 조용히 링크되지 않는다.
"""

import os
import sys
import unittest
from unittest.mock import patch

PIPELINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

import review_to_html as R  # noqa: E402


class ThemeNeutralityTests(unittest.TestCase):
    def test_known_topics_keep_their_theme(self):
        """기존 토픽의 색과 링크는 그대로여야 한다 (배포된 사이트 보호)."""
        ai4s = R.theme_for("ai4s")
        self.assertEqual(ai4s["accent"], "#D63423")
        self.assertEqual(ai4s["back_href"], "../../ai4s/index.html")

        scisci = R.theme_for("scisci")
        self.assertEqual(scisci["accent"], "#2374D6")
        self.assertEqual(scisci["back_href"], "../../scisci/index.html")

    def test_unknown_topic_does_not_borrow_ai4s_theme(self):
        """미등록 토픽이 ai4s 빨강을 물려받으면 안 된다."""
        theme = R.theme_for("physical-ai")
        self.assertNotEqual(theme["accent"], R.THEMES["ai4s"]["accent"])

    def test_unknown_topic_back_href_points_at_itself(self):
        """back_href 는 자기 토픽. 이게 깨지면 '목록으로' 가 404 였다."""
        for topic in ("physical-ai", "bioml", "climate"):
            with self.subTest(topic=topic):
                self.assertEqual(
                    R.theme_for(topic)["back_href"],
                    f"../../{topic}/index.html",
                )

    def test_unknown_topic_theme_is_complete(self):
        """중립 테마도 알려진 테마와 같은 키를 전부 갖춰야 렌더가 KeyError 로 죽지 않는다."""
        required = set(R.THEMES["ai4s"].keys())
        self.assertTrue(required.issubset(set(R.theme_for("bioml").keys())))

    def test_unknown_topic_accent_matches_topic_index_default(self):
        """build_topic_index 의 미지-토픽 기본 accent 와 같아야 사이트 안에서 색이 안 갈린다."""
        self.assertEqual(R.theme_for("bioml")["accent"], "#3B82F6")


class DetectTopicFallbackTests(unittest.TestCase):
    def test_single_configured_topic_is_used(self):
        """토픽이 하나면 그것으로 폴백한다 (ai4s 가 아니라)."""
        with patch("config_loader.get_default_topic", return_value="physical-ai"):
            self.assertEqual(R._fallback_topic(), "physical-ai")

    def test_ambiguous_config_does_not_guess(self):
        """토픽이 여럿이면 임의로 고르지 않고 눈에 띄게 남긴다."""
        with patch("config_loader.get_default_topic", return_value=""):
            self.assertEqual(R._fallback_topic(), "unknown")

    def test_unreadable_config_does_not_crash(self):
        """config 를 못 읽어도 렌더가 죽으면 안 된다."""
        with patch("config_loader.get_default_topic", side_effect=RuntimeError("no config")):
            self.assertEqual(R._fallback_topic(), "unknown")

    def test_index_topic_wins_over_fallback(self):
        """인덱스가 토픽을 말하면 그것이 우선이다."""
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            idx = os.path.join(td, "_papers_index.json")
            with open(idx, "w", encoding="utf-8") as f:
                json.dump([{"slug": "001_A", "topics": ["bioml"]}], f)
            self.assertEqual(R.detect_topic("001_A", idx), "bioml")


class ConfigDefaultTopicTests(unittest.TestCase):
    def test_single_topic_resolves(self):
        import config_loader

        with patch.object(config_loader, "load_config",
                          return_value={"zotero": {"collections": {"bioml": "BioML"}}}):
            self.assertEqual(config_loader.get_default_topic(), "bioml")

    def test_multiple_topics_refuse_to_guess(self):
        import config_loader

        with patch.object(config_loader, "load_config",
                          return_value={"zotero": {"collections": {"a": "A", "b": "B"}}}):
            self.assertEqual(config_loader.get_default_topic(), "")

    def test_no_topics_is_empty(self):
        import config_loader

        with patch.object(config_loader, "load_config", return_value={"zotero": {}}):
            self.assertEqual(config_loader.get_default_topic(), "")

class ResolveTopicMigrationTests(unittest.TestCase):
    """--topic 생략 시의 이행 동작. 기존 사용자를 깨지 않으면서 오작동은 막는다."""

    def _cfg(self, collections):
        import config_loader
        return patch.object(config_loader, "load_config",
                            return_value={"zotero": {"collections": collections}})

    def test_single_topic_install_keeps_working(self):
        """매일 --topic 없이 돌리던 단일 토픽 설치는 그대로 돌아간다."""
        import config_loader

        with self._cfg({"physical-ai": "Physical AI"}):
            self.assertEqual(config_loader.resolve_topic(""), "physical-ai")

    def test_single_topic_install_says_what_it_chose(self):
        """조용히 고르지 않고 무엇을 골랐는지 알린다."""
        import config_loader
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with self._cfg({"physical-ai": "Physical AI"}):
            with redirect_stdout(buf):
                config_loader.resolve_topic("")
        self.assertIn("physical-ai", buf.getvalue())

    def test_explicit_topic_always_wins(self):
        import config_loader

        with self._cfg({"a": "A", "b": "B"}):
            self.assertEqual(config_loader.resolve_topic("b"), "b")

    def test_multiple_topics_stop_instead_of_guessing(self):
        """여러 토픽에서 임의로 하나를 고르면 남의 토픽을 건드린다 — 멈춰야 한다."""
        import config_loader

        with self._cfg({"ai4s": "A", "scisci": "S"}):
            with self.assertRaises(SystemExit) as cm:
                config_loader.resolve_topic("")
        msg = str(cm.exception)
        self.assertIn("ai4s", msg)
        self.assertIn("scisci", msg)

    def test_no_topic_configured_is_actionable(self):
        """토픽이 없으면 무엇을 해야 하는지 말해준다."""
        import config_loader

        with self._cfg({}):
            with self.assertRaises(SystemExit) as cm:
                config_loader.resolve_topic("")
        self.assertIn("setup", str(cm.exception))

    def test_never_silently_falls_back_to_ai4s(self):
        """핵심 회귀 — ai4s 가 설정에 없는데 ai4s 로 가면 안 된다."""
        import config_loader

        with self._cfg({"bioml": "BioML"}):
            self.assertEqual(config_loader.resolve_topic(""), "bioml")

        with self._cfg({"a": "A", "b": "B"}):
            with self.assertRaises(SystemExit):
                config_loader.resolve_topic("")


class EntrypointsUseResolverTests(unittest.TestCase):
    """개별 스크립트가 ai4s 를 다시 기본값으로 박지 못하게 고정."""

    SCRIPTS = [
        "run_update_force", "generate_network", "generate_timelines",
        "topic_modeling", "build_papers_index", "inject_frontmatter",
        "prepare_deploy", "generate_moc", "build_category_summaries",
        "extract_insights", "validate_papers", "build_rss",
    ]

    def test_no_script_defaults_to_ai4s(self):
        import re

        pattern = re.compile(r'add_argument\(\s*"-?-?topic"[^)]*default\s*=\s*["\']ai4s["\']')
        for name in self.SCRIPTS:
            with self.subTest(script=name):
                src = open(os.path.join(PIPELINE, f"{name}.py"), encoding="utf-8").read()
                self.assertIsNone(pattern.search(src),
                                  f"{name}.py 가 --topic 기본값으로 ai4s 를 다시 박았다")

    def test_every_script_routes_through_resolver(self):
        for name in self.SCRIPTS:
            with self.subTest(script=name):
                src = open(os.path.join(PIPELINE, f"{name}.py"), encoding="utf-8").read()
                self.assertIn("resolve_topic", src,
                              f"{name}.py 가 resolve_topic 을 거치지 않는다")



if __name__ == "__main__":
    unittest.main(verbosity=2)
