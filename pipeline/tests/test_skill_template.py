"""SKILL.md.template 이 SKILL.md 와 갈라지지 않게, 그리고 빈 config 가 문장을 조용히 망가뜨리지 않게 고정한다.

배경. setup.py step_skill_md 는 SKILL.md.template 을 렌더해 저장소 루트의 SKILL.md 를
덮어쓰고, step_install 이 그걸 ~/.claude/skills/ 로 복사한다. 그런데 SKILL.md 는 추적되는
파일이라 손으로도 고쳐진다. 실제로 SKILL.md 는 run_full.py 단일 진입점 디스패처로 바뀐 뒤
템플릿만 옛 791줄 플레이북으로 남아 있었다. 그 상태에서 setup 을 돌리면 (a) 저장소의
디스패처가 조용히 구버전으로 되돌아가고 (b) 설치되는 스킬이 존재하지 않는 워크플로를
지시한다. 값이 없는 슬롯을 빈 문자열로 치환하던 것도 같은 종류의 조용한 손상이었다 —
`--topic ` 이나 `배포 URL: /{topic}/` 처럼 망가진 채로 그럴듯해 보인다.
"""

import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import setup as setup_cli  # noqa: E402

REPO = PIPELINE.parent
TEMPLATE = REPO / "SKILL.md.template"

# 커밋된 SKILL.md 를 만들어 낸 값. 이 저장소(레퍼런스 설치)의 topic alias 와 Pages URL.
# setup 의 --write-reference 가 쓰는 값과 같아야 한다 — 두 벌로 갈라지면 테스트는
# 통과하는데 재생성 결과가 커밋본과 달라진다. 그래서 여기서 직접 참조한다.
REFERENCE = setup_cli.REFERENCE_REPLACEMENTS


