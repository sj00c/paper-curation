"""
paper-curation end-to-end 오케스트레이터.

SKILL.md의 Recipe A~H 를 단일 엔트리포인트로 통합한다. 3축(`--mode`,
`--source`, `--images`)로 동작을 선언하고, 하부 스크립트
(search_papers / register_zotero / sync_zotero / run_update_force /
prepare_deploy) 를 순서대로 호출한다.

Usage (가장 자주 쓰는 패턴):
  # 주간 운영 — 검색 + Zotero 등록 + 신규만 리뷰
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode curate --source web --days 7

  # 로컬 업데이트 — 검색 스킵, Zotero 변경만 동기화 후 신규 리뷰
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode curate --source zotero

  # 특정 슬러그만 force-rebuild (복구 시)
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode rebuild --slugs 088,1093 --strict-pdf

  # 카테고리 재분류만
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode reclassify

  # 타임라인 이미지만 재생성
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode retime --images all

  # 배포만
  PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode deploy

플래그 자동 연계:
  --source web    → --with-search --with-register --with-sync 자동 활성
  --source zotero → --with-sync 만 자동 활성
  명시적 --with-* 은 자동 활성을 override
"""

import argparse
import subprocess
import sys
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE))
from lib.pipeline_state import mark_running, mark_finished  # noqa: E402


def run(cmd, timeout=None, env=None):
    """Return exit code. stdout/stderr inherited."""
    print(f"\n$ {' '.join(str(c) for c in cmd)}", flush=True)
    return subprocess.call(cmd, timeout=timeout, env=env)


def build_parser():
    p = argparse.ArgumentParser(description="Paper-curation end-to-end orchestrator (3-axis)")
    p.add_argument("--topic", required=True)
    p.add_argument("--mode", choices=["curate", "rebuild", "reclassify", "retime", "deploy",
                                       "audit", "fix-matching", "dedup", "validate"],
                   required=True,
                   help="MECE action axis. curate/rebuild/reclassify/retime/deploy "
                        "for pipeline runs; audit/fix-matching/dedup/validate "
                        "for standalone tooling (audit → audit_matching.py, "
                        "fix-matching → fix_matching.py, dedup → dedup_zotero.py, "
                        "validate → validate_papers.py).")
    p.add_argument("--source", choices=["web", "zotero"], default="zotero",
                   help="Input source. web=검색+등록+sync+review / zotero=sync+review.")
    p.add_argument("--images", choices=["skip", "changed", "all"], default=None,
                   help="타임라인 이미지 범위. 기본은 mode별 (curate=skip, rebuild/retime=all).")

    # --with-* overrides
    p.add_argument("--with-search", action="store_true",
                   help="search_papers.py 실행 (자동 매핑 override).")
    p.add_argument("--no-search", action="store_true",
                   help="--source web 이어도 search_papers 스킵.")
    p.add_argument("--with-register", action="store_true")
    p.add_argument("--no-register", action="store_true")
    p.add_argument("--with-sync", action="store_true")
    p.add_argument("--no-sync", action="store_true")

    # Aux
    p.add_argument("--days", type=int, default=7, help="search_papers 검색 기간.")
    p.add_argument("--max-papers", type=int, default=20)
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--slugs", default="", help="특정 슬러그만 force-rebuild.")
    p.add_argument("--strict-pdf", action="store_true",
                   help="fuzzy PDF 매칭 차단 (ID-first 실패 시 skip).")
    p.add_argument("--also-reclassify", action="store_true",
                   help="curate 중 기존 논문까지 재분류.")
    p.add_argument("--skip-dedup", action="store_true",
                   help="Zotero dedup preflight 스킵.")
    p.add_argument("--dedup-execute", action="store_true",
                   help="preflight가 dry-run 대신 실제 삭제까지 수행.")
    p.add_argument("--dry-run", action="store_true",
                   help="실행 계획만 출력, 실제 호출 없음.")
    p.add_argument("--yes", action="store_true",
                   help="--mode rebuild 파괴적 확인 프롬프트 생략.")
    p.add_argument("--no-validate", action="store_true",
                   help="curate/rebuild 후 validate_papers --strict --fix 자동 호출 비활성.")

    return p


def resolve_source_routing(args):
    """Translate --source (+ --with-* overrides) into concrete booleans."""
    # Auto defaults per source
    if args.source == "web":
        auto = {"search": True, "register": True, "sync": True}
    else:  # zotero
        auto = {"search": False, "register": False, "sync": True}

    # --with-* or --no-* explicit overrides
    for k in ("search", "register", "sync"):
        if getattr(args, f"with_{k}"):
            auto[k] = True
        if getattr(args, f"no_{k}"):
            auto[k] = False

    # retime/reclassify/deploy 는 검색·등록·sync 모두 무의미
    if args.mode in ("retime", "reclassify", "deploy"):
        if args.mode == "deploy":
            auto = {"search": False, "register": False, "sync": False}
        elif not any(getattr(args, f"with_{k}") for k in ("search", "register", "sync")):
            # 명시적 --with-* 없으면 스킵
            auto = {"search": False, "register": False, "sync": False}
    return auto


def resolve_images_default(args):
    if args.images is not None:
        return args.images
    return {
        "curate": "skip",
        "rebuild": "all",
        "reclassify": "changed",
        "retime": "all",
        "deploy": "skip",
    }[args.mode]


