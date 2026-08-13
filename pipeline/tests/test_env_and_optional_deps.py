"""py312 탐색 · 선택 의존성 격리 · 학습 파일 부재 내성.

세 건 다 "설치돼 있어야 할 게 없을 때 조용히 엉뚱하게 실패한다"는 같은 계열의
버그였고, 셋 다 실제로 이 저장소에서 재현됐다:

* `_env_guard.find_py312()` 가 conda **밖** 인터프리터로 진입하면 표준 위치에
  py312 가 멀쩡히 있어도 못 찾아, 모든 CLI 진입점이 죽었다.
* 도메인 전용 다이제스트가 SDK 의존성과 순수 Markdown 변환을 섞어, citedby
  리포트가 선택 SDK 없이 마크다운을 렌더하지 못했다. 변환기는 `lib/mdhtml.py`
  로 분리했고 전용 다이제스트는 제품 파이프라인에서 제거했다.
* `originality_extractor.load_triggers()` 는 선택 사전이 없어도 import된다.
"""
from __future__ import annotations

import ast
import builtins
import importlib
import re
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
    """텍스트 헬퍼가 선택 SDK(MP3 인코더·Gemini)를 요구하면 안 된다."""

    def test_markdown_helper_imports_without_optional_sdks(self):
        blocked = ("google", "anthropic", "openai")

        real_import = builtins.__import__

        def deny(name, *a, **kw):
            if any(name == b or name.startswith(b + ".") for b in blocked):
                raise ModuleNotFoundError(f"No module named '{name}'")
            return real_import(name, *a, **kw)

        sys.modules.pop("lib.mdhtml", None)
        for b in blocked:
            sys.modules.pop(b, None)
        with patch.object(builtins, "__import__", deny):
            mod = importlib.import_module("lib.mdhtml")
            html = mod.md_to_html("## 제목\n\n**굵게** 본문")
        self.assertIn("<h2>", html)
        self.assertIn("<strong>굵게</strong>", html)

    def test_markdown_helper_stays_in_the_dependency_light_module(self):
        """순수 Markdown 변환은 provider SDK와 무관한 모듈에 둔다."""
        self.assertTrue((PIPELINE / "lib" / "mdhtml.py").exists())

    def test_citedby_report_renders_narrative_markdown(self):
        from lib.citedby import report
        html = report.build_report_html(
            papers=[{"title": "P"}], timeline_narrative="## 제목\n\n**굵게** 본문")
        self.assertIn("<strong>굵게</strong>", html)
        self.assertNotIn("<p>## 제목</p>", html)


