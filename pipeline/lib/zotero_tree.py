"""Zotero 컬렉션 트리를 분류 공급원으로 읽는다.

왜 필요한가. 사용자는 Zotero 안에서 이미 논문을 분류해 둔다. 실제 라이브러리는
이런 모양이다:

    AI for Science  [67W74439]  15,388편        ← 최상위 = 토픽
      ├ 01 General Methods & Platforms   3,984  ← 하위 = 사람이 만든 카테고리
      ├ 02 Biology & Medicine            2,920
      ├ …
      └ 99 Unclassified                  2,286

파이프라인은 최상위 컬렉션에서 논문을 긁어오기만 하고 이 하위 구조를 버린 뒤,
HDBSCAN 으로 카테고리를 처음부터 새로 만들었다. 사람이 정리해 둔 분류와 겹치지도
않는 별개 체계가 나온다. 이 모듈은 그 하위 구조를 그대로 카테고리로 읽어,
classify_papers 가 쓰는 것과 같은 `_new_classification.json` 형식으로 돌려준다.

추가 API 호출은 없다. Zotero 의 items 응답에 각 논문의 소속 컬렉션 키가 이미
들어 있다:

    {"title": "...", "collections": ["9GMSEJCW", "AT43FF5G"]}

매핑 키. `_papers_index.json` 의 zotero_item_key 는 3273편 중 1편에만 있어서 쓸 수
없다. DOI(3249/3273)를 먼저 보고, 없으면 정규화한 제목으로 잇는다.
"""

from __future__ import annotations

import json
import re
import urllib.request

_API = "https://api.zotero.org"


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


def build_assignments(index_papers, zotero_items, categories,
                      *, unclassified_names=("99 Unclassified", "Unclassified")):
    """Zotero 소속 컬렉션 → classify_papers 형식의 assignments.

    Args:
        index_papers: `_papers_index.json` 의 항목들 (이 토픽 것만).
        zotero_items: Zotero items 응답의 `data` dict 목록.
        categories: {collection_key: category_name} — child_categories() 결과.

    Returns:
        (assignments, stats). assignments 는 classify_papers 가 쓰는 것과 같은
        {slug, primary_category, all_categories, sub_category} 형식.

        사람이 여러 하위 컬렉션에 넣어 둔 논문은 all_categories 에 전부 실리고,
        primary 는 이름순 첫 번째다 — 임의로 하나를 고르지 않는다.
        "99 Unclassified" 만 배정된 논문은 미분류로 남겨 호출자가 처리하게 한다
        (HDBSCAN 제안을 붙일 수 있는 자리).
    """
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

    unclassified = {n.strip().lower() for n in unclassified_names}
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
        real = [n for n in names if n.strip().lower() not in unclassified]
        if not real:
            stats["unclassified"] += 1
            continue

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
