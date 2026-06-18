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
from config_loader import PAPERS_DIR as _PAPERS_DIR, get_topic_dir, load_config

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

# Sonnet 4.6 의 context window 는 1M 이고, 실제 insight 호출은 max_tokens=8000
# 출력을 요청한다 (_cc_anthropic_call). 따라서 input+output 이 window 를 넘지 않으려면
# 프롬프트 자체는 (window - max_output - safety_margin) 아래여야 한다. 1M 를 그대로
# 임계값으로 쓰면 ~192~200k 프롬프트가 shrink gate 를 그냥 통과한 뒤 호출 시점에
# context-length 초과로 죽고, 바깥 try/except 가 빈 insight 를 돌려준다.
# CONTEXT_WINDOW - MAX_OUTPUT_TOKENS - SAFETY_MARGIN = 1000000 - 8000 - 4000 = 988000.
_CONTEXT_WINDOW = 1000000
_MAX_OUTPUT_TOKENS = 8000   # _cc_anthropic_call max_tokens
_SAFETY_MARGIN = 4000       # tool schema/오버헤드/추정 오차 흡수
MAX_PROMPT_TOKENS = _CONTEXT_WINDOW - _MAX_OUTPUT_TOKENS - _SAFETY_MARGIN  # 988000
TARGET_PROMPT_TOKENS = 900000


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
    resp = client.with_options(timeout=600.0).messages.create(
        model="claude-haiku-4-5",
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
    target_prompt_tokens. Returns the concatenated text + set of summarized
    category names.

    Token 측정 비용 최적화: count_tokens API (네트워크 왕복) 는 시작 1회 +
    종료 1회만 호출한다. shrink 루프 안에서는 매 반복마다 API 를 때리는 대신,
    시작 시 측정한 (authoritative tokens / total chars) 비율로 char→token 을
    국소 추정해서 언제 멈출지 결정한다. 이렇게 하면 큰 토픽에서 발생하던
    ~22 회의 직렬 count_tokens 왕복이 2 회로 줄어든다. (한국↔Anthropic 경로에서
    각 호출은 ~150~200k 페이로드라 수십 초씩 걸림.)
    """
    blocks = {}
    summarized = set()
    for cat_name, papers in cat_papers.items():
        if cat_name == "Other" or not papers:
            continue
        blocks[cat_name] = _build_cat_block(cat_name, papers)

    def full_prompt_text():
        cat_text = "\n\n".join(blocks[c] for c in sorted(blocks.keys()))
        return prompt_head + cat_text + prompt_tail

    def api_total_tokens():
        return _count_tokens(client, full_prompt_text())

    # ── 시작 1회: authoritative 측정 ──────────────────────────────────────
    initial_text = full_prompt_text()
    initial_total = _count_tokens(client, initial_text)
    log(f"  Prompt token count (authoritative): {initial_total}")
    if initial_total <= max_prompt_tokens:
        return "\n\n".join(blocks[c] for c in sorted(blocks.keys())), summarized

    log(f"  {initial_total} > {max_prompt_tokens} — running Haiku summarization "
        f"loop (target {target_prompt_tokens}).")

    # 시작 시점의 토큰/문자 비율로 char→token 국소 추정기를 보정한다.
    # (Korean-heavy 혼합 텍스트라 _est_tokens 의 고정 1/1.5 보다 실측 비율이 정확.)
    tok_per_char = (initial_total / max(1, len(initial_text)))

    def est_total_tokens():
        return int(len(full_prompt_text()) * tok_per_char)

    max_loops = 20
    for _ in range(max_loops):
        cur = est_total_tokens()  # 국소 추정 — 루프 안에서는 API 호출 없음
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

    # ── 종료 1회: 실제 Sonnet 호출 전 authoritative 재측정 ────────────────
    final_total = api_total_tokens()
    log(f"  Prompt after summarization: ~{final_total} tokens "
        f"(summarized categories: {len(summarized)})")
    return "\n\n".join(blocks[c] for c in sorted(blocks.keys())), summarized


def extract_cross_category_insights(topic, cat_papers, cat_summaries, client):
    """카테고리 간 교차 insight 추출. Sonnet 1회 호출.

    988k 토큰 초과 시 Haiku summarization fallback 으로 900k 아래로 압축.
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
    log(f"    [insights] calling Sonnet 4.6 via tool-use (max_tokens=8000)...")

    insight_schema = {
        "name": "emit_insights",
        "description": "Emit cross-category research insights.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cross_category": {
                    "type": "array",
                    "minItems": 3, "maxItems": 7,
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"enum": ["convergence", "gap", "emerging", "declining"]},
                            "title": {"type": "string", "maxLength": 30},
                            "description": {"type": "string", "minLength": 30},
                            "categories": {"type": "array", "items": {"type": "string"}},
                            "evidence": {"type": "array",
                                          "items": {"type": "string"}},
                            "signal_strength": {"enum": ["strong", "weak"]},
                            "policy_implication": {"type": "string", "minLength": 10},
                        },
                        "required": ["type", "title", "description", "categories",
                                      "evidence", "signal_strength",
                                      "policy_implication"],
                    },
                },
                "per_category": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "trend": {"enum": ["ACCELERATING", "STABLE",
                                                "EMERGING", "DECLINING"]},
                            "key_finding": {"type": "string", "minLength": 10},
                            "gap": {"type": "string", "minLength": 10},
                            "policy_implication": {"type": "string", "minLength": 10},
                        },
                        "required": ["trend", "key_finding", "gap",
                                      "policy_implication"],
                    },
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "underserved_domains": {"type": "array",
                                                 "items": {"type": "string"}},
                        "hot_combinations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "pair": {"type": "array", "minItems": 2,
                                              "maxItems": 2,
                                              "items": {"type": "string"}},
                                    "description": {"type": "string"},
                                },
                                "required": ["pair", "description"],
                            },
                        },
                    },
                },
            },
            "required": ["cross_category", "per_category"],
        },
    }

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from api._llm import cached_call, topic_cache_dir
    cache_dir = topic_cache_dir(topic)

    def _make_call():
        last_err = None
        for backend in _CC_BACKENDS:
            try:
                if backend == "anthropic":
                    out = _cc_anthropic_call(client, prompt, insight_schema)
                elif backend == "openai":
                    out = _cc_openai_call(prompt, insight_schema)
                elif backend == "gemini":
                    out = _cc_gemini_call(prompt, insight_schema)
                else:
                    log(f"    [insights:{backend}] unknown backend, skipping")
                    continue
                log(f"    [insights:{backend}] OK in {time.time()-_t0:.0f}s")
                return out
            except Exception as e:
                last_err = e
                log(f"    [insights:{backend}] failed ({type(e).__name__}: {str(e)[:80]}) → next backend")
        raise RuntimeError(f"all cross-category backends failed: "
                           f"{type(last_err).__name__}: {str(last_err)[:120]}")

    try:
        return cached_call(cache_dir, prompt, "+".join(_CC_BACKENDS), _make_call,
                            schema_version="v1")
    except Exception as e:
        log(f"  WARNING: insight tool-use failed: {e}")
        return {"cross_category": [], "per_category": {}, "meta": {}}


