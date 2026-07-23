"""
pipeline/doctor.py — 설치 환경 일괄 진단 도구.

신규 사용자가 설치 후 "왜 안 되지"를 5초 만에 알 수 있도록, 파이프라인 실행에
필요한 환경(인터프리터·패키지·Java·config·API 키·Zotero·node·산출물)을 한 번에
점검한다. 각 항목은 ✓(정상) / △(선택·경고) / ✗(필수 실패) 로 표시하고, 실패하면
바로 아래에 한 줄 해결법을 붙인다.

이 도구는 진단이 목적이므로 _env_guard.force_py312() 를 호출하지 않는다 — 잘못된
인터프리터로 실행돼도 그 사실을 보고해야 하기 때문이다. config.json / 네트워크가
깨져 있어도 끝까지 돌 수 있도록 모든 검사를 방어적으로 감싼다.

Usage:
  PYTHONUTF8=1 python pipeline/doctor.py                    # 로컬 환경만 점검
  PYTHONUTF8=1 python pipeline/doctor.py --network          # Zotero API 연결까지
  PYTHONUTF8=1 python pipeline/doctor.py --topic humanoid   # 특정 토픽 산출물까지

종료코드: 필수 항목이 하나라도 ✗ 이면 1, 아니면 0.
"""

import argparse
import importlib
import json
import os
import shutil
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path
from types import SimpleNamespace
try:
    from anthropic_auth import (
        MIN_CLAUDE_CODE_VERSION,
        auth_status,
        claude_version,
        run_structured_smoke,
    )
except Exception:
    MIN_CLAUDE_CODE_VERSION = (2, 1, 205)
    claude_version = None
    auth_status = None
    run_structured_smoke = None

try:
    from lib.search_index_metadata import (
        EMBEDDING_SIDECAR_FILE,
        KEY_EMBEDDING_DIMENSION,
        KEY_EMBEDDING_MODEL,
        canonicalize_cache_metadata,
        canonicalize_index_metadata,
        format_validation_errors,
        validate_cache_metadata,
        validate_index_metadata,
        validate_known_safe_legacy_cache,
        validate_known_safe_legacy_index,
    )
except ModuleNotFoundError:
    from pipeline.lib.search_index_metadata import (
        EMBEDDING_SIDECAR_FILE,
        KEY_EMBEDDING_DIMENSION,
        KEY_EMBEDDING_MODEL,
        canonicalize_cache_metadata,
        canonicalize_index_metadata,
        format_validation_errors,
        validate_cache_metadata,
        validate_index_metadata,
        validate_known_safe_legacy_cache,
        validate_known_safe_legacy_index,
    )

PIPELINE_DIR = Path(__file__).resolve().parent
REPO = PIPELINE_DIR.parent
CONFIG_PATH = REPO / "config.json"
EXAMPLE_PATH = REPO / "config.example.json"
ENV_PATH = REPO / ".env"
DOCS_DIR = REPO / "docs"
PAPERS_INDEX = DOCS_DIR / "papers" / "_papers_index.json"
EMBED_CACHE_NAME = "_embedding_cache.json"

def _validate_current_or_known_safe_legacy_index(idx: dict):
    legacy_validation = validate_known_safe_legacy_index(idx)
    if legacy_validation.ok:
        return legacy_validation

    current_validation = validate_index_metadata(idx, allow_legacy=False)
    if current_validation.ok and canonicalize_index_metadata(idx) == idx:
        return current_validation
    if current_validation.ok:
        return legacy_validation
    return current_validation


def _validate_current_or_known_safe_legacy_cache(cache: dict, *, model: str):
    legacy_validation = validate_known_safe_legacy_cache(cache, model=model)
    if legacy_validation.ok:
        return legacy_validation

    current_validation = validate_cache_metadata(cache, model=model, allow_legacy=False)
    if current_validation.ok and canonicalize_cache_metadata(cache) == cache:
        return current_validation
    if current_validation.ok:
        return legacy_validation
    return current_validation

# Verify TLS for credential-bearing network checks. Custom enterprise roots should
# be installed through SSL_CERT_FILE/REQUESTS_CA_BUNDLE instead of disabling TLS.
_SSL_CTX = ssl.create_default_context()
_TLS_CERT_ENV_NAMES = ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE")
_SECRET_ENV_NAMES = (
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "ANTHROPIC_AUTH_TOKEN",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "RESEND_API_KEY",
    "CLOUDFLARE_API_TOKEN",
    "CF_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "ZOTERO_API_KEY",
)
_LEGACY_SECRET_CONFIG_KEYS = (
    "anthropic_api_key",
    "google_api_key",
    "gemini_api_key",
    "openai_api_key",
    "resend_api_key",
)


