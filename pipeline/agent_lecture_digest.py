#!/usr/bin/env python3
"""자율 강의 다이제스트 엔진 — Dashun Wang 커리큘럼의 한 강을 처리한다.

강 1개 → 핵심 논문 + 관련 논문(연결 1-hop) 근거 수집 → Gemini 심화 리포트(방법론·메시지 축)
→ 50분 Audio Overview(2인·전문가·학술·한국어) → 자립형 HTML → 제N강·오늘의 학습목표를 명시해
이메일 발송(다중 수신자) → 원장(curriculum.json)에 done 기록.

맥미니에서 launchd 로 06:00 / 16:00 (+ 최초 킥오프 23:00) 발화:
    python pipeline/agent_lecture_digest.py --due        # 지금 시각 기준 다음 예정 강 1개
    python pipeline/agent_lecture_digest.py --lecture 1  # 특정 강 강제
    python pipeline/agent_lecture_digest.py --lecture 1 --no-audio   # 오디오 없이 리포트+메일만(검증)
"""
import argparse, json, os, re, sys, base64, urllib.request, urllib.error
import html as H
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

PIPE = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPE))
from config_loader import PAPERS_DIR, DOCS_DIR, get_google_key  # noqa: E402
from generate_audio import (  # noqa: E402
    build_prompt, parse_turns, chunk_turns, chunk_paragraphs, tts_call, concat_pcm,
    speech_multi, speech_single, ROLES, TTS_PREFIX, SAMPLE_RATE, MAX_CHUNK_CHARS,
)
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402
import lameenc  # noqa: E402

PAPERS = Path(PAPERS_DIR)
DOCS = Path(DOCS_DIR)
# 산출물·원장은 맥미니 전용 디렉토리에 누적 (docs/ 밖 → pc_sync·git 과 분리, 에이전트 소유).
AGENT_DIR = Path(os.environ.get("PC_AGENT_DIR", str(Path.home() / "pc_agent" / "dashun_wang")))
LEDGER = AGENT_DIR / "curriculum.json"
OUTDIR = AGENT_DIR / "lectures"
REPORT_MODEL = "gemini-3.1-pro-preview"
TTS_WORKERS = 4

def load_ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save_ledger(led):
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 근거 수집 ──────────────────────────────────────────────────────────────
def _find_dir(slug):
    if (PAPERS / slug).is_dir():
        return PAPERS / slug
    for d in PAPERS.iterdir():
        if d.is_dir() and d.name.startswith(slug.split("_")[0] + "_"):
            return d
    return None


def read_review(slug, cap=2800):
    d = _find_dir(slug)
    if not d:
        return ""
    rp = d / "review.md"
    if not rp.exists():
        return ""
    t = rp.read_text(encoding="utf-8")
    while t.startswith("---"):                      # strip YAML frontmatter
        lines = t.split("\n")
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is None:
            break
        t = "\n".join(lines[end + 1:]).lstrip("\n")
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)       # drop image embeds
    return t.strip()[:cap]


_CONN_CACHE = None
def all_connections():
    global _CONN_CACHE
    if _CONN_CACHE is not None:
        return _CONN_CACHE
    merged = {}
    for cp in DOCS.glob("*/_paper_connections.json"):
        try:
            conn = json.loads(cp.read_text(encoding="utf-8"))
        except Exception:
            continue
        for slug, edges in conn.items():
            merged.setdefault(slug, [])
            seen = {(e.get("slug"), e.get("relation")) for e in merged[slug]}
            for e in edges if isinstance(edges, list) else []:
                k = (e.get("slug"), e.get("relation"))
                if k not in seen:
                    merged[slug].append(e); seen.add(k)
    _CONN_CACHE = merged
    return merged


def title_of(slug):
    d = _find_dir(slug)
    if d:
        rp = d / "review.md"
        if rp.exists():
            m = re.search(r'(?m)^title:\s*"?(.+?)"?\s*$', rp.read_text(encoding="utf-8")[:2000])
            if m:
                return m.group(1)
    return slug.split("_", 1)[-1].replace("_", " ")