# ─────────────────────────────────────────────────────────────────────────────
# Cross-category insights backend helpers (Anthropic / OpenAI / Gemini)
# All three return a dict matching ``insight_schema`` so the caller stays
# provider-agnostic. Each helper raises on failure so the outer try/except
# chain can move to the next backend.
# ─────────────────────────────────────────────────────────────────────────────

def _cc_anthropic_call(client, prompt, schema):
    if client is None:
        raise RuntimeError("Anthropic client unavailable")
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        tools=[schema],
        tool_choice={"type": "tool", "name": schema["name"]},
        messages=[{"role": "user", "content": prompt}],
    )
    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" \
                and getattr(block, "name", None) == schema["name"]:
            return dict(block.input)
    raise RuntimeError(f"{schema['name']} tool was not invoked")


def _cc_openai_call(prompt, schema):
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(f"openai SDK missing: {e}")
    api_key = (os.environ.get("OPENAI_API_KEY") or
               load_config().get("openai_api_key", ""))
    if not api_key:
        raise RuntimeError("no OpenAI API key (OPENAI_API_KEY env or config)")
    oai = OpenAI(api_key=api_key, timeout=180.0, max_retries=1)
    func_def = {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema.get("description", ""),
            "parameters": schema["input_schema"],
        },
    }
    resp = oai.chat.completions.create(
        model=_OPENAI_CC_MODEL,
        max_tokens=8000,
        tools=[func_def],
        tool_choice={"type": "function", "function": {"name": schema["name"]}},
        messages=[{"role": "user", "content": prompt}],
    )
    msg = resp.choices[0].message
    if not getattr(msg, "tool_calls", None):
        raise RuntimeError(f"OpenAI did not invoke {schema['name']}")
    return json.loads(msg.tool_calls[0].function.arguments)


