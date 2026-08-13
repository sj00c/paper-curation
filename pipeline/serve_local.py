#!/usr/bin/env python3
"""로컬 미리보기 서버 — docs/ 정적 서빙 + /api/embed Gemini 프록시.

`python -m http.server` 는 정적 파일만 돌려주므로, Deep Research UI 가
같은 출처(`/api/embed`) 로 쿼리 임베딩을 요청하면 응답하지 못한다. 이
스크립트는 docs/ 를 그대로 서빙하면서 `/api/embed` POST 를 운영자의
Gemini 키로 프록시해 로컬 미리보기에서도 검색이 동작하게 한다.

- GET                 → docs/ 정적 파일 (mime 자동, 디렉토리는 index.html)
- POST /api/embed     → {"text": ...} → gemini-embedding-001 (768d,
                        taskType RETRIEVAL_QUERY) → L2 정규화 후
                        {"embedding": [...], "model": ..., "dim": 768}
추가 의존성 없음 — 표준 라이브러리만 사용.

키 우선순위:
- 임베딩: GOOGLE_API_KEY/GEMINI_API_KEY env → config.json
  (gemini_api_key/google_api_key) → docs/_local_keys.json (google_key/gemini_key).
"""

import argparse
import functools
import json
import math
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# config_loader 를 그대로 재사용 (sys.path 트릭 — config_loader 는 건드리지 않는다).
PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"
sys.path.insert(0, str(PIPELINE_DIR))
try:
    from config_loader import load_config
except Exception:  # config.json 없거나 import 실패해도 env/_local_keys 로 동작
    load_config = None

# Gemini 임베딩 설정 (인덱스 빌드와 동일 — RETRIEVAL_QUERY 만 다르다).
GEMINI_MODEL = "gemini-embedding-001"
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:embedContent"
)
EMBED_DIM = 768
MAX_REQUEST_BYTES = 2 * 1024 * 1024

_CA_BUNDLE = os.environ.get("PAPER_CURATION_CA_BUNDLE", "").strip()
_ssl_ctx = ssl.create_default_context(cafile=_CA_BUNDLE or None)

_GOOGLE_KEY_CACHE = None


def resolve_google_key():
    """Gemini 키 조회. env → config.json → docs/_local_keys.json 순. 캐싱(비어있으면 재시도)."""
    global _GOOGLE_KEY_CACHE
    if _GOOGLE_KEY_CACHE:
        return _GOOGLE_KEY_CACHE

    # 공용 해석기가 env → config.json 을 담당한다. 여기서 직접 읽으면
    # PAPER_CURATION_NO_GEMINI off 스위치가 이 경로에서만 무시된다.
    key = ""
    try:
        from config_loader import get_google_key
        key = get_google_key() or ""
    except Exception:
        key = ""

    # docs/_local_keys.json 은 로컬 서버 전용 보조 경로다. off 스위치가
    # 켜져 있으면 여기서도 되살리지 않는다.
    if not key and not os.environ.get("PAPER_CURATION_NO_GEMINI"):
        local_keys = DOCS_DIR / "_local_keys.json"
        if local_keys.exists():
            try:
                data = json.loads(local_keys.read_text(encoding="utf-8"))
                key = data.get("google_key") or data.get("gemini_key") or ""
            except Exception:
                key = ""

    if key:
        _GOOGLE_KEY_CACHE = key
    return key


