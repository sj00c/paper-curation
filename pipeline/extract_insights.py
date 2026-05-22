"""
Cross-paper insight 추출 + 논문 간 연결 생성.

카테고리별 논문 essence를 Sonnet으로 분석하여:
1. _insights.json — 카테고리 간 교차 트렌드, 연구 갭, 융합 신호
2. _paper_connections.json — 논문별 "같이 보면 좋은 논문" 추천 (이유 포함)

Usage:
  PYTHONUTF8=1 python pipeline/extract_insights.py --topic scisci
  PYTHONUTF8=1 python pipeline/extract_insights.py --topic ai4s --connections-only
  PYTHONUTF8=1 python pipeline/extract_insights.py --topic ai4s --insights-only
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime

from anthropic import Anthropic
from config_loader import PAPERS_DIR as _PAPERS_DIR, get_topic_dir

PAPERS_DIR = str(_PAPERS_DIR)


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_topic_data(topic):
    """토픽의 논문, 분류, 카테고리 요약 로드."""
    with open(os.path.join(PAPERS_DIR, "_papers_index.json"), "r", encoding="utf-8") as f:
        all_papers = json.load(f)

    topic_papers = [p for p in all_papers if topic in p.get("topics", [])]

    # 카테고리별 분류 (all_categories 기반, multi-class)
    cat_papers = defaultdict(list)
    seen_in_cat = defaultdict(set)  # 중복 방지
    for p in topic_papers:
        cls = p.get("classifications", {}).get(topic, {})
        all_cats = cls.get("all_categories", [cls.get("primary_category", "Other")])
        for cat in all_cats:
            if p["slug"] not in seen_in_cat[cat]:
                cat_papers[cat].append(p)
                seen_in_cat[cat].add(p["slug"])

    # 카테고리 요약 로드
    topic_dir = str(get_topic_dir(topic))
    sum_path = os.path.join(topic_dir, "_category_summaries.json")
    cat_summaries = []
    if os.path.exists(sum_path):
        with open(sum_path, "r", encoding="utf-8") as f:
            cat_summaries = json.load(f)

    return topic_papers, cat_papers, cat_summaries


# ═══════════════════════════════════════════
# 1. Cross-Category Insights
# ═══════════════════════════════════════════

MAX_PROMPT_TOKENS = 200000
TARGET_PROMPT_TOKENS = 150000


def _est_tokens(text):
    """Conservative rough estimate for scaffolding (Korean-heavy=1.5)."""
    return int(len(text) / 1.5)


def _count_tokens(client, text, model="claude-sonnet-4-6"):
    """Authoritative token count via Anthropic API (no output tokens spent).
    Falls back to _est_tokens on any API error."""
    try:
        resp = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": text}],
        )
        return resp.input_tokens
    except Exception as e:
        log(f"  count_tokens API failed ({e}); using local estimate")
        return _est_tokens(text)


def _build_cat_block(cat_name, papers, essence_chars=None):
    """Render one category's block as plain text. essence_chars truncates
    each paper's essence if set."""
    sorted_papers = sorted(papers, key=lambda x: -x.get("score", 0))
    lines = []
    for p in sorted_papers:
        num = p["slug"].split("_")[0]
        essence = p.get("essence", "") or ""
        if essence_chars is not None:
            essence = essence[:essence_chars]
        year = str(p.get("date", ""))[:4]
        lines.append(f"  [{num}] ({year}) {p.get('title', '')[:60]} | {essence}")
    return (f"### {cat_name} ({len(papers)} papers)\n" + "\n".join(lines))


