"""
Paper classification via HDBSCAN approximate_predict (원 설계).

Density-faithful 분류기. `topic_modeling.py` 가 학습·저장한 모델 번들
(`{topic}/_hdbscan_model.joblib`) 을 로드해서 신규 논문을 같은 클러스터 공간
으로 라우팅한다.

분류 흐름 (원 설계 그대로):
  1. SPECTER2 768D 임베딩 (`_embeddings_cache.json` + `topic_modeling.compute_embeddings`)
  2. `umap_cluster.transform()` 으로 5D 투영 (학습 시와 동일 transformer)
  3. `hdbscan.approximate_predict(hdbscan_model, vec_5d)` → primary sub-cluster (int tid)
  4. tid == -1 (outlier) 이면 768D 공간에서 **가장 가까운 sub-cluster centroid**
     로 강제 배정 (모든 논문이 반드시 하나의 sub-category 소속)
  5. `all_categories` = 768D centroid 코사인 거리 오름차순 상위 sub-cluster 의
     parent category 를 중복 제거해 최대 TOP_N_CATEGORIES 개. primary 는 항상
     index 0 에 고정.

왜 centroid 거리는 outlier·all_categories 에만 쓰는가:
  HDBSCAN 자체는 density-based 이라 centroid 가 없다. 메인 분류는
  `approximate_predict` 가 mutual reachability + condensed tree 를 사용해
  density-faithful 로 수행한다. centroid 는 "outlier 도 어떤 클러스터에 강제
  편입" 이라는 운영 요구와 "다중 라벨 top-N 후보" 에만 보조적으로 쓰인다.

Pipeline contract:
  * Reads `{topic}/_hdbscan_model.joblib` (필수 — 없으면 exit 2)
      bundle keys: hdbscan_model, umap_cluster, centroids,
                   tid_to_cat, tid_to_subname
  * Reads `{topic}/_embeddings_cache.json` (slug → 768D SPECTER2)
  * 신규 임베딩은 `topic_modeling.compute_embeddings` 로 즉시 계산 (cache 갱신).
  * Updates `docs/papers/_papers_index.json` (classifications[topic] 갱신)
  * Rewrites `{topic}/_new_classification.json` (assignments 재기록)

실행 환경:
  UMAP + hdbscan + sentence-transformers 가 모두 설치된 환경에서 실행한다.
  표준이자 유일 환경은 conda env `py312` (Python 3.12). **py314 사용 금지** —
  진입점(__main__)의 `_env_guard.force_py312()` 가 다른 인터프리터로 실행되면
  py312 로 자동 재실행한다. (numba 가 Python 3.14 의 CALL_KW opcode 를 못 다뤄
  py312 로 통일했다 — 운영자 지시 2026-06-18.)

Usage:
  PYTHONUTF8=1 python pipeline/classify_papers.py --topic ai4s
  PYTHONUTF8=1 python pipeline/classify_papers.py --topic ai4s --slugs 088,1093
  PYTHONUTF8=1 python pipeline/classify_papers.py --topic ai4s --dry-run
"""

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from config_loader import PAPERS_DIR as _PAPERS_DIR, get_topic_dir
PAPERS_DIR = str(_PAPERS_DIR)

TOP_N_CATEGORIES = 3


def log(msg):
    print(msg, flush=True)


def load_index():
    p = Path(PAPERS_DIR) / "_papers_index.json"
    return json.loads(p.read_text(encoding="utf-8")), p


