"""py312 탐색 · 선택 의존성 격리 · 학습 파일 부재 내성.

세 건 다 "설치돼 있어야 할 게 없을 때 조용히 엉뚱하게 실패한다"는 같은 계열의
버그였고, 셋 다 실제로 이 저장소에서 재현됐다:

* `_env_guard.find_py312()` 가 conda **밖** 인터프리터로 진입하면 표준 위치에
  py312 가 멀쩡히 있어도 못 찾아, 모든 CLI 진입점이 죽었다.
* `agent_lecture_digest` 가 MP3 인코더(`lameenc`)를 최상단에서 import 해서,
  그 모듈의 순수 텍스트 헬퍼를 빌려 쓰는 citedby 리포트가 마크다운을 렌더하지
  못하고 `##` 를 글자 그대로 노출했다.
* `originality_extractor.load_triggers()` 가 self-learning 파일이 없으면
  FileNotFoundError 로 죽었다. 정작 쓰는 쪽(`_update_triggers`)은 빈 상태에서
  파일을 새로 만들 수 있었는데 읽는 쪽만 못 했다.
"""
from __future__ import annotations

import builtins
import importlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE))

import _env_guard  # noqa: E402
from lib import originality_extractor as oe  # noqa: E402


def _make_conda_root(tmp: Path, env_name: str = "py312") -> Path:
    """conda 설치 루트 흉내 — <root>/envs/<name>/bin/python."""
    interp = tmp / "envs" / env_name / "bin" / "python"
    interp.parent.mkdir(parents=True)
    interp.write_text("#!/bin/sh\n", encoding="utf-8")
    interp.chmod(0o755)
    return tmp


class FindPy312Tests(unittest.TestCase):
    def test_explicit_env_var_wins(self):
        with tempfile.TemporaryDirectory() as td:
            root = _make_conda_root(Path(td))
            explicit = str(root / "envs" / "py312" / "bin" / "python")
            with patch.dict(os.environ, {"PAPER_CURATION_PY312": explicit}, clear=False):
                self.assertEqual(_env_guard.find_py312(), explicit)

    def test_found_from_conda_root_when_interpreter_is_outside_any_env(self):
        """회귀 방지: 예전 탐색은 `sys.executable` 조상에 `envs` 가 있을 때만
        동작해, `/usr/local/bin/python3` 로 들어오면 실패했다."""
        with tempfile.TemporaryDirectory() as td:
            root = _make_conda_root(Path(td))
            expected = str(root / "envs" / "py312" / "bin" / "python")
            env = {k: v for k, v in os.environ.items()
                   if k not in ("PAPER_CURATION_PY312", "CONDA_PREFIX", "CONDA_EXE")}
            env["CONDA_PREFIX"] = str(root)
            with (
                patch.dict(os.environ, env, clear=True),
                patch.object(_env_guard.sys, "executable", "/usr/local/bin/python3"),
                patch.object(_env_guard.shutil, "which", return_value=None),
            ):
                self.assertEqual(_env_guard.find_py312(), expected)

    def test_conda_prefix_inside_an_env_resolves_to_its_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = _make_conda_root(Path(td))
            (root / "envs" / "other" / "bin").mkdir(parents=True)
            expected = str(root / "envs" / "py312" / "bin" / "python")
            env = {k: v for k, v in os.environ.items()
                   if k not in ("PAPER_CURATION_PY312", "CONDA_PREFIX", "CONDA_EXE")}
            env["CONDA_PREFIX"] = str(root / "envs" / "other")
            with (
                patch.dict(os.environ, env, clear=True),
                patch.object(_env_guard.sys, "executable", "/usr/local/bin/python3"),
                patch.object(_env_guard.shutil, "which", return_value=None),
            ):
                self.assertEqual(_env_guard.find_py312(), expected)

    def test_returns_none_when_nothing_is_installed(self):
        """못 찾으면 None 이어야 한다 — force_py312 가 py314 로 진행하지 않고
        명확히 실패하는 근거다."""
        with tempfile.TemporaryDirectory() as td:
            env = {k: v for k, v in os.environ.items()
                   if k not in ("PAPER_CURATION_PY312", "CONDA_PREFIX", "CONDA_EXE")}
            with (
                patch.dict(os.environ, env, clear=True),
                patch.object(_env_guard.sys, "executable", "/usr/local/bin/python3"),
                patch.object(_env_guard.sys, "version_info", (3, 11, 7)),
                patch.object(_env_guard.shutil, "which", return_value=None),
                patch.object(_env_guard, "_conda_roots", return_value=[Path(td)]),
            ):
                self.assertIsNone(_env_guard.find_py312())

    def test_this_machine_resolves_a_real_py312(self):
        found = _env_guard.find_py312()
        self.assertIsNotNone(found, "이 머신에서 py312 를 못 찾는다 — CLI 전부가 죽는다")
        assert found is not None
        self.assertTrue(os.path.exists(found), found)


