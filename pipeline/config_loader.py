"""
config.json 로더 + Zotero User ID / Collection Key 자동 조회.

모든 스크립트가 이 모듈을 통해 설정을 읽는다.
config.json이 없으면 환경변수 폴백.

Collection은 이름(예: "AI assisted Research")으로 지정하면
Zotero API로 collection key를 자동 조회한다.
"""

import json
import os
import ssl
import urllib.request
from pathlib import Path

# TLS verification is mandatory. Private/corporate CAs may be supplied
# explicitly without disabling hostname or certificate checks.
_ca_bundle = os.environ.get("PAPER_CURATION_CA_BUNDLE", "").strip()
_ssl_ctx = ssl.create_default_context(cafile=_ca_bundle or None)

PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"

# 배포 파일 경로 (GitHub Pages 서빙 루트)
DOCS_DIR = PROJECT_ROOT / "docs"
PAPERS_DIR = DOCS_DIR / "papers"

# 타임라인/워크플로우 이미지 출력
IMG_TIMELINES_DIR = PIPELINE_DIR / "_img_timelines"
IMG_WORKFLOWS_DIR = PIPELINE_DIR / "_img_workflows"

REPO = PROJECT_ROOT  # backward compat alias

_config_cache = None
_user_id_cache = None
_collection_key_cache = None