def load_bundle(topic_dir):
    """Load the joblib bundle saved by topic_modeling.py.

    Returns dict with: hdbscan_model, umap_cluster, centroids (tid→768D vec),
    tid_to_cat (tid→parent name), tid_to_subname (tid→textual sub name).
    """
    import joblib
    bundle_path = Path(topic_dir) / "_hdbscan_model.joblib"
    if not bundle_path.exists():
        log(f"ERROR: {bundle_path} missing — run topic_modeling.py first to "
            f"train and persist the HDBSCAN model.")
        sys.exit(2)
    bundle = joblib.load(bundle_path)
    required = {"hdbscan_model", "umap_cluster", "centroids",
                "tid_to_cat", "tid_to_subname"}
    missing = required - set(bundle.keys())
    if missing:
        log(f"ERROR: bundle at {bundle_path} missing keys: {sorted(missing)}.")
        sys.exit(2)

    # 임베딩 모드 가드: 번들의 HDBSCAN manifold 가 어떤 임베딩으로 학습됐는지를
    # 현재 분류에 쓸 임베딩 모드와 대조한다. 다르면 신 모델 벡터를 구 모델
    # manifold 에 투영하는 셈이라 분류가 조용히 망가진다 (approximate_predict 가
    # 엉뚱한 sub-cluster 로 보냄). 구 번들에는 키가 없으므로 base/mean 으로 간주.
    from lib import specter2_embed
    bundle_tag = bundle.get("embed_model", "specter2_base_mean")
    if bundle_tag != specter2_embed.EMBED_TAG:
        log("ERROR: 분류 임베딩 모드가 학습된 모델 번들과 다릅니다 "
            f"(번들 embed_model={bundle_tag!r}, 현재={specter2_embed.EMBED_TAG!r}).\n"
            "       임베딩이 바뀌었으니 신 모델 벡터를 구 모델 manifold 에 그대로\n"
            "       투영할 수 없습니다. topic_modeling.py 를 먼저 재실행해 같은\n"
            "       임베딩으로 HDBSCAN 모델을 다시 학습·저장한 뒤 classify_papers 를\n"
            "       돌리세요.")
        sys.exit(2)

    return bundle


def cosine_distances(query_vec, centroid_dict):
    """Return list of (tid, cosine_distance) sorted ascending.

    Used only for outlier fallback and all_categories top-N.
    """
    q = np.asarray(query_vec, dtype=np.float32)
    qn = q / (np.linalg.norm(q) + 1e-12)
    out = []
    for tid, c in centroid_dict.items():
        c = np.asarray(c, dtype=np.float32)
        cn = c / (np.linalg.norm(c) + 1e-12)
        out.append((tid, 1.0 - float(qn @ cn)))
    out.sort(key=lambda x: x[1])
    return out


def classify_via_bundle(vec_768, bundle):
    """Original-design classification:

      1. UMAP transform → 5D
      2. hdbscan.approximate_predict → primary sub-cluster
      3. outlier → nearest centroid (cosine, 768D)
      4. all_categories = top-N parent categories from centroid-ranked subs

    Returns (primary_cat, all_cats, primary_subname, sub_per_cat_map, raw_outlier).
    `raw_outlier` 는 centroid fallback 적용 *전* 의 raw label 이 -1 이었는지로,
    호출부가 비싼 umap_cluster.transform() 를 다시 돌리지 않고 outlier 를
    집계할 수 있게 한다 (per-paper transform 1회로 단일화).
    """
    import hdbscan as _hdbscan

    hdbscan_model = bundle["hdbscan_model"]
    umap_cluster = bundle["umap_cluster"]
    centroids = bundle["centroids"]
    tid_to_cat = bundle["tid_to_cat"]
    tid_to_subname = bundle["tid_to_subname"]

    vec = np.asarray(vec_768, dtype=np.float32).reshape(1, -1)
    vec_5d = umap_cluster.transform(vec)

    labels, strengths = _hdbscan.approximate_predict(hdbscan_model, vec_5d)
    primary_tid = int(labels[0])
    raw_outlier = primary_tid == -1

    # Outlier 강제 배정: 768D centroid 코사인 최단
    if primary_tid == -1 or primary_tid not in tid_to_cat:
        ranked = cosine_distances(vec_768, centroids)
        if not ranked:
            raise RuntimeError("No centroids available for outlier fallback")
        primary_tid = int(ranked[0][0])

    primary_cat = tid_to_cat[primary_tid]
    primary_subname = tid_to_subname.get(primary_tid, str(primary_tid))

    # all_categories: centroid 거리 오름차순으로 부모 카테고리 중복 제거 top-N
    ranked = cosine_distances(vec_768, centroids)
    sub_per_cat = {primary_cat: primary_subname}
    all_cats = [primary_cat]
    for tid, _dist in ranked:
        cat = tid_to_cat.get(int(tid))
        if not cat or cat in all_cats:
            continue
        all_cats.append(cat)
        sub_per_cat[cat] = tid_to_subname.get(int(tid), str(tid))
        if len(all_cats) >= TOP_N_CATEGORIES:
            break

    return primary_cat, all_cats, primary_subname, sub_per_cat, raw_outlier


