"""
Zotero 컬렉션과 _papers_index.json 간 동기화.

기능:
  1. 삭제 감지: Zotero에서 제거된 논문 → index에서도 제거
  2. 제목 변경 감지: Zotero에서 제목이 바뀐 논문 → index 제목 업데이트
  3. 매칭: DOI 우선, 제목 퍼지 매칭 폴백

Usage:
  PYTHONUTF8=1 python sync_zotero.py --topic my-topic
  PYTHONUTF8=1 python sync_zotero.py --topic my-topic --dry-run
"""

import argparse
import json
import os
import re
import shutil
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

from lib.zotero_bounded import UrllibZoteroTransport, ZoteroBoundedReader

from config_loader import PAPERS_DIR as _PAPERS_DIR
PAPERS_DIR = str(_PAPERS_DIR)

from config_loader import get_zotero_api_key, get_zotero_user_id, get_collections, _ssl_ctx

API_KEY = get_zotero_api_key()
USER_ID = get_zotero_user_id()
COLLECTIONS = get_collections()


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def _safe_slug_dir(root, slug):
    root = Path(root).resolve()
    if (
        not isinstance(slug, str)
        or not slug
        or slug in {".", ".."}
        or "/" in slug
        or "\\" in slug
        or "\x00" in slug
    ):
        raise RuntimeError("unsafe paper slug in index; refusing deletion")
    candidate = root / slug
    if candidate.resolve(strict=False).parent != root or candidate.is_symlink():
        raise RuntimeError("paper path escapes or aliases the papers root; refusing deletion")
    return candidate

def _atomic_write_json(path, value):
    path = Path(path)
    parent = path.parent.resolve(strict=True)
    if path.is_symlink():
        raise RuntimeError("index path is a symlink; refusing update")
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = parent / f".{path.name}.{os.getpid()}.tmp"
    descriptor = None
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
def normalize_title(title):
    """제목 정규화: 소문자, 비알파벳 제거, 앞 50자."""
    return re.sub(r"[^a-z0-9]", "", title.lower())[:50]


def normalize_doi(doi):
    """DOI 정규화: 소문자, 앞뒤 공백 제거. arXiv: prefix 포함."""
    if not doi:
        return ""
    doi = doi.strip().lower()
    # Remove URL prefix
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi


def fetch_zotero_items(collection_key):
    """Return a complete, version-pinned, deterministically ordered collection snapshot."""
    reader = ZoteroBoundedReader(
        UrllibZoteroTransport(_ssl_ctx), API_KEY, USER_ID,
    )
    items = []
    for item in reader.collection_items(collection_key):
        d = item["data"]
        if d.get("itemType") in ("attachment", "note", "forumPost", "videoRecording"):
            continue
        title = d.get("title", "").strip()
        doi = normalize_doi(d.get("DOI", ""))
        arxiv_id = ""
        archive_id = d.get("archiveID", "")
        url_field = d.get("url", "")
        if "arXiv:" in archive_id:
            arxiv_id = archive_id.split("arXiv:")[-1]
        elif "arxiv.org/abs/" in url_field:
            arxiv_id = url_field.split("arxiv.org/abs/")[-1].split("v")[0]
        items.append({
            "key": d["key"],
            "title": title,
            "title_norm": normalize_title(title),
            "doi": doi,
            "arxiv_id": arxiv_id,
        })
    return items


def match_paper(index_paper, zotero_items, zotero_doi_map, zotero_title_map):
    """Index 논문을 Zotero 아이템과 매칭. 매칭된 Zotero 아이템 반환, 없으면 None."""
    # 1차: DOI 매칭
    idx_doi = normalize_doi(index_paper.get("doi", ""))
    if idx_doi and idx_doi in zotero_doi_map:
        return zotero_doi_map[idx_doi]

    # 2차: arXiv ID 매칭 (doi 필드에 arXiv: 형태로 저장된 경우)
    idx_doi_raw = index_paper.get("doi", "")
    if idx_doi_raw.startswith("arXiv:"):
        arxiv_id = idx_doi_raw.split("arXiv:")[-1]
        for zi in zotero_items:
            if zi.get("arxiv_id") == arxiv_id:
                return zi

    # 3차: 제목 정규화 매칭
    idx_title_norm = normalize_title(index_paper.get("title", ""))
    if idx_title_norm and idx_title_norm in zotero_title_map:
        return zotero_title_map[idx_title_norm]

    # 4차: 제목 앞 25자 퍼지 매칭 (제목이 약간 바뀐 경우)
    idx_short = idx_title_norm[:25]
    if len(idx_short) > 15:
        for zi in zotero_items:
            if zi["title_norm"][:25] == idx_short:
                return zi

    return None


# 삭제 안전 가드 임계값.
#   - 빈 fetch: 토픽 논문이 있는데 Zotero 가 0건을 돌려주면 (transient 200-empty 등)
#     모든 단일-토픽 논문 디렉토리가 rmtree 대상이 되므로 무조건 차단.
#   - 비율: 한 사이클에 토픽 논문의 이 비율 이상이 삭제 대상이면 (정상 주간 churn 이
#     아니라 fetch 결함일 가능성) 차단. --force-delete 로 우회.
_DELETE_RATIO_THRESHOLD = 0.30