class DeclaredDependencyTests(unittest.TestCase):
    """최상단에서 import 하는 서드파티는 requirements.txt 에 선언돼 있어야 한다.

    `lib/metrics/store.py` 가 `import yaml` 을 최상단에서 하는데 PyYAML 이
    선언돼 있지 않았다. run_metrics 는 soft step 이라, 깨끗한 설치에서는
    피인용/레퍼런스 수집이 매 사이클 조용히 실패만 하고 아무도 몰랐다.
    """

    # import 이름 → 배포 이름
    _DIST = {
        "PIL": "Pillow",
        "google": "google-genai",
        "sklearn": "scikit-learn",
        "umap": "umap-learn",
        "yaml": "PyYAML",
        "fitz": "pymupdf",
        "cv2": "opencv-python",
    }

    @staticmethod
    def _norm(name: str) -> str:
        return name.lower().replace("_", "-")

    def _declared(self) -> set[str]:
        req = (PIPELINE.parent / "requirements.txt").read_text(encoding="utf-8")
        out = set()
        for line in req.splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            out.add(self._norm(re.split(r"[<>=!\[;]", line)[0].strip()))
        return out

    def _local_module_names(self) -> set[str]:
        names = set()
        for pat in ("*.py", "lib/*.py", "lib/*/*.py", "api/*.py"):
            names |= {p.stem for p in PIPELINE.glob(pat)}
        names |= {d.name for d in PIPELINE.iterdir() if d.is_dir()}
        names |= {d.name for d in (PIPELINE / "lib").iterdir() if d.is_dir()}
        names |= {d.name for d in (PIPELINE.parent / "src").iterdir() if d.is_dir()}
        return names

    def test_every_module_level_third_party_import_is_declared(self):
        declared = self._declared()
        local = self._local_module_names()
        undeclared: dict[str, list[str]] = {}

        for path in sorted(PIPELINE.rglob("*.py")):
            if "_archive" in path.parts or "tests" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in tree.body:  # 최상단만 — 지연 import 는 선택 의존성이다
                if isinstance(node, ast.Import):
                    names = [a.name.split(".")[0] for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    names = [node.module.split(".")[0]]
                else:
                    continue
                for name in names:
                    if name in sys.stdlib_module_names or name in local:
                        continue
                    dist = self._norm(self._DIST.get(name, name))
                    if dist not in declared:
                        undeclared.setdefault(name, []).append(
                            str(path.relative_to(PIPELINE.parent)))

        self.assertEqual(
            undeclared, {},
            "requirements.txt 에 없는 최상단 서드파티 import — 깨끗한 설치에서 죽는다")


class MachineSpecificPathTests(unittest.TestCase):
    """다른 머신에서 죽는 절대 홈 경로를 제품 소스에 박지 않는다."""

    _HOME_PATH = re.compile(r"""["'](?:/Users/|/home/|[A-Za-z]:\\Users\\)""")

    def test_no_module_hardcodes_a_home_directory(self):
        offenders = []
        for path in sorted(PIPELINE.rglob("*.py")):
            if "_archive" in path.parts or "tests" in path.parts:
                continue
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("#"):
                    continue
                if self._HOME_PATH.search(line):
                    offenders.append(f"{path.relative_to(PIPELINE.parent)}:{i}")
        self.assertEqual(offenders, [], "머신 고유 절대 경로가 박혀 있다")


class GenericProductSurfaceTests(unittest.TestCase):
    """개인 연구 프로젝트용 one-off가 제품 파이프라인으로 돌아오지 않는다."""

    RETIRED = {
        "agent_lecture_digest.py",
        "agent_lecture_watchdog.py",
        "curriculum_map.py",
        "dashun_timeline.py",
        "dashun_timeline_pb.py",
        "lecture_map.py",
        "generate_mas_schematics.py",
        "build_slide_deck.py",
        "build_slide_essay.py",
        "lib/slide_prose_ai4s.py",
        "audit_reviews.py",
        "dedup_text.py",
        "detach_zotero_pdf.py",
        "inspect_zotero_item.py",
        "reextract_figures.py",
        "resolve_stuck_pdfs.py",
        "restore_zotero_doi.py",
        "salvage_reviews.py",
        "scan_figures.py",
        "compare_papers.py",
        "generate_audio.py",
        "generate_moc.py",
        "generate_workflow.py",
        "import_references.py",
        "rebuild_connections.py",
        "sync_bibliography_db.py",
        "sync_paper_connections.py",
        "build_institution_report.py",
        "build_schema_diagram.py",
        "lib/affiliation_groups.py",
        "lib/db_digest.py",
    }

    def test_retired_domain_scripts_are_absent(self):
        present = {
            str(path.relative_to(PIPELINE))
            for path in PIPELINE.rglob("*.py")
        }
        self.assertTrue(self.RETIRED.isdisjoint(present))

    def test_product_source_has_no_named_researcher_workflow(self):
        offenders = []
        for path in sorted(PIPELINE.rglob("*.py")):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if "Dashun Wang" in text or "dashun_wang" in text:
                offenders.append(str(path.relative_to(PIPELINE.parent)))
        self.assertEqual(offenders, [])


class LoadTriggersTests(unittest.TestCase):
    """선택 trigger 파일 없이도 fallback 경로가 동작해야 한다."""

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

if __name__ == "__main__":
    unittest.main()
