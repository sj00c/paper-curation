"""py312 단독 환경 가드.

운영자 지시(2026-06-18): paper-curation 은 **py312 단독**으로 사용한다. py314 등
다른 인터프리터로 진입하는 모든 경로를 차단한다. 각 실행 진입점(__main__)에서
``force_py312()`` 를 가장 먼저 호출하면, py312 가 아닌 인터프리터로 실행됐을 때
py312 인터프리터로 **자동 재실행**한다(py312 를 못 찾으면 명확히 실패).

라이브러리로 import 될 때(예: Paper Curio 브리지가 run_update_force 의 함수를
호출)는 영향이 없도록, 반드시 ``if __name__ == "__main__":`` 안에서만 호출한다.
"""

import os
import shutil
import sys
from pathlib import Path


def _interp(env_root) -> str | None:
    """conda env 루트에서 인터프리터 경로. POSIX/Windows 양쪽."""
    for rel in ("bin/python", "Scripts/python.exe"):
        cand = Path(env_root) / rel
        if cand.exists():
            return str(cand)
    return None


def _conda_roots():
    """py312 env 를 담고 있을 수 있는 conda 설치 루트 후보들.

    이 함수가 존재하는 이유: 기존 탐색은 `sys.executable` 조상에 `envs` 가
    있을 때만 형제 env 를 찾았다. conda 밖 인터프리터(`/usr/local/bin/python3`
    등)로 진입하면 조상에 `envs` 가 없어, py312 가 표준 위치에 멀쩡히 설치돼
    있어도 "찾을 수 없습니다" 로 죽었다. 실제로 이 저장소에서 `run_citedby.py
    --help` 가 그렇게 실패했다.
    """
    roots = []
    prefix = os.environ.get("CONDA_PREFIX", "").strip()
    if prefix:
        p = Path(prefix)
        # <root>/envs/<name> 이면 두 단계 위가 root, 아니면 그 자체가 base.
        roots.append(p.parent.parent if p.parent.name == "envs" else p)
    exe = os.environ.get("CONDA_EXE", "").strip()
    if exe:
        roots.append(Path(exe).resolve().parent.parent)
    which_conda = shutil.which("conda")
    if which_conda:
        # `conda` 는 보통 <root>/condabin/conda 또는 <root>/bin/conda 로 해석된다.
        roots.append(Path(which_conda).resolve().parent.parent)
    home = Path.home()
    roots += [home / "miniforge3", home / "miniconda3", home / "anaconda3",
              home / "mambaforge", Path("/opt/miniconda3"),
              Path("/opt/homebrew/Caskroom/miniforge/base")]
    return roots


def find_py312() -> str | None:
    """py312 인터프리터 경로를 찾는다. 우선순위:
    PAPER_CURATION_PY312 → 형제 conda env <base>/envs/py312 → conda 설치 루트
    (CONDA_PREFIX/CONDA_EXE/which conda/표준 경로) → which python3.12 →
    현재 인터프리터가 py312 면 그것. 없으면 None.
    """
    explicit = os.environ.get("PAPER_CURATION_PY312", "").strip()
    if explicit and os.path.exists(explicit):
        return explicit
    here = Path(sys.executable).resolve()
    for anc in here.parents:
        if anc.name == "envs":
            cand = _interp(anc / "py312")
            if cand:
                return cand
            break
    seen = set()
    for root in _conda_roots():
        if root in seen:
            continue
        seen.add(root)
        cand = _interp(root / "envs" / "py312")
        if cand:
            return cand
    found = shutil.which("python3.12")
    if found:
        return found
    if sys.version_info[:2] == (3, 12):
        return sys.executable
    return None


def force_py312() -> None:
    """현재 인터프리터가 py312 가 아니면 py312 로 재실행한다(py314 차단)."""
    if sys.version_info[:2] == (3, 12):
        return
    if os.environ.get("_PC_PY312_REEXEC") == "1":
        # 이미 한 번 재실행했는데도 py312 가 아니다 → 무한 루프 방지 + 명확히 실패.
        raise SystemExit(
            "paper-curation 은 py312 단독 환경을 사용합니다 (py314 금지). "
            f"현재 인터프리터: {sys.executable} (Python {sys.version.split()[0]})"
        )
    py312 = find_py312()
    if not py312:
        raise SystemExit(
            "py312 인터프리터를 찾을 수 없습니다. paper-curation 은 py312 단독 환경입니다 "
            "(py314 금지). conda env py312 를 만들거나 PAPER_CURATION_PY312 로 절대 경로를 지정하세요."
        )
    os.environ["_PC_PY312_REEXEC"] = "1"
    print(f"[env] py312 단독 강제: {sys.executable} → {py312} 로 재실행", file=sys.stderr)
    os.execv(py312, [py312, *sys.argv])