def gemini_embed(text, api_key):
    """gemini-embedding-001 으로 쿼리 임베딩 → L2 정규화한 768d 리스트 반환.

    중요: output_dimensionality != 3072 이면 Gemini 가 비정규화 벡터를 돌려준다.
    int8 양자화/코사인 비교 전에 반드시 L2 정규화해야 인덱스와 스케일이 맞는다.
    """
    payload = {
        "model": f"models/{GEMINI_MODEL}",
        "content": {"parts": [{"text": text}]},
        "taskType": "RETRIEVAL_QUERY",
        "outputDimensionality": EMBED_DIM,
    }
    req = urllib.request.Request(
        GEMINI_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
        out = json.load(resp)

    values = (out.get("embedding") or {}).get("values") or []
    if not values:
        raise ValueError("Gemini 응답에 embedding.values 가 없습니다: " + json.dumps(out)[:200])

    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


class LocalHandler(SimpleHTTPRequestHandler):
    """docs/ 정적 서빙 + /api/* POST 핸들러."""

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "frame-ancestors 'none'; base-uri 'self'; object-src 'none'",
        )
        super().end_headers()

    def do_GET(self):  # noqa: N802 (stdlib 규약)
        route = self.path.split("?", 1)[0]
        if route == "/api/health":
            self._send_json(200, {
                "ok": True,
                "service": "paper-curation-serve-local",
            })
            return
        return super().do_GET()

    def _send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length > MAX_REQUEST_BYTES:
            raise ValueError(f"request body exceeds {MAX_REQUEST_BYTES} bytes")
        return self.rfile.read(length) if length > 0 else b""

    def do_POST(self):  # noqa: N802 (stdlib 규약)
        origin = self.headers.get("Origin", "")
        if origin:
            origin_host = (urllib.parse.urlsplit(origin).hostname or "").casefold()
            request_host = (
                urllib.parse.urlsplit("//" + self.headers.get("Host", "")).hostname
                or ""
            ).casefold()
            bound_host = str(self.server.server_address[0]).casefold()
            loopback = {"localhost", "127.0.0.1", "::1"}
            if origin_host != request_host or (
                    bound_host in {"127.0.0.1", "::1"} and request_host not in loopback):
                self._send_json(403, {"error": "cross-origin request rejected"})
                return
        route = self.path.split("?", 1)[0]
        if route == "/api/embed":
            self._handle_embed()
        elif route == "/api/citedby-answer":
            self._handle_citedby_answer()
        elif route == "/api/citedby":
            self._handle_citedby()
        else:
            self._send_json(404, {"error": "not found"})

    # ── Citedby (인용논문 분석) — NDJSON 스트리밍 ──────────────────────────
    #
    # 분석은 수 분이 걸린다. 한 번에 응답하면 브라우저가 죽은 것처럼 보이므로
    # 진행 이벤트를 한 줄에 하나씩(JSON) 흘려보낸다. HTTP/1.0 + Content-Length
    # 생략이면 연결 종료가 곧 스트림 끝이라 별도 chunked 인코딩이 필요 없다.
    # 클라이언트는 fetch() + ReadableStream 으로 읽는다 (Deep Research 와 동일 패턴).
    def _stream_line(self, obj):
        try:
            self.wfile.write(
                (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
            self.wfile.flush()
            return True
        except (BrokenPipeError, ConnectionResetError):
            return False    # 사용자가 탭을 닫았거나 중단했다

    # ── Deep Research 답변 생성 ────────────────────────────────────────────
    #
    # **키는 브라우저로 내려보내지 않는다.** 로컬 전용이므로 서버가 이미 가진
    # 키(env → config.json)로 서버에서 호출하고 텍스트만 돌려준다. 예전엔 리포트
    # 화면에서 사용자가 키를 붙여넣게 했는데, 로컬 환경에서는 불필요한 노출이다.
    def _handle_citedby_answer(self):
        try:
            req = json.loads(self._read_body() or b"{}")
        except Exception as e:
            self._send_json(400, {"error": f"invalid JSON body: {e}"})
            return

        prompt = (req.get("prompt") or "").strip()
        if not prompt:
            self._send_json(400, {"error": "missing 'prompt'"})
            return
        try:
            max_tokens = int(req.get("max_tokens") or 16000)
        except (TypeError, ValueError):
            max_tokens = 16000
        max_tokens = max(256, min(max_tokens, 24000))
        web_search = bool(req.get("web_search", False))
        purpose = "plan" if req.get("purpose") == "plan" else "answer"
        if purpose == "plan":
            web_search = False
            max_tokens = min(max_tokens, 2000)

        sys.path.insert(0, str(PIPELINE_DIR))
        try:
            from lib.citedby.topic_filter import PLAN_MODELS, llm_text_stream
        except Exception as e:
            self._send_json(500, {"error": f"citedby 모듈 로드 실패: {e}"})
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        alive = {"ok": True}

        def emit_delta(text):
            if alive["ok"]:
                alive["ok"] = self._stream_line({
                    "event": "delta", "text": text,
                })

        def emit_event(event, payload):
            if not alive["ok"]:
                return
            data = {"event": event}
            if isinstance(payload, dict):
                data.update(payload)
            alive["ok"] = self._stream_line(data)
        try:
            answer, provider, model = llm_text_stream(
                prompt, emit_delta, max_tokens=max_tokens,
                web_search=web_search,
                models=(PLAN_MODELS if purpose == "plan" else None),
                on_event=emit_event)
        except Exception as e:  # noqa: BLE001 — 스트림 안 오류로 전달
            self._stream_line({"event": "error", "message": str(e)[:400]})
            return
        if not answer:
            self._stream_line({
                "event": "error",
                "message": "답변 생성 실패 — LLM 키가 없거나 모든 provider가 "
                           "실패했습니다. 서버 로그를 확인하세요.",
            })
            return
        self._stream_line({
            "event": "done", "provider": provider, "model": model,
            "chars": len(answer), "purpose": purpose,
        })

    def _handle_citedby(self):
        try:
            req = json.loads(self._read_body() or b"{}")
        except Exception as e:
            self._send_json(400, {"error": f"invalid JSON body: {e}"})
            return

        doi = (req.get("doi") or "").strip()
        if not doi:
            self._send_json(400, {"error": "missing 'doi'"})
            return

        sources = req.get("sources") or None
        topic = (req.get("topic") or "").strip()
        lang = (req.get("lang") or "ko").strip()
        slug = (req.get("slug") or "").strip()
        use_llm = bool(req.get("use_llm_originality", True))

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        alive = {"ok": True}

        def on_event(phase, message, current=0, total=0):
            if not alive["ok"]:
                return
            alive["ok"] = self._stream_line({
                "event": "progress", "phase": phase, "message": message,
                "current": current, "total": total,
            })

        try:
            # 지연 import — citedby 를 안 쓰는 서버 기동에 pandas 비용을 물리지 않는다.
            from lib.citedby import run_citedby
            result = run_citedby(doi, sources=sources, topic=topic, lang=lang,
                                 use_llm_originality=use_llm, on_event=on_event)
        except Exception as e:
            self._stream_line({"event": "error", "message": str(e)[:400]})
            return

        files = self._save_citedby_outputs(slug, result)
        self._stream_line({
            "event": "done",
            "doi": result["doi"],
            "matched": result["matched"],
            "total": result["total"],
            "elapsed_sec": result["elapsed_sec"],
            "source_counts": result["source_counts"],
            "report_html": result["report_html"],
            "files": files,
        })

    def _save_citedby_outputs(self, slug, result):
        """리포트/CSV 를 docs/papers/{slug}/citedby/ 에 저장하고 URL 을 돌려준다.

        slug 가 없으면 저장을 건너뛴다. docs/papers/ 는 gitignore +
        .assetsignore 대상이라 저장소·배포를 오염시키지 않는다.
        """
        if not slug:
            return {}
        # 경로 소독 2단: 허용 문자만 남기고 → 남은 점 연속(`..`)을 접는다.
        # 문자 필터만으로는 "../../etc/evil" 이 "....etcevil" 로 남아 경로
        # 성분에 `..` 가 살아난다.
        safe = re.sub(r"[^A-Za-z0-9._-]", "", slug)
        safe = re.sub(r"\.{2,}", ".", safe).strip("._-")
        if not safe:
            return {}
        papers_root = (DOCS_DIR / "papers").resolve()
        out_dir = (papers_root / safe / "citedby").resolve()
        # 봉쇄 검증 — 어떤 입력이 와도 papers/ 밖에는 쓰지 않는다.
        if not str(out_dir).startswith(str(papers_root) + os.sep):
            print(f"  [citedby] slug 거부(경로 이탈): {slug!r}")
            return {}
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            from lib.dateutil import now_local
            stamp = now_local().strftime("%y%m%d_%H%M")
            files = {}
            report_path = out_dir / f"report_{stamp}.html"
            report_path.write_text(result["report_html"], encoding="utf-8")
            files["report"] = f"/papers/{safe}/citedby/{report_path.name}"
            if result.get("csv"):
                csv_path = out_dir / f"citing_{stamp}.csv"
                csv_path.write_text(result["csv"], encoding="utf-8")
                files["csv"] = f"/papers/{safe}/citedby/{csv_path.name}"
            return files
        except OSError as e:
            print(f"  [citedby] 저장 실패: {e}")
            return {}

    def _handle_embed(self):
        try:
            req = json.loads(self._read_body() or b"{}")
        except Exception as e:
            self._send_json(400, {"error": f"invalid JSON body: {e}"})
            return

        text = (req.get("text") or "").strip()
        if not text:
            self._send_json(400, {"error": "missing 'text'"})
            return

        api_key = resolve_google_key()
        if not api_key:
            self._send_json(503, {
                "error": "Gemini 키 없음 — GOOGLE_API_KEY env 또는 "
                         "config.json(gemini_api_key) 를 설정하세요.",
            })
            return

        try:
            vec = gemini_embed(text, api_key)
        except urllib.error.HTTPError as e:
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                detail = str(e)
            self._send_json(502, {"error": f"Gemini embed {e.code}: {detail}"})
            return
        except Exception as e:
            self._send_json(502, {"error": f"Gemini embed 실패: {e}"})
            return

        self._send_json(200, {"embedding": vec, "model": GEMINI_MODEL, "dim": len(vec)})



def main():
    parser = argparse.ArgumentParser(
        description="docs/ 정적 서빙 + /api/embed Gemini 프록시 (로컬 미리보기용)"
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="바인드 주소 (기본 127.0.0.1; 외부 공개는 명시 필요)")
    parser.add_argument("--port", type=int, default=8000, help="리슨 포트 (기본 8000)")
    parser.add_argument("--topic", default="", help="열어볼 토픽 alias (URL 안내용)")
    args = parser.parse_args()

    if not DOCS_DIR.exists():
        print(f"ERROR: docs 디렉토리를 찾을 수 없습니다: {DOCS_DIR}", file=sys.stderr)
        sys.exit(1)

    sub = (args.topic.strip("/") + "/") if args.topic else ""
    display_host = "localhost" if args.host in {"127.0.0.1", "::1"} else args.host
    url = f"http://{display_host}:{args.port}/{sub}"

    handler = functools.partial(LocalHandler, directory=str(DOCS_DIR))
    httpd = ThreadingHTTPServer((args.host, args.port), handler)

    has_key = bool(resolve_google_key())
    print(f"docs/ 서빙 + /api/embed → Gemini ({GEMINI_MODEL}, {EMBED_DIM}d) 프록시")
    print(f"Gemini 키: {'감지됨' if has_key else '없음 (검색 임베딩 비활성 — 키 설정 필요)'}")
    print(f"열기: {url}")
    if (DOCS_DIR / "_cross" / "index.html").exists():
        print(f"통합 Deep Research (로컬 전용): http://{display_host}:{args.port}/_cross/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
