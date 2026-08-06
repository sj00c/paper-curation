"""줄바꿈 오염 가드 고정.

배경. 이 저장소는 CRLF 파일과 LF 파일이 섞여 있다 (CRLF 17개, LF 다수 —
`git ls-files --eol`) — upstream 원저자가 Windows 에서 만든 파일이 CRLF 로 커밋됐고
upstream 은 지금도 그렇게 커밋한다. 그 상태에서
편집 도구나 일괄 치환 스크립트가 CRLF 파일을 LF 로 다시 저장하면, 두 줄 고친
변경이 파일 전체 재작성으로 잡힌다. 실제로 15개 파일 359줄 변경이 6,138줄로 부푼
적이 있다 — 내용은 같은데 diff 가 쓰레기가 되어 리뷰가 불가능해졌다.

전부 LF 로 정규화하는 것은 오답이다. 9,912줄을 한 번에 재작성해야 하고, upstream 이
계속 CRLF 로 커밋하므로 머지할 때마다 같은 파일이 통째로 충돌한다.

여기서 고정하는 계약:
  - 줄바꿈만 바뀐 변경은 감지되고 exit 1 이다.
  - --fix 는 원래 줄바꿈으로 되돌리되, 함께 들어온 내용 변경은 지운다면 안 된다.
  - 줄바꿈을 보존한 정상 변경은 오탐하지 않는다.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts" / "check-eol.py"


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


class _Sandbox:
    """줄바꿈이 섞인 작은 저장소를 만들어 가드를 실제로 돌린다."""

    def __enter__(self):
        self.tmp = tempfile.mkdtemp()
        d = Path(self.tmp)
        _git(d, "init", "-q", ".")
        _git(d, "config", "user.email", "t@t")
        _git(d, "config", "user.name", "t")
        (d / "crlf.py").write_bytes(b"import os\r\nx = 1\r\ny = 2\r\n")
        (d / "lf.py").write_bytes(b"import os\nx = 1\ny = 2\n")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", "base")
        return d

    def __exit__(self, *exc):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)


def _run_checker(cwd, *args):
    return subprocess.run([sys.executable, str(CHECKER), *args],
                          cwd=cwd, capture_output=True, text=True, check=False)


class EolGuardTests(unittest.TestCase):
    def test_checker_exists_and_runs(self):
        self.assertTrue(CHECKER.is_file(), "scripts/check-eol.py 가 없다")

    def test_clean_tree_passes(self):
        with _Sandbox() as d:
            self.assertEqual(_run_checker(d).returncode, 0)

    def test_crlf_to_lf_is_detected(self):
        """핵심 회귀 — 이게 6,138줄 diff 를 만들었다."""
        with _Sandbox() as d:
            p = d / "crlf.py"
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
            r = _run_checker(d)
            self.assertEqual(r.returncode, 1, "줄바꿈 오염을 놓쳤다")
            self.assertIn("crlf.py", r.stderr)

    def test_lf_to_crlf_is_detected(self):
        """반대 방향도 같은 문제다."""
        with _Sandbox() as d:
            p = d / "lf.py"
            p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
            self.assertEqual(_run_checker(d).returncode, 1)

    def test_content_change_preserving_eol_is_not_flagged(self):
        """줄바꿈을 지킨 정상 변경은 통과해야 한다 (오탐 금지)."""
        with _Sandbox() as d:
            p = d / "crlf.py"
            p.write_bytes(p.read_bytes() + b"z = 3\r\n")
            (d / "lf.py").write_bytes((d / "lf.py").read_bytes() + b"z = 3\n")
            self.assertEqual(_run_checker(d).returncode, 0)

    def test_fix_restores_original_eol(self):
        with _Sandbox() as d:
            p = d / "crlf.py"
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
            self.assertEqual(_run_checker(d, "--fix").returncode, 0)
            self.assertIn(b"\r\n", p.read_bytes(), "CRLF 로 복원되지 않았다")
            self.assertEqual(_run_checker(d).returncode, 0)

    def test_fix_keeps_real_content_changes(self):
        """가장 중요한 계약 — 줄바꿈만 되돌리고 내용은 건드리지 않는다."""
        with _Sandbox() as d:
            p = d / "crlf.py"
            polluted = p.read_bytes().replace(b"\r\n", b"\n")
            p.write_bytes(polluted.replace(b"y = 2", b"y = 99"))

            _run_checker(d, "--fix")
            restored = p.read_bytes()

            self.assertIn(b"\r\n", restored, "줄바꿈이 복원되지 않았다")
            self.assertIn(b"y = 99", restored, "--fix 가 내용 변경을 날렸다")
            self.assertNotIn(b"\r\r", restored, "CR 이 중복됐다")

    def test_fix_does_not_create_mixed_endings(self):
        with _Sandbox() as d:
            p = d / "crlf.py"
            p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
            _run_checker(d, "--fix")
            data = p.read_bytes()
            self.assertEqual(data.count(b"\n"), data.count(b"\r\n"),
                             "LF 와 CRLF 가 섞였다")


class RepoPolicyTests(unittest.TestCase):
    def test_gitattributes_disables_eol_conversion(self):
        """`* -text` 가 있어야 git 이 제멋대로 변환하지 않는다."""
        ga = REPO / ".gitattributes"
        self.assertTrue(ga.is_file(), ".gitattributes 가 없다")
        self.assertIn("* -text", ga.read_text(encoding="utf-8"))

    def test_pre_push_invokes_the_guard(self):
        hook = REPO / "scripts" / "pre-push"
        if not hook.is_file():
            self.skipTest("pre-push 훅 없음")
        self.assertIn("check-eol.py", hook.read_text(encoding="utf-8"))

    def test_pre_push_no_longer_hardcodes_ai4s(self):
        """훅도 ai4s 를 박고 있었다 — 같은 뿌리."""
        hook = REPO / "scripts" / "pre-push"
        if not hook.is_file():
            self.skipTest("pre-push 훅 없음")
        self.assertNotIn('PAPER_CURATION_TOPIC:-ai4s}', hook.read_text(encoding="utf-8"))

    def test_no_tracked_source_states_the_127_lf_regression(self):
        """gen-2 의 127-계열 LF 개수 회귀가 추적 소스에 되살아나지 않게 고정한다.

        LF 개수는 커밋마다 흘러 금방 거짓이 된다 (한때 127 로 적혔다가 184 가 됨).
        실제로 한 번은 branch-ledger 만 고치고 .gitattributes/pre-push/CI 코멘트에
        옛 숫자가 남아 저장소가 같은 사실을 두고 자기모순을 냈다. glob 필터한 grep 은
        확장자 없는 .gitattributes/pre-push 를 구조적으로 못 봐서 놓쳤다 — git grep 으로
        전 추적 파일을 훑는다. 논문 콘텐츠(docs/papers)는 무관하므로 제외.

        범위는 그 사건의 값(12x)으로 좁힌다: 일반 3자리 규칙은 코퍼스의 정당한
        한글 개수 표현('642개 tests', '3,273개 …')과 충돌해 오탐이 난다. 다른
        고정 개수가 문제되면 EOL-정책 파일에 한정한 별도 규칙으로 넓히면 된다.
        """
        proc = subprocess.run(
            ["git", "grep", "-n", "-E", r"LF 12[0-9]|12[0-9]개",
             "--", ".", ":!docs/papers"],
            cwd=REPO, capture_output=True, text=True, check=False,
        )
        # git grep exits 0 (match) or 1 (no match); anything else means the scan
        # itself failed and an empty stdout would be a vacuous pass.
        self.assertIn(proc.returncode, (0, 1),
                      f"git grep failed ({proc.returncode}): {proc.stderr}")
        self.assertEqual(
            proc.stdout, "",
            f"frozen LF count found in tracked source:\n{proc.stdout}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