def gather_evidence(lecture, related_per_paper=2, related_cap=8):
    conns = all_connections()
    core = lecture["papers"]
    core_slugs = {p["slug"] for p in core}
    blocks = ["## 핵심 논문 (이 강의 대상)"]
    for p in core:
        rv = read_review(p["slug"])
        blocks.append(f"### ({p['year']}) {p['title']}\n{rv or '(리뷰 없음)'}")
    # related 1-hop
    rel, seen = [], set()
    for p in core:
        for e in (conns.get(p["slug"]) or [])[:related_per_paper]:
            rs = e.get("slug")
            if not rs or rs in core_slugs or rs in seen:
                continue
            seen.add(rs)
            rel.append(f"- [{e.get('relation','관련')}] {title_of(rs)} — {e.get('reason','')}")
            if len(rel) >= related_cap:
                break
        if len(rel) >= related_cap:
            break
    if rel:
        blocks.append("## 방법론적으로 연결된 관련 논문 (맥락)\n" + "\n".join(rel))
    return "\n\n".join(blocks)


# ── 리포트 합성 (심화 Deeper) ───────────────────────────────────────────────
def synthesize_report(course, lecture, evidence, client):
    obj = "\n".join(f"  {i+1}. {o}" for i, o in enumerate(lecture["objectives"]))
    plist = ", ".join(f"({p['year']}) {p['title']}" for p in lecture["papers"])
    prompt = (
        f"당신은 '{course}' 심화 강의를 집필하는 전문 연구자입니다. 이것은 **제{lecture['lecture']}강: {lecture['title']}** 입니다.\n\n"
        f"오늘의 학습목표:\n{obj}\n\n"
        f"이 강이 다루는 논문: {plist}\n\n"
        "아래 근거(핵심 논문 리뷰 + 관련 논문 맥락)를 바탕으로 심층 한국어 강의 리포트를 작성하세요.\n"
        "규칙:\n"
        "- 학습목표 3개를 모두 충실히 충족.\n"
        "- 논문을 단순 나열하지 말고 **연구 방법론·핵심 메시지 축**으로 엮고 연구 계보를 짚을 것.\n"
        "- 전문가 청중, 학술적 톤. 논문을 언급할 때 (제목, 연도)를 본문에 자연스럽게 명시.\n"
        "- 마크다운(## 소제목, 단락). 서론 → 방법론/주제별 본론 → 종합·시사점 구조. **3500자 이상** 충실히.\n"
        "- 메타 설명·머리말 없이 곧바로 강의 본문으로 시작.\n\n"
        f"=== 근거 ===\n{evidence}"
    )
    resp = client.models.generate_content(
        model=REPORT_MODEL, contents=prompt,
        config=types.GenerateContentConfig(temperature=0.6, max_output_tokens=32768))
    return (resp.text or "").strip()


# ── 오디오 (50분·2인·전문가·학술·한국어) ─────────────────────────────────────
def make_audio(report_text, client, minutes=50):
    lang, speakers = "ko", 2
    roles = ROLES[lang][speakers]
    direction = "질문·주제에 대한 답을 중심으로, 핵심 논문들을 방법론과 메시지로 엮어 전체 계보와 통찰을 심층 설명한다."
    prompt = build_prompt(report_text, [], speakers, lang, "expert", minutes, "academic", "", direction)
    resp = client.models.generate_content(
        model="gemini-3.1-pro-preview", contents=prompt,
        config=types.GenerateContentConfig(temperature=0.85, max_output_tokens=65536))
    script = (resp.text or "").strip()
    if not script:
        raise RuntimeError("대본 생성 실패")
    labels = [r["label"] for r in roles]
    turns = parse_turns(script, labels)
    if turns:
        chunks = chunk_turns(turns, MAX_CHUNK_CHARS); cfg = speech_multi(roles); prefix = TTS_PREFIX[lang]
        get = lambda i: prefix + chunks[i]
    else:
        chunks = chunk_paragraphs(script, MAX_CHUNK_CHARS); cfg = speech_single(roles[0]["voice"]); get = lambda i: chunks[i]
    print(f"    TTS {len(chunks)} chunks ...", flush=True)
    parts = [None] * len(chunks)
    with ThreadPoolExecutor(max_workers=TTS_WORKERS) as ex:
        futs = {ex.submit(tts_call, client, get(i), cfg): i for i in range(len(chunks))}
        done = 0
        for fut in futs:
            pass
        from concurrent.futures import as_completed
        for fut in as_completed(futs):
            i = futs[fut]; parts[i] = fut.result(); done += 1
            print(f"      [{done}/{len(chunks)}]", flush=True)
    pcm = concat_pcm([p for p in parts if p])
    enc = lameenc.Encoder(); enc.set_bit_rate(64); enc.set_in_sample_rate(SAMPLE_RATE); enc.set_channels(1); enc.set_quality(2)
    mp3 = enc.encode(pcm) + enc.flush()
    dur_min = len(pcm) / 2 / SAMPLE_RATE / 60
    return mp3, script, dur_min