def load_config():
    """config.json 로드. 없으면 환경변수 폴백."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    else:
        _config_cache = {
            "zotero": {
                "api_key": os.environ.get("ZOTERO_API_KEY", ""),
                "email": os.environ.get("UNPAYWALL_EMAIL", ""),
                "collections": {},
            },
            "unpaywall_email": os.environ.get("UNPAYWALL_EMAIL", ""),
        }

    return _config_cache


def get_zotero_api_key():
    cfg = load_config()
    return cfg.get("zotero", {}).get("api_key", "") or os.environ.get("ZOTERO_API_KEY", "")


def get_google_key():
    """Google(Gemini) API 키. env(GOOGLE_API_KEY/GEMINI_API_KEY) 우선, 없으면
    config.json(gemini_api_key/google_api_key). figure 검증·TTS·임베딩 공용 해석기.

    참고: figure 검증처럼 'env 키 유무'를 Gemini on/off 스위치로 쓰던 호출부는
    이 함수가 config.json 까지 보므로 env 를 pop 해도 키가 남는다. 그런 곳은
    PAPER_CURATION_NO_GEMINI 환경 플래그로 명시 비활성화한다."""
    if os.environ.get("PAPER_CURATION_NO_GEMINI"):
        # docstring 이 약속하는 명시 off 스위치. 이게 없으면 env 를 pop 해도
        # config.json 키가 남아 스위치가 안 먹는다.
        return ""
    cfg = load_config()
    for candidate in (os.environ.get("GOOGLE_API_KEY"),
                      os.environ.get("GEMINI_API_KEY"),
                      cfg.get("gemini_api_key", ""),
                      cfg.get("google_api_key", "")):
        resolved = (candidate or "").strip()
        if resolved:
            return resolved
    return ""


def get_local_model_config():
    """로컬 LLM fallback (Ollama / LM Studio / llama.cpp / vLLM) 설정.

    OpenAI 호환 엔드포인트 한 개를 가정한다. 환경변수가 config.json 보다 우선.
    base_url 과 model 이 둘 다 있어야 유효하고, 그렇지 않으면 None 을 반환해
    호출자가 "로컬 fallback 미설정" 으로 조용히 건너뛰게 한다.

    config.json 예시::

        "local_model": {
          "base_url": "http://localhost:11434/v1",
          "model": "qwen2.5:7b-instruct",
          "api_key": "ollama",      # 로컬 서버는 대개 무시하지만 SDK 가 비어있으면 거부
          "batch_size": 8,          # (선택) 로컬 연결 배치 크기
          "timeout": 300            # (선택) per-call 초
        }
    """
    cfg = load_config().get("local_model", {}) or {}
    base_url = os.environ.get("LOCAL_MODEL_BASE_URL") or cfg.get("base_url")
    model = os.environ.get("LOCAL_MODEL_NAME") or cfg.get("model")
    if not base_url or not model:
        return None
    out = {
        "base_url": base_url,
        "model": model,
        "api_key": os.environ.get("LOCAL_MODEL_API_KEY") or cfg.get("api_key") or "local",
    }
    if cfg.get("batch_size"):
        out["batch_size"] = int(cfg["batch_size"])
    if cfg.get("timeout"):
        out["timeout"] = float(cfg["timeout"])
    if cfg.get("reasoning_effort"):
        # thinking 모델(EXAONE-4.5 등): "none" 이면 think OFF — 없으면 content 가
        # 빈 채 thinking 채널만 채우는 모델이 있다 (lib/local_llm.chat_json 참조)
        out["reasoning_effort"] = str(cfg["reasoning_effort"])
    if cfg.get("json_mode"):
        # response_format json_object — 서버 문법 제약으로 JSON 유효성 보장
        out["json_mode"] = True
    if cfg.get("num_ctx"):
        # Ollama 네이티브 경로 전용: 요청 단위 컨텍스트(기본 8192). 신형 Ollama 가
        # 모델 최대치(128K+)로 로드해 느려지는 것을 요청 단위로 줄인다.
        out["num_ctx"] = int(cfg["num_ctx"])
    if cfg.get("retries"):
        # 형식 깨짐은 확률적이라 배치당 재시도 횟수(기본 2)
        out["retries"] = int(cfg["retries"])
    return out


def get_zotero_user_id():
    """Zotero API Key로 User ID를 자동 조회. 캐싱."""
    global _user_id_cache
    if _user_id_cache is not None:
        return _user_id_cache

    env_id = os.environ.get("ZOTERO_USER_ID", "")
    if env_id:
        _user_id_cache = env_id
        return env_id

    api_key = get_zotero_api_key()
    if not api_key:
        raise ValueError("Zotero API key not found. Set config.json or ZOTERO_API_KEY env var.")

    try:
        url = "https://api.zotero.org/keys/current"
        req = urllib.request.Request(url, headers={
            "Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0",
        })
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
            data = json.load(resp)
        _user_id_cache = str(data.get("userID", ""))
        return _user_id_cache
    except Exception as e:
        raise ValueError(f"Failed to fetch Zotero User ID: {e}")


def _fetch_collection_keys():
    """Zotero에서 collection name → key 매핑을 조회. 캐싱."""
    global _collection_key_cache
    if _collection_key_cache is not None:
        return _collection_key_cache

    api_key = get_zotero_api_key()
    user_id = get_zotero_user_id()

    try:
        url = f"https://api.zotero.org/users/{user_id}/collections?format=json&limit=100"
        req = urllib.request.Request(url, headers={
            "Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0",
        })
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
            cols = json.load(resp)
        _collection_key_cache = {c["data"]["name"]: c["data"]["key"] for c in cols}
        return _collection_key_cache
    except Exception as e:
        print(f"WARNING: Failed to fetch Zotero collections: {e}")
        _collection_key_cache = {}
        return _collection_key_cache


def _resolve_collection_value(value):
    """Collection value가 이름이면 key로 변환, 이미 key면 그대로.

    Zotero collection key는 8자 대문자 영숫자 (예: WKEZLEE8).
    같은 길이의 컬렉션 이름과 구분하기 위해
    먼저 이름으로 조회한다.
    """
    if not value:
        return ""
    # 이름으로 먼저 조회 (API 캐시)
    name_to_key = _fetch_collection_keys()
    if value in name_to_key:
        return name_to_key[value]
    # Zotero key 패턴: 8자 + 대문자/숫자만 (소문자 불가)
    if len(value) == 8 and value.isalnum() and not any(c.islower() for c in value):
        return value
    print(f"WARNING: Collection '{value}' not found in Zotero.")
    return value


def get_collections():
    """topic → collection key dict 반환. 이름은 자동으로 key로 변환."""
    cfg = load_config()
    raw = cfg.get("zotero", {}).get("collections", {})
    return {topic: _resolve_collection_value(val) for topic, val in raw.items()}


def get_collection_key(topic):
    return get_collections().get(topic, "")


def get_unpaywall_email():
    cfg = load_config()
    return cfg.get("unpaywall_email", "") or cfg.get("zotero", {}).get("email", "")


def get_openalex_email():
    """OpenAlex polite-pool contact, without an implicit maintainer address."""
    if "OPENALEX_EMAIL" in os.environ:
        return os.environ["OPENALEX_EMAIL"].strip()
    return str(get_unpaywall_email() or "").strip()


def get_operator_identity():
    """Configured operator attribution, with explicit environment overrides."""
    operator = load_config().get("operator", {}) or {}
    if not isinstance(operator, dict):
        operator = {}
    fields = {
        "name": "PAPER_CURATION_OPERATOR_NAME",
        "organization": "PAPER_CURATION_OPERATOR_ORGANIZATION",
        "email": "PAPER_CURATION_OPERATOR_EMAIL",
    }
    return {
        field: str(os.environ[env] if env in os.environ else operator.get(field, "") or "").strip()
        for field, env in fields.items()
    }


def get_operator_attribution():
    """Plain-text operator attribution, or empty when no identity is configured."""
    identity = get_operator_identity()
    name_and_organization = ", ".join(
        value for value in (identity["name"], identity["organization"]) if value
    )
    values = [value for value in (name_and_organization, identity["email"]) if value]
    return f"Developed by {' | '.join(values)}" if values else ""


def get_completion_email():
    """Explicit recipient for bibliography completion notifications."""
    if "BIBLIOGRAPHY_COMPLETION_EMAIL" in os.environ:
        return os.environ["BIBLIOGRAPHY_COMPLETION_EMAIL"].strip()
    notifications = load_config().get("notifications", {}) or {}
    if not isinstance(notifications, dict):
        return ""
    return str(notifications.get("completion_email", "") or "").strip()


# ---------------------------------------------------------------------------
# 검색 키워드 (Core-1 search)
# ---------------------------------------------------------------------------
# Every topic owns its search vocabulary in config.json. Product source does
# not carry privileged domain presets.


def get_search_keywords(topic):
    """topic → {"primary": [...], "secondary": [...]} 검색 키워드 dict 반환.

    없으면 config.json 에 그대로 붙여넣을 수 있는 JSON 블록을 담은
    ValueError 를 던진다.
    """
    cfg = load_config()
    configured = cfg.get("search_keywords", {}) or {}
    if topic in configured:
        return configured[topic]
    example_block = json.dumps(
        {
            "search_keywords": {
                topic: {
                    "primary": [
                        f"{topic} 핵심 키워드 1",
                        f"{topic} 핵심 키워드 2",
                        f"{topic} 핵심 키워드 3",
                    ],
                    "secondary": [
                        f"{topic} 보조 키워드 1",
                        f"{topic} 보조 키워드 2",
                    ],
                }
            }
        },
        ensure_ascii=False,
        indent=2,
    )
    raise ValueError(
        f"'{topic}' 토픽의 검색 키워드(search_keywords)가 정의되지 않았습니다.\n"
        f"config.json 최상위에 아래 \"search_keywords\" 블록을 추가하세요.\n"
        f"  - primary: 관련성 가중치가 높은 핵심 키워드 (제목/초록 매칭 0.5점)\n"
        f"  - secondary: 보조 키워드 (매칭 0.2점)\n\n"
        f"{example_block}"
    )


def get_paperbanana_dir():
    cfg = load_config()
    return cfg.get("paperbanana_dir", "")


def _hostname():
    """짧은 호스트명 (소문자, 도메인/`.local` 제거)."""
    import socket
    return socket.gethostname().split(".")[0].strip().lower()


def get_zotero_dir():
    """Zotero PDF 저장 디렉토리 — 머신마다 다른 경로를 순서대로 해결한다.

    같은 라이브러리를 여러 대에서 쓰면 Zotero 경로가 머신마다 다르다.
    linked_file 첨부는 만들어진 머신의 절대경로를 저장하므로 hostname별
    경로 설정을 지원한다.

    해결 순서 — 먼저 맞는 것이 이긴다:

      1. ``ZOTERO_DIR`` 환경변수 — 머신이 언제든 직접 선언하는 최상위 수단
      2. ``zotero.pdf_dir_by_host[<hostname>]`` — 머신별 명시 매핑
      3. ``zotero.pdf_dir_candidates`` 중 **실제로 존재하는** 첫 경로
      4. ``zotero.pdf_dir`` — 단일 머신 기본값

    2·3 이 비어 있으면 기존 동작(4번)과 동일하다.
    """
    cfg = load_config().get("zotero", {})

    env = os.environ.get("ZOTERO_DIR", "").strip()
    if env:
        return env

    by_host = cfg.get("pdf_dir_by_host") or {}
    if isinstance(by_host, dict):
        host = _hostname()
        for name, path in by_host.items():
            if str(name).split(".")[0].strip().lower() == host and path:
                return str(Path(path).expanduser())

    for path in cfg.get("pdf_dir_candidates") or []:
        # 존재하는 것만 채택 — 후보 목록은 "이 중 하나가 이 머신의 것" 이라는
        # 뜻이지, 순서가 우선순위라는 뜻이 아니다.
        if path and os.path.isdir(os.path.expanduser(str(path))):
            return os.path.expanduser(str(path))

    return cfg.get("pdf_dir", "")


def get_github_repo():
    """GitHub repo (owner/repo 형식)."""
    cfg = load_config()
    return (cfg.get("github", {}).get("repo", "")
            or os.environ.get("GITHUB_REPO", ""))


def get_github_branch():
    """GitHub branch (기본 master)."""
    cfg = load_config()
    return (cfg.get("github", {}).get("branch", "")
            or os.environ.get("GITHUB_BRANCH", "master"))


def get_pages_base_url():
    """GitHub Pages base URL."""
    cfg = load_config()
    return (cfg.get("github", {}).get("pages_base_url", "")
            or os.environ.get("PAGES_BASE_URL", ""))


def get_public_base_url() -> str:
    """Explicit public site base URL, or empty for local-only installs."""
    configured = load_config().get("publication", {}) or {}
    if not isinstance(configured, dict):
        configured = {}
    return (
        os.environ.get("PAPER_CURATION_PUBLIC_BASE_URL", "").strip()
        or str(configured.get("base_url", "") or "").strip()
    ).rstrip("/")


def get_topic_dir(topic: str) -> Path:
    """docs/{topic} 경로 반환."""
    return DOCS_DIR / topic


def get_topic_names() -> list:
    """설정된 topic alias 목록. 네트워크 없음.

    get_collections() 는 컬렉션 이름을 Zotero 키로 해석하느라 API 를 탈 수 있다.
    토픽 alias 만 필요한 자리(기본값 결정, 폴백)에서는 이 함수를 쓴다.
    """
    cfg = load_config()
    raw = cfg.get("zotero", {}).get("collections", {}) or {}
    return [t for t in raw.keys() if t]


def get_topic_profile(topic: str) -> dict:
    """Optional presentation metadata for a topic."""
    profiles = load_config().get("topic_profiles", {}) or {}
    if not isinstance(profiles, dict):
        return {}
    profile = profiles.get(topic, {}) or {}
    return dict(profile) if isinstance(profile, dict) else {}


def get_default_topic() -> str:
    """--topic 생략 시 쓸 토픽. 유일할 때만 확정, 아니면 빈 문자열.

    토픽이 하나뿐인 설치(대다수)는 --topic 없이도 그 토픽으로 돌아간다.
    여러 개면 무엇을 뜻했는지 알 수 없으므로 호출자가 명시를 요구해야 한다.
    """
    names = get_topic_names()
    return names[0] if len(names) == 1 else ""

def resolve_topic(explicit: str = "", *, script: str = "") -> str:
    """--topic 인자를 해석한다. 개별 스크립트를 직접 부를 때의 공통 진입점.

    토픽이 하나면 그 alias를 사용하고, 여러 개면 명시를 요구한다.

    그래서 세 갈래로 나눈다.
      - 명시했으면 그대로 쓴다.
      - 생략했고 설정된 토픽이 하나뿐이면 그것으로 진행하되, 한 줄 알린다.
        (토픽이 하나인 설치가 대다수 — 이 경로가 기존 사용자를 지킨다)
      - 생략했고 토픽이 여럿/없으면 무엇을 뜻했는지 알 수 없으므로 멈춘다.
        조용히 하나를 고르면 엉뚱한 토픽을 건드린다.
    """
    if explicit:
        return explicit

    names = get_topic_names()
    where = f"{script}: " if script else ""

    if len(names) == 1:
        topic = names[0]
        print(f"[topic] {where}--topic 생략 → 설정된 유일한 토픽 '{topic}' 사용 "
              f"(명시하려면 --topic {topic})")
        return topic

    if not names:
        raise SystemExit(
            f"[topic] {where}--topic 이 필요합니다. config.json 의 "
            f"zotero.collections 에 토픽이 없습니다 — 먼저 setup 을 실행하세요."
        )

    raise SystemExit(
        f"[topic] {where}--topic 이 필요합니다. 설정된 토픽이 여러 개라 "
        f"자동으로 고를 수 없습니다: {', '.join(sorted(names))}"
    )



def get_papers_index_path() -> Path:
    """papers/_papers_index.json 경로 반환."""
    return PAPERS_DIR / "_papers_index.json"

# ---------------------------------------------------------------------------
# Gemini usage instrumentation (dashboard 종량제 그래프)
# ---------------------------------------------------------------------------
# Every pipeline entry point imports config_loader, and so does the PaperBanana
# wrapper (lib/paperbanana.py) before it runs PaperBanana's agents in-process.
# Instrumentation is an explicit process-level opt-in. Importing configuration
# alone must not monkey-patch SDK classes or start telemetry.
if os.environ.get("PC_USAGE_ENDPOINT", "").strip():
    import usage_log as _usage_log

    _usage_log.instrument_genai()