# ---------------------------------------------------------------------------
# 출력 헬퍼
# ---------------------------------------------------------------------------
class Reporter:
    """검사 결과를 ✓/△/✗ 로 출력하고 실패·경고 수를 집계한다."""

    def __init__(self):
        on = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        self._g = "\033[32m" if on else ""
        self._y = "\033[33m" if on else ""
        self._r = "\033[31m" if on else ""
        self._b = "\033[1m" if on else ""
        self._dim = "\033[2m" if on else ""
        self._x = "\033[0m" if on else ""
        self.fails = 0   # ✗ (필수 실패) → 종료코드 1
        self.warns = 0   # △ (선택·경고)
        self.oks = 0     # ✓

    def section(self, title):
        print(f"\n{self._b}── {title}{self._x}")

    def ok(self, label, detail=""):
        self.oks += 1
        tail = f" {self._dim}— {detail}{self._x}" if detail else ""
        print(f"  {self._g}✓{self._x} {label}{tail}")

    def warn(self, label, detail="", fix=""):
        self.warns += 1
        tail = f" {self._dim}— {detail}{self._x}" if detail else ""
        print(f"  {self._y}△{self._x} {label}{tail}")
        if fix:
            print(f"      {self._y}→ {fix}{self._x}")

    def fail(self, label, detail="", fix=""):
        self.fails += 1
        tail = f" {self._dim}— {detail}{self._x}" if detail else ""
        print(f"  {self._r}✗{self._x} {label}{tail}")
        if fix:
            print(f"      {self._r}→ {fix}{self._x}")

    def note(self, text):
        print(f"    {self._dim}{text}{self._x}")

    def summary(self):
        print(f"\n{self._b}{'─' * 52}{self._x}")
        print(
            f"요약: {self._g}✓ {self.oks}{self._x}  "
            f"{self._y}△ {self.warns}{self._x}  "
            f"{self._r}✗ {self.fails}{self._x}"
        )
        if self.fails:
            print(
                f"{self._r}{self._b}✗ 필수 항목 {self.fails}개 실패{self._x} — "
                "위 → 해결법을 확인한 뒤 다시 실행하세요."
            )
        elif self.warns:
            print(
                f"{self._g}{self._b}✓ 필수 항목 통과{self._x} — 파이프라인 실행 준비 완료 "
                f"({self._y}△ {self.warns}개는 선택 기능{self._x})."
            )
        else:
            print(f"{self._g}{self._b}✓ 모든 항목 통과 — 완벽합니다.{self._x}")


# ---------------------------------------------------------------------------
# 1. Python 인터프리터 (py312 단독)
# ---------------------------------------------------------------------------
def _find_py312():
    """_env_guard.find_py312() 로 py312 경로를 찾는다 (import 실패 시 None)."""
    try:
        sys.path.insert(0, str(PIPELINE_DIR))
        from _env_guard import find_py312  # type: ignore
        return find_py312()
    except Exception:
        return shutil.which("python3.12")


def check_python(rep):
    rep.section("1. Python 인터프리터 (py312 단독)")
    ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info[:2] == (3, 12):
        rep.ok("Python 3.12", f"{sys.executable} (Python {ver})")
        return
    alt = _find_py312()
    if alt and Path(alt).resolve() != Path(sys.executable).resolve():
        fix = f"py312 로 실행: PYTHONUTF8=1 {alt} pipeline/doctor.py"
    else:
        fix = ("conda create -n py312 -c conda-forge python=3.12 -y && conda activate py312 "
               "(또는 PAPER_CURATION_PY312 로 절대경로 지정)")
    rep.fail("Python 3.12 아님", f"현재 Python {ver} — py314 등 비-3.12 금지", fix)


# ---------------------------------------------------------------------------
# 2. 필수/선택 패키지 import
# ---------------------------------------------------------------------------
# (import 명, pip 패키지명, 용도)
REQUIRED_PKGS = [
    ("anthropic", "anthropic", "리뷰·분류·인사이트·Deep Research 답변 생성"),
    ("google.genai", "google-genai", "Gemini 임베딩·figure 검증·TTS"),
    ("fitz", "pymupdf", "PyMuPDF — PDF 텍스트/figure 추출"),
    ("PIL", "Pillow", "PNG→WebP 변환"),
    ("requests", "requests", "HTTP (검색·다운로드)"),
]
# 재클러스터링(topic_modeling/classify_papers) 전용 — 없으면 리뷰·인덱스·배포는 되고
# 재분류만 불가.
CLUSTER_PKGS = [
    ("umap", "umap-learn"),
    ("hdbscan", "hdbscan"),
    ("sentence_transformers", "sentence-transformers"),
]


