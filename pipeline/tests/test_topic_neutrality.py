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


class NoThemeFallbackToAi4sTests(unittest.TestCase):
    """THEMES["ai4s"] 로 폴백하는 자리가 다시 생기지 않게.

    review_to_html 에서 고쳤는데 compare_papers 에 같은 줄이 한 벌 더 있었다.
    폴백은 theme_for() 한 곳에만 있어야 한다.
    """

    def test_no_module_falls_back_to_the_ai4s_theme(self):
        """review_to_html 밖에서 THEMES["ai4s"] 를 참조하면 안 된다."""
        import re

        pattern = re.compile(r'THEMES\[["\']ai4s["\']\]')
        offenders = []
        for root, _dirs, files in os.walk(PIPELINE):
            if "tests" in root or "_archive" in root:
                continue
            for fn in files:
                if not fn.endswith(".py") or fn == "review_to_html.py":
                    continue
                path = os.path.join(root, fn)
                for line in open(path, encoding="utf-8").read().splitlines():
                    if pattern.search(line):
                        offenders.append(
                            f"{os.path.relpath(path, PIPELINE)}: {line.strip()}")
        self.assertEqual([], offenders,
                         "ai4s 테마로 폴백하는 자리가 남았다 — theme_for() 를 쓸 것")



class TopicIndexMetadataTests(unittest.TestCase):
    """CLI topic resolution must also reach generated social metadata."""

    def test_social_metadata_uses_resolved_topic(self):
        src = open(
            os.path.join(PIPELINE, "build_topic_index.py"),
            encoding="utf-8",
        ).read()
        self.assertIn(
            'paper-curation.jehyunlee.dev/{TOPIC}/',
            src,
        )
        self.assertNotIn(
            'paper-curation.jehyunlee.dev/{topic}/',
            src,
        )

class DeployTopicNeutralityTests(unittest.TestCase):
    """배포 경로도 토픽을 하드코딩하지 않는다.

    두 군데가 박혀 있었다.
      - _TOPIC_TITLES: humanoid/physical-ai/ai4s/scisci 만 담은 dict. 새 토픽은
        전부 alias 흉내(bioml → "Bioml")로 gh-pages 스텁에 실렸다. 사용자는 이미
        setup 에서 label 을 정했는데 그걸 안 봤다.
      - CF_PROBE_PATHS: ("/", "/humanoid/", "/physical-ai/", "/index.html"). 배포
        검증이 그 두 토픽을 고정으로 찔러서, 없는 설치는 영영 200 을 못 받고
        타임아웃했다. topic 인자를 받으면서 쓰지도 않았다.
    """

    def _prepare_deploy(self):
        import prepare_deploy
        return prepare_deploy

    def test_label_comes_from_config_profile(self):
        P = self._prepare_deploy()
        cfg = {"topic_profiles": {"bioml": {"label": "Biology × ML"}}}
        with patch("config_loader.load_config", return_value=cfg):
            self.assertEqual(P._topic_title("bioml"), "Biology × ML")

    def test_label_falls_back_to_collection_name(self):
        P = self._prepare_deploy()
        cfg = {"zotero": {"collections": {"climate": "Climate Science"}}}
        with patch("config_loader.load_config", return_value=cfg):
            self.assertEqual(P._topic_title("climate"), "Climate Science")

    def test_label_last_resort_is_the_alias(self):
        P = self._prepare_deploy()
        with patch("config_loader.load_config", return_value={}):
            self.assertEqual(P._topic_title("physical-ai"), "Physical Ai")

    def test_label_survives_unreadable_config(self):
        P = self._prepare_deploy()
        with patch("config_loader.load_config", side_effect=RuntimeError("boom")):
            self.assertEqual(P._topic_title("bioml"), "Bioml")

    def test_probe_paths_have_no_hardcoded_topics(self):
        """루트 경로만 고정이어야 한다."""
        P = self._prepare_deploy()
        for path in P.CF_ROOT_PROBE_PATHS:
            with self.subTest(path=path):
                self.assertNotIn("humanoid", path)
                self.assertNotIn("physical-ai", path)

    def test_verify_probes_the_requested_topic(self):
        """_verify_cloudflare 가 받은 토픽을 실제로 찔러야 한다."""
        import inspect

        P = self._prepare_deploy()
        src = inspect.getsource(P._verify_cloudflare)
        self.assertIn("probe_paths", src)
        self.assertIn("topic", src.split("def _verify_cloudflare")[1][:400])


if __name__ == "__main__":
    unittest.main(verbosity=2)