def _haiku_summarize_block(block, client, target_chars):
    """Compress a category block while preserving category header, paper
    numbers/years, and distilled technical signal."""
    prompt = (
        f"Compress the following academic-paper list to at most {target_chars} characters. "
        f"Preserve:\n"
        f"  * The first '### CategoryName (N papers)' header line verbatim\n"
        f"  * Paper numbers in brackets (e.g. [091])\n"
        f"  * Year when present\n"
        f"  * Key technical themes (condense essence sentences but keep keywords)\n"
        f"Keep the top-represented papers in full, then group remaining papers into\n"
        f"one or two summary lines like '  [015, 042, 088] (2024-2025) survey papers on X focusing on Y, Z'.\n"
        f"Output plain text only (no markdown fences).\n\n"
        f"INPUT:\n{block}"
    )
    _t0 = time.time()
    log(f"    [haiku-summarize] calling Haiku 4.5 (~{_est_tokens(prompt)} input tokens, target {target_chars} chars)...")
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max(2000, target_chars // 3),
        messages=[{"role": "user", "content": prompt}],
    )
    out = resp.content[0].text.strip()
    log(f"    [haiku-summarize] -> {len(out)} chars in {time.time()-_t0:.0f}s")
    return out


def _fit_cat_blocks(cat_papers, client, max_prompt_tokens, target_prompt_tokens,
                    prompt_head, prompt_tail):
    """Assemble cat blocks. If (head+blocks+tail) token count > max_prompt_tokens,
    progressively summarize the largest block (via Haiku) until total ≤
    target_prompt_tokens. Uses Anthropic's count_tokens API for authoritative
    measurement. Returns the concatenated text + set of summarized category names.
    """
    blocks = {}
    summarized = set()
    for cat_name, papers in cat_papers.items():
        if cat_name == "Other" or not papers:
            continue
        blocks[cat_name] = _build_cat_block(cat_name, papers)

    def total_tokens():
        cat_text = "\n\n".join(blocks[c] for c in sorted(blocks.keys()))
        return _count_tokens(client, prompt_head + cat_text + prompt_tail)

    initial_total = total_tokens()
    log(f"  Prompt token count (authoritative): {initial_total}")
    if initial_total <= max_prompt_tokens:
        return "\n\n".join(blocks[c] for c in sorted(blocks.keys())), summarized

    log(f"  {initial_total} > {max_prompt_tokens} — running Haiku summarization "
        f"loop (target {target_prompt_tokens}).")

    max_loops = 20
    for _ in range(max_loops):
        cur = total_tokens()
        if cur <= target_prompt_tokens:
            break
        # Summarize the biggest remaining block
        biggest_cat = max(blocks, key=lambda c: len(blocks[c]))
        # Target char size for this summary: proportional to shortfall
        overflow = cur - target_prompt_tokens
        shrink_chars = max(2000, int(overflow * 2.5))  # tokens → chars
        current_chars = len(blocks[biggest_cat])
        target_chars = max(1500, current_chars - shrink_chars)
        if target_chars >= current_chars - 200:
            # Can't meaningfully shrink; stop to avoid infinite loop
            log(f"  WARN: {biggest_cat} already near target; stopping summary loop")
            break
        log(f"  [summary] {biggest_cat}: {current_chars} → ≤{target_chars} chars")
        blocks[biggest_cat] = _haiku_summarize_block(
            blocks[biggest_cat], client, target_chars)
        summarized.add(biggest_cat)

    final_total = total_tokens()
    log(f"  Prompt after summarization: ~{final_total} tokens "
        f"(summarized categories: {len(summarized)})")
    return "\n\n".join(blocks[c] for c in sorted(blocks.keys())), summarized