def _can_import(mod):
    try:
        importlib.import_module(mod)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_packages(rep):
    rep.section("2. 필수 패키지")
    missing_pip = []
    for mod, pip_name, why in REQUIRED_PKGS:
        ok, err = _can_import(mod)
        if ok:
            rep.ok(mod, why)
        else:
            missing_pip.append(pip_name)
            rep.fail(mod, why, f"pip install {pip_name}")
    if missing_pip:
        rep.note(f"한 번에: pip install {' '.join(dict.fromkeys(missing_pip))}")

    rep.section("2b. 재클러스터링 패키지 (선택 — reclassify/topic_modeling 전용)")
    missing_cluster = [pip for mod, pip in CLUSTER_PKGS if not _can_import(mod)[0]]
    if not missing_cluster:
        rep.ok("umap-learn / hdbscan / sentence-transformers", "재클러스터링 가능")
    else:
        rep.warn(
            "클러스터링 스택 일부 없음",
            f"미설치: {', '.join(missing_cluster)} — 리뷰·인덱스·배포는 정상, 재분류만 불가",
            f"pip install {' '.join(missing_cluster)}",
        )


# ---------------------------------------------------------------------------
# 3. Java 런타임 (opendataloader-pdf)
# ---------------------------------------------------------------------------
def check_java(rep):
    rep.section("3. Java 런타임 (opendataloader-pdf)")
    java = shutil.which("java")
    if not java:
        rep.warn(
            "java 없음",
            "opendataloader-pdf 대신 PyMuPDF 로 fallback → 표/구조 추출 품질 저하",
            "brew install --cask temurin  (macOS) / apt install default-jre (Linux)",
        )
        return
    try:
        out = subprocess.run([java, "-version"], capture_output=True, text=True, timeout=10)
        blob = (out.stderr or out.stdout).strip()
        ver = blob.splitlines()[0] if blob else java
        if out.returncode != 0:
            rep.warn(
                "java 실행 불가",
                f"{ver} — PyMuPDF fallback 사용",
                "brew install --cask temurin  (macOS) / apt install default-jre (Linux)",
            )
            return
    except Exception as exc:
        rep.warn(
            "java 확인 실패",
            f"{type(exc).__name__} — PyMuPDF fallback 사용",
            "brew install --cask temurin  (macOS) / apt install default-jre (Linux)",
        )
        return
    rep.ok("java", ver)


# ---------------------------------------------------------------------------
# 4. config.json (존재 + 필수 필드)
# ---------------------------------------------------------------------------
def _load_config():
    if not CONFIG_PATH.exists():
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"__error__": str(e)}


def check_config(rep, cfg):
    rep.section("4. config.json")
    if cfg is None:
        rep.fail(
            "config.json 없음",
            f"{CONFIG_PATH}",
            "npx . setup --auth oauth 실행 (키 export는 선택사항이며 setup이 대화형으로 config.json 생성)",
        )
        return
    if isinstance(cfg, dict) and "__error__" in cfg:
        rep.fail("config.json 파싱 실패", cfg["__error__"], "JSON 문법을 확인하세요")
        return
    if not isinstance(cfg, dict):
        rep.fail(
            "config.json 형식 오류",
            f"최상위가 JSON 객체가 아님 ({type(cfg).__name__})",
            'config.json 은 {"zotero": {...}} 형태의 객체여야 합니다',
        )
        return
    rep.ok("config.json 로드", str(CONFIG_PATH))

    zot = cfg.get("zotero", {}) if isinstance(cfg.get("zotero"), dict) else {}

    # zotero.api_key — placeholder 는 미설정 취급
    api_key = str(zot.get("api_key", "")).strip()
    if api_key and api_key != "YOUR_ZOTERO_API_KEY_HERE":
        rep.ok("zotero.api_key", "설정됨")
    elif os.environ.get("ZOTERO_API_KEY", "").strip():
        rep.ok("zotero.api_key", "env ZOTERO_API_KEY 로 대체")
    else:
        rep.fail(
            "zotero.api_key 미설정",
            "Zotero 컬렉션·PDF 가져오기에 필요",
            "npx . setup --auth oauth 실행 후 프롬프트에 Zotero API key 입력",
        )

    # zotero.collections — 최소 1개
    cols = zot.get("collections", {}) if isinstance(zot.get("collections"), dict) else {}
    if cols:
        rep.ok("zotero.collections", f"{len(cols)}개 토픽: {', '.join(cols.keys())}")
    else:
        rep.fail(
            "zotero.collections 비어있음",
            "최소 1개 토픽→컬렉션 매핑 필요",
            "npx . setup --auth oauth 실행 후 topic alias와 정확한 Collection 이름 입력",
        )

    # zotero.pdf_dir — 필드 존재 여부 (실제 디렉토리 점검은 6번에서)
    if str(zot.get("pdf_dir", "")).strip():
        rep.ok("zotero.pdf_dir", str(zot.get("pdf_dir")))
    else:
        default_pdf_dir = REPO / "pdf_cache"
        default_pdf_dir.mkdir(parents=True, exist_ok=True)
        rep.ok("zotero.pdf_dir", f"자동 cache: {default_pdf_dir}")

    # unpaywall_email — 선택 (OA 조회 시 예의상 필요)
    if str(cfg.get("unpaywall_email", "")).strip() or str(zot.get("email", "")).strip():
        rep.ok("unpaywall_email", "설정됨")
    else:
        rep.warn(
            "unpaywall_email 미설정",
            "Unpaywall OA PDF 조회에만 사용 (없어도 리뷰는 가능)",
            "config.json 최상위 unpaywall_email 에 이메일 지정",
        )

    return cfg


