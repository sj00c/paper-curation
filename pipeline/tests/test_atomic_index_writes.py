"""`_papers_index.json` 은 원자적으로만 써야 한다.

이 파일은 문서가 "single source of truth" 라고 부르는 마스터 인덱스다.
`build_papers_index.py` 는 `lib/atomic_io` 로 원자적으로 썼지만, 정작 이걸
되쓰는 다른 두 곳은 평범한 `open(..., "w") + json.dump` 였다:

* `topic_modeling.py` — 분류 결과 write-back
* `sync_zotero.py` — Zotero 삭제 동기화. 바로 위에서 slug 디렉토리를 rmtree
  한 뒤라, 여기서 잘려 쓰이면 인덱스와 디스크가 함께 깨진다.

수백 편짜리 인덱스를 쓰는 도중에 프로세스가 죽으면(타임아웃 kill 포함) 잘린
JSON 이 남고, 그 다음 단계 전부가 그걸 읽는다. 규칙은 코드로 고정한다.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent.parent
INDEX = "_papers_index.json"


def _plain_writes(src: str) -> list[tuple[int, str]]:
    """`open(<_papers_index.json 경로>, "w")` 호출 위치."""
    tree = ast.parse(src)

    # `index_path = os.path.join(PAPERS_DIR, "_papers_index.json")` 같은 간접 참조.
    index_vars: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        if INDEX not in (ast.get_source_segment(src, node) or ""):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        index_vars |= {t.id for t in targets if isinstance(t, ast.Name)}

    hits = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "open"):
            continue
        seg = ast.get_source_segment(src, node) or ""
        if '"w"' not in seg and "'w'" not in seg:
            continue
        first = node.args[0] if node.args else None
        if first is None:
            continue
        touches_index = INDEX in (ast.get_source_segment(src, first) or "")
        if isinstance(first, ast.Name) and first.id in index_vars:
            touches_index = True
        if touches_index:
            hits.append((node.lineno, seg[:100]))
    return hits


class AtomicIndexWriteTests(unittest.TestCase):
    def test_master_index_is_never_written_with_plain_open(self):
        offenders: dict[str, list[tuple[int, str]]] = {}
        for path in sorted(PIPELINE.rglob("*.py")):
            if "_archive" in path.parts or "tests" in path.parts:
                continue
            src = path.read_text(encoding="utf-8")
            if INDEX not in src:
                continue
            hits = _plain_writes(src)
            if hits:
                offenders[str(path.relative_to(PIPELINE.parent))] = hits

        self.assertEqual(
            offenders, {},
            "마스터 인덱스를 비원자적으로 쓴다 — lib/atomic_io.atomic_write_json 을 써라")

    def test_the_detector_actually_detects(self):
        """탐지기가 늘 빈 dict 만 돌려주는 무해한 통과가 되지 않게 한다."""
        sample = (
            'import json, os\n'
            'index_path = os.path.join(PAPERS_DIR, "_papers_index.json")\n'
            'with open(index_path, "w", encoding="utf-8") as f:\n'
            '    json.dump(papers, f)\n'
        )
        self.assertEqual(len(_plain_writes(sample)), 1)


if __name__ == "__main__":
    unittest.main()