def _git_show(path):
    try:
        proc = subprocess.run(
            ["git", "show", f"HEAD:{path}"],
            cwd=REPO,
            capture_output=True,
            check=False,
        )
    except (OSError, FileNotFoundError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8")


class SkillTemplateDriftTests(unittest.TestCase):
    def setUp(self):
        self.template = TEMPLATE.read_text(encoding="utf-8")

    @unittest.skipUnless(shutil.which("git"), "git 없이는 커밋본을 읽을 수 없다")
    def test_render_reproduces_committed_skill_md(self):
        """레퍼런스 값으로 렌더한 템플릿 == 커밋된 SKILL.md.

        로컬 SKILL.md 가 아니라 커밋본과 비교한다. 다른 topic alias 로 설치한
        사용자의 작업 트리는 정당하게 달라지지만, 추적되는 두 파일이 서로
        갈라지는 것은 언제나 결함이다.
        """
        committed = _git_show("SKILL.md")
        if committed is None:
            self.skipTest("HEAD:SKILL.md 를 읽을 수 없음")

        rendered, unresolved = setup_cli.render_skill_md(self.template, REFERENCE)
        self.assertEqual([], unresolved)
        self.assertEqual(
            committed,
            rendered,
            "SKILL.md.template 과 SKILL.md 가 갈라졌다. 한쪽만 고치면 setup 이 "
            "다른 쪽을 조용히 덮어쓴다.",
        )

    def test_template_is_the_dispatcher_not_the_legacy_playbook(self):
        """템플릿은 run_full.py 단일 진입점을 지시해야 한다."""
        self.assertIn("pipeline/run_full.py", self.template)
        for stale in (
            'subagent_type="paper-scout"',
            "run_update_force.py --topic",
            "Phase 0~7 전체 파이프라인",
        ):
            self.assertNotIn(
                stale,
                self.template,
                f"템플릿에 폐기된 워크플로가 남아 있다: {stale}",
            )

    def test_every_placeholder_has_a_stated_reason(self):
        """템플릿이 쓰는 슬롯은 전부 치환 대상이고, 비었을 때 이유를 말할 수 있어야 한다."""
        replacements = setup_cli.skill_replacements({})
        for placeholder in REFERENCE:
            self.assertIn(placeholder, self.template)
            self.assertIn(placeholder, replacements)
            self.assertIn(placeholder, setup_cli.SKILL_PLACEHOLDER_REASONS)


class SkillRenderTests(unittest.TestCase):
    def test_empty_value_leaves_the_slot_visible(self):
        """값이 없으면 빈 문자열로 지우지 않고 슬롯을 남긴다."""
        template = "python run_full.py --topic {topic_alias}\nURL: {pages_base_url}/{topic}/\n"
        rendered, unresolved = setup_cli.render_skill_md(
            template, {"{topic_alias}": "", "{pages_base_url}": ""}
        )
        self.assertEqual(template, rendered)
        self.assertEqual(["{topic_alias}", "{pages_base_url}"], unresolved)
        # 예전 동작이 만들던 조용히 망가진 문장이 아니어야 한다.
        self.assertNotIn("--topic \n", rendered)
        self.assertNotIn("URL: /", rendered)

    def test_unused_empty_slot_is_not_reported(self):
        """템플릿에 없는 슬롯은 값이 비어도 보고하지 않는다 (없는 걸 경고하지 않는다)."""
        rendered, unresolved = setup_cli.render_skill_md(
            "no slots here", {"{email}": "", "{zotero_dir}": ""}
        )
        self.assertEqual("no slots here", rendered)
        self.assertEqual([], unresolved)

    def test_topic_alias_comes_from_the_configured_collection(self):
        cfg = {"zotero": {"collections": {"bioml": "ABC123", "ai4s": "DEF456"}}}
        self.assertEqual("bioml", setup_cli.resolve_topic_alias(cfg))

        rendered, unresolved = setup_cli.render_skill_md(
            TEMPLATE.read_text(encoding="utf-8"), setup_cli.skill_replacements(cfg)
        )
        self.assertIn("--topic bioml --mode curate", rendered)
        self.assertNotIn("--topic ai4s", rendered)
        # github 미설정이므로 배포 URL 슬롯만 남는다.
        self.assertEqual(["{pages_base_url}"], unresolved)

    def test_topic_alias_missing_is_empty_not_a_guess(self):
        self.assertEqual("", setup_cli.resolve_topic_alias({}))
        self.assertEqual("", setup_cli.resolve_topic_alias({"zotero": {"collections": {}}}))
        self.assertEqual("", setup_cli.resolve_topic_alias({"zotero": {"collections": None}}))


class StepSkillMdTests(unittest.TestCase):
    def _run(self, cfg, template_text):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            template = tmp / "SKILL.md.template"
            template.write_text(template_text, encoding="utf-8")
            out = tmp / "SKILL.md"
            gitignore = tmp / ".gitignore"
            gitignore.write_text("config.json\n", encoding="utf-8")

            buf = io.StringIO()
            with patch.object(setup_cli, "TEMPLATE_PATH", template), \
                 patch.object(setup_cli, "SKILL_OUTPUT", out), \
                 patch.object(setup_cli, "GITIGNORE_PATH", gitignore), \
                 redirect_stdout(buf):
                ok = setup_cli.step_skill_md(cfg)
            return ok, out.read_text(encoding="utf-8"), buf.getvalue()

    def test_unresolved_slots_are_reported_with_a_reason(self):
        ok, written, output = self._run({}, "--topic {topic_alias}\n{pages_base_url}/x/\n")
        self.assertTrue(ok)
        self.assertIn("{topic_alias}", written)
        self.assertIn("{topic_alias} 미해결", output)
        self.assertIn("zotero.collections", output)
        self.assertIn("{pages_base_url} 미해결", output)
        self.assertIn("github.pages_base_url", output)

    def test_fully_configured_render_is_silent_and_complete(self):
        cfg = {
            "zotero": {"collections": {"bioml": "K"}, "email": "a@b.c", "pdf_dir": "/tmp/z"},
            "github": {"repo": "u/r", "pages_base_url": "https://u.github.io/r"},
        }
        ok, written, output = self._run(cfg, "--topic {topic_alias}\n{pages_base_url}/x/\n")
        self.assertTrue(ok)
        self.assertEqual("--topic bioml\nhttps://u.github.io/r/x/\n", written)
        self.assertNotIn("미해결", output)

    def test_missing_template_fails_instead_of_writing_a_blank_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            out = tmp / "SKILL.md"
            with patch.object(setup_cli, "TEMPLATE_PATH", tmp / "nope.template"), \
                 patch.object(setup_cli, "SKILL_OUTPUT", out), \
                 patch.object(setup_cli, "GITIGNORE_PATH", tmp / ".gitignore"), \
                 redirect_stdout(io.StringIO()):
                self.assertFalse(setup_cli.step_skill_md({}))
            self.assertFalse(out.exists())


class ReferenceOutputSeparationTests(unittest.TestCase):
    """setup 이 추적 파일을 덮지 않는다는 계약.

    예전에는 SKILL_OUTPUT 이 추적되는 REPO/SKILL.md 라, setup 을 돌린 사람은 누구나
    자기 topic alias 가 박힌 diff 를 안고 있었다. 실수로 커밋되면 남의 설치값이
    저장소의 레퍼런스로 남는다.
    """

    def test_setup_renders_to_an_untracked_path(self):
        self.assertNotEqual(setup_cli.SKILL_OUTPUT, setup_cli.SKILL_REFERENCE)
        self.assertEqual(setup_cli.SKILL_REFERENCE.name, "SKILL.md")

    def test_generated_output_is_gitignored(self):
        """생성물이 추적되면 같은 문제가 되돌아온다."""
        proc = subprocess.run(
            ["git", "check-ignore", "-q", setup_cli.SKILL_OUTPUT.name],
            cwd=REPO, capture_output=True, check=False,
        )
        self.assertEqual(0, proc.returncode,
                         f"{setup_cli.SKILL_OUTPUT.name} 이 gitignore 되지 않는다")

    def test_write_reference_reproduces_the_committed_file(self):
        """--write-reference 는 커밋본을 그대로 재현해야 한다 (idempotent)."""
        committed = _git_show("SKILL.md")
        if committed is None:
            self.skipTest("HEAD:SKILL.md 를 읽을 수 없음")
        template = TEMPLATE.read_text(encoding="utf-8")
        rendered, unresolved = setup_cli.render_skill_md(
            template, setup_cli.REFERENCE_REPLACEMENTS)
        self.assertEqual([], unresolved)
        self.assertEqual(committed, rendered)

    def test_step_skill_md_does_not_touch_the_reference(self):
        """로컬 설치값으로 렌더해도 레퍼런스 파일은 그대로여야 한다."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            template = tmp / "SKILL.md.template"
            template.write_text("--topic {topic_alias}\n", encoding="utf-8")
            reference = tmp / "SKILL.md"
            reference.write_text("REFERENCE-UNTOUCHED\n", encoding="utf-8")
            out = tmp / "SKILL.generated.md"

            cfg = {"zotero": {"collections": {"bioml": "BioML"}}}
            with patch.object(setup_cli, "TEMPLATE_PATH", template), \
                 patch.object(setup_cli, "SKILL_OUTPUT", out), \
                 patch.object(setup_cli, "SKILL_REFERENCE", reference), \
                 patch.object(setup_cli, "GITIGNORE_PATH", tmp / ".gitignore"), \
                 redirect_stdout(io.StringIO()):
                setup_cli.step_skill_md(cfg)

            self.assertEqual("REFERENCE-UNTOUCHED\n",
                             reference.read_text(encoding="utf-8"),
                             "setup 이 레퍼런스 파일을 덮었다")
            self.assertIn("bioml", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