# ---------------------------------------------------------------------------
# 5. API 키 (env / config.json)
# ---------------------------------------------------------------------------
def _resolve_key(cfg, env_names, cfg_keys):
    """env → config.json 순으로 키를 찾는다. (found_bool, source) 반환. 값은 노출 안 함."""
    for name in env_names:
        if os.environ.get(name, "").strip():
            return True, f"env:{name}"
    if isinstance(cfg, dict):
        for k in cfg_keys:
            if str(cfg.get(k, "")).strip():
                return True, f"config:{k}"
    return False, ""

def _explicit_oauth_config(cfg):
    if not isinstance(cfg, dict):
        return False
    auth_cfg = cfg.get("anthropic_auth")
    if not isinstance(auth_cfg, dict):
        return False
    return str(auth_cfg.get("mode", "")).strip().lower().replace("_", "-") == "oauth"


def _configured_secret_sources(cfg):
    sources = []
    if isinstance(cfg, dict):
        for key in _LEGACY_SECRET_CONFIG_KEYS:
            if str(cfg.get(key, "")).strip():
                sources.append(f"config:{key}")
        zotero = cfg.get("zotero")
        if isinstance(zotero, dict) and str(zotero.get("api_key", "")).strip():
            sources.append("config:zotero.api_key")
    for name in _SECRET_ENV_NAMES:
        if os.environ.get(name, "").strip():
            sources.append(f"env:{name}")
    return sources


def _check_secret_sources(rep, cfg):
    sources = _configured_secret_sources(cfg)
    env_detail = ".env present; values not read" if ENV_PATH.exists() else ".env absent"
    if sources:
        rep.ok("Secret source inventory", f"{env_detail}; 설정 출처: " + ", ".join(sources))
    else:
        rep.warn("Secret source inventory", f"{env_detail}; process env/config secret source 없음")
    legacy = [src for src in sources if src.startswith("config:")]
    if legacy:
        rep.warn(
            "Legacy config secret source",
            "값은 출력하지 않음; 출처만 표시: " + ", ".join(legacy),
            "secret-free config로 마이그레이션: .env/process env 또는 각 서비스 secret store에 값을 두고 config.json에는 비밀값을 저장하지 마세요.",
        )


def _check_tls_status(rep):
    cert_sources = [name for name in _TLS_CERT_ENV_NAMES if os.environ.get(name, "").strip()]
    if _SSL_CTX.verify_mode == ssl.CERT_REQUIRED and _SSL_CTX.check_hostname:
        detail = "certificate verification enabled"
        if cert_sources:
            detail += "; custom trust env: " + ", ".join(cert_sources)
        rep.ok("TLS verification", detail)
    else:
        rep.fail(
            "TLS verification disabled",
            "credential-bearing network checks require certificate verification",
            "TLS 검증을 끄지 말고 SSL_CERT_FILE/REQUESTS_CA_BUNDLE 로 신뢰 루트를 지정하세요.",
        )



def _format_version(ver):
    return ".".join(str(part) for part in ver) if ver else "not found"


def _redact_anthropic_text(text):
    redacted = str(text)
    for name in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN"):
        secret = os.environ.get(name, "").strip()
        if secret:
            redacted = redacted.replace(secret, f"<redacted:{name}>")
    return redacted


