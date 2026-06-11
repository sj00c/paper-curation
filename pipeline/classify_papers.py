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
  표준 셋업은 conda env `py314` (Python 3.14, macOS) — CLAUDE.md
  Python Environment 섹션 참조. Windows 의 경우 Smart App Control 이
  numba/llvmlite DLL 을 차단하면 Python 3.12 전용 env (`py312` 등)
  fallback 이 필요할 수 있다.

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

    cats_list = sorted({a["primary_category"] for a in assignments})
    cls_data = {
        "categories": [{"name": c} for c in cats_list],
        "assignments": assignments,
    }
    cls_path = Path(topic_dir) / "_new_classification.json"
    atomic_write_json(cls_path, cls_data)
    log(f"[write] {cls_path}  ({len(cats_list)} categories)")


def main():
    ap = argparse.ArgumentParser(
        description="HDBSCAN approximate_predict classifier (원 설계)")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--slugs", default="",
                    help="Comma-separated slug prefixes. If set, only these "
                         "papers are (re)classified; others keep existing entries.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print assignment summary without writing JSONs.")
    args = ap.parse_args()
    _run_classify(topic=args.topic, slugs=args.slugs, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