def extract_cross_category_insights(topic, cat_papers, cat_summaries, client):
    """카테고리 간 교차 insight 추출. Sonnet 1회 호출.

    200k 토큰 초과 시 Haiku summarization fallback 으로 150k 아래로 압축.
    """

    # Build prompt skeleton first (without cat data) to measure overhead.
    total = sum(len(v) for v in cat_papers.values() if v)
    prompt_head = (
        f"You are analyzing {total} academic papers across {len(cat_papers)} "
        f'categories in the "{topic}" research field.\n\nBelow is a summary '
        f"of each category with representative papers:\n\n"
    )
    prompt_tail = """

Produce a JSON array of 3-7 cross-category research insights. Each insight should be one of:
- "convergence": Two+ categories are merging or their methods are combining
- "gap": Important research gap — something NOT being studied that should be
- "emerging": A new trend just starting to appear
- "declining": An approach losing traction

For each insight, provide:
- type: convergence | gap | emerging | declining
- title: 한국어 제목 (15자 이내)
- description: 한국어 설명 (2-3문장, 구체적 근거 포함)
- categories: related category names (array)
- evidence: paper numbers as strings (array, e.g. ["045", "123"])
- signal_strength: "strong" (5+ papers support) or "weak" (2-4 papers)
- policy_implication: 한국어 1문장 — 정책 보고서에 어떤 시사점이 있는지

Also produce a per-category object with:
- trend: ACCELERATING | STABLE | EMERGING | DECLINING
- key_finding: 한국어 1문장 핵심 발견
- gap: 한국어 1문장 연구 갭
- policy_implication: 한국어 1문장 정책 시사점

Output ONLY valid JSON in this exact format:
{
  "cross_category": [ ... ],
  "per_category": {
    "Category Name": {
      "trend": "...",
      "key_finding": "...",
      "gap": "...",
      "policy_implication": "..."
    }
  },
  "meta": {
    "underserved_domains": ["...", "..."],
    "hot_combinations": [
      {"pair": ["A", "B"], "description": "한국어 설명"}
    ]
  }
}"""
    all_cats_text, summarized_cats = _fit_cat_blocks(
        cat_papers, client,
        max_prompt_tokens=MAX_PROMPT_TOKENS,
        target_prompt_tokens=TARGET_PROMPT_TOKENS,
        prompt_head=prompt_head,
        prompt_tail=prompt_tail,
    )
    prompt = prompt_head + all_cats_text + prompt_tail

    log(f"  Cross-category insight extraction ({total} papers, {len(cat_papers)} categories, "
        f"~{_est_tokens(prompt)} tokens)...")
    _t0 = time.time()
    log(f"    [insights] calling Sonnet 4.6 (max_tokens=4000)...")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    log(f"    [insights] -> {len(text)} chars in {time.time()-_t0:.0f}s "
        f"(stop_reason={getattr(resp, 'stop_reason', '?')})")

    # Parse JSON (handle markdown code block)
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        log(f"  WARNING: JSON parse failed: {e}")
        log(f"  Raw response (first 500 chars): {text[:500]}")
        return {"cross_category": [], "per_category": {}, "meta": {}}


# ═══════════════════════════════════════════
# 2. Paper Connections (per-category batch)
# ═══════════════════════════════════════════

def _call_connections_batch(papers_batch, cat_name, topic, all_paper_lines,
                            cross_cat_lines, client):
    """논문 배치에 대해 connections 호출. 같은 카테고리 + 다른 카테고리 후보 모두 제공."""

    batch_lines = []
    for p in papers_batch:
        num = p["slug"].split("_")[0]
        essence = p.get("essence", "")[:200]
        year = str(p.get("date", ""))[:4]
        cls = p.get("classifications", {}).get(topic, {})
        sub = cls.get("sub_category", "")
        batch_lines.append(f"[{num}] ({year}) [{sub}] {p.get('title', '')[:70]} | {essence}")

    batch_nums = ", ".join(p["slug"].split("_")[0] for p in papers_batch)
    batch_text = "\n".join(batch_lines)

    cross_section = ""
    if cross_cat_lines:
        cross_section = f"""
PAPERS FROM OTHER CATEGORIES (also use as connection targets):
{cross_cat_lines}
"""

    prompt = f"""You are analyzing papers in the "{cat_name}" category of {topic}.

TARGET PAPERS (generate connections for these):
{batch_text}

PAPERS IN SAME CATEGORY:
{all_paper_lines}
{cross_section}
For each TARGET paper, recommend related papers from BOTH lists above.
Cross-category connections are especially valuable.

Connection types:
- alternative: Same problem, different approach
- extension: Builds on or extends this work
- foundation: This paper's theoretical/methodological foundation
- counterpoint: Opposite perspective or critiques limitations
- application: Applies this method to a real problem

Output ONLY valid JSON — a dict where keys are paper numbers (e.g. "045") and values are arrays:
{{
  "045": [
    {{"target": "123", "relation": "alternative", "reason": "한국어 이유 1문장"}},
    {{"target": "267", "relation": "extension", "reason": "한국어 이유 1문장"}}
  ]
}}

Rules:
- ONLY include keys for these target papers: {batch_nums}
- reason은 한국어로, 왜 같이 읽어야 하는지 구체적으로 (1문장)
- 모든 논문에 대해 최소 2개 연결 생성 (카테고리 내외 모두 가능)
- 같은 sub-category끼리만 연결하지 말 것 — 다른 카테고리의 논문도 적극 포함
- target은 위 목록에 있는 논문 번호만 사용"""

    _t0 = time.time()
    log(f"    [conn-batch:{cat_name[:30]}] calling Sonnet 4.6 ({len(papers_batch)} targets, max_tokens=10000)...")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    log(f"    [conn-batch:{cat_name[:30]}] -> {len(text)} chars in {time.time()-_t0:.0f}s "
        f"(stop_reason={getattr(resp, 'stop_reason', '?')})")
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