def _check_claude_structured_output(rep):
    if claude_version is None:
        rep.fail(
            "Claude Code CLI 버전 확인 실패",
            "OAuth structured output에는 Claude Code >= 2.1.205 필요",
            "Claude Code를 설치/업데이트한 뒤 `claude --version` 확인",
        )
        return False
    ver = claude_version()
    if ver >= MIN_CLAUDE_CODE_VERSION:
        rep.ok("Claude Code CLI", f"{_format_version(ver)} — OAuth structured output 지원")
        return True
    rep.fail(
        "Claude Code CLI 버전 낮음",
        f"현재 {_format_version(ver)}, 필요 >= {_format_version(MIN_CLAUDE_CODE_VERSION)}",
        "Claude Code를 2.1.205 이상으로 업데이트한 뒤 다시 실행",
    )
    return False


def _anthropic_auth_status():
    if auth_status is None:
        return SimpleNamespace(
            mode="auto",
            source="",
            ready=False,
            detail="pipeline/anthropic_auth.py 로드 실패",
        )
    return auth_status()


def _anthropic_remedy():
    return (
        "API key: export ANTHROPIC_API_KEY=sk-ant-... "
        "(https://console.anthropic.com/settings/keys) / OAuth: claude auth login "
        "또는 claude setup-token 후 export CLAUDE_CODE_OAUTH_TOKEN=..."
    )


def _check_anthropic_auth(rep, cfg):
    status = _anthropic_auth_status()
    source = status.source or "none"
    detail = _redact_anthropic_text(f"mode={status.mode}, source={source}; {status.detail}")

    if not status.ready:
        rep.fail(
            "Anthropic 인증 미설정",
            detail,
            _anthropic_remedy(),
        )
        return status

    if status.mode == "oauth":
        rep.ok("Anthropic auth", f"{detail} — Claude Code 구독 OAuth")
        _check_claude_structured_output(rep)
        api_found, api_src = _resolve_key(cfg, ["ANTHROPIC_API_KEY"], ["anthropic_api_key"])
        if api_found and _explicit_oauth_config(cfg):
            rep.warn(
                "Anthropic API key + explicit OAuth 공존",
                f"{api_src} 존재, config anthropic_auth.mode=oauth",
                "OAuth를 선택했으므로 API 종량 과금으로 전환되지 않게 하위 프로세스에서 API credentials를 제거합니다.",
            )
    else:
        rep.ok("Anthropic auth", f"{detail} — Console API key")
    return status


def _check_anthropic_smoke(rep, auth_mode):
    if run_structured_smoke is None:
        rep.fail(
            "Anthropic structured smoke 실행 불가",
            "pipeline/anthropic_auth.py 로드 실패",
            _anthropic_remedy(),
        )
        return
    result = run_structured_smoke(auth_mode)
    detail = _redact_anthropic_text(
        f"mode={result.get('mode', 'unknown')}, source={result.get('source', 'none')}"
    )
    if result.get("smoke") == "ok":
        rep.ok("Anthropic structured smoke", f"{detail} — Claude adapter structured output OK")
    else:
        error = _redact_anthropic_text(result.get("error") or result.get("detail") or "unknown failure")
        rep.fail(
            "Anthropic structured smoke 실패",
            f"{detail}; {error}",
            "인증 상태와 Claude Code/API key 설정을 확인한 뒤 --anthropic-smoke 로 재시도",
        )


