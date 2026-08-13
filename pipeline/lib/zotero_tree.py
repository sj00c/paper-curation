"""Zotero 컬렉션 트리를 분류 공급원으로 읽는다.

왜 필요한가. 사용자는 Zotero 안에서 이미 논문을 분류해 둔다. 예:

    My Research  [TOPLEVEL]                 ← 최상위 = 토픽
      ├ 01 Methods                         ← 하위 = 사람이 만든 카테고리
      ├ 02 Applications
      ├ …
      └ 99 Unclassified

파이프라인은 최상위 컬렉션에서 논문을 긁어오기만 하고 이 하위 구조를 버린 뒤,
HDBSCAN 으로 카테고리를 처음부터 새로 만들었다. 사람이 정리해 둔 분류와 겹치지도
않는 별개 체계가 나온다. 이 모듈은 그 하위 구조를 그대로 카테고리로 읽어,
classify_papers 가 쓰는 것과 같은 `_new_classification.json` 형식으로 돌려준다.

추가 API 호출은 없다. Zotero 의 items 응답에 각 논문의 소속 컬렉션 키가 이미
들어 있다:

    {"title": "...", "collections": ["9GMSEJCW", "AT43FF5G"]}

매핑은 DOI를 우선하고, 없으면 정규화한 제목으로 잇는다.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import tempfile
import urllib.request
from pathlib import Path

_API = "https://api.zotero.org"

# 로컬 Zotero DB. lib/citedby/local_library.py 와 같은 규약을 쓴다 —
# ZOTERO_SQLITE env 가 우선, 없으면 Zotero 의 기본 위치.
DEFAULT_DB = Path.home() / "Zotero" / "zotero.sqlite"


def local_db_path(explicit=None):
    """읽을 zotero.sqlite 경로. 없으면 None."""
    db = Path(explicit or os.environ.get("ZOTERO_SQLITE") or DEFAULT_DB)
    return db if db.exists() else None


def _open_readonly(db_path):
    """Zotero 가 실행 중이면 원본이 잠기므로 복사본을 읽는다.

    citedby/local_library.py 가 쓰는 방식 그대로다. 220MB 복사가 0.1초라 매번
    떠도 부담이 없고, 잠금 경합이나 반쯤 쓰인 상태를 볼 위험이 없다.
    """
    fd, tmp = tempfile.mkstemp(suffix=".sqlite", prefix="zotero_tree_")
    os.close(fd)
    shutil.copy2(db_path, tmp)
    return sqlite3.connect(f"file:{tmp}?mode=ro", uri=True), tmp


_COLLECTIONS_SQL = """
SELECT c.key, c.collectionName, p.key
FROM collections c
LEFT JOIN collections p ON c.parentCollectionID = p.collectionID
"""

# 부모 컬렉션의 자식들에 속한 논문 + DOI/제목. 한 번의 쿼리로 끝난다.
# Web API 는 자식마다 100건씩 페이징해야 하므로 로컬 DB가 훨씬 빠르다.
_CHILD_ITEMS_SQL = """
SELECT ci.itemID, c.key,
       MAX(CASE WHEN f.fieldName = 'DOI'   THEN idv.value END) AS doi,
       MAX(CASE WHEN f.fieldName = 'title' THEN idv.value END) AS title