def _run_sync(topic, *, dry_run=False, force_delete=False):
    """Programmatic entrypoint for sync_zotero."""
    if force_delete:
        raise ValueError("force-delete bypass is unsupported; reconcile the Zotero snapshot first")
    collection_key = COLLECTIONS.get(topic)
    if not collection_key:
        print(f"Unknown topic: {topic}")
        return

    index_path = os.path.join(PAPERS_DIR, "_papers_index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            papers = json.load(f)
    else:
        os.makedirs(PAPERS_DIR, exist_ok=True)
        papers = []
        log("Index not found — treating this as the first pipeline run.")

    # Fetch Zotero
    log(f"Fetching Zotero collection '{topic}' ({collection_key})...")
    zotero_items = fetch_zotero_items(collection_key)
    log(f"Zotero: {len(zotero_items)} papers")

    # Build lookup maps
    zotero_doi_map = {}
    zotero_title_map = {}
    for zi in zotero_items:
        if zi["doi"]:
            zotero_doi_map[zi["doi"]] = zi
        if zi["title_norm"]:
            zotero_title_map[zi["title_norm"]] = zi

    # Find papers in index with this topic
    topic_papers = [p for p in papers if topic in p.get("topics", [])]
    log(f"Index: {len(topic_papers)} papers with topic '{topic}'")

    # Compare
    matched = []
    title_changed = []
    deleted = []

    for p in topic_papers:
        zi = match_paper(p, zotero_items, zotero_doi_map, zotero_title_map)
        if zi:
            matched.append((p, zi))
            # Check title change
            if normalize_title(p["title"])[:30] != zi["title_norm"][:30]:
                title_changed.append((p, zi))
        else:
            remaining_topics = [t for t in p.get("topics", []) if t != topic]
            deleted.append((p, remaining_topics))

    log(f"\nResults:")
    log(f"  Matched: {len(matched)}")
    log(f"  Title changed: {len(title_changed)}")
    log(f"  Deleted from Zotero: {len(deleted)}")

    if title_changed:
        log(f"\n--- Title changes ---")
        for p, zi in title_changed:
            log(f"  {p['slug'][:35]}")
            log(f"    OLD: {p['title'][:70]}")
            log(f"    NEW: {zi['title'][:70]}")

    to_remove_topic = [(p, remaining) for p, remaining in deleted if remaining]
    to_delete_dir = [(p, remaining) for p, remaining in deleted if not remaining]

    if to_remove_topic:
        log(f"\n--- Remove '{topic}' tag (keep other topics): {len(to_remove_topic)} ---")
        for p, remaining in to_remove_topic:
            log(f"  {p['slug'][:40]} | remaining: {remaining}")

    if to_delete_dir:
        log(f"\n--- Delete entirely: {len(to_delete_dir)} ---")
        for p, _ in to_delete_dir:
            log(f"  {p['slug'][:40]} | {p.get('title','')[:60]}")

    if not title_changed and not deleted:
        log("\nAll in sync. No changes needed.")
        return

    if dry_run:
        log("\n--dry-run: no changes made.")
        return

    # Any suspicious snapshot blocks the complete transaction, including title and
    # classification changes. A partial application would make the local index
    # claim a Zotero state that was never corroborated.
    if to_delete_dir:
        n_papers = len(topic_papers)
        del_ratio = len(to_delete_dir) / max(1, n_papers)
        if not zotero_items and n_papers:
            raise RuntimeError(
                f"Zotero returned 0 items for {n_papers} indexed papers; refusing all changes"
            )
        if del_ratio > _DELETE_RATIO_THRESHOLD:
            raise RuntimeError(
                f"{len(to_delete_dir)}/{n_papers} papers would be deleted; "
                "refusing all changes until a complete snapshot is confirmed"
            )

    # Build and validate the complete local transaction before the first mutation.
    log("\nExecuting...")
    changes = 0
    next_papers = json.loads(json.dumps(papers))
    root = Path(PAPERS_DIR).resolve()
    delete_dirs = {
        paper["slug"]: _safe_slug_dir(root, paper["slug"])
        for paper, _remaining in to_delete_dir
    }

    for current, zotero in title_changed:
        for paper in next_papers:
            if paper["slug"] == current["slug"]:
                paper["title"] = zotero["title"]
                changes += 1
                break

    for current, remaining in to_remove_topic:
        for paper in next_papers:
            if paper["slug"] == current["slug"]:
                paper["topics"] = remaining
                classifications = paper.get("classifications", {})
                classifications.pop(topic, None)
                changes += 1
                break

    deleted_slugs = set(delete_dirs)
    next_papers = [paper for paper in next_papers if paper["slug"] not in deleted_slugs]
    changes += len(deleted_slugs)

    # The index is authoritative. Commit it atomically before best-effort removal
    # of now-unreferenced paper directories; a crash can leave only safe orphans,
    # never an index that references already-deleted content.
    _atomic_write_json(index_path, next_papers)

    for current, zotero in title_changed:
        log(f"  Updated title: {current['slug'][:40]}")
    for current, _remaining in to_remove_topic:
        log(f"  Removed '{topic}': {current['slug'][:40]}")
    for slug, slug_dir in delete_dirs.items():
        if slug_dir.is_dir():
            shutil.rmtree(slug_dir)
            log(f"  Deleted: {slug[:40]} (dir removed)")
        else:
            log(f"  Deleted: {slug[:40]} (index only)")

    log(f"\nDone. {changes} changes applied. {len(next_papers)} papers remaining.")


def main():
    parser = argparse.ArgumentParser(description="Sync deletions/renames from Zotero")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Show changes, don't execute")
    parser.add_argument(
        "--force-delete",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    _run_sync(topic=args.topic, dry_run=args.dry_run, force_delete=args.force_delete)


if __name__ == "__main__":
    main()