def check_api_keys(rep, cfg, anthropic_smoke=False):
    rep.section("5. Anthropic 인증 및 API 키")
    _check_secret_sources(rep, cfg)
    _check_tls_status(rep)

    # 필수: Anthropic은 API key 또는 Claude Code OAuth 둘 중 하나
    status = _check_anthropic_auth(rep, cfg)
    if os.environ.get("PAPER_CURATION_NO_DEPLOY") == "1":
        rep.note("PAPER_CURATION_NO_DEPLOY=1 — doctor/smoke 결과는 배포를 수행하지 않는 검증 전용입니다.")
    if anthropic_smoke:
        _check_anthropic_smoke(rep, status.mode if getattr(status, "ready", False) else None)

    found, src = _resolve_key(
        cfg, ["GOOGLE_API_KEY", "GEMINI_API_KEY"], ["google_api_key", "gemini_api_key"]
    )
    if found:
        rep.ok("GOOGLE_API_KEY", f"설정됨 ({src}) — figure 검증·TTS·Deep Research 임베딩")
    else:
        rep.fail(
            "GOOGLE_API_KEY 미설정",
            "figure 검증·Audio Overview·Deep Research 임베딩에 필수",
            "export GOOGLE_API_KEY=AIza...  (https://aistudio.google.com/apikey)",
        )

    # 선택
    found, src = _resolve_key(cfg, ["OPENAI_API_KEY"], ["openai_api_key"])
    if found:
        rep.ok("OPENAI_API_KEY", f"설정됨 ({src}) — reader BYOK 답변 / insights fallback")
    else:
        rep.warn(
            "OPENAI_API_KEY 미설정 (선택)",
            "reader BYOK 답변 백엔드 / insights cross-category fallback 에만 사용",
        )
    found, src = _resolve_key(cfg, ["RESEND_API_KEY"], ["resend_api_key"])
    if found:
        rep.ok("RESEND_API_KEY", f"설정됨 ({src}) — Audio Overview 이메일 발송")
    else:
        rep.warn(
            "RESEND_API_KEY 미설정 (선택)",
            "Audio Overview 이메일 발송/Worker secret 등록 때만 필요 — 로컬 setup 차단 안 함",
            "필요 시 `npx wrangler secret put RESEND_API_KEY`",
        )

    found, src = _resolve_key(cfg, ["CLOUDFLARE_API_TOKEN", "CF_API_TOKEN"], [])
    if found:
        rep.ok("CLOUDFLARE_API_TOKEN", f"설정됨 ({src}) — Cloudflare Workers 배포")
    else:
        rep.warn(
            "CLOUDFLARE_API_TOKEN 미설정 (선택)",
            "wrangler deploy (Cloudflare) 에만 필요 — 로컬 운영은 불필요",
        )

    found, src = _resolve_key(cfg, ["CLOUDFLARE_ACCOUNT_ID"], [])
    if found:
        rep.ok("CLOUDFLARE_ACCOUNT_ID", f"설정됨 ({src}) — Cloudflare 계정 식별")
    else:
        rep.warn(
            "CLOUDFLARE_ACCOUNT_ID 미설정 (선택)",
            "Cloudflare 배포 시에만 필요",
        )