FROM collections c
JOIN collections p          ON c.parentCollectionID = p.collectionID AND p.key = ?
JOIN collectionItems ci     ON ci.collectionID = c.collectionID
LEFT JOIN itemData id       ON id.itemID = ci.itemID
LEFT JOIN fields f          ON f.fieldID = id.fieldID
LEFT JOIN itemDataValues idv ON idv.valueID = id.valueID
WHERE ci.itemID NOT IN (SELECT itemID FROM deletedItems)
GROUP BY ci.itemID, c.key
"""


def fetch_collections_local(db_path=None):
    """로컬 DB 에서 {key: {name, parent}}. Web API 응답과 같은 형식."""
    db = local_db_path(db_path)
    if not db:
        return None
    conn, tmp = _open_readonly(db)
    try:
        return {key: {"name": name, "parent": parent}
                for key, name, parent in conn.execute(_COLLECTIONS_SQL) if key}
    finally:
        conn.close()
        Path(tmp).unlink(missing_ok=True)


def fetch_items_local(root_key, db_path=None):
    """루트의 자식 컬렉션에 속한 논문들을 Web API items 형식으로.

    build_assignments 가 그대로 받을 수 있도록 {DOI, title, collections} 모양으로
    맞춘다. 한 논문이 여러 자식에 들어 있으면 collections 에 전부 담긴다.
    """
    db = local_db_path(db_path)
    if not db:
        return None
    conn, tmp = _open_readonly(db)
    try:
        merged = {}
        for item_id, ckey, doi, title in conn.execute(_CHILD_ITEMS_SQL, (root_key,)):
            rec = merged.setdefault(
                item_id, {"DOI": doi or "", "title": title or "", "collections": []})
            rec["collections"].append(ckey)
            # 같은 논문의 다른 행에서 값이 채워질 수 있다.
            if doi and not rec["DOI"]:
                rec["DOI"] = doi
            if title and not rec["title"]:
                rec["title"] = title
        return list(merged.values())
    finally:
        conn.close()
        Path(tmp).unlink(missing_ok=True)


def _norm_doi(value: str) -> str:
    if not value:
        return ""
    d = str(value).strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d.removeprefix("doi:").strip()


def _norm_title(value: str) -> str:
    """제목 매칭용 정규화. 공백/구두점/대소문자 차이를 흡수한다."""
    if not value:
        return ""
    t = re.sub(r"<[^>]+>", " ", str(value))
    t = re.sub(r"[^0-9a-z]+", " ", t.lower())
    return " ".join(t.split())


def fetch_collections(api_key: str, user_id: str, *, ssl_ctx=None) -> dict:
    """전체 컬렉션을 {key: {name, parent, ...}} 로 반환. 1회 호출."""
    out = {}
    start = 0
    while True:
        url = (f"{_API}/users/{user_id}/collections"
               f"?format=json&limit=100&start={start}")
        req = urllib.request.Request(
            url, headers={"Zotero-API-Key": api_key, "User-Agent": "paper-curation"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            batch = json.load(resp)
        if not batch:
            break
        for c in batch:
            d = c.get("data", {})
            out[d.get("key", "")] = {
                "name": d.get("name", ""),
                "parent": d.get("parentCollection") or None,
            }
        if len(batch) < 100:
            break
        start += 100
    out.pop("", None)
    return out


def child_categories(collections: dict, root_key: str) -> dict:
    """최상위 컬렉션의 직계 하위를 {key: name} 으로. 정렬은 이름순.

    "01 …", "02 …" 처럼 번호가 붙은 관례를 그대로 살리려면 이름순이 맞다.
    """
    kids = {k: v["name"] for k, v in collections.items() if v.get("parent") == root_key}
    return dict(sorted(kids.items(), key=lambda kv: kv[1]))


def find_root_key(collections: dict, name_or_key: str) -> str:
    """컬렉션 이름 또는 키로 최상위 키를 찾는다. 못 찾으면 빈 문자열."""
    if name_or_key in collections:
        return name_or_key
    for key, meta in collections.items():
        if meta["name"] == name_or_key:
            return key
    return ""


# 미분류 컬렉션의 관례적 이름. 실제 라이브러리마다 번호 유무가 달라
# "99 Unclassified"와 "Unclassified"를 모두 인식한다.
DEFAULT_UNCLASSIFIED_NAMES = ("99 Unclassified", "Unclassified", "미분류")

# unclassified 처리 방식.
#   "skip"    — 배정하지 않고 남긴다. 나중에 HDBSCAN 제안을 붙일 자리.
#   "include" — 그대로 하나의 카테고리로 쓴다. 사용자가 Zotero 에서 만든 칸이니
#               페이지에도 그대로 보이는 편이 정직하다.
UNCLASSIFIED_MODES = ("skip", "include")


def is_unclassified(name, unclassified_names=DEFAULT_UNCLASSIFIED_NAMES):
    """이 카테고리 이름이 '미분류' 칸인가.

    번호 접두사("99 ")를 떼고 비교하므로, 사용자가 번호를 바꿔 달아도("90 …")
    같은 칸으로 인식한다. 이름 규칙에 기대는 건 취약하지만, Zotero 에 '이건
    미분류 칸' 이라고 표시할 자리가 없어서 이게 유일한 신호다.
    """
    n = re.sub(r"^\d+\s+", "", str(name or "")).strip().lower()
    return n in {re.sub(r"^\d+\s+", "", x).strip().lower()
                 for x in unclassified_names}


def build_assignments(index_papers, zotero_items, categories,
                      *, unclassified="skip",
                      unclassified_names=DEFAULT_UNCLASSIFIED_NAMES):
    """Zotero 소속 컬렉션 → classify_papers 형식의 assignments.

    Args:
        index_papers: `_papers_index.json` 의 항목들 (이 토픽 것만).
        zotero_items: Zotero items 응답의 `data` dict 목록.
        categories: {collection_key: category_name} — child_categories() 결과.
        unclassified: "skip"(기본) 또는 "include". UNCLASSIFIED_MODES 참조.

    Returns:
        (assignments, stats). assignments 는 classify_papers 가 쓰는 것과 같은
        {slug, primary_category, all_categories, sub_category} 형식.

        사람이 여러 하위 컬렉션에 넣어 둔 논문은 all_categories 에 전부 실리고,
        primary 는 이름순 첫 번째다 — 임의로 하나를 고르지 않는다.

        미분류 칸은 `unclassified` 로 갈린다. "skip" 이면 그 칸에만 든 논문을
        배정하지 않고 stats["unclassified"] 로만 세고, "include" 면 다른 카테고리와
        똑같이 취급한다. 어느 쪽이든 실제 카테고리가 하나라도 있으면 미분류 칸은
        가려진다 — 사람이 분류해 둔 것이 우선이다.
    """
    if unclassified not in UNCLASSIFIED_MODES:
        raise ValueError(
            f"unclassified must be one of {UNCLASSIFIED_MODES}, got {unclassified!r}")
    by_doi, by_title = {}, {}
    for item in zotero_items:
        doi = _norm_doi(item.get("DOI") or item.get("doi") or "")
        title = _norm_title(item.get("title", ""))
        cols = [c for c in (item.get("collections") or []) if c in categories]
        if not cols:
            continue
        if doi:
            by_doi.setdefault(doi, cols)
        if title:
            by_title.setdefault(title, cols)

    assignments = []
    stats = {"matched_doi": 0, "matched_title": 0, "unmatched": 0, "unclassified": 0}

    for paper in index_papers:
        slug = paper.get("slug")
        if not slug:
            continue

        doi = _norm_doi(paper.get("doi", ""))
        cols, hit = None, ""
        if doi and doi in by_doi:
            cols, hit = by_doi[doi], "matched_doi"
        else:
            title = _norm_title(paper.get("title", ""))
            if title and title in by_title:
                cols, hit = by_title[title], "matched_title"

        if not cols:
            stats["unmatched"] += 1
            continue

        names = [categories[c] for c in cols]
        real = [n for n in names if not is_unclassified(n, unclassified_names)]

        if not real:
            # 미분류 칸에만 들어 있다.
            stats["unclassified"] += 1
            if unclassified == "skip":
                continue
            real = sorted(dict.fromkeys(names))

        real = sorted(dict.fromkeys(real))
        stats[hit] += 1
        assignments.append({
            "slug": slug,
            "primary_category": real[0],
            "all_categories": real,
            "sub_category": "",
        })

    return assignments, stats


def to_classification(assignments) -> dict:
    """classify_papers 가 쓰는 `_new_classification.json` 구조로 감싼다."""
    cats = sorted({a["primary_category"] for a in assignments})
    return {"categories": [{"name": c} for c in cats], "assignments": assignments}