class OptionalHeavyDepTests(unittest.TestCase):
    """텍스트 헬퍼가 MP3 인코더를 요구하면 안 된다."""

    def test_markdown_helper_imports_without_lameenc(self):
        blocked = "lameenc"

        real_import = builtins.__import__

        def deny(name, *a, **kw):
            if name == blocked or name.startswith(blocked + "."):
                raise ModuleNotFoundError(f"No module named '{blocked}'")
            return real_import(name, *a, **kw)

        for mod in [m for m in list(sys.modules) if m == "agent_lecture_digest"]:
            del sys.modules[mod]
        sys.modules.pop(blocked, None)
        with patch.object(builtins, "__import__", deny):
            mod = importlib.import_module("agent_lecture_digest")
            html = mod.md_to_html("## 제목\n\n**굵게** 본문")
        self.assertIn("<h2>", html)
        self.assertIn("<strong>굵게</strong>", html)

    def test_lameenc_is_not_a_module_level_import(self):
        src = (PIPELINE / "agent_lecture_digest.py").read_text(encoding="utf-8")
        top_level = [
            ln for ln in src.splitlines()
            if ln.startswith("import lameenc") or ln.startswith("from lameenc")
        ]
        self.assertEqual(top_level, [], "lameenc 가 다시 최상단 import 로 올라왔다")

    def test_citedby_report_renders_narrative_markdown(self):
        from lib.citedby import report
        html = report.build_report_html(
            papers=[{"title": "P"}], timeline_narrative="## 제목\n\n**굵게** 본문")
        self.assertIn("<strong>굵게</strong>", html)
        self.assertNotIn("<p>## 제목</p>", html)


class LoadTriggersTests(unittest.TestCase):
    """self-learning 파일은 없는 상태에서 출발할 수 있어야 한다."""

    def test_missing_file_yields_an_empty_trigger_set(self):
        with tempfile.TemporaryDirectory() as td:
            out = oe.load_triggers(Path(td) / "nope.json")
        self.assertEqual(out["categories"], {})
        self.assertEqual(out["all"], [])
        self.assertTrue(out["_path"].endswith("nope.json"))

    def test_corrupt_file_does_not_kill_the_run(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "broken.json"
            p.write_text("{ not json", encoding="utf-8")
            out = oe.load_triggers(p)
        self.assertEqual(out["all"], [])

    def test_non_dict_json_is_tolerated(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "list.json"
            p.write_text("[1, 2, 3]", encoding="utf-8")
            self.assertEqual(oe.load_triggers(p)["categories"], {})

    def test_existing_file_still_loads(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.json"
            p.write_text(json.dumps({
                "rule_base_novelty": ["for the first time"],
                "_version": "test",
            }), encoding="utf-8")
            out = oe.load_triggers(p)
        self.assertEqual(out["categories"], {"rule_base_novelty": ["for the first time"]})
        self.assertEqual(out["all"], ["for the first time"])

    def test_learning_creates_the_file_from_empty(self):
        """읽기가 빈 집합을 주면, 쓰기가 그 위에 파일을 만들어 낸다 —
        비대칭이 사라졌다는 증거."""
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "grown.json"
            data = oe.load_triggers(p)
            added = oe._update_triggers(data, ["systematically evaluated"])
            self.assertEqual(added, 1)
            self.assertTrue(p.exists(), "학습 결과가 파일로 남지 않았다")
            reloaded = oe.load_triggers(p)
        self.assertIn("systematically evaluated", reloaded["all"])


if __name__ == "__main__":
    unittest.main()