def _run_classify_zotero(topic, *, unclassified="skip", dry_run=False):
    """Zotero 컬렉션 트리를 분류로 그대로 쓴다 (HDBSCAN 대안 공급원).

    사용자는 Zotero 안에서 이미 논문을 정리해 둔다. 최상위 컬렉션이 분야(=토픽)
    이고 그 아래 하위 컬렉션이 사람이 만든 카테고리다. HDBSCAN 경로는 그 구조를
    무시하고 임베딩으로 카테고리를 새로 만드는데, 그러면 사용자가 고른 체계와
    겹치지도 않는 결과가 나온다.

    이 경로는 무거운 의존성을 타지 않는다 — UMAP/hdbscan/sentence-transformers,
    `_hdbscan_model.joblib` 번들, 임베딩 캐시 전부 불필요하다. Zotero API 응답에
    각 논문의 소속 컬렉션 키가 이미 들어 있어서 추가 호출도 없다.

    출력은 HDBSCAN 경로와 동일하다 — `_new_classification.json` 과
    `_papers_index.json` 의 `classifications[topic]`. 그래서 하류(카테고리 요약,
    insights, 타임라인, 네트워크, 토픽 인덱스, 검색 인덱스)는 그대로 돈다.
    """
    import urllib.request

    from config_loader import (_ssl_ctx, get_collection_key, get_zotero_api_key,
                               get_zotero_user_id)
    from lib.zotero_tree import (build_assignments, child_categories,
                                 fetch_collections, to_classification)

    topic_dir = str(get_topic_dir(topic))
    api_key = get_zotero_api_key()
    user_id = get_zotero_user_id()

    root_key = get_collection_key(topic)
    if not root_key:
        raise SystemExit(
            f"[classify:zotero] '{topic}' 의 Zotero 컬렉션을 찾을 수 없습니다. "
            f"config.json 의 zotero.collections 를 확인하세요.")

    collections = fetch_collections(api_key, user_id, ssl_ctx=_ssl_ctx)
    categories = child_categories(collections, root_key)
    if not categories:
        raise SystemExit(
            f"[classify:zotero] '{topic}' [{root_key}] 아래에 하위 컬렉션이 없습니다. "
            f"Zotero 에서 카테고리 폴더를 만들거나 --classify-source hdbscan 을 쓰세요.")
    log(f"[zotero] {len(categories)} categories under {topic} [{root_key}]")

    # 하위 컬렉션별로 긁는다. 부모를 한 번에 긁으면 하위 논문까지 전부 나와서
    # (부모 items = 자식 합계) 대형 토픽에서 페이징이 몇 배로 길어진다.
    items = []
    for ckey, cname in categories.items():
        start = 0
        while True:
            url = (f"https://api.zotero.org/users/{user_id}/collections/{ckey}"
                   f"/items/top?limit=100&start={start}&format=json")
            req = urllib.request.Request(
                url, headers={"Zotero-API-Key": api_key, "User-Agent": "paper-curation"})
            with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as resp:
                batch = json.load(resp)
            if not batch:
                break
            items.extend(i.get("data", {}) for i in batch)
            if len(batch) < 100:
                break
            start += 100
        log(f"  {cname}: {len(items)} cumulative")

    all_papers, index_path = load_index()
    topic_papers = [p for p in all_papers if topic in p.get("topics", [])]
    log(f"[index] {len(topic_papers)} {topic} papers")

    assignments, stats = build_assignments(
        topic_papers, items, categories, unclassified=unclassified)
    log(f"[classify:zotero] {stats} → assigned {len(assignments)}/{len(topic_papers)}")

    if stats["unmatched"]:
        log(f"  NOTE: {stats['unmatched']} papers are not in any category folder "
            f"(they stay with their existing classification)")
    if unclassified == "skip" and stats["unclassified"]:
        log(f"  NOTE: {stats['unclassified']} papers sit only in the unclassified bin "
            f"— pass --unclassified include to keep them")

    if dry_run:
        cats = Counter(a["primary_category"] for a in assignments)
        log("[dry-run] per-category counts:")
        for c, n in cats.most_common():
            log(f"  {c}: {n}")
        return

    by_slug = {a["slug"]: a for a in assignments}
    for p in topic_papers:
        a = by_slug.get(p.get("slug"))
        if not a:
            continue           # 매칭 실패/미분류는 기존 분류를 그대로 둔다
        p.setdefault("classifications", {})[topic] = {
            "primary_category": a["primary_category"],
            "all_categories": a["all_categories"],
            "sub_category": a["sub_category"],
            "sub_categories": {},
        }

    from lib.atomic_io import atomic_write_json
    atomic_write_json(index_path, all_papers)
    log(f"[write] {index_path}")

    cls_data = to_classification(assignments)
    cls_path = Path(topic_dir) / "_new_classification.json"
    atomic_write_json(cls_path, cls_data)
    log(f"[write] {cls_path}  ({len(cls_data['categories'])} categories)")