BATCH_SIZE = 25


def _process_category(cat_name, papers, topic, client,
                      all_topic_papers=None):
    """단일 카테고리의 connections 추출. 다른 카테고리 논문도 후보로 제공."""
    sorted_papers = sorted(papers, key=lambda x: -x.get("score", 0))
    all_paper_lines = "\n".join(
        f"[{p['slug'].split('_')[0]}] {p.get('title', '')[:60]}"
        for p in sorted_papers
    )

    # 다른 카테고리 논문 목록 (cross-category connection 후보)
    cat_slugs = {p["slug"] for p in papers}
    cross_cat_lines = ""
    if all_topic_papers:
        other_papers = [p for p in all_topic_papers if p["slug"] not in cat_slugs]
        if other_papers:
            cross_cat_lines = "\n".join(
                f"[{p['slug'].split('_')[0]}] [{p.get('classifications',{}).get(topic,{}).get('primary_category','')}] {p.get('title','')[:60]}"
                for p in other_papers
            )

    batches = [sorted_papers[i:i + BATCH_SIZE]
                for i in range(0, len(sorted_papers), BATCH_SIZE)]

    log(f"  {cat_name} ({len(papers)} papers, {len(batches)} batch{'es' if len(batches) > 1 else ''})...")

    # num_to_slug: 같은 카테고리 + 다른 카테고리 모두 포함
    num_to_slug = {}
    for p in papers:
        num = p["slug"].split("_")[0]
        num_to_slug[num] = p["slug"]
    if all_topic_papers:
        for p in all_topic_papers:
            num = p["slug"].split("_")[0]
            if num not in num_to_slug:
                num_to_slug[num] = p["slug"]

    cat_connections = {}
    cat_total = 0
    for bi, batch in enumerate(batches):
        try:
            batch_result = _call_connections_batch(
                batch, cat_name, topic, all_paper_lines,
                cross_cat_lines, client
            )

            for num, conns in batch_result.items():
                slug = num_to_slug.get(num)
                if not slug:
                    continue
                resolved = []
                for c in conns:
                    target_slug = num_to_slug.get(c.get("target", ""))
                    if target_slug:
                        resolved.append({
                            "slug": target_slug,
                            "relation": c.get("relation", "alternative"),
                            "reason": c.get("reason", ""),
                        })
                if resolved:
                    existing = cat_connections.get(slug, [])
                    seen_targets = {c["slug"] for c in existing}
                    for r in resolved:
                        if r["slug"] not in seen_targets:
                            existing.append(r)
                            seen_targets.add(r["slug"])
                    cat_connections[slug] = existing

            cat_total += len(batch_result)
            if len(batches) > 1:
                log(f"    [{cat_name}] batch {bi + 1}/{len(batches)}: {len(batch_result)} papers")
        except Exception as e:
            log(f"    [{cat_name}] batch {bi + 1}/{len(batches)} ERROR: {str(e)[:100]}")

        time.sleep(1)  # rate limit

    log(f"    [{cat_name}] → {cat_total} papers connected")
    return cat_connections


MAX_PARALLEL_CATEGORIES = 4