def build_update_force_cmd(args, images):
    """run_update_force 호출 명령 조립. 기존 스크립트의 legacy flags 를 사용."""
    cmd = [sys.executable, "-u", str(PIPELINE / "run_update_force.py"),
           "--topic", args.topic,
           "--concurrency", str(args.concurrency)]
    # Map our 3-axis to run_update_force's --mode
    if args.mode in ("curate", "rebuild", "reclassify", "retime"):
        cmd.extend(["--mode", args.mode])
    if args.strict_pdf:
        cmd.append("--strict-pdf")
    if args.slugs:
        cmd.extend(["--slugs", args.slugs])
    if args.also_reclassify:
        cmd.append("--category")
    if images in ("changed", "all"):
        cmd.append("--timeline")
    if args.skip_dedup:
        cmd.append("--skip-dedup")
    if args.dedup_execute:
        cmd.append("--dedup-execute")
    if args.dry_run:
        cmd.append("--dry-run")
    return cmd


def confirm_rebuild(args):
    if args.mode != "rebuild" or args.yes or args.dry_run or args.slugs:
        return True
    print("\n** WARNING ** --mode rebuild 는 전체 review.md 를 재생성합니다 (수 시간 소요, API 비용 발생).")
    print("  --slugs 로 범위를 제한하거나, --yes 로 진행하세요.")
    return False


def build_tool_plan(args):
    """Standalone tooling modes dispatch to single scripts; no full pipeline."""
    py = sys.executable
    if args.mode == "audit":
        return [([py, "-u", str(PIPELINE / "audit_matching.py"),
                  "--topic", args.topic], None)]
    if args.mode == "fix-matching":
        cmd = [py, "-u", str(PIPELINE / "fix_matching.py"),
               "--topic", args.topic]
        if args.yes:          # --yes → --execute (destructive)
            cmd.append("--execute")
        if args.slugs:
            cmd.extend(["--slugs", args.slugs])
        return [(cmd, None)]
    if args.mode == "dedup":
        cmd = [py, "-u", str(PIPELINE / "dedup_zotero.py"),
               "--topic", args.topic]
        if args.yes:          # --yes → --execute
            cmd.append("--execute")
        return [(cmd, None)]
    if args.mode == "validate":
        cmd = [py, "-u", str(PIPELINE / "validate_papers.py"),
               "--topic", args.topic]
        if args.yes or args.strict_pdf:
            # Reuse --yes as strict-gate flag for validate
            cmd.append("--strict")
        return [(cmd, None)]
    return None


def main():
    args = build_parser().parse_args()
    # Standalone tooling modes (audit / fix-matching / dedup / validate)
    tool_plan = build_tool_plan(args)
    if tool_plan is not None:
        plan = tool_plan
        images = None
        routing = {"search": False, "register": False, "sync": False}
    else:
        routing = resolve_source_routing(args)
        images = resolve_images_default(args)

        plan = []
        if routing["search"]:
            plan.append(([sys.executable, "-u", str(PIPELINE / "search_papers.py"),
                          "--topic", args.topic,
                          "--days", str(args.days),
                          "--max-papers", str(args.max_papers)], None))
        if routing["register"]:
            plan.append(([sys.executable, "-u", str(PIPELINE / "register_zotero.py"),
                          "--topic", args.topic], None))
        if routing["sync"]:
            plan.append(([sys.executable, "-u", str(PIPELINE / "sync_zotero.py"),
                          "--topic", args.topic], None))

        if args.mode == "deploy":
            plan.append(([sys.executable, "-u", str(PIPELINE / "prepare_deploy.py"),
                          "--topic", args.topic, "--push"], None))
        else:
            plan.append((build_update_force_cmd(args, images), None))

        # Post-pipeline validation gate: ensures figure refs / links / format
        # issues introduced by LLM steps don't ship. Auto-repairs in --fix mode
        # then fails build (--strict) if anything remains.
        if args.mode in ("curate", "rebuild") and not args.no_validate:
            plan.append(([sys.executable, "-u", str(PIPELINE / "validate_papers.py"),
                          "--topic", args.topic, "--fix", "--strict"], None))

    # Print plan summary
    print(f"[run_full] topic={args.topic} mode={args.mode} source={args.source} images={images}")
    print(f"[run_full] routing: search={routing['search']} register={routing['register']} sync={routing['sync']}")
    print(f"[run_full] {len(plan)} step(s) to execute")
    for i, (cmd, _) in enumerate(plan, 1):
        print(f"  {i}. {' '.join(str(c) for c in cmd)}")

    if args.dry_run:
        print("\n[dry-run] exiting without execution")
        return

    if not confirm_rebuild(args):
        sys.exit(2)

    # Mark this run so next Claude session can detect unclean shutdown
    # (e.g. Windows update reboot mid-run). Cleared at successful end.
    mark_running(
        mode=args.mode, topic=args.topic,
        command=" ".join(sys.argv),
        extra={"source": args.source, "images": images,
                "slugs": args.slugs or None},
    )

    # Execute
    try:
        for i, (cmd, timeout) in enumerate(plan, 1):
            rc = run(cmd, timeout=timeout)
            if rc != 0:
                print(f"\n[run_full] step {i} failed with exit {rc} — aborting")
                sys.exit(rc)
    finally:
        mark_finished()

    print(f"\n[run_full] done.")


if __name__ == "__main__":
    main()