def _run_classify(topic, *, slugs=None, dry_run=False):
    """Programmatic entrypoint for classify_papers.

    `slugs` may be a list of slug-prefixes or a comma-separated string.
    """
    if isinstance(slugs, str):
        slugs_str = slugs
    elif slugs:
        slugs_str = ",".join(slugs)
    else:
        slugs_str = ""

    topic_dir = str(get_topic_dir(topic))

    # 1. HDBSCAN bundle (학습된 모델)
    bundle = load_bundle(topic_dir)
    # n_subclusters 는 metadata-only 키라 load_bundle 의 required 검증 대상이 아니다.
    # 구버전/부분 번들에 없을 수 있으므로 centroids 개수로 fallback (KeyError 방지).
    n_subclusters = bundle.get("n_subclusters", len(bundle.get("centroids", {})))
    log(f"[bundle] {n_subclusters} sub-clusters, "
        f"{len(set(bundle['tid_to_cat'].values()))} parent categories, "
        f"trained_at={bundle.get('trained_at', '?')}")

    # 2. Index → topic_papers
    all_papers, index_path = load_index()
    topic_papers = [p for p in all_papers if topic in p.get("topics", [])]
    log(f"[index] {len(topic_papers)} {topic} papers")

    # 3. Embeddings (incremental cache; SPECTER2 on demand)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from topic_modeling import extract_originalities, compute_embeddings
    originalities = extract_originalities(topic_papers)
    cache_path = os.path.join(topic_dir, "_embeddings_cache.json")
    embeddings, slugs = compute_embeddings(originalities, cache_path)
    slug_to_vec = dict(zip(slugs, embeddings))

    # 4. Slug filter (--slugs)
    slug_filter = None
    if slugs_str:
        prefixes = [s.strip() for s in slugs_str.split(",") if s.strip()]
        slug_filter = {p["slug"] for p in topic_papers
                       if any(p["slug"].startswith(pref) or p["slug"] == pref
                              for pref in prefixes)}
        log(f"[slug filter] restricting to {len(slug_filter)} papers")

    # 5. Classify each paper via approximate_predict
    reassigned = 0
    unchanged = 0
    skipped = 0
    outlier_count = 0
    assignments = []
    processed_vecs = []  # (slug, vec_768) for papers (re)classified this run → viz coords

    for p in topic_papers:
        slug = p["slug"]
        if slug_filter is not None and slug not in slug_filter:
            cls = p.get("classifications", {}).get(topic)
            if cls:
                assignments.append({
                    "slug": slug,
                    "primary_category": cls.get("primary_category", ""),
                    "all_categories": cls.get("all_categories", []),
                    "sub_category": cls.get("sub_category", ""),
                })
            continue
        vec = slug_to_vec.get(slug)
        if vec is None:
            log(f"  WARN: {slug} missing embedding — skipped")
            skipped += 1
            continue

        # umap_cluster.transform() 는 per-call 비용이 크므로 paper 당 1회만 돈다.
        # classify_via_bundle 가 raw outlier 여부를 반환하므로 별도 transform 불필요.
        primary, all_cats, sub, sub_map, raw_outlier = classify_via_bundle(vec, bundle)
        if raw_outlier:
            outlier_count += 1

        prev = p.get("classifications", {}).get(topic, {})
        if prev.get("primary_category") == primary and prev.get("sub_category") == sub:
            unchanged += 1
        else:
            reassigned += 1

        if not dry_run:
            if "classifications" not in p:
                p["classifications"] = {}
            p["classifications"][topic] = {
                "primary_category": primary,
                "all_categories": all_cats,
                "sub_category": sub,
                "sub_categories": sub_map,
            }
            processed_vecs.append((slug, vec))

        assignments.append({
            "slug": slug,
            "primary_category": primary,
            "all_categories": all_cats,
            "sub_category": sub,
        })

    log(f"[classify] reassigned={reassigned}, unchanged={unchanged}, "
        f"skipped={skipped}, outliers_force_assigned={outlier_count}")

    if dry_run:
        cats = Counter(a["primary_category"] for a in assignments)
        log("[dry-run] per-category counts:")
        for c, n in cats.most_common():
            log(f"  {c}: {n}")
        return

    # Write back
    from lib.atomic_io import atomic_write_json
    atomic_write_json(index_path, all_papers)
    log(f"[write] {index_path}")

    # 시각화 좌표 갱신 — 번들에 umap_2d/3d 가 있으면 신규 논문 위치를
    # _umap_coords.json 에 채운다(네트워크에 제대로 배치되도록). 기존 좌표는
    # topic_modeling/복구가 fit_transform 으로 만든 canonical 값이므로 보존하고,
    # _umap_coords 에 없는(=진짜 신규) slug 만 bundle.transform 으로 추가한다.
    if processed_vecs:
        cpath = Path(topic_dir) / "_umap_coords.json"
        existing = {}
        if cpath.exists():
            try:
                existing = json.loads(cpath.read_text(encoding="utf-8"))
            except Exception:
                existing = {}
        missing = [(s, v) for s, v in processed_vecs if s not in existing]
        viz = compute_viz_coords([v for _, v in missing], bundle) if missing else None
        if viz:
            for (s, _v), c in zip(missing, viz):
                existing[s] = c
            atomic_write_json(cpath, existing)
            log(f"[write] {cpath}  (+{len(viz)} new viz coords)")

    cats_list = sorted({a["primary_category"] for a in assignments})
    cls_data = {
        "categories": [{"name": c} for c in cats_list],
        "assignments": assignments,
    }
    cls_path = Path(topic_dir) / "_new_classification.json"
    atomic_write_json(cls_path, cls_data)
    log(f"[write] {cls_path}  ({len(cats_list)} categories)")