# ── HTML ────────────────────────────────────────────────────────────────────
def md_to_html(md):
    out = []
    for block in re.split(r"\n\s*\n", md):
        b = block.strip()
        if not b:
            continue
        if b.startswith("### "):
            out.append(f"<h3>{H.escape(b[4:])}</h3>")
        elif b.startswith("## "):
            out.append(f"<h2>{H.escape(b[3:])}</h2>")
        elif b.startswith("# "):
            out.append(f"<h2>{H.escape(b[2:])}</h2>")
        else:
            t = H.escape(b).replace("\n", "<br>")
            t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
            out.append(f"<p>{t}</p>")
    return "\n".join(out)


def make_html(course, lecture, report_md):
    obj = "".join(f"<li>{H.escape(o)}</li>" for o in lecture["objectives"])
    papers = "".join(f"<li>({H.escape(str(p['year']))}) {H.escape(p['title'])}</li>" for p in lecture["papers"])
    body = md_to_html(report_md)
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>제{lecture['lecture']}강 — {H.escape(lecture['title'])}</title>
<style>
body{{font-family:'KoPub Dotum',-apple-system,'Noto Sans KR',sans-serif;line-height:1.8;color:#222;max-width:820px;margin:0 auto;padding:2rem 1.4rem;background:#fbfbfd}}
.hero{{background:linear-gradient(135deg,#1a0d2a,#3a1a5c 55%,#6b21a8);color:#fff;border-radius:16px;padding:1.8rem 1.6rem;margin-bottom:1.6rem}}
.hero .kicker{{opacity:.8;font-size:.85rem;font-weight:600}}
.hero h1{{font-size:1.35rem;margin:.35rem 0 .2rem}}
.card{{background:#fff;border:1px solid #eee;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:1.3rem}}
.card h3{{font-size:.95rem;color:#6B21A8;margin-bottom:.5rem}}
.card ul{{margin:0 0 0 1.1rem}} .card li{{margin:.2rem 0}}
h2{{font-size:1.12rem;color:#6B21A8;margin:1.6rem 0 .6rem;border-bottom:1px solid #eee;padding-bottom:.3rem}}
h3{{font-size:1rem;margin:1.1rem 0 .4rem}}
p{{margin:.6rem 0}}
.foot{{color:#999;font-size:.82rem;border-top:1px solid #eee;margin-top:2rem;padding-top:1rem}}
</style></head><body>
<div class="hero"><div class="kicker">{H.escape(course)} · 제{lecture['lecture']}강 / {{TOTAL}}</div>
<h1>{H.escape(lecture['title'])}</h1><div style="opacity:.85;font-size:.9rem">{H.escape(lecture['scheduled_at'])}</div></div>
<div class="card"><h3>🎯 오늘의 학습목표</h3><ul>{obj}</ul></div>
<div class="card"><h3>📄 다루는 논문 ({len(lecture['papers'])}편)</h3><ul>{papers}</ul></div>
{body}
<div class="foot">Dashun Wang 연구 흐름 따라잡기 · 자동 생성 다이제스트 · Paper Curation</div>
</body></html>"""


# ── 이메일 (Resend, 다중 수신자, UA로 CF 1010 우회) ──────────────────────────
def send_email(recipients, subject, html_body, attachments):
    resend = os.environ.get("RESEND_API_KEY", "")
    if not resend:
        raise RuntimeError("RESEND_API_KEY 없음")
    lk = {}
    p = DOCS / "_local_keys.json"
    if p.exists():
        lk = json.loads(p.read_text(encoding="utf-8"))
    payload = {
        "from": lk.get("audio_from") or "Paper Curation <onboarding@resend.dev>",
        "to": recipients,
        "subject": subject,
        "html": html_body,
        "attachments": [{"filename": fn, "content": base64.b64encode(data).decode()} for fn, data in attachments],
    }
    if lk.get("audio_reply_to"):
        payload["reply_to"] = lk["audio_reply_to"]
    req = urllib.request.Request(
        "https://api.resend.com/emails", data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + resend, "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (paper-curation lecture agent)"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]


# ── 오케스트레이션 ───────────────────────────────────────────────────────────
def pick_lecture(led, args):
    lecs = led["lectures"]
    if args.lecture:
        for L in lecs:
            if L["lecture"] == args.lecture:
                return L
        sys.exit(f"제{args.lecture}강 없음")
    now = datetime.now()
    due = [L for L in lecs if L.get("status") != "done"
           and datetime.strptime(L["scheduled_at"], "%Y-%m-%d %H:%M") <= now]
    if not due:
        print("[agent] 지금 발화할 예정 강 없음."); return None
    return min(due, key=lambda L: L["scheduled_at"])


def run_lecture(L, led, args):
    total = led["total"]
    course = led["course"]
    recipients = led["recipients"]
    print(f"[agent] 제{L['lecture']}강/{total} · {L['title']} · {len(L['papers'])}편")
    client = genai.Client(api_key=get_google_key())

    print("  1) 근거 수집")
    evidence = gather_evidence(L)
    print(f"     근거 {len(evidence):,}자")
    print("  2) 심화 리포트 합성")
    report = synthesize_report(course, L, evidence, client)
    if not report:
        sys.exit("리포트 합성 실패")
    print(f"     리포트 {len(report):,}자")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    html = make_html(course, L, report).replace("{TOTAL}", str(total))
    html_path = OUTDIR / f"lecture_{L['lecture']:02d}.html"
    html_path.write_text(html, encoding="utf-8")
    (OUTDIR / f"lecture_{L['lecture']:02d}_report.md").write_text(report, encoding="utf-8")

    attachments = [(f"제{L['lecture']}강_{re.sub(r'[^가-힣A-Za-z0-9]+','_',L['title'])[:30]}.html", html.encode("utf-8"))]
    dur_txt = "리포트만"
    if not args.no_audio:
        print("  3) 50분 오디오 생성")
        mp3, script, dur = make_audio(report, client, minutes=led.get("audio", {}).get("minutes", 50))
        mp3_path = OUTDIR / f"lecture_{L['lecture']:02d}.mp3"
        mp3_path.write_bytes(mp3)
        (OUTDIR / f"lecture_{L['lecture']:02d}_script.txt").write_text(script, encoding="utf-8")
        attachments.append((f"제{L['lecture']}강.mp3", mp3))
        dur_txt = f"{len(mp3)/1048576:.1f}MB · ~{dur:.0f}분"
        print(f"     {dur_txt}")

    print("  4) 이메일 발송")
    obj_html = "".join(f"<li>{H.escape(o)}</li>" for o in L["objectives"])
    plist_html = "".join(f"<li>({p['year']}) {H.escape(p['title'])}</li>" for p in L["papers"])
    body = (f"<p><b>{H.escape(course)} · 제{L['lecture']}강 / {total}</b></p>"
            f"<h2>{H.escape(L['title'])}</h2>"
            f"<p><b>🎯 오늘의 학습목표</b></p><ul>{obj_html}</ul>"
            f"<p><b>📄 다루는 논문 ({len(L['papers'])}편)</b></p><ul>{plist_html}</ul>"
            f"<p>첨부: Deeper Research 리포트(HTML)" + ("" if args.no_audio else " + 50분 Audio Overview(MP3, 2인·전문가·학술)") + "</p>"
            f"<p style='color:#999;font-size:.85rem'>Paper Curation 자동 발송 · {L['scheduled_at']}</p>")
    subject = f"[제{L['lecture']}강/{total}] {L['title']}"
    st, resp = send_email(recipients, subject, body, attachments)
    ok = st == 200
    print(f"     이메일 {'성공' if ok else '실패'} (status {st}) {resp}  → {recipients}")

    if ok and not args.no_audio:
        L["status"] = "done"
        L["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        L["artifacts"] = {"html": str(html_path), "audio_mb": round(len(mp3) / 1048576, 1)}
        save_ledger(led)
        print(f"[agent] 제{L['lecture']}강 done 기록.")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Dashun Wang 강의 다이제스트 엔진")
    ap.add_argument("--lecture", type=int, help="특정 강 번호 강제")
    ap.add_argument("--due", action="store_true", help="지금 시각 기준 다음 예정 강 1개")
    ap.add_argument("--no-audio", action="store_true", help="오디오 생략(리포트+메일만, 검증용)")
    args = ap.parse_args()
    if not args.lecture and not args.due:
        ap.error("--lecture N 또는 --due 필요")
    led = load_ledger()
    L = pick_lecture(led, args)
    if L is None:
        return 0
    run_lecture(L, led, args)
    return 0


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    sys.exit(main())