# ---------------------------------------------------------------------------
# 6. Zotero (pdf_dir 존재 + --network 시 API 연결)
# ---------------------------------------------------------------------------
def check_zotero(rep, cfg, do_network):
    rep.section("6. Zotero")
    zot = cfg.get("zotero", {}) if isinstance(cfg, dict) and isinstance(cfg.get("zotero"), dict) else {}
    pdf_dir = (
        str(zot.get("pdf_dir", "")).strip()
        or os.environ.get("ZOTERO_DIR", "").strip()
        or str(REPO / "pdf_cache")
    )

    try:
        cache_path = Path(pdf_dir).expanduser().resolve()
        cache_path.mkdir(parents=True, exist_ok=True)
        n_pdf = sum(1 for _ in cache_path.glob("*.pdf"))
        rep.ok("Zotero PDF cache", f"{cache_path} (PDF {n_pdf}개)")
    except Exception as exc:
        rep.fail("Zotero PDF cache 생성 실패", str(exc), "경로 쓰기 권한 확인")

    if not do_network:
        rep.note("Zotero API 연결 테스트는 생략됨 (--network 로 활성화)")
        return

    api_key = (str(zot.get("api_key", "")).strip() or os.environ.get("ZOTERO_API_KEY", "").strip())
    if not api_key or api_key == "YOUR_ZOTERO_API_KEY_HERE":
        rep.fail("Zotero API 연결 불가", "API key 미설정", "config.json 의 zotero.api_key 지정")
        return

    # User ID 조회
    try:
        req = urllib.request.Request(
            "https://api.zotero.org/keys/current",
            headers={"Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
            data = json.load(resp)
        user_id = str(data.get("userID", ""))
        rep.ok("Zotero User ID", user_id)
    except Exception as e:
        rep.fail("Zotero User ID 조회 실패", str(e), "API key/네트워크 확인")
        return

    # 컬렉션 검증
    cols = zot.get("collections", {}) if isinstance(zot.get("collections"), dict) else {}
    if not cols:
        rep.warn("컬렉션 미설정", "config.json 의 zotero.collections 비어있음")
        return
    try:
        req = urllib.request.Request(
            f"https://api.zotero.org/users/{user_id}/collections?format=json&limit=100",
            headers={"Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
            fetched = json.load(resp)
        name_to_key = {c["data"]["name"]: c["data"]["key"] for c in fetched}
    except Exception as e:
        rep.fail("Zotero 컬렉션 목록 조회 실패", str(e), "네트워크 확인")
        return

    available = sorted(name_to_key.keys())
    for alias, name in cols.items():
        # name 이 이미 8자 대문자 key 형태면 그대로 인정
        is_key = len(str(name)) == 8 and str(name).isalnum() and not any(c.islower() for c in str(name))
        if name in name_to_key:
            rep.ok(f"컬렉션 '{alias}'", f"'{name}' → {name_to_key[name]}")
        elif is_key and name in name_to_key.values():
            rep.ok(f"컬렉션 '{alias}'", f"key {name}")
        else:
            rep.fail(
                f"컬렉션 '{alias}' 없음",
                f"'{name}' 을 Zotero 에서 찾을 수 없음",
                f"사용 가능: {', '.join(available) if available else '(없음)'}",
            )


# ---------------------------------------------------------------------------
# 7. node / npx (NPX 온보딩 / Cloudflare 배포)
# ---------------------------------------------------------------------------
def check_node(rep):
    rep.section("7. node / npx (NPX 온보딩 / Cloudflare 배포)")
    node = shutil.which("node")
    npx = shutil.which("npx")
    if node and npx:
        ver = ""
        try:
            out = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=10)
            ver = out.stdout.strip()
        except Exception:
            pass
        rep.ok("node / npx", f"node {ver} — NPX 온보딩 / wrangler deploy 가능")
    else:
        rep.warn(
            "node/npx 없음",
            "NPX 온보딩과 wrangler deploy에 필요 — Python CLI 직접 실행만 가능",
            "https://nodejs.org 또는 fnm/nvm 으로 Node.js 설치",
        )


# ---------------------------------------------------------------------------
# 8. papers index
# ---------------------------------------------------------------------------
def _load_papers_index():
    try:
        with open(PAPERS_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def check_papers_index(rep, papers):
    rep.section("8. 마스터 논문 인덱스")
    if not PAPERS_INDEX.exists():
        rep.warn(
            "_papers_index.json 없음",
            str(PAPERS_INDEX),
            "첫 파이프라인 실행(run_full.py) 후 자동 생성됩니다",
        )
        return
    if papers is None:
        rep.fail("_papers_index.json 파싱 실패", str(PAPERS_INDEX), "JSON 손상 여부 확인")
        return
    n = len(papers) if isinstance(papers, list) else 0
    rep.ok("_papers_index.json", f"{n}개 논문")


# ---------------------------------------------------------------------------
# 9. --topic 산출물
# ---------------------------------------------------------------------------
# (파일명, 필수여부, 설명)
TOPIC_ARTIFACTS = [
    ("index.html", True, "토픽 카드 인덱스"),
    ("_new_classification.json", True, "카테고리 분류"),
    ("_search_index.json", False, "Deep Research RAG 인덱스"),
    ("network.html", False, "D3 네트워크 시각화"),
]

def _validate_topic_search_index(rep, topic, tdir):
    idx_path = tdir / "_search_index.json"
    if not idx_path.exists():
        return
    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    except Exception as exc:
        rep.fail(
            f"{topic}/_search_index.json 파싱 실패",
            str(exc),
            "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.",
        )
        return
    validation = _validate_current_or_known_safe_legacy_index(idx)
    if not validation.ok:
        rep.fail(
            f"{topic}/_search_index.json metadata incompatible",
            format_validation_errors(f"{topic}/_search_index.json", validation),
            "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.",
        )
        return
    legacy = "known-safe legacy; " if validation.is_legacy else ""
    normalized = canonicalize_index_metadata(idx)
    chunks = idx.get("chunks")
    if not isinstance(chunks, list):
        rep.fail(
            f"{topic}/_search_index.json chunks 오류",
            f"{type(chunks).__name__}",
            "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.",
        )
        return
    dim = int(normalized[KEY_EMBEDDING_DIMENSION])
    emb_file = EMBEDDING_SIDECAR_FILE
    emb_path = tdir / emb_file
    expected = len(chunks) * dim
    if not emb_path.exists():
        rep.fail(
            f"{topic}/{emb_file} 없음",
            "검색 인덱스 sidecar 누락",
            "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.",
        )
        return
    actual = emb_path.stat().st_size
    if actual != expected:
        rep.fail(
            f"{topic}/{emb_file} length mismatch",
            f"{actual}B != count*dim {expected}B",
            "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.",
        )
        return
    rep.ok(f"{topic}/_search_index metadata", f"{legacy}{len(chunks)} chunks; sidecar length ok")

    cache_path = tdir / EMBED_CACHE_NAME
    if not cache_path.exists():
        rep.warn(f"{topic}/{EMBED_CACHE_NAME} 없음", "임베딩 resume cache 없음 (선택)")
        return
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception as exc:
        rep.fail(
            f"{topic}/{EMBED_CACHE_NAME} 파싱 실패",
            str(exc),
            "손상된 cache를 제거하거나 pipeline/build_search_index.py 로 명시적으로 재빌드하세요; doctor는 재빌드하지 않습니다.",
        )
        return
    cache_validation = _validate_current_or_known_safe_legacy_cache(cache, model=str(normalized[KEY_EMBEDDING_MODEL]))
    if cache_validation.ok:
        cache_legacy = "known-safe legacy; " if cache_validation.is_legacy else ""
        rep.ok(f"{topic}/{EMBED_CACHE_NAME}", f"{cache_legacy}metadata compatible")
    else:
        rep.fail(
            f"{topic}/{EMBED_CACHE_NAME} metadata incompatible",
            format_validation_errors(f"{topic}/{EMBED_CACHE_NAME}", cache_validation),
            "손상된 cache를 제거하거나 pipeline/build_search_index.py 로 명시적으로 재빌드하세요; doctor는 재빌드하지 않습니다.",
        )



def check_topic(rep, topic, cfg, papers):
    rep.section(f"9. 토픽 산출물: {topic}")
    tdir = DOCS_DIR / topic

    # config 에 등록된 토픽인지 (정보성)
    cols = {}
    if isinstance(cfg, dict) and isinstance(cfg.get("zotero"), dict):
        cols = cfg["zotero"].get("collections", {}) or {}
    if topic in cols:
        rep.ok(f"'{topic}' config 등록됨", f"컬렉션 매핑 존재")
    else:
        rep.warn(
            f"'{topic}' config 미등록",
            f"zotero.collections 에 없음 (등록된 토픽: {', '.join(cols.keys()) or '없음'})",
        )

    if not tdir.is_dir():
        command = f"PAPER_CURATION_NO_DEPLOY=1 PYTHONUTF8=1 python pipeline/run_full.py --topic {topic} --mode curate --source zotero --no-deploy"
        if not PAPERS_INDEX.exists():
            rep.warn(
                f"docs/{topic}/ 없음 (첫 실행 전 정상)",
                str(tdir),
                command,
            )
        else:
            rep.fail(
                f"docs/{topic}/ 없음",
                str(tdir),
                command,
            )
        return

    for fname, required, desc in TOPIC_ARTIFACTS:
        fpath = tdir / fname
        if fpath.exists():
            rep.ok(f"{topic}/{fname}", desc)
        elif required:
            rep.fail(
                f"{topic}/{fname} 없음",
                desc,
                f"PYTHONUTF8=1 python pipeline/build_topic_index.py {topic}",
            )
        else:
            rep.warn(f"{topic}/{fname} 없음", f"{desc} (선택)")
    _validate_topic_search_index(rep, topic, tdir)

    # 인덱스에서 이 토픽 논문 수 교차 확인 (정보성)
    if isinstance(papers, list):
        n_topic = sum(1 for p in papers if isinstance(p, dict) and topic in (p.get("topics") or []))
        rep.note(f"_papers_index.json 에서 topics 에 '{topic}' 포함: {n_topic}개")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="paper-curation 설치 환경 일괄 진단 (✓/△/✗)"
    )
    parser.add_argument("--network", action="store_true",
                        help="Zotero API 연결까지 테스트 (네트워크 필요)")
    parser.add_argument("--topic", default="",
                        help="해당 토픽의 산출물 존재 여부까지 점검 (예: humanoid)")
    parser.add_argument("--anthropic-smoke", action="store_true",
                        help="작은 Anthropic structured output 호출까지 검증 (네트워크/과금 가능)")
    args = parser.parse_args()

    print("=" * 52)
    print("  Paper Curation — Doctor (환경 진단)")
    print("=" * 52)

    rep = Reporter()
    cfg = _load_config()
    papers = _load_papers_index()

    check_python(rep)
    check_packages(rep)
    check_java(rep)
    check_config(rep, cfg)
    check_api_keys(rep, cfg, args.anthropic_smoke)
    check_zotero(rep, cfg, args.network)
    check_node(rep)
    check_papers_index(rep, papers)
    if args.topic:
        check_topic(rep, args.topic, cfg, papers)

    rep.summary()
    sys.exit(1 if rep.fails else 0)


if __name__ == "__main__":
    main()
