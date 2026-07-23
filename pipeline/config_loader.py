"""
config.json 로더 + Zotero User ID / Collection Key 자동 조회.

모든 스크립트가 이 모듈을 통해 설정을 읽는다.
config.json이 없으면 환경변수 폴백.

Collection은 이름(예: "AI assisted Research")으로 지정하면
Zotero API로 collection key를 자동 조회한다.
"""

import json
import os
import re
import ssl
import urllib.request
from pathlib import Path

try:
    from tls import create_ssl_context
except ImportError:
    try:
        from pipeline.tls import create_ssl_context
    except ImportError:
        def create_ssl_context(purpose=None, config=None):
            return ssl.create_default_context()

_ssl_ctx = create_ssl_context(purpose="config_loader")

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

def _load_dotenv(path=PROJECT_ROOT / ".env"):
    """Load simple .env entries without overriding process exports."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if (
            not key
            or not (key[0].isalpha() or key[0] == "_")
            or any(not (char.isalnum() or char == "_") for char in key)
        ):
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        if value and key not in os.environ:
            os.environ[key] = value



def load_config():
    """Load config.json plus process/.env secrets; env wins at access time."""
    global _config_cache
    _load_dotenv()
    if _config_cache is not None:
        return _config_cache

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    else:
        _config_cache = {
            "zotero": {
                "collections": {},
            },
            "topic_profiles": {},
            "paths": {
                "zotero_dir": str(PROJECT_ROOT / "pdf_cache"),
            },
            "features": {},
        }

    return _config_cache


def get_zotero_api_key():
    cfg = load_config()
    return os.environ.get("ZOTERO_API_KEY", "") or cfg.get("zotero", {}).get("api_key", "")


def get_google_key():
    """Google(Gemini) API 키. env(GOOGLE_API_KEY/GEMINI_API_KEY) 우선, 없으면
    config.json(gemini_api_key/google_api_key). figure 검증·TTS·임베딩 공용 해석기.

    참고: figure 검증처럼 'env 키 유무'를 Gemini on/off 스위치로 쓰던 호출부는
    이 함수가 config.json 까지 보므로 env 를 pop 해도 키가 남는다. 그런 곳은
    PAPER_CURATION_NO_GEMINI 환경 플래그로 명시 비활성화한다
    (reextract_figures.py 의 geometric-only 모드 참조)."""
    cfg = load_config()
    return (os.environ.get("GOOGLE_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
            or cfg.get("gemini_api_key", "")
            or cfg.get("google_api_key", "")) or ""


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
    "Humanoid"처럼 8자이면서 알파벳이 섞인 이름과 구분하기 위해
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


def _topic_profile_collection_key(topic, raw):
    if not isinstance(raw, dict):
        raise ValueError(f"Malformed config at topic_profiles.{topic}: expected object.")
    if "label" not in raw:
        raise ValueError(f"Malformed config at topic_profiles.{topic}.label: expected non-empty string.")
    label = raw.get("label")
    if not isinstance(label, str) or not label.strip():
        raise ValueError(f"Malformed config at topic_profiles.{topic}.label: expected non-empty string.")
    if "collection_key" in raw:
        key = raw.get("collection_key")
        if key in (None, ""):
            return ""
        if not isinstance(key, str):
            raise ValueError(f"Malformed config at topic_profiles.{topic}.collection_key: expected string.")
        return key.strip()
    if "collection_name" in raw:
        name = raw.get("collection_name")
        if name in (None, ""):
            return ""
        if not isinstance(name, str):
            raise ValueError(f"Malformed config at topic_profiles.{topic}.collection_name: expected string.")
        return _resolve_collection_value(name.strip())
    return ""


def get_collections():
    """topic → collection key dict 반환. canonical profiles win; legacy mapping falls back."""
    cfg = load_config()
    out = {}
    profiles = cfg.get("topic_profiles", {}) or {}
    if profiles and not isinstance(profiles, dict):
        raise ValueError("Malformed config at topic_profiles: expected object.")
    for topic, raw in profiles.items():
        key = _topic_profile_collection_key(topic, raw)
        if key:
            out[topic] = key

    raw = cfg.get("zotero", {}).get("collections", {}) or {}
    if not isinstance(raw, dict):
        raise ValueError("Malformed config at zotero.collections: expected object.")
    for topic, value in raw.items():
        if topic not in profiles:
            out[topic] = _resolve_collection_value(value)
    return out


def get_collection_key(topic):
    return get_collections().get(topic, "")


def get_unpaywall_email():
    cfg = load_config()
    return (
        os.environ.get("UNPAYWALL_EMAIL", "")
        or os.environ.get("ZOTERO_EMAIL", "")
        or cfg.get("unpaywall_email", "")
        or cfg.get("zotero", {}).get("email", "")
    )


# ---------------------------------------------------------------------------
# 검색 키워드 / 토픽 프로필 (Core-1 search)
# ---------------------------------------------------------------------------

def _as_list(value, path):
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError(f"Malformed config at {path}: expected string list.")

def _as_keyword_list(value, path):
    if value in (None, ""):
        return []
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError(f"Malformed config at {path}: expected keyword list.")



def _normalize_keyword(value):
    collapsed = re.sub(r"\s+", " ", value.strip())
    return collapsed


def _dedupe_keywords(values):
    out = []
    seen = set()
    for value in values:
        normalized = _normalize_keyword(value)
        if not normalized:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(normalized)
    return out


def _alias_tokens(topic):
    tokens = re.split(r"[-_./\s]+", topic)
    return [token for token in tokens if token and token != topic]


def _profile_from_collections(topic, collections):
    value = collections.get(topic, "")
    labels = _as_list(value, f"zotero.collections.{topic}") if value else []
    aliases = [topic]
    primary = labels or [topic.replace("-", " ").replace("_", " ")]
    secondary = aliases + _alias_tokens(topic)
    label = _dedupe_keywords(labels)[0] if labels else topic.replace("-", " ").replace("_", " ")
    return {
        "topic": topic,
        "label": label,
        "collection_name": _dedupe_keywords(labels)[0] if labels else "",
        "collection_key": "",
        "aliases": _dedupe_keywords(aliases),
        "collections": _dedupe_keywords(labels),
        "collection_label": _dedupe_keywords(labels)[0] if labels else "",
        "search_keywords": {
            "primary": _dedupe_keywords(primary),
            "secondary": _dedupe_keywords(secondary),
        },
    }


def _normalize_explicit_topic_profile(topic, raw):
    if not isinstance(raw, dict):
        raise ValueError(f"Malformed config at topic_profiles.{topic}: expected object.")

    if "label" not in raw:
        raise ValueError(f"Malformed config at topic_profiles.{topic}.label: expected non-empty string.")
    label_value = raw.get("label")
    if not isinstance(label_value, str) or not label_value.strip():
        raise ValueError(f"Malformed config at topic_profiles.{topic}.label: expected non-empty string.")
    label = _normalize_keyword(label_value)

    aliases = _as_list(raw.get("aliases", []), f"topic_profiles.{topic}.aliases")
    collection_name = raw.get("collection_name", "")
    if collection_name in (None, ""):
        collection_name = ""
    elif not isinstance(collection_name, str):
        raise ValueError(f"Malformed config at topic_profiles.{topic}.collection_name: expected string.")
    else:
        collection_name = _normalize_keyword(collection_name)

    collection_key = raw.get("collection_key", "")
    if collection_key in (None, ""):
        collection_key = ""
    elif not isinstance(collection_key, str):
        raise ValueError(f"Malformed config at topic_profiles.{topic}.collection_key: expected string.")
    else:
        collection_key = collection_key.strip()

    collection_values = []
    if collection_name:
        collection_values.append(collection_name)

    keyword_block = raw.get("search_keywords", raw.get("keywords", {})) or {}
    if not isinstance(keyword_block, dict):
        raise ValueError(f"Malformed config at topic_profiles.{topic}.search_keywords: expected object.")
    primary = _as_keyword_list(keyword_block.get("primary", []), f"topic_profiles.{topic}.search_keywords.primary")
    secondary = _as_keyword_list(keyword_block.get("secondary", []), f"topic_profiles.{topic}.search_keywords.secondary")

    primary = _dedupe_keywords(primary + [label] + collection_values)
    secondary = _dedupe_keywords(secondary + aliases + [topic] + _alias_tokens(topic))
    return {
        "topic": topic,
        "label": label,
        "collection_name": collection_name,
        "collection_key": collection_key,
        "aliases": _dedupe_keywords(aliases + [topic]),
        "collections": _dedupe_keywords(collection_values),
        "collection_label": label,
        "search_keywords": {
            "primary": primary,
            "secondary": secondary,
        },
    }


def get_topic_profile(topic):
    """Return a normalized, offline topic profile for any topic alias."""
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic must be a non-empty string.")
    topic = topic.strip()
    cfg = load_config()
    profiles = cfg.get("topic_profiles", {}) or {}
    if not isinstance(profiles, dict):
        raise ValueError("Malformed config at topic_profiles: expected object.")

    collections = cfg.get("zotero", {}).get("collections", {}) or {}
    if not isinstance(collections, dict):
        raise ValueError("Malformed config at zotero.collections: expected object.")

    if topic not in profiles:
        return _profile_from_collections(topic, collections)

    return _normalize_explicit_topic_profile(topic, profiles[topic])


def get_search_keywords(topic):
    """Return normalized keyword lists; legacy search_keywords.<topic> wins."""
    cfg = load_config()
    configured = cfg.get("search_keywords", {}) or {}
    if not isinstance(configured, dict):
        raise ValueError("Malformed config at search_keywords: expected object.")
    if topic in configured:
        block = configured[topic]
        if not isinstance(block, dict):
            raise ValueError(f"Malformed config at search_keywords.{topic}: expected object.")
        primary = _dedupe_keywords(_as_keyword_list(block.get("primary", []), f"search_keywords.{topic}.primary"))
        secondary = _dedupe_keywords(_as_keyword_list(block.get("secondary", []), f"search_keywords.{topic}.secondary"))
        if not primary or not secondary:
            raise ValueError(f"Malformed config at search_keywords.{topic}: primary and secondary must be non-empty.")
        return {"primary": primary, "secondary": secondary}

    keywords = get_topic_profile(topic)["search_keywords"]
    if not keywords["primary"] or not keywords["secondary"]:
        raise ValueError(f"Malformed config at topic_profiles.{topic}: primary and secondary keywords must be non-empty.")
    return keywords


def get_paperbanana_dir():
    cfg = load_config()
    return os.environ.get("PAPERBANANA_DIR", "") or cfg.get("paperbanana_dir", "")


def get_zotero_dir():
    """Return the configured PDF directory, creating a project-local cache by default."""
    cfg = load_config()
    configured = (
        os.environ.get("ZOTERO_DIR", "")
        or cfg.get("paths", {}).get("zotero_dir", "")
        or cfg.get("zotero", {}).get("pdf_dir", "")
        or str(PROJECT_ROOT / "pdf_cache")
    )
    directory = Path(configured).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory)


def get_github_repo():
    """GitHub repo (owner/repo 형식)."""
    cfg = load_config()
    return (os.environ.get("GITHUB_REPO", "")
            or cfg.get("github", {}).get("repo", ""))


def get_github_branch():
    """GitHub branch (기본 master)."""
    cfg = load_config()
    return (os.environ.get("GITHUB_BRANCH", "")
            or cfg.get("github", {}).get("branch", "master"))


def get_pages_base_url():
    """GitHub Pages base URL."""
    cfg = load_config()
    return (os.environ.get("PAGES_BASE_URL", "")
            or cfg.get("github", {}).get("pages_base_url", ""))


def get_topic_dir(topic: str) -> Path:
    """docs/{topic} 경로 반환."""
    return DOCS_DIR / topic


def get_papers_index_path() -> Path:
    """papers/_papers_index.json 경로 반환."""
    return PAPERS_DIR / "_papers_index.json"
