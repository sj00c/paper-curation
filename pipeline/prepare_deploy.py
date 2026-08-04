"""
배포 준비: PNG→WebP 변환 + API key strip + Cloudflare/gh-pages 배포.

아키텍처:
  - **로컬 docs/**: wrangler 배포 소스 (풀 콘텐츠)
  - **Cloudflare Workers**: `wrangler deploy` 로 직접 업로드. 실제 사용자
    콘텐츠. docs/.assetsignore 로 ai4s/scisci 등 로컬 전용 토픽 제외.
  - **GitHub gh-pages 브랜치**: 작은 리다이렉트 스텁만. github.io 에 접근한
    사용자를 Cloudflare 로 리다이렉트.
  - **GitHub master 브랜치**: 코드 + 설정만. docs/ 내 대용량 콘텐츠는
    .gitignore 로 제외.

Usage:
  PYTHONUTF8=1 python prepare_deploy.py --topic ai4s
  PYTHONUTF8=1 python prepare_deploy.py --topic ai4s --quality 90    # WebP 품질 (기본 90)
  PYTHONUTF8=1 python prepare_deploy.py --topic ai4s --dry-run       # 변환 없이 크기 예상만
  PYTHONUTF8=1 python prepare_deploy.py --topic ai4s --push          # WebP 변환 + wrangler deploy + gh-pages 스텁 + master push

환경변수 (--push 시 필수):
  CLOUDFLARE_API_TOKEN (or CF_API_TOKEN) : Cloudflare Pages:Edit 권한
  CLOUDFLARE_ACCOUNT_ID                   : 계정 ID

단계:
  1. papers/*/figures/*.png → *.webp 변환 (quality 90)
  2. papers/*/index.html, review.md에서 .png → .webp 경로 업데이트
  3. {topic}/index.html에서 figure .png → .webp 업데이트 (타임라인 PNG는 유지)
  4. 원본 PNG 삭제 (WebP 검증된 것만)
  5. HTML 에서 API key 제거 (로컬 working tree 는 나중에 복원)
  6. (--push) `wrangler deploy` 로 Cloudflare 업로드
  7. (--push) gh-pages 브랜치에 리다이렉트 스텁 idempotent 동기화
  8. (--push) Cloudflare 엔드포인트 200 OK 검증
  9. (--push) master 에 코드/설정 변경만 commit + push (대용량 콘텐츠는 gitignored)
  10. 로컬 HTML 의 API key 복원
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from config_loader import get_github_branch, PAPERS_DIR as _PAPERS_DIR, DOCS_DIR, PROJECT_ROOT, get_topic_dir, load_config
PAPERS_DIR = str(_PAPERS_DIR)
REPO = str(PROJECT_ROOT)
from lib.secret_patterns import (
    find_local_emails,
    find_secrets,
    redact,
    reinject_key_slot,
    strip_key_slots,
    strip_local_emails,
)

# 배포되는 텍스트 자산 확장자. wrangler 는 `docs/` 아래를 통째로 올리므로
# leak 검사는 index.html 만이 아니라 이 전부를 봐야 한다.
_SCANNED_SUFFIXES = frozenset({".html", ".json", ".js", ".xml", ".txt", ".md"})


def _assetsignore_rules(docs_dir):
    """`docs/.assetsignore` 를 읽어 (패턴, 디렉터리여부) 목록으로."""
    path = Path(docs_dir) / ".assetsignore"
    rules = []
    if not path.exists():
        return rules
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        rules.append((line.rstrip("/"), line.endswith("/")))
    return rules


def _segments_match(path_parts, pattern_parts):
    """세그먼트 단위 glob. `fnmatch` 를 통짜 경로에 쓰면 `*` 가 `/` 를 넘어
    `papers/*/citedby` 가 `papers/a/b/citedby` 까지 먹는다 — 검사 범위를
    넓히는 게 아니라 **좁히는** 방향의 오류라 위험하다."""
    import fnmatch
    if len(path_parts) != len(pattern_parts):
        return False
    return all(fnmatch.fnmatch(a, b) for a, b in zip(path_parts, pattern_parts))


def _is_ignored(rel_posix, rules):
    """wrangler 가 이 상대경로를 업로드에서 뺐는지.

    파일 자신뿐 아니라 모든 상위 경로를 대조한다. `papers/*/citedby/` 같은
    디렉터리 규칙은 그 아래 전부를 제외하기 때문이다.
    """
    parts = rel_posix.split("/")
    prefixes = [parts[:i] for i in range(1, len(parts) + 1)]
    for pattern, _dir_only in rules:
        if pattern.startswith("**/"):
            tail = pattern[3:].split("/")
            if any(_segments_match(p[-len(tail):], tail) for p in prefixes
                   if len(p) >= len(tail)):
                return True
            continue
        pat_parts = pattern.split("/")
        if any(_segments_match(p, pat_parts) for p in prefixes):
            return True
    return False


def _scannable_files(docs_dir):
    """**wrangler 가 실제로 올리는** 텍스트 파일 전부.

    `.assetsignore` 를 존중하는 이유는 편의가 아니라 정확성이다. 업로드되지
    않는 로컬 캐시(`_local_keys.json` 은 이름 그대로 키를 담는다)에서 오탐이
    나면 배포가 영구 abort 되고, 그럼 운영자가 안전망을 꺼 버린다. wrangler
    와 **같은 파일**을 읽으므로 검사 범위와 업로드 범위가 어긋날 수 없다.

    strip 은 이 필터와 무관하게 모든 .html 에 걸린다 — 지운 뒤 복원하므로
    로컬에 손해가 없고, 범위를 좁히다 실수할 이유가 없다.
    """
    docs_dir = Path(docs_dir)
    rules = _assetsignore_rules(docs_dir)
    out = []
    for p in docs_dir.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in _SCANNED_SUFFIXES:
            continue
        if _is_ignored(p.relative_to(docs_dir).as_posix(), rules):
            continue
        out.append(p)
    return sorted(out)


def ensure_gitignore():
    """text.md를 .gitignore에 추가."""
    gi_path = os.path.join(REPO, ".gitignore")
    existing = ""
    if os.path.exists(gi_path):
        with open(gi_path, "r", encoding="utf-8") as f:
            existing = f.read()

    additions = []
    for pattern in ["papers/*/text.md", "__pycache__/", "_update_force_checkpoint.json",
                     "_regen_*.py", "_update_force.log"]:
        if pattern not in existing:
            additions.append(pattern)

    if additions:
        with open(gi_path, "a", encoding="utf-8") as f:
            f.write("\n# Auto-generated by prepare_deploy.py\n")
            for p in additions:
                f.write(f"{p}\n")
        print(f"  .gitignore: added {len(additions)} patterns")
    else:
        print("  .gitignore: already up to date")


MIN_VALID_WEBP_BYTES = 200  # anything smaller is almost certainly corrupt


def convert_png_to_webp(png_path, quality=90):
    """PNG → WebP 변환. 성공 시 (원본크기, 변환크기, webp_path) 반환.

    실패하거나 손상된 WebP (너무 작음)의 경우 dangling webp 파일을
    정리하고 None 을 반환해, 뒤따르는 Step 5 의 PNG 삭제 로직이
    원본을 실수로 지우지 않도록 한다."""
    webp_path = png_path.replace(".png", ".webp")
    try:
        from PIL import Image
        img = Image.open(png_path)
        img.save(webp_path, "WEBP", quality=quality)
        orig_size = os.path.getsize(png_path)
        webp_size = os.path.getsize(webp_path)
        if webp_size < MIN_VALID_WEBP_BYTES:
            raise RuntimeError(
                f"WebP output too small ({webp_size} bytes, likely corrupt)")
        return orig_size, webp_size, webp_path
    except Exception as e:
        print(f"  ERR: {png_path}: {e}")
        # Clean up any partial/corrupt webp file so Step 5 does not
        # treat it as a successful conversion and delete the PNG.
        if os.path.exists(webp_path):
            try:
                os.remove(webp_path)
            except Exception as cleanup_err:
                print(f"    (failed to clean dangling webp: {cleanup_err})")
        return 0, 0, None


def update_html_refs(file_path, fig_only=False):
    """HTML/MD 파일에서 figure .png → .webp 참조 업데이트."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if fig_only:
        # 타임라인 PNG는 유지, figure 참조만 변환
        new_content = re.sub(r'(figures/[^"\']+)\.png', r'\1.webp', content)
    else:
        # 모든 .png → .webp (review.md, papers/*/index.html)
        new_content = re.sub(r'(figures/[^)\s"\']+)\.png', r'\1.webp', content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


CF_BASE_URL = "https://paper-curation.jehyunlee.dev"
CF_PROBE_PATHS = ("/", "/humanoid/", "/physical-ai/", "/index.html")


def _verify_cloudflare(topic, timeout_s=300, interval_s=15):
    """Poll Cloudflare Worker endpoints until they all return 200 or timeout.

    We can't read a commit hash from response headers (Workers Static Assets
    don't expose one), so we only verify reachability + content size sanity.
    """
    import time as _time
    import urllib.request as _ur
    import urllib.error as _ue
    print(f"\n  [cf-verify] polling Cloudflare for ≤{timeout_s}s …")
    deadline = _time.time() + timeout_s
    last_status = {}
    while _time.time() < deadline:
        all_ok = True
        for path in CF_PROBE_PATHS:
            url = CF_BASE_URL + path
            try:
                req = _ur.Request(url, method="HEAD",
                                   headers={"User-Agent": "paper-curation/cf-verify"})
                resp = _ur.urlopen(req, timeout=10)
                code = resp.status
                size = resp.headers.get("content-length", "?")
                last_status[path] = (code, size)
                if code != 200:
                    all_ok = False
            except _ue.HTTPError as e:
                last_status[path] = (e.code, "?")
                all_ok = False
            except Exception as e:
                last_status[path] = ("err", str(e)[:60])
                all_ok = False
        if all_ok:
            print(f"  [cf-verify] all {len(CF_PROBE_PATHS)} endpoints 200 OK")
            for p, (c, s) in last_status.items():
                print(f"    {p}: {c} ({s} bytes)")
            return True
        _time.sleep(interval_s)
    print(f"  [cf-verify] TIMEOUT after {timeout_s}s — last status:")
    for p, (c, s) in last_status.items():
        print(f"    {p}: {c} ({s})")
    return False


_STUB_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={cf_url}/{topic}/">
<title>{title} — Paper Curation</title>
<script>window.location.replace("{cf_url}/{topic}/");</script>
</head>
<body>
<p>Redirecting to <a href="{cf_url}/{topic}/">{title} — Paper Curation</a>...</p>
</body>
</html>
"""

_TOPIC_TITLES = {
    "humanoid": "Humanoid",
    "physical-ai": "Physical AI",
    "ai4s": "AI for Science",
    "scisci": "Science of Science",
}


def _discover_deployable_topics():
    """Scan docs/ for topic dirs deployed to Cloudflare (index.html present,
    not in .assetsignore, not the shared 'papers' repo)."""
    docs = str(DOCS_DIR)
    assetsignore = os.path.join(docs, ".assetsignore")
    excluded = {"papers", "notes"}
    if os.path.exists(assetsignore):
        with open(assetsignore, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip().rstrip("/")
                if line and not line.startswith("#") and "/" not in line:
                    excluded.add(line)
    topics = []
    for entry in os.listdir(docs):
        if entry.startswith(("_", ".")) or entry in excluded:
            continue
        full = os.path.join(docs, entry)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "index.html")):
            topics.append(entry)
    return sorted(topics)


_PREFLIGHT_MIN_BYTES = 100_000  # topic index < this = likely stub/broken


def _preflight_topics(topics=None, min_size=_PREFLIGHT_MIN_BYTES):
    """Abort before wrangler deploy if any topic's index.html is missing or
    suspiciously small (e.g. redirect stub ~500 bytes, partial regen failure).

    We had an incident where a deploy went out with the topic dirs missing
    because a stale working tree was deployed — this guard stops that
    class of error. The threshold is deliberately loose (100 KB); real
    topic indices are multi-MB.
    """
    docs = str(DOCS_DIR)
    topics = topics or _discover_deployable_topics()
    if not topics:
        print("  [preflight] no deployable topics discovered (nothing to guard)")
        return
    problems, ok_sizes = [], []
    for t in topics:
        path = os.path.join(docs, t, "index.html")
        if not os.path.isfile(path):
            problems.append(f"{t}: index.html missing")
            continue
        size = os.path.getsize(path)
        if size < min_size:
            problems.append(f"{t}: index.html only {size:,} bytes "
                            f"(< {min_size:,} threshold; likely stub)")
        else:
            ok_sizes.append((t, size))
    if problems:
        print("\n  [preflight] ABORT — deployable topics look broken:")
        for p in problems:
            print(f"    - {p}")
        print("\n  Fix: regenerate topic indices before redeploying, e.g.")
        print("       PYTHONUTF8=1 python pipeline/build_topic_index.py <topic>")
        raise SystemExit("Refusing to deploy: preflight failed")
    print("  [preflight] deployable topics OK:")
    for t, sz in ok_sizes:
        print(f"    - {t}: {sz / 1024:.0f} KB")


def _search_index_freshness(topic):
    """Return fingerprint-based freshness evidence for one topic index.

    Existing indexes without a fingerprint are reported as unknown (warning,
    not a false-positive deploy block). The next normal rebuild establishes the
    baseline; subsequent source changes are blocked until rebuilt.
    """
    topic_dir = Path(DOCS_DIR) / topic
    index_path = topic_dir / "_search_index.json"
    if not index_path.exists():
        return {"topic": topic, "fresh": False, "reason": "index JSON missing"}
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"topic": topic, "fresh": False, "reason": f"invalid index JSON: {exc}"}

    emb_name = index.get("emb_file") or "_search_index_emb.bin"
    emb_path = topic_dir / emb_name
    if not emb_path.exists():
        return {"topic": topic, "fresh": False, "reason": f"embedding sidecar missing: {emb_name}"}

    expected = index.get("source_fingerprint")
    if not expected:
        return {
            "topic": topic,
            "fresh": None,
            "reason": "index predates source fingerprint; rebuild recommended",
        }

    from build_search_index import source_fingerprint
    actual, source_count = source_fingerprint(
        topic, (index.get("papers") or {}).keys(),
        docs_dir=DOCS_DIR, papers_dir=PAPERS_DIR)
    fresh = actual == expected
    return {
        "topic": topic,
        "fresh": fresh,
        "reason": "" if fresh else "indexed source files changed after build",
        "source_file_count": source_count,
    }


def _preflight_search_indexes(topics=None):
    """Abort a public deploy when a deployable topic's RAG index is stale."""
    topics = topics or _discover_deployable_topics()
    results = [_search_index_freshness(t) for t in topics]
    stale = [r for r in results if r["fresh"] is False]
    if stale:
        print("\n  [preflight] ABORT — search index missing or stale:")
        for result in stale:
            print(f"    - {result['topic']}: {result['reason']}")
        print("\n  Fix: rebuild each affected index before deploying:")
        print("       PYTHONUTF8=1 python pipeline/build_search_index.py --topic <topic>")
        raise SystemExit("Refusing to deploy: stale search index")
    unknown = [r for r in results if r["fresh"] is None]
    for result in unknown:
        print(f"  [preflight] WARNING — {result['topic']}: {result['reason']}")
    fresh = [r["topic"] for r in results if r["fresh"] is True]
    if fresh:
        print("  [preflight] search indexes fresh: " + ", ".join(fresh))


def _wrangler_env():
    """Build env for wrangler subprocess — accepts CF_API_TOKEN or
    CLOUDFLARE_API_TOKEN, maps the former to the latter for wrangler."""
    env = os.environ.copy()
    if "CLOUDFLARE_API_TOKEN" not in env and "CF_API_TOKEN" in env:
        env["CLOUDFLARE_API_TOKEN"] = env["CF_API_TOKEN"]
    missing = [k for k in ("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID") if not env.get(k)]
    if missing:
        raise SystemExit(
            f"Missing env vars for wrangler: {', '.join(missing)}. "
            f"Set CF_API_TOKEN (or CLOUDFLARE_API_TOKEN) and CLOUDFLARE_ACCOUNT_ID."
        )
    return env


def _wrangler_deploy():
    """Run `npx wrangler deploy` from the repo root. Raises on failure.

    Windows note: Python's CreateProcess won't locate `npx` without the
    `.cmd` extension, so we resolve the real executable via shutil.which.
    """
    import shutil as _sh
    env = _wrangler_env()
    npx = _sh.which("npx") or _sh.which("npx.cmd") or "npx"
    print(f"\n  [wrangler] {npx} wrangler deploy ...")
    result = subprocess.run(
        [npx, "wrangler", "deploy"],
        cwd=REPO, env=env,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.stdout:
        # Print last 15 lines for signal (upload summary, deploy URL)
        tail = "\n".join(result.stdout.splitlines()[-15:])
        print(f"  [wrangler stdout tail]\n{tail}")
    if result.returncode != 0:
        print(f"  [wrangler stderr]\n{result.stderr}")
        raise SystemExit(f"wrangler deploy failed with exit {result.returncode}")


def _sync_gh_pages_stubs(topics, cf_url=CF_BASE_URL):
    """Ensure origin/gh-pages has redirect stubs for each topic. Idempotent:
    only commits + pushes when a stub would actually change."""
    import tempfile
    print(f"\n  [gh-pages] syncing stubs for: {', '.join(topics)}")
    # Always fetch to ensure we act on the current remote state
    subprocess.run(["git", "fetch", "origin", "gh-pages"], check=True, cwd=REPO)
    worktree = tempfile.mkdtemp(prefix="paper-curation-ghpages-")
    try:
        subprocess.run(
            ["git", "worktree", "add", "--force", worktree, "gh-pages"],
            check=True, cwd=REPO,
        )
        changed = []
        for topic in topics:
            title = _TOPIC_TITLES.get(topic, topic.replace("-", " ").title())
            content = _STUB_HTML.format(cf_url=cf_url, topic=topic, title=title)
            stub_dir = os.path.join(worktree, topic)
            os.makedirs(stub_dir, exist_ok=True)
            stub_file = os.path.join(stub_dir, "index.html")
            need_write = True
            if os.path.exists(stub_file):
                with open(stub_file, "r", encoding="utf-8") as f:
                    if f.read() == content:
                        need_write = False
            if need_write:
                with open(stub_file, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
                changed.append(topic)

        # Prune orphaned stubs so the gh-pages stub set is reproducible from the
        # deployable-topics list alone: remove any top-level dir that is one of
        # OUR redirect stubs (window.location.replace -> cf_url) but is no longer
        # a deployable topic (e.g. a topic moved back to local-only).
        import shutil
        pruned = []
        topic_set = set(topics)
        for name in sorted(os.listdir(worktree)):
            d = os.path.join(worktree, name)
            if name in topic_set or not os.path.isdir(d) or name == ".git":
                continue
            idx = os.path.join(d, "index.html")
            if not os.path.exists(idx):
                continue
            try:
                with open(idx, "r", encoding="utf-8") as f:
                    body = f.read()
            except Exception:
                continue
            if "window.location.replace(" in body and cf_url in body:
                shutil.rmtree(d)
                pruned.append(name)
                print(f"  [gh-pages] pruned orphaned stub: {name}")

        if not changed and not pruned:
            print("  [gh-pages] all stubs up to date — no push needed")
            return
        subprocess.run(["git", "add", "-A"], check=True, cwd=worktree)
        summary = []
        if changed:
            summary.append("sync " + ", ".join(changed))
        if pruned:
            summary.append("prune " + ", ".join(pruned))
        msg = (
            f"gh-pages redirect stubs: {'; '.join(summary)}\n\n"
            "Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
        )
        subprocess.run(["git", "commit", "-m", msg], check=True, cwd=worktree)
        subprocess.run(["git", "push", "origin", "gh-pages"], check=True, cwd=worktree)
        print(f"  [gh-pages] pushed ({'; '.join(summary)})")
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", worktree],
            cwd=REPO, check=False,
        )


def _reinject_local_keys(docs_dir=None, *, verbose=True):
    """배포용 strip 으로 비워진 로컬 HTML 키 슬롯을 env→config 값으로 재주입한다.

    키 값은 build 와 동일한 env→config 출처에서 결정론적으로 재유도하므로, deploy
    가 (kill -9 등으로) Step 6 strip 과 finally restore 사이에서 죽어 로컬 working
    tree 가 strip 된 채 남아도 별도 백업 없이 복원된다. 배포본에는 영향이 없다 —
    strip 은 항상 wrangler deploy 직전에 다시 실행되기 때문.

    재주입 대상: _GEMINI_KEY(Audio Overview) · _ANTHROPIC_KEY · _OPENAI_KEY
    (Deep Research) · _LOCAL_EMAILS(로컬 이메일). 값이 없으면 해당 슬롯은 건너뛴다.
    반환: 실제로 수정된 파일 수.
    """
    docs_dir = Path(docs_dir or DOCS_DIR)
    try:
        cfg = load_config() or {}
    except Exception:
        cfg = {}
    gemini = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
              or cfg.get("gemini_api_key", "") or cfg.get("google_api_key", "")) or ""
    anthropic = (os.environ.get("ANTHROPIC_API_KEY") or cfg.get("anthropic_api_key", "")) or ""
    openai = (os.environ.get("OPENAI_API_KEY") or cfg.get("openai_api_key", "")) or ""
    raw_emails = (os.environ.get("PAPER_CURATION_LOCAL_EMAILS", "")
                  or ",".join(cfg.get("local_emails", []) or []))
    emails = [e.strip() for e in raw_emails.split(",") if e.strip()]
    emails_js = "[" + ", ".join(json.dumps(e) for e in emails) + "]"

    # 슬롯→값 매핑. 이 dict 와 strip 이 같은 `KEY_SLOTS` 표를 공유하므로
    # 한쪽만 바뀌어 서로 어긋날 수 없다. `_LLM_KEY` 는 페이지에서
    # `localStorage || _ANTHROPIC_KEY` 로 유도되므로 굽지 않는다.
    slot_values = {
        "_GEMINI_KEY": gemini,
        "_ANTHROPIC_KEY": anthropic,
        "_OPENAI_KEY": openai,
    }
    n = 0
    for html_path in docs_dir.rglob("*.html"):
        try:
            text = html_path.read_text(encoding="utf-8")
        except OSError:
            continue
        new = text
        for slot, value in slot_values.items():
            new, _ = reinject_key_slot(new, slot, value)
        if emails:
            new = new.replace('window._LOCAL_EMAILS = []', 'window._LOCAL_EMAILS = ' + emails_js)
        if new != text:
            html_path.write_text(new, encoding="utf-8")
            n += 1
    if verbose:
        print(f"  로컬 HTML 키 재주입: {n} 파일 (env→config)")
    return n


def _deploy_slugs(topics):
    import json
    idx = json.load(open(os.path.join(PAPERS_DIR, "_papers_index.json"), encoding="utf-8"))
    tset = set(topics or [])
    return sorted({e["slug"] for e in idx if tset & set(e.get("topics") or [])})


def _restore_full_copies(snaps):
    """Restore the full (ungated) local HTML snapshots taken before public re-render."""
    for p, data in (snaps or {}).items():
        try:
            with open(p, "wb") as f:
                f.write(data)
        except Exception as e:
            print(f"  WARN: failed to restore full local copy {p}: {e}")


def _render_public_copies(topics):
    """Snapshot full local HTML for the deploy topics, then re-render those pages
    in PUBLIC mode (PC_PUBLIC_BUILD=1) so the *uploaded* copy is license-gated
    (figure/ND/audio). The full snapshot is restored in the finally, so the LOCAL
    working tree stays fully unrestricted. Returns {path: full_bytes}."""
    topics = topics or _discover_deployable_topics()
    slugs = _deploy_slugs(topics)
    paths = [str(get_topic_dir(t) / "index.html") for t in topics]
    for s in slugs:
        paths.append(os.path.join(PAPERS_DIR, s, "index.html"))
    snaps = {}
    for p in paths:
        try:
            with open(p, "rb") as f:
                snaps[p] = f.read()
        except Exception:
            pass
    print(f"\nStep 5.9: Re-rendering {len(topics)} topic(s) + {len(slugs)} papers "
          f"in PUBLIC mode (license gating; local stays full)...")
    _pd = os.path.dirname(os.path.abspath(__file__))
    if _pd not in sys.path:
        sys.path.insert(0, _pd)
    prev = {k: os.environ.get(k) for k in ("PC_PUBLIC_BUILD", "SKIP_ZOTERO_KEYS")}
    os.environ["PC_PUBLIC_BUILD"] = "1"
    os.environ["SKIP_ZOTERO_KEYS"] = "1"
    try:
        import review_to_html as _rth
        import build_topic_index as _bti
        _rth._run_review_to_html(slugs=slugs)
        for t in topics:
            _bti._run_topic_index(t)
    except Exception:
        _restore_full_copies(snaps)
        raise
    finally:
        for k, v in prev.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return snaps


def _run_deploy(topic="ai4s", *, quality=90, dry_run=False, push=False,
                topics=None, workers=8, cf_strict=False):
    """Programmatic entrypoint for prepare_deploy."""
    topic_dir = str(get_topic_dir(topic))

    # Self-heal: 이전 deploy 가 Step 6 strip 과 finally restore 사이에서 죽으면
    # (예: kill -9) 로컬 HTML 이 키-strip 된 채 남아 Audio Overview/Deep Research 가
    # 로컬에서 깨진다. 본격 작업 전에 env→config 로 재주입해 복원한다 (이미 키가 있으면
    # no-op). 배포 직전 Step 6 가 다시 strip 하므로 배포본에는 영향 없음.
    if not dry_run:
        _healed = _reinject_local_keys(DOCS_DIR, verbose=False)
        if _healed:
            print(f"  [self-heal] 이전 배포 중단으로 비워진 로컬 키 복원: {_healed} HTML")

    print("Step 1: .gitignore")
    if not dry_run:
        ensure_gitignore()

    print("\nStep 2: Finding PNGs...")
    png_files = []
    for slug in os.listdir(PAPERS_DIR):
        fig_dir = os.path.join(PAPERS_DIR, slug, "figures")
        if not os.path.isdir(fig_dir):
            continue
        for f in os.listdir(fig_dir):
            if f.endswith(".png"):
                png_files.append(os.path.join(fig_dir, f))

    total_png_size = sum(os.path.getsize(f) for f in png_files)
    print(f"  Found {len(png_files)} PNGs ({total_png_size / 1048576:.0f} MB)")

    if dry_run:
        sample = png_files[:10]
        sample_orig = sum(os.path.getsize(f) for f in sample)
        sample_webp = 0
        for f in sample:
            orig, webp, _ = convert_png_to_webp(f, quality)
            sample_webp += webp
            wp = f.replace(".png", ".webp")
            if os.path.exists(wp):
                os.remove(wp)
        if sample_orig > 0:
            ratio = sample_webp / sample_orig
            est_total = total_png_size * ratio / 1048576
            print(f"\n  Estimated WebP size: {est_total:.0f} MB ({ratio:.0%} of original)")
            print(f"  Savings: {(total_png_size / 1048576) - est_total:.0f} MB")
        return

    print(f"\nStep 3: Converting to WebP (quality={quality})...")
    total_orig = 0
    total_webp = 0
    converted = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(convert_png_to_webp, f, quality): f for f in png_files}
        for future in futures:
            orig, webp, webp_path = future.result()
            if webp_path:
                total_orig += orig
                total_webp += webp
                converted += 1

    print(f"  Converted: {converted}/{len(png_files)}")
    print(f"  {total_orig / 1048576:.0f} MB → {total_webp / 1048576:.0f} MB "
          f"({total_webp / max(1, total_orig):.0%})")

    # Step 4: Update HTML/MD references (.png → .webp where .webp exists)
    # Always run regardless of PNG conversion count — HTML may have been
    # regenerated with .png refs after a previous PNG→WebP conversion.
    print("\nStep 4: Updating references...")
    updated = 0
    for slug in os.listdir(PAPERS_DIR):
        slug_dir = os.path.join(PAPERS_DIR, slug)
        if not os.path.isdir(slug_dir):
            continue
        # Only update if .webp figures actually exist
        fig_dir = os.path.join(slug_dir, "figures")
        has_webp = os.path.isdir(fig_dir) and any(f.endswith(".webp") for f in os.listdir(fig_dir))
        if not has_webp:
            continue
        for fname in ["index.html", "review.md"]:
            fpath = os.path.join(slug_dir, fname)
            if os.path.exists(fpath) and update_html_refs(fpath):
                updated += 1

    # Update topic index.html (figures only, keep timeline PNGs)
    topic_index = os.path.join(topic_dir, "index.html")
    if os.path.exists(topic_index) and update_html_refs(topic_index, fig_only=True):
        updated += 1

    print(f"  Updated: {updated} files")

    # Step 5: Delete original PNGs (only when WebP is verifiably good).
    # Double-defense against WebP-conversion races: we require the WebP
    # to actually exist AND to be at least MIN_VALID_WEBP_BYTES, which
    # catches cases where Pillow crashed halfway and left a tiny or
    # corrupt output. Any PNG preserved by this guard is logged so the
    # operator can investigate and retry.
    print("\nStep 5: Deleting original PNGs...")
    deleted = 0
    preserved = 0
    for png_path in png_files:
        webp_path = png_path.replace(".png", ".webp")
        if not os.path.exists(webp_path):
            preserved += 1
            print(f"  KEEP: {png_path} (no WebP)")
            continue
        webp_size = os.path.getsize(webp_path)
        if webp_size < MIN_VALID_WEBP_BYTES:
            preserved += 1
            print(f"  KEEP: {png_path} (WebP too small: {webp_size} bytes)")
            continue
        os.remove(png_path)
        deleted += 1
    print(f"  Deleted: {deleted} PNGs, Preserved: {preserved}")

    # Step 5.9: 배포 사본만 PUBLIC 모드로 재렌더(라이선스 게이팅). 로컬 full 은 finally 에서 복원.
    _full_snaps = _render_public_copies(topics) if push else {}

    # Step 6: Strip credentials from every deployed HTML (local tree restored after commit).
    #
    # Strip 은 **슬롯 이름** 으로 한다 (lib/secret_patterns). 예전 구현은 값이
    # `sk-`/`AIza` 로 시작할 때만 지웠는데, 그건 fail-open 이다 — 접두사가 다른
    # 키(사내 게이트웨이·Azure)나 `window._OPENAI_KEY = "sk-…"` 처럼 선언 형태가
    # 다른 조합을 조용히 통과시켰다. 이제 슬롯에 든 문자열 리터럴은 모양과
    # 무관하게 전부 비운다.
    #
    # 대상도 `index.html` 에서 **모든 .html** 로 넓혔다. wrangler 는 docs/ 아래를
    # 통째로 올리므로 `generate_network.py` 가 쓰는 `{topic}/network.html` 도
    # 업로드된다. 예전 루프는 그 파일을 아예 보지 않았다.
    print("\nStep 6: Stripping credentials from deployed HTML (local keys preserved)...")
    _originals = {}  # Path -> original content, restored after push
    _slots_blanked = 0
    for html_path in DOCS_DIR.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        new_text, n_keys = strip_key_slots(text)
        new_text, _ = strip_local_emails(new_text)
        _slots_blanked += n_keys
        if new_text != text:
            _originals[html_path] = text
            html_path.write_text(new_text, encoding="utf-8")

    def _restore_originals():
        for p, orig in _originals.items():
            p.write_text(orig, encoding="utf-8")

    # The working tree now holds stripped (key-less) HTML. EVERYTHING that
    # follows — leak-scans, deploy, commit — must run under this try so that
    # _restore_originals() in the finally ALWAYS runs back: any exception in
    # the leak-scan window (e.g. read_text OSError/UnicodeDecodeError, or a
    # KeyboardInterrupt during rglob) would otherwise leave the local working
    # tree with emptied keys (Deep Research / Audio Overview silently broken
    # until a rebuild). restore is idempotent, so it's the single restore site.
    try:
        # Safety net. 두 가지를 예전 구현에서 고쳤다:
        #
        # 1) **범위** — `index.html` 만 훑었다. wrangler 는 docs/ 아래 텍스트
        #    자산을 전부 올린다 (network.html, _search_index.json, RSS …).
        #    그물이 업로드 surface 보다 좁으면 안전망이 아니다.
        # 2) **패턴** — `sk-(ant|proj)-` 만 찾아, 레거시 OpenAI 키
        #    (`sk-` + 48 alnum) 는 stripper 는 지우는데 검사는 못 보는
        #    비대칭이 있었다. 이제 lib/secret_patterns 의 단일 표를 쓰므로
        #    검사는 정의상 stripper 의 상위집합이다.
        _scan_targets = _scannable_files(DOCS_DIR)
        _leaks = []       # (path, 패턴 이름, 축약값)
        _email_leaks = []
        for p in _scan_targets:
            try:
                body = p.read_text(encoding="utf-8", errors="ignore")
            except OSError as e:
                print(f"  ABORT: 배포 자산을 읽지 못해 검사할 수 없습니다: {p} ({e})")
                sys.exit(1)
            for name, value in find_secrets(body):
                _leaks.append((str(p), name, redact(value)))
            if find_local_emails(body):
                _email_leaks.append(str(p))

        if _leaks:
            _files = {path for path, _, _ in _leaks}
            print(f"  ABORT: 자격증명이 배포 자산 {len(_files)}개 파일에 남아 있습니다 — 커밋/업로드 거부:")
            for path, name, shown in _leaks[:20]:
                print(f"    - {path}: {name} ({shown})")
            if len(_leaks) > 20:
                print(f"    … and {len(_leaks) - 20} more")
            sys.exit(1)
        if _email_leaks:
            print(f"  ABORT: _LOCAL_EMAILS still populated in {len(_email_leaks)} files — refusing to commit:")
            for p in _email_leaks:
                print(f"    - {p}")
            sys.exit(1)
        print(f"  Stripped {_slots_blanked} key slots in {len(_originals)} files; "
              f"scanned {len(_scan_targets)} deploy assets (0 leaks)")

        # Step 7-10: Deploy (only if --push). Otherwise we stop here — the
        # working tree was modified by API-key strip in Step 6 so we still
        # need to restore it in the finally block.
        if not push:
            print("\n(--push 없이 실행됨. Cloudflare 업로드/gh-pages 동기화/master push 모두 스킵)")
        else:
            # Step 7: Upload full content to Cloudflare via wrangler
            print("\nStep 7: Deploying to Cloudflare (wrangler deploy)...")
            print("  [preflight] verifying topic indices before upload")
            _preflight_search_indexes(topics)
            _preflight_topics(topics)
            _wrangler_deploy()

            # Step 8: Ensure gh-pages has redirect stubs for every deployed topic
            topics_for_stubs = topics or _discover_deployable_topics()
            if topics_for_stubs:
                print(f"\nStep 8: Syncing gh-pages redirect stubs "
                      f"({len(topics_for_stubs)} topics)...")
                _sync_gh_pages_stubs(topics_for_stubs)
            else:
                print("\nStep 8: No deployable topics found — skipping gh-pages sync")

            # Step 9: Verify Cloudflare endpoints return 200.
            # Bind the result — a failed/timed-out deploy must NOT be recorded
            # as a clean "Deploy:" commit on master. cf_strict 면 hard abort,
            # 기본은 warn-only (느린 CF propagation 이 300s 를 넘기는 경우를 위해
            # master push 만 건너뛰고 로컬 복원은 finally 가 처리).
            print("\nStep 9: Verifying Cloudflare endpoints...")
            cf_ok = _verify_cloudflare(topic)
            if not cf_ok:
                if cf_strict:
                    print("  ABORT: Cloudflare verification failed/timed out "
                          "(--cf-strict) — refusing to commit master")
                    sys.exit(1)
                print("  WARN: Cloudflare verification failed/timed out — "
                      "skipping master commit/push (deploy NOT recorded as clean)")

            # Step 10: Commit + push master — only code/config changes.
            # docs/* content is gitignored, so this only captures genuine
            # source changes (pipeline scripts, wrangler.toml, etc.).
            # Gated on cf_ok: a broken deploy is never committed as success.
            if not cf_ok:
                print("\nStep 10: Skipped (Cloudflare verification failed)")
                return
            print("\nStep 10: Committing code/config changes to master...")
            os.chdir(REPO)
            subprocess.run(["git", "add", "-A"], check=True)
            staged = subprocess.run(
                ["git", "diff", "--cached", "--quiet"], capture_output=True,
            )
            if staged.returncode == 0:
                print("  No master-tracked changes to commit")
            else:
                name_status = subprocess.run(
                    ["git", "diff", "--cached", "--name-status"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                )
                ns_lines = [l for l in (name_status.stdout or "").splitlines() if l.strip()]
                print(f"  Master-tracked diff: {len(ns_lines)} files")
                for l in ns_lines[:15]:
                    print(f"    {l}")
                if len(ns_lines) > 15:
                    print(f"    ... +{len(ns_lines) - 15} more")
                subprocess.run(
                    ["git", "commit", "-m",
                     f"Deploy: {converted} figures WebP, "
                     f"{total_orig // 1048576}→{total_webp // 1048576}MB\n\n"
                     f"Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"],
                    check=True,
                )
                subprocess.run(["git", "push", "origin", "master"], check=True)
                print("  Pushed code/config changes to master")
    finally:
        # Restore local working tree so Deep Research UI keeps working without rebuild
        _restore_originals()
        if _originals:
            print(f"  Restored {len(_originals)} local HTML files (API keys preserved for local dev)")
        _restore_full_copies(_full_snaps)
        if _full_snaps:
            print(f"  Restored {len(_full_snaps)} local HTML files to full (ungated) view")

    print(f"\nDone! Total savings: {(total_orig - total_webp) / 1048576:.0f} MB")


def main():
    parser = argparse.ArgumentParser(description="Prepare for GitHub Pages deployment")
    parser.add_argument("--topic", default="", help="대상 토픽 (생략 시 설정된 토픽이 하나면 그것)")
    parser.add_argument("--quality", type=int, default=90, help="WebP quality (1-100)")
    parser.add_argument("--dry-run", action="store_true", help="Estimate only, no conversion")
    parser.add_argument("--push", action="store_true", help="Git add + commit + push after conversion")
    parser.add_argument("--topics", nargs="+", help="Only deploy these topics (exclude others from git add)")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers for conversion")
    parser.add_argument("--cf-strict", action="store_true",
                        help="Abort (no master commit/push) if Cloudflare 200-OK verification fails/times out")
    parser.add_argument("--restore-keys", action="store_true",
                        help="strip 으로 비워진 로컬 HTML 키 슬롯을 env→config 로 재주입하고 종료 (배포 중단 복구 도구)")
    args = parser.parse_args()
    from config_loader import resolve_topic
    args.topic = resolve_topic(args.topic, script="prepare_deploy")
    if args.restore_keys:
        _reinject_local_keys(DOCS_DIR)
        return
    _run_deploy(topic=args.topic, quality=args.quality, dry_run=args.dry_run,
                push=args.push, topics=args.topics, workers=args.workers,
                cf_strict=args.cf_strict)


if __name__ == "__main__":
    main()