def _cc_gemini_call(prompt, schema):
    try:
        from google import genai
        from google.genai import types as gtypes
    except ImportError as e:
        raise RuntimeError(f"google-genai SDK missing: {e}")
    api_key = (os.environ.get("GEMINI_API_KEY")
               or os.environ.get("GOOGLE_API_KEY")
               or load_config().get("gemini_api_key", "")
               or load_config().get("google_api_key", ""))
    if not api_key:
        raise RuntimeError("no Gemini API key (GEMINI_API_KEY/GOOGLE_API_KEY env or config)")
    gem = genai.Client(api_key=api_key)
    resp = gem.models.generate_content(
        model=_GEMINI_CC_MODEL,
        contents=prompt,
        config=gtypes.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema["input_schema"],
        ),
    )
    text = (resp.text or "").strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


# ═══════════════════════════════════════════
# 2. Paper Connections (per-category batch)
# ═══════════════════════════════════════════

def _call_with_deadline(fn, deadline_s, label=""):
    """Run fn() in a daemon thread; raise TimeoutError if it exceeds deadline_s.

    The Anthropic SDK has no hard total-request deadline, and httpx's read
    timeout doesn't reliably fire when a Korea↔US TCP connection is silently
    severed by a middlebox (socket stays ESTABLISHED, recv() blocks forever).
    This wraps the call in a wall-clock watchdog: past the deadline we abandon
    the (un-killable) thread + its hung socket and raise, so the caller's
    per-batch except handler can skip it instead of hanging the whole run."""
    import threading
    box = {}

    def _w():
        try:
            box["v"] = fn()
        except BaseException as e:  # noqa: BLE001 — propagate any failure
            box["e"] = e

    t = threading.Thread(target=_w, daemon=True)
    t.start()
    t.join(deadline_s)
    if t.is_alive():
        raise TimeoutError(f"{label} exceeded {deadline_s}s wall-clock deadline")
    if "e" in box:
        raise box["e"]
    return box.get("v")


# Hard per-batch wall-clock cap. Legit batches finish in 2~6 min; rare ones
# reach ~10 min. Hangs run 20~60+ min. 900s kills hangs while allowing almost
# all real completions.
_CONN_BATCH_DEADLINE_S = 900

# Backend fallback chain. Korea↔Anthropic route stalls badly some windows while
# the OpenAI route stays healthy (and vice-versa). The connection task is plain
# structured-JSON generation, not provider-specific — so we try backends in
# order and fall back on failure. Default: Anthropic primary, OpenAI fallback.
# Override order with EXTRACT_INSIGHTS_BACKENDS=openai,anthropic (or just one).
_BACKENDS = [b.strip().lower() for b in
             os.environ.get("EXTRACT_INSIGHTS_BACKENDS",
                            os.environ.get("EXTRACT_INSIGHTS_BACKEND", "anthropic") + ",openai")
             .split(",") if b.strip()]