def compute_viz_coords(vecs_768, bundle):
    """번들의 umap_2d/umap_3d transformer 로 2D/3D 시각화 좌표 계산. 번들에 없으면 None.

    generate_network 가 읽는 `_umap_coords.json` 의 {x,y,x3,y3,z3} 형식 리스트를 반환.
    backfill/topic_modeling 이 transformer 를 번들에 저장해 둔 경우에만 동작하며,
    신규 논문을 full topic_modeling 재실행 없이 같은 시각화 공간에 투영한다.
    """
    u2 = bundle.get("umap_2d")
    u3 = bundle.get("umap_3d")
    if u2 is None or u3 is None:
        return None
    arr = np.asarray(vecs_768, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    c2 = u2.transform(arr)
    c3 = u3.transform(arr)
    return [{"x": float(c2[i, 0]), "y": float(c2[i, 1]),
             "x3": float(c3[i, 0]), "y3": float(c3[i, 1]), "z3": float(c3[i, 2])}
            for i in range(len(arr))]


def main():
    ap = argparse.ArgumentParser(
        description="Paper classifier — HDBSCAN approximate_predict (원 설계) 또는 "
                    "Zotero 컬렉션 트리")
    ap.add_argument("--topic", default="",
                    help="대상 토픽 (생략 시 설정된 토픽이 하나면 그것)")
    ap.add_argument("--classify-source", choices=("hdbscan", "zotero"),
                    default="hdbscan",
                    help="분류 공급원. hdbscan(기본)=임베딩 클러스터링, "
                         "zotero=사용자가 Zotero 에서 만든 하위 컬렉션을 카테고리로 사용.")
    ap.add_argument("--unclassified", choices=("skip", "include"), default="skip",
                    help="--classify-source zotero 전용. 미분류 폴더에만 있는 논문을 "
                         "빼거나(skip, 기본) 하나의 카테고리로 포함(include).")
    ap.add_argument("--slugs", default="",
                    help="Comma-separated slug prefixes. If set, only these "
                         "papers are (re)classified; others keep existing entries. "
                         "(hdbscan 공급원 전용)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print assignment summary without writing JSONs.")
    args = ap.parse_args()

    from config_loader import resolve_topic
    topic = resolve_topic(args.topic, script="classify_papers")

    if args.classify_source == "zotero":
        if args.slugs:
            raise SystemExit(
                "[classify] --slugs 는 hdbscan 공급원 전용입니다. Zotero 공급원은 "
                "사용자의 컬렉션 배치를 그대로 반영하므로 일부만 골라 적용하지 않습니다.")
        _run_classify_zotero(topic=topic, unclassified=args.unclassified,
                             dry_run=args.dry_run)
        return

    if args.unclassified != "skip":
        raise SystemExit(
            "[classify] --unclassified 는 --classify-source zotero 에서만 의미가 있습니다.")
    _run_classify(topic=topic, slugs=args.slugs, dry_run=args.dry_run)


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    main()
