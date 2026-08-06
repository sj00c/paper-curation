"""자식 프로세스는 부모와 **같은** 인터프리터로 띄워야 한다.

`_env_guard.force_py312()` 는 진입점을 py312 로 재실행한다. 그런데
`run_update_force` 는 무거운 단계 35개를 전부 리터럴 `"python"` 으로 띄우고
있었다 — 즉 가드가 잡아 준 인터프리터가 아니라 PATH 의 `python` 이 돌았다.

* venv/pyenv/uv 처럼 `python` 별칭이 없는 환경: 전 단계 FileNotFoundError.
* launchd/cron/`.command` 런처: PATH 가 로그인 셸과 달라 엉뚱한 인터프리터.
* `python` 이 다른 env 를 가리키면 py312 강제가 조용히 무력화된다.

같은 버그를 `scripts/pre-push` 에서 이미 한 번 고쳤다(거기 주석에 "advisory
검사가 실제로는 한 번도 돌지 않았다"고 적혀 있다). 오케스트레이터에는 남아
있었다. `sys.executable` 로 고정한다.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent.parent
BAD_HEADS = {"python", "python3", "python3.12", "py"}


def _literal_interpreter_commands(src: str) -> list[tuple[int, str]]:
    """첫 원소가 리터럴 인터프리터 이름인 리스트 = 자식 프로세스 커맨드."""
    tree = ast.parse(src)
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.List) or not node.elts:
            continue
        first = node.elts[0]
        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            continue
        if first.value not in BAD_HEADS:
            continue
        rest = node.elts[1] if len(node.elts) > 1 else None
        arg = rest.value if isinstance(rest, ast.Constant) else ""
        # 인터프리터로 스크립트를 띄우는 형태만 문제 삼는다 (["python", "x.py", ...]).
        if isinstance(arg, str) and (arg.endswith(".py") or arg in {"-c", "-m"}):
            hits.append((node.lineno, first.value))
    return hits


class ChildInterpreterTests(unittest.TestCase):
    def test_no_pipeline_module_spawns_a_bare_python(self):
        offenders: dict[str, list[tuple[int, str]]] = {}
        for path in sorted(PIPELINE.rglob("*.py")):
            if "_archive" in path.parts or "tests" in path.parts:
                continue
            hits = _literal_interpreter_commands(path.read_text(encoding="utf-8"))
            if hits:
                offenders[str(path.relative_to(PIPELINE.parent))] = hits

        self.assertEqual(
            offenders, {},
            "자식 단계를 PATH 의 python 으로 띄운다 — sys.executable 을 써라")

    def test_the_detector_actually_detects(self):
        sample = 'run_step("x", ["python", "pipeline/cleanup.py", "--execute"], 300)\n'
        self.assertEqual(_literal_interpreter_commands(sample), [(1, "python")])


if __name__ == "__main__":
    unittest.main()