# de-dup preserving order
_BACKENDS = list(dict.fromkeys(_BACKENDS))
_OPENAI_CONN_MODEL = os.environ.get("EXTRACT_INSIGHTS_OPENAI_MODEL", "gpt-5.5")
# Cross-category insights fallback chain (separate from paper_connections):
# anthropic → openai → gemini. Each backend is forced into the same JSON schema
# so the downstream consumer is provider-agnostic. Override with
# EXTRACT_INSIGHTS_CC_BACKENDS=openai,gemini etc.
_CC_BACKENDS = [b.strip().lower() for b in
                 os.environ.get("EXTRACT_INSIGHTS_CC_BACKENDS",
                                "anthropic,openai,gemini").split(",")
                 if b.strip()]
_CC_BACKENDS = list(dict.fromkeys(_CC_BACKENDS))
_OPENAI_CC_MODEL = os.environ.get("EXTRACT_INSIGHTS_CC_OPENAI_MODEL", "gpt-5.5")
_GEMINI_CC_MODEL = os.environ.get("EXTRACT_INSIGHTS_CC_GEMINI_MODEL", "gemini-3.1-pro-preview")
# Per-attempt wall-clock cap (thread watchdog) — fail fast so fallback kicks in.
_ATTEMPT_DEADLINE_S = int(os.environ.get("EXTRACT_INSIGHTS_ATTEMPT_DEADLINE", "150"))
# Circuit breaker: after this many consecutive failures of a backend, drop it
# for the rest of the run (don't keep wasting _ATTEMPT_DEADLINE_S per batch).
_CB_TRIP = 3
_cb_fails: dict[str, int] = {}
_cb_lock = __import__("threading").Lock()


_CONNECTIONS_TOOL_SCHEMA = {
    "name": "emit_connections",
    "description": (
        "Emit paper connection recommendations. Each entry in "
        "`connections` is one source paper plus 2+ related target papers."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "connections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string",
                                    "description": "Source paper number (e.g. '045')."},
                        "targets": {
                            "type": "array",
                            "minItems": 2,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string",
                                                "description": "Target paper number."},
                                    "relation": {"enum": ["alternative", "extension",
                                                           "foundation", "counterpoint",
                                                           "application"]},
                                    "reason": {"type": "string", "minLength": 5,
                                                "description": "한국어로 왜 같이 읽어야 하는지 1문장."},
                                },
                                "required": ["target", "relation", "reason"],
                            },
                        },
                    },
                    "required": ["source", "targets"],
                },
            },
        },
        "required": ["connections"],
    },
}