def extract_paper_connections(topic, cat_papers, client, all_topic_papers=None):
    """카테고리별 병렬로 논문 간 연결 추출. 다른 카테고리 논문도 후보로 제공."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_connections = {}
    targets = {cat: papers for cat, papers in cat_papers.items()
                if cat != "Other" and len(papers) >= 3}

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_CATEGORIES) as executor:
        futures = {
            executor.submit(_process_category, cat_name, papers, topic, client,
                            all_topic_papers): cat_name
            for cat_name, papers in sorted(targets.items())
        }

        for future in as_completed(futures):
            cat_name = futures[future]
            try:
                cat_connections = future.result()
                for slug, conns in cat_connections.items():
                    existing = all_connections.get(slug, [])
                    seen_targets = {c["slug"] for c in existing}
                    for c in conns:
                        if c["slug"] not in seen_targets:
                            existing.append(c)
                            seen_targets.add(c["slug"])
                    all_connections[slug] = existing
            except Exception as e:
                log(f"  {cat_name} FAILED: {str(e)[:100]}")

    return all_connections


def main():
    parser = argparse.ArgumentParser(description="Extract cross-paper insights and connections")
    parser.add_argument("--topic", default="ai4s")
    parser.add_argument("--insights-only", action="store_true", help="Cross-category insights only")
    parser.add_argument("--connections-only", action="store_true", help="Paper connections only")
    parser.add_argument("--categories", nargs="+", help="Specific categories to process (others preserved)")
    args = parser.parse_args()

    topic = args.topic
    topic_dir = str(get_topic_dir(topic))

    log(f"Loading {topic} data...")
    topic_papers, cat_papers, cat_summaries = load_topic_data(topic)

    # Filter to specific categories if requested
    if args.categories:
        cat_papers = {k: v for k, v in cat_papers.items() if k in args.categories}
        cat_summaries = [s for s in cat_summaries if s.get("category") in args.categories]
        log(f"  {len(topic_papers)} papers total, {len(cat_papers)} categories (filtered)")
    else:
        log(f"  {len(topic_papers)} papers, {len(cat_papers)} categories")

    # Explicit timeout + retry: previously a single messages.create() in this
    # script stalled for 1h22m with no log activity, suggesting an httpx read
    # without a deadline. 5-min per-attempt cap × 2 retries = ~15 min worst
    # case before the SDK raises, instead of hanging forever.
    client = Anthropic(timeout=300.0, max_retries=2)
    run_insights = not args.connections_only
    run_connections = not args.insights_only

    # ── Cross-category insights ──
    if run_insights:
        log("\n" + "=" * 50)
        log("CROSS-CATEGORY INSIGHTS (Sonnet)")
        log("=" * 50)

        insights = extract_cross_category_insights(topic, cat_papers, cat_summaries, client)
        insights["generated_at"] = datetime.now().strftime("%Y-%m-%d")
        insights["topic"] = topic
        insights["paper_count"] = len(topic_papers)

        insights_path = os.path.join(topic_dir, "_insights.json")
        # Merge with existing insights when --categories is used
        if args.categories and os.path.exists(insights_path):
            with open(insights_path, "r", encoding="utf-8") as f:
                existing_insights = json.load(f)
            # Merge per_category (overwrite updated categories, keep rest);
            # drop entries whose category no longer exists in current cat_papers
            current_cats = set(cat_papers.keys())
            existing_per_cat = {k: v for k, v in existing_insights.get("per_category", {}).items()
                                if k in current_cats}
            existing_per_cat.update(insights.get("per_category", {}))
            insights["per_category"] = existing_per_cat
            insights["paper_count"] = len(topic_papers)
        from lib.atomic_io import atomic_write_json
        atomic_write_json(insights_path, insights)
        log(f"\nSaved: {insights_path}")
        log(f"  {len(insights.get('cross_category', []))} cross-category insights")
        log(f"  {len(insights.get('per_category', {}))} per-category insights")

    # ── Paper connections ──
    if run_connections:
        log("\n" + "=" * 50)
        log("PAPER CONNECTIONS (Sonnet)")
        log("=" * 50)

        connections = extract_paper_connections(topic, cat_papers, client, topic_papers)

        topic_slugs = [p["slug"] for p in topic_papers]
        from lib.connections import sync_topic_connections
        sync_topic_connections(connections, topic, topic_slugs, topic_dir, log=log)

    log("\nDone!")


if __name__ == "__main__":
    main()