def _one_backend_call(backend: str, clients: dict, prompt: str) -> str:
    """Call a single backend and return the JSON-encoded connection map
    text. Both branches reach the same downstream ``json.loads`` so the
    fallback contract is preserved.

    Anthropic uses tool-use (forced ``emit_connections``) to eliminate
    raw-text JSON parsing fragility; the tool result is converted to
    the legacy ``{source_num: [{target, relation, reason}, ...]}`` dict
    shape and re-serialised. OpenAI keeps ``response_format=json_object``
    since that backend already returns deterministic JSON.
    """
    if backend == "openai":
        resp = clients["openai"].chat.completions.create(
            model=_OPENAI_CONN_MODEL,
            max_tokens=16000,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return (resp.choices[0].message.content or "").strip()

    resp = clients["anthropic"].messages.create(
        model="claude-sonnet-4-6",
        max_tokens=20000,
        tools=[_CONNECTIONS_TOOL_SCHEMA],
        tool_choice={"type": "tool", "name": "emit_connections"},
        messages=[{"role": "user", "content": prompt}],
    )
    tool_input = None
    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" \
                and getattr(block, "name", None) == "emit_connections":
            tool_input = dict(block.input)
            break
    if tool_input is None:
        raise RuntimeError("emit_connections tool was not invoked")
    # Tool emits `[{source, targets:[{target,relation,reason}]}]`; rewrite
    # to the legacy `{source_num: [{target, relation, reason}]}` shape so
    # the downstream json.loads parser sees the same structure as before.
    legacy = {}
    for entry in tool_input.get("connections", []) or []:
        src = str(entry.get("source", "")).strip()
        if not src:
            continue
        legacy[src] = entry.get("targets", []) or []
    return json.dumps(legacy, ensure_ascii=False)


def _conn_llm_text(clients: dict, prompt: str, label: str = "") -> tuple[str, str]:
    """Try backends in _BACKENDS order with a per-attempt deadline; fall back on
    failure. Circuit-breaks a backend after _CB_TRIP consecutive failures.
    Returns (text, backend_used). Raises if every available backend fails."""
    last_err = None
    for b in _BACKENDS:
        if clients.get(b) is None:
            continue
        with _cb_lock:
            if _cb_fails.get(b, 0) >= _CB_TRIP:
                continue  # tripped — skip for rest of run
        try:
            text = _call_with_deadline(
                lambda: _one_backend_call(b, clients, prompt),
                _ATTEMPT_DEADLINE_S, label=f"{label}:{b}")
            with _cb_lock:
                _cb_fails[b] = 0  # success resets the breaker
            return text, b
        except Exception as e:  # noqa: BLE001
            last_err = e
            with _cb_lock:
                _cb_fails[b] = _cb_fails.get(b, 0) + 1
                tripped = _cb_fails[b] >= _CB_TRIP
            log(f"      [fallback] {b} failed ({type(e).__name__}: {str(e)[:70]})"
                f"{' — CIRCUIT TRIPPED, dropping for rest of run' if tripped else ' → next backend'}")
    raise RuntimeError(f"all backends failed: {type(last_err).__name__}: {str(last_err)[:80]}")


def _call_connections_batch(papers_batch, cat_name, topic, all_paper_lines,
                            cross_cat_lines, clients):
    """논문 배치에 대해 connections 호출. 같은 카테고리 + 다른 카테고리 후보 모두 제공.
    clients 는 {'anthropic': ..., 'openai': ...} dict — backend fallback 용."""

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
    log(f"    [conn-batch:{cat_name[:30]}] calling {'/'.join(_BACKENDS)} ({len(papers_batch)} targets, attempt-deadline={_ATTEMPT_DEADLINE_S}s)...")
    text, used = _conn_llm_text(clients, prompt, label=f"conn-batch:{cat_name[:20]}")
    log(f"    [conn-batch:{cat_name[:30]}] -> {len(text)} chars in {time.time()-_t0:.0f}s (via {used})")
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


BATCH_SIZE = 25


def _process_category(cat_name, papers, topic, clients,
                      all_topic_papers=None):
    """단일 카테고리의 connections 추출. 다른 카테고리 논문도 후보로 제공.
    clients 는 backend fallback dict."""
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
                cross_cat_lines, clients
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


MAX_PARALLEL_CATEGORIES = int(os.environ.get("EXTRACT_INSIGHTS_PARALLEL", "4"))


def extract_paper_connections(topic, cat_papers, clients, all_topic_papers=None,
                              topic_dir=None, topic_slugs=None):
    """카테고리별 병렬로 논문 간 연결 추출. 다른 카테고리 논문도 후보로 제공.

    topic_dir + topic_slugs 가 주어지면 카테고리가 끝날 때마다 누적 결과를
    _paper_connections.json 에 incremental 저장한다 — hang/kill 로 죽어도
    이미 끝난 카테고리의 connections 는 디스크에 보존된다."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_connections = {}
    targets = {cat: papers for cat, papers in cat_papers.items()
                if cat != "Other" and len(papers) >= 3}

    def _persist():
        if topic_dir is None or topic_slugs is None:
            return
        try:
            from lib.connections import sync_topic_connections
            sync_topic_connections(all_connections, topic, topic_slugs, topic_dir, log=log)
        except Exception as e:
            log(f"  [incremental-save] failed: {str(e)[:100]}")

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_CATEGORIES) as executor:
        futures = {
            executor.submit(_process_category, cat_name, papers, topic, clients,
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
                # Incremental checkpoint: persist after every finished category
                _persist()
                log(f"  [incremental-save] {cat_name} → {len(all_connections)} papers w/ connections saved")
            except Exception as e:
                log(f"  {cat_name} FAILED: {str(e)[:100]}")

    return all_connections


def _run_insights(topic="ai4s", *, insights_only=False, connections_only=False,
                   categories=None):
    """Programmatic entrypoint for extract_insights."""
    topic_dir = str(get_topic_dir(topic))

    log(f"Loading {topic} data...")
    topic_papers, cat_papers, cat_summaries = load_topic_data(topic)

    if categories:
        cat_papers = {k: v for k, v in cat_papers.items() if k in categories}
        cat_summaries = [s for s in cat_summaries if s.get("category") in categories]
        log(f"  {len(topic_papers)} papers total, {len(cat_papers)} categories (filtered)")
    else:
        log(f"  {len(topic_papers)} papers, {len(cat_papers)} categories")

    clients: dict = {"anthropic": None, "openai": None}
    try:
        clients["anthropic"] = Anthropic(timeout=120.0, max_retries=1)
    except Exception as e:
        log(f"  [backend] Anthropic init failed: {str(e)[:80]}")
    try:
        from openai import OpenAI
        _oai_key = os.environ.get("OPENAI_API_KEY") or load_config().get("openai_api_key", "")
        if _oai_key:
            clients["openai"] = OpenAI(api_key=_oai_key, timeout=120.0, max_retries=1)
    except Exception as e:
        log(f"  [backend] OpenAI init failed: {str(e)[:80]}")
    client = clients["anthropic"] or clients["openai"]
    log(f"  [backend] connection fallback chain: {' → '.join(b for b in _BACKENDS if clients.get(b))}")
    run_insights = not connections_only
    run_connections = not insights_only

    if run_insights:
        log("\n" + "=" * 50)
        log("CROSS-CATEGORY INSIGHTS (Sonnet)")
        log("=" * 50)

        insights = extract_cross_category_insights(topic, cat_papers, cat_summaries, client)
        insights["generated_at"] = datetime.now().strftime("%Y-%m-%d")
        insights["topic"] = topic
        insights["paper_count"] = len(topic_papers)

        insights_path = os.path.join(topic_dir, "_insights.json")
        if categories and os.path.exists(insights_path):
            with open(insights_path, "r", encoding="utf-8") as f:
                existing_insights = json.load(f)
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

    if run_connections:
        log("\n" + "=" * 50)
        log("PAPER CONNECTIONS (Sonnet)")
        log("=" * 50)

        topic_slugs = [p["slug"] for p in topic_papers]
        connections = extract_paper_connections(
            topic, cat_papers, clients, topic_papers,
            topic_dir=topic_dir, topic_slugs=topic_slugs)

        from lib.connections import sync_topic_connections
        sync_topic_connections(connections, topic, topic_slugs, topic_dir, log=log)

    log("\nDone!")


def main():
    parser = argparse.ArgumentParser(description="Extract cross-paper insights and connections")
    parser.add_argument("--topic", default="ai4s")
    parser.add_argument("--insights-only", action="store_true", help="Cross-category insights only")
    parser.add_argument("--connections-only", action="store_true", help="Paper connections only")
    parser.add_argument("--only", choices=["connections", "insights", "all"], default="all",
                        help="생성 대상 선택. connections=paper connections(Core)만, "
                             "insights=cross-category insights(Option)만, all=둘 다(기본, 하위호환).")
    parser.add_argument("--categories", nargs="+", help="Specific categories to process (others preserved)")
    args = parser.parse_args()
    # --only 를 기존 *_only 게이트로 매핑 (둘 다 동일 효과; --insights-only/--connections-only 와 OR).
    insights_only = args.insights_only or args.only == "insights"
    connections_only = args.connections_only or args.only == "connections"
    _run_insights(topic=args.topic, insights_only=insights_only,
                  connections_only=connections_only, categories=args.categories)


if __name__ == "__main__":
    main()
