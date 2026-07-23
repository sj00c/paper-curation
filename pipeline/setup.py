"""
paper-curation 설치 스크립트.

한 번 실행으로 전체 설치를 완료한다:
  1. config.json 생성 (인터랙티브)
  2. Core credential 게이트 — ZOTERO/GOOGLE 필수, Anthropic은 API key 또는 OAuth
     (Resend는 Audio Overview 이메일 발송 단계로 지연)
  3. Zotero 연결 테스트 (User ID 조회 + 컬렉션 검증)
  4. PaperBanana 확인 (없으면 선택 기능만 비활성화; 자동 클론 없음)
  5. SKILL.md 생성 (템플릿 플레이스홀더 치환)
  6. SKILL.md를 ~/.claude/skills/paper-curation/에 설치

Usage:
  python pipeline/setup.py              # 전체 설치
  python pipeline/setup.py --no-install # SKILL.md 스킬 설치 건너뛰기
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
try:
    from anthropic_auth import MIN_CLAUDE_CODE_VERSION, auth_status, claude_version
except Exception:  # setup should still print an actionable remedy if auth helper import fails
    MIN_CLAUDE_CODE_VERSION = (2, 1, 205)
    auth_status = None
    claude_version = None

REPO = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO / "config.json"
ENV_PATH = REPO / ".env"
EXAMPLE_PATH = REPO / "config.example.json"
TEMPLATE_PATH = REPO / "SKILL.md.template"
SKILL_OUTPUT = REPO / "SKILL.md"
GITIGNORE_PATH = REPO / ".gitignore"
SKILL_INSTALL_DIR = Path.home() / ".claude" / "skills" / "paper-curation"

def _load_dotenv(path=ENV_PATH):
    """Load a dependency-free .env subset without overriding shell exports."""
    loaded = []
    if not path.exists():
        return loaded
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            print(f"  △ .env:{line_number} 무시됨 (`KEY=value` 형식 필요)")
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        valid_key = (
            bool(key)
            and (key[0].isalpha() or key[0] == "_")
            and all(char.isalnum() or char == "_" for char in key)
        )
        if not valid_key:
            print(f"  △ .env:{line_number} 잘못된 변수명 무시됨")
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        if value and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)
    return loaded

def _fetch_zotero_collections(api_key):
    """Resolve the Zotero user and available collection names from one API key."""
    import urllib.request

    current_req = urllib.request.Request(
        "https://api.zotero.org/keys/current",
        headers={"Zotero-API-Key": api_key, "User-Agent": "paper-curation-setup"},
    )
    with urllib.request.urlopen(current_req, timeout=15) as response:
        user_id = str(json.load(response).get("userID", "")).strip()
    if not user_id:
        raise RuntimeError("Zotero API key 응답에 userID가 없습니다")

    collections_req = urllib.request.Request(
        f"https://api.zotero.org/users/{user_id}/collections?format=json&limit=100",
        headers={"Zotero-API-Key": api_key, "User-Agent": "paper-curation-setup"},
    )
    with urllib.request.urlopen(collections_req, timeout=15) as response:
        payload = json.load(response)
    collections = [
        (str(item.get("data", {}).get("name", "")).strip(), str(item.get("key", "")).strip())
        for item in payload
        if str(item.get("data", {}).get("name", "")).strip()
    ]
    return user_id, collections


def _topic_alias(name, key=""):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or key.lower() or "zotero"

def _topic_profile(alias, collection):
    if isinstance(collection, dict):
        label = str(collection.get("label") or collection.get("name") or "").strip()
        collection_name = str(collection.get("name") or label).strip()
        collection_key = str(collection.get("key") or "").strip()
    else:
        label = str(collection).strip()
        collection_name = label
        collection_key = ""
    primary = [label] if label else [alias.replace("-", " ").replace("_", " ")]
    profile = {
        "label": label,
        "collection_name": collection_name,
        "search_keywords": {
            "primary": primary,
            "secondary": [alias],
        },
    }
    if collection_key:
        profile["collection_key"] = collection_key
    return profile


def _topic_profiles(collections):
    return {
        alias: _topic_profile(alias, collection_name)
        for alias, collection_name in collections.items()
    }



def _select_zotero_collections(api_key):
    """Select one or more collections and return an alias->metadata mapping."""
    configured_name = os.environ.get("ZOTERO_COLLECTION_NAME", "").strip()
    configured_alias = os.environ.get("ZOTERO_TOPIC_ALIAS", "").strip()
    if configured_name:
        return {
            configured_alias or _topic_alias(configured_name): {
                "label": configured_name,
                "name": configured_name,
            }
        }

    try:
        _, collections = _fetch_zotero_collections(api_key)
    except Exception as exc:
        print(f"\n  ✗ Zotero 컬렉션 자동 조회 실패: {exc}")
        print("    API key 권한과 네트워크를 확인한 뒤 setup을 다시 실행하세요.")
        raise SystemExit(1) from exc

    if not collections:
        print("\n  ✗ Zotero 컬렉션이 없습니다. Zotero에서 컬렉션을 만든 뒤 다시 실행하세요.")
        raise SystemExit(1)
    if len(collections) == 1:
        name, key = collections[0]
        print(f"  ✓ Zotero 컬렉션 자동 선택: {name}")
        return {_topic_alias(name, key): {"label": name, "name": name, "key": key}}

    print("\n  Zotero 컬렉션을 선택하세요 (여러 개는 쉼표로 구분):")
    for index, (candidate, _) in enumerate(collections, 1):
        print(f"    {index}. {candidate}")
    selected = input(f"  번호 입력 [1-{len(collections)}]: ").strip()
    try:
        indexes = [int(value.strip()) for value in selected.split(",") if value.strip()]
    except ValueError:
        indexes = []
    if not indexes or any(index < 1 or index > len(collections) for index in indexes):
        print("  ✗ 올바른 컬렉션 번호가 필요합니다.")
        raise SystemExit(1)

    selected_collections = {}
    for index in dict.fromkeys(indexes):
        name, key = collections[index - 1]
        alias = _topic_alias(name, key)
        if alias in selected_collections:
            alias = f"{alias}-{key.lower()}"
        selected_collections[alias] = {"label": name, "name": name, "key": key}
    return selected_collections


def _select_zotero_collection(api_key):
    """Backward-compatible single-selection helper."""
    alias, collection = next(iter(_select_zotero_collections(api_key).items()))
    return collection["name"], alias


def step_config(existing_mode="prompt"):
    """Step 1: create config.json without silently trusting fork residue."""
    if CONFIG_PATH.exists():
        if existing_mode == "reuse":
            print(f"[1/6] 기존 config.json 명시적으로 재사용: {CONFIG_PATH}")
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        if existing_mode == "prompt":
            if not sys.stdin.isatty():
                print("ERROR: 기존 config.json이 있습니다. --reuse-config 또는 --fresh-config를 명시하세요.")
                raise SystemExit(2)
            print(f"[1/6] 기존 config.json 발견: {CONFIG_PATH}")
            choice = input("  현재 사용자의 설정입니까? [r=새로 설정/K=재사용] (기본 r): ").strip().lower()
            if choice == "k":
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        backup_path = CONFIG_PATH.with_name(f"{CONFIG_PATH.name}.backup")
        shutil.copy2(CONFIG_PATH, backup_path)
        print(f"  기존 설정 백업: {backup_path}")
    if not EXAMPLE_PATH.exists():
        print("ERROR: config.example.json이 없습니다.")
        sys.exit(1)

    print("=== Paper Curation 초기 설정 ===\n")
    print("[1/6] config.json 생성\n")
    print("  config.json은 clone/pull 또는 export만으로 생성되지 않습니다.")
    print("  이 설정 마법사가 지금 로컬 config.json을 생성합니다.")
    print("  API 키/토큰은 config.json에 저장하지 않고 .env 또는 프로세스 환경변수에서만 읽습니다.\n")

    # Zotero 설정 — 이미 export 한 값은 다시 입력받지 않는다.
    api_key = os.environ.get("ZOTERO_API_KEY", "").strip()
    if api_key:
        print("  ✓ ZOTERO_API_KEY 환경변수 감지")
    else:
        api_key = input("  Zotero API Key (https://www.zotero.org/settings/keys): ").strip()
    if not api_key:
        print("  ✗ ZOTERO_API_KEY가 필요합니다.")
        sys.exit(1)
    os.environ["ZOTERO_API_KEY"] = api_key
    email = (
        os.environ.get("ZOTERO_EMAIL", "").strip()
        or os.environ.get("UNPAYWALL_EMAIL", "").strip()
    )
    collections = _select_zotero_collections(api_key)
    for alias, collection in collections.items():
        print(f"  ✓ Topic alias: {alias} → {collection['name']}")

    pdf_dir = str(
        Path(os.environ.get("ZOTERO_DIR", "").strip() or REPO / "pdf_cache")
        .expanduser()
        .resolve()
    )
    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    print(f"  ✓ PDF cache 준비: {pdf_dir}")

    paperbanana_dir = os.environ.get("PAPERBANANA_DIR", "").strip()
    github_repo = os.environ.get("GITHUB_REPO", "").strip()

    cfg = {
        "zotero": {
            "email": email,
            "collections": {alias: collection["name"] for alias, collection in collections.items()},
            "pdf_dir": pdf_dir,
        },
        "topic_profiles": _topic_profiles(collections),
        "paths": {
            "zotero_dir": pdf_dir,
        },
        "anthropic_auth": {
            "mode": os.environ.get("PAPER_CURATION_ANTHROPIC_AUTH", "auto").strip() or "auto",
        },
        "features": {
            "auto_publish": False,
            "paperbanana": bool(paperbanana_dir),
        },
        "unpaywall_email": email,
    }
    if github_repo:
        cfg["github"] = {
            "repo": github_repo,
            "branch": "master",
            "pages_base_url": f"https://{github_repo.split('/')[0]}.github.io/{github_repo.split('/')[-1]}" if '/' in github_repo else ""
        }
    if paperbanana_dir:
        cfg["paperbanana_dir"] = paperbanana_dir

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"\n  → config.json 생성 완료")

    return cfg


# Core credentials gate. Zotero and Google are required for local setup; Anthropic
# is handled separately because it supports either Console API-key mode or Claude
# Code subscription OAuth. Resend is deferred until Audio Overview email delivery.
REQUIRED_KEYS = [
    {
        "env": "ZOTERO_API_KEY",
        "path": ("zotero", "api_key"),
        "placeholder": "YOUR_ZOTERO_API_KEY_HERE",
        "why": "Zotero 컬렉션·PDF 가져오기",
        "issue": "https://www.zotero.org/settings/keys",
        "prompt": "Zotero API Key",
    },
    {
        "env": "GOOGLE_API_KEY",
        "env_names": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        "path": ("google_api_key",),
        "why": "figure 검증·Audio Overview·PaperBanana 타임라인·Deep Research 임베딩",
        "issue": "https://aistudio.google.com/apikey",
        "prompt": "Google API Key (AIza...)",
    },
]
ANTHROPIC_API_SPEC = {
    "env": "ANTHROPIC_API_KEY",
    "path": ("anthropic_api_key",),
    "why": "리뷰·내러티브·Deep Research 답변 생성",
    "issue": "https://console.anthropic.com/settings/keys",
    "prompt": "Anthropic API Key (sk-ant-...)",
}
RESEND_SPEC = {
    "env": "RESEND_API_KEY",
    "path": ("resend_api_key",),
    "why": "Audio Overview 이메일 발송",
    "issue": "https://resend.com/api-keys",
}

OPENAI_SPEC = {
    "env": "OPENAI_API_KEY",
    "path": ("openai_api_key",),
    "why": "reader BYOK 답변 백엔드 / insights fallback",
}


def _cfg_get(cfg, path):
    """중첩 path(예: ("zotero","api_key"))를 따라 문자열 값을 읽는다. 없으면 ""."""
    node = cfg
    for k in path:
        if not isinstance(node, dict):
            return ""
        node = node.get(k, "")
    return node if isinstance(node, str) else ""


def _cfg_set(cfg, path, value):
    """중첩 path 에 값을 쓴다. 중간 dict 가 없으면 만든다."""
    node = cfg
    for k in path[:-1]:
        node = node.setdefault(k, {})
    node[path[-1]] = value


def _key_value(cfg, spec):
    """필수 키를 env → config.json 순으로 찾는다. placeholder 는 빈 값 취급.

    반환: (value, source) — 값이 없으면 ("", None)."""
    for env_name in spec.get("env_names", (spec["env"],)):
        env_val = os.environ.get(env_name, "").strip()
        if env_val:
            return env_val, "env"
    cfg_val = _cfg_get(cfg, spec["path"]).strip()
    if cfg_val and cfg_val != spec.get("placeholder"):
        return cfg_val, "config.json"
    return "", None


def _cfg_path_label(spec):
    return ".".join(spec["path"])


def _warn_legacy_config_secret(spec):
    field_path = _cfg_path_label(spec)
    print(
        f"  △ Migration: config.json field {field_path} contains a credential; "
        f"move it to {spec['env']} and remove the config field. Value is not shown."
    )




def missing_required_keys(cfg):
    """필수 Core 키 중 env·config 어디에도 값이 없는 항목 리스트를 반환한다.

    프롬프트·sys.exit 없는 순수 함수 — 게이트 로직 단위 테스트용."""
    return [spec for spec in REQUIRED_KEYS if not _key_value(cfg, spec)[0]]


def _prompt_required(spec):
    """필수 키가 어디에도 없을 때 직접 입력받는다. 입력을 건너뛰면 설치 중단."""
    print()
    print(f"  ✗ {spec['env']} 미설정 — {spec['why']}에 필요합니다.")
    print(f"    발급: {spec['issue']}")
    print("    지금 입력한 값은 현재 프로세스에만 보관되며 config.json에는 저장하지 않습니다.")
    print("    입력을 건너뛰면 설치가 여기서 중단됩니다.")
    user_input = input(f"    {spec['prompt']} (Enter 로 중단): ").strip()
    if not user_input:
        print(f"\n  {spec['env']} 가 필요합니다. 설치를 중단합니다.")
        print("  키를 발급한 뒤 다시 `python pipeline/setup.py` 를 실행해주세요.")
        sys.exit(1)
    return user_input


def _configured_anthropic_mode(cfg):
    value = cfg.get("anthropic_auth", {}) if isinstance(cfg, dict) else {}
    if isinstance(value, dict):
        mode = str(value.get("mode", "")).strip().lower().replace("_", "-")
        if mode in {"auto", "oauth", "api-key"}:
            return mode
    return ""


def _prompt_anthropic_choice():
    print()
    print("  Anthropic 인증 방식을 선택하세요:")
    print("    1) Claude Code OAuth (Pro/Max/Team/Enterprise 구독 사용량)")
    print("    2) Anthropic Console API key (종량제 API 과금)")
    choice = input("    선택 [1/2] (Enter=1): ").strip()
    return "api-key" if choice == "2" else "oauth"


def _oauth_unready_exit(status):
    print()
    detail = f" ({status.detail})" if getattr(status, "detail", "") else ""
    print(f"  ✗ Claude Code OAuth가 준비되지 않았습니다{detail}.")
    print("    해결:")
    print("      claude auth login")
    print("    또는 장기 토큰을 쓰는 환경에서는:")
    print("      claude setup-token")
    print("      export CLAUDE_CODE_OAUTH_TOKEN=...")
    print("    완료 후 다시 `python pipeline/setup.py --anthropic-auth oauth` 를 실행하세요.")
    sys.exit(1)


def _anthropic_status(mode):
    if auth_status is None:
        return SimpleNamespace(
            ready=False,
            source="",
            detail="pipeline/anthropic_auth.py 로드 실패",
            mode=mode,
        )
    return auth_status(None if mode == "auto" else mode)


def _ensure_anthropic_auth(cfg, requested_mode):
    """Anthropic auth gate: API key or Claude Code OAuth.

    OAuth persists only the non-secret mode marker. OAuth tokens are never read
    from prompts, written to config, logged, or passed on command lines.
    """
    dirty = False
    configured = _configured_anthropic_mode(cfg)
    mode = configured if requested_mode == "auto" and configured in {"oauth", "api-key"} else requested_mode
    status = _anthropic_status(mode)
    auto_selected = False

    if mode == "auto" and status.ready:
        mode = status.mode
        auto_selected = True
    elif mode == "auto":
        mode = _prompt_anthropic_choice()
        status = _anthropic_status(mode)

    if mode == "oauth":
        if not status.ready:
            _oauth_unready_exit(status)
        version = claude_version() if claude_version is not None else ()
        if version < MIN_CLAUDE_CODE_VERSION:
            installed = ".".join(str(part) for part in version) or "확인 불가"
            required = ".".join(str(part) for part in MIN_CLAUDE_CODE_VERSION)
            print(f"\n  ✗ Claude Code {installed}: OAuth structured output에는 >= {required} 필요")
            print("    `claude update` 실행 후 setup을 다시 시작하세요.")
            sys.exit(1)
        if not auto_selected and cfg.get("anthropic_auth") != {"mode": "oauth"}:
            cfg["anthropic_auth"] = {"mode": "oauth"}
            dirty = True
        source = status.source or "Claude Code"
        print(f"  ✓ Anthropic 인증 설정됨 (mode=oauth, source={source}) — Claude Code 구독 OAuth")
        print("    OAuth 토큰은 config.json 에 저장하지 않습니다.")
        return dirty

    if mode == "api-key":
        value, source = _key_value(cfg, ANTHROPIC_API_SPEC)
        if not value:
            value = _prompt_required(ANTHROPIC_API_SPEC)
            source = "입력"
        os.environ[ANTHROPIC_API_SPEC["env"]] = value
        if not auto_selected and cfg.get("anthropic_auth") != {"mode": "api-key"}:
            cfg["anthropic_auth"] = {"mode": "api-key"}
            dirty = True
        print(f"  ✓ Anthropic 인증 설정됨 (mode=api-key, source={source}) — {ANTHROPIC_API_SPEC['why']}")
        if source == "config.json":
            _warn_legacy_config_secret(ANTHROPIC_API_SPEC)
        print("    API key는 config.json에 새로 저장하지 않습니다.")
        return dirty

    print(f"  ✗ 알 수 없는 Anthropic 인증 모드: {mode}")
    sys.exit(1)


def step_env_check(cfg, anthropic_auth_mode="auto"):
    """Step 2: Core credential gate.

    Zotero and Google are required API keys. Anthropic accepts either Console
    API-key mode or Claude Code OAuth. Resend is optional/deferred until email
    delivery setup.
    """
    print("\n[2/6] Core credentials 확인")

    dirty = False
    for spec in REQUIRED_KEYS:
        value, source = _key_value(cfg, spec)
        if not value:
            value = _prompt_required(spec)
            source = "입력"
        os.environ[spec["env"]] = value
        print(f"  ✓ {spec['env']} 설정됨 ({source}) — {spec['why']}")
        if source == "config.json":
            _warn_legacy_config_secret(spec)
        if source == "입력":
            print("    값은 현재 프로세스에만 보관되며 config.json에 저장하지 않습니다.")

    dirty = _ensure_anthropic_auth(cfg, anthropic_auth_mode) or dirty

    resend_key, resend_source = _key_value(cfg, RESEND_SPEC)
    if resend_key:
        print(f"  ✓ RESEND_API_KEY 설정됨 (선택, {resend_source}) — {RESEND_SPEC['why']}")
        if resend_source == "config.json":
            _warn_legacy_config_secret(RESEND_SPEC)
    else:
        print("  · RESEND_API_KEY 미설정 (선택) — Audio Overview 이메일 발송 때 설정하면 됩니다.")
        print("    배포 후 `npx wrangler secret put RESEND_API_KEY` 로 등록하세요.")

    if dirty:
        _save_config(cfg)

    # OPTIONAL: OPENAI_API_KEY 는 게이트 없음 (정보성 안내만)
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if openai_key:
        print("  ✓ OPENAI_API_KEY 설정됨 (선택) — reader BYOK 답변 백엔드 / insights fallback")
    else:
        openai_key = cfg.get("openai_api_key", "").strip()
        if openai_key:
            _warn_legacy_config_secret(OPENAI_SPEC)
            print("  ✓ OPENAI_API_KEY 설정됨 (선택, config.json) — reader BYOK 답변 백엔드 / insights fallback")
        else:
            print("  · OPENAI_API_KEY 미설정 (선택) — Deep Research 임베딩은 Gemini 로 이동했습니다.")
            print("    reader BYOK 답변 백엔드 / insights fallback 으로만 선택적으로 유용합니다.")


def step_zotero_test(cfg):
    """Step 3: Zotero API 연결 테스트."""
    import urllib.request

    print("\n[3/6] Zotero 연결 테스트")

    api_key = (
        os.environ.get("ZOTERO_API_KEY", "").strip()
        or cfg.get("zotero", {}).get("api_key", "").strip()
    )
    if not api_key or api_key == "YOUR_ZOTERO_API_KEY_HERE":
        print("  ✗ Zotero API key가 설정되지 않았습니다")
        return False

    # User ID 조회
    try:
        url = "https://api.zotero.org/keys/current"
        req = urllib.request.Request(url, headers={
            "Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        user_id = str(data.get("userID", ""))
        print(f"  ✓ User ID: {user_id}")
    except Exception as e:
        print(f"  ✗ User ID 조회 실패: {e}")
        return False

    # 컬렉션 검증
    collections = cfg.get("zotero", {}).get("collections", {})
    if not collections:
        print("  ✗ 컬렉션이 설정되지 않았습니다")
        return False

    try:
        url = f"https://api.zotero.org/users/{user_id}/collections?format=json&limit=100"
        req = urllib.request.Request(url, headers={
            "Zotero-API-Key": api_key, "User-Agent": "Mozilla/5.0",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            cols = json.load(resp)
        name_to_key = {c["data"]["name"]: c["data"]["key"] for c in cols}
    except Exception as e:
        print(f"  ✗ 컬렉션 목록 조회 실패: {e}")
        return False

    all_ok = True
    failed = {}
    available = sorted(name_to_key.keys())
    for alias, name in collections.items():
        if name in name_to_key:
            print(f"  ✓ '{alias}' → '{name}' (key: {name_to_key[name]})")
        else:
            print(f"  ✗ '{alias}' → '{name}' — Zotero에서 찾을 수 없습니다")
            print(f"    사용 가능한 컬렉션: {', '.join(available)}")
            failed[alias] = name
            all_ok = False

    if failed:
        # Claude Code가 파싱할 수 있도록 JSON으로도 출력
        print(f"  [COLLECTION_ERROR] {json.dumps({'failed': failed, 'available': available}, ensure_ascii=False)}")

    return all_ok


PAPERBANANA_DEFAULT_DIR = REPO / "paperbanana"


def step_paperbanana(cfg):
    """Step 4: report optional PaperBanana availability without installing it."""
    print("\n[4/6] 선택 기능 확인")
    pb_dir = cfg.get("paperbanana_dir", "")
    if pb_dir and Path(pb_dir).exists():
        print(f"  ✓ PaperBanana: {pb_dir}")
        return cfg
    if PAPERBANANA_DEFAULT_DIR.exists() and (PAPERBANANA_DEFAULT_DIR / "README.md").exists():
        print(f"  ✓ PaperBanana 발견: {PAPERBANANA_DEFAULT_DIR}")
        cfg["paperbanana_dir"] = str(PAPERBANANA_DEFAULT_DIR)
        _save_config(cfg)
        return cfg
    if pb_dir:
        print(f"  △ PaperBanana 경로가 존재하지 않습니다: {pb_dir}")
    print("  · PaperBanana 미설치 — 선택 기능인 타임라인 이미지 생성만 건너뜁니다.")
    print("    setup은 외부 저장소를 자동 clone하지 않습니다.")
    return cfg


def _save_config(cfg):
    """config.json 업데이트."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def step_skill_md(cfg):
    """Step 5: SKILL.md 생성."""
    print("\n[5/6] SKILL.md 생성")

    zotero = cfg.get("zotero", {})
    github = cfg.get("github", {})

    replacements = {
        "{github_repo}": github.get("repo", ""),
        "{pages_base_url}": github.get("pages_base_url", ""),
        "{zotero_dir}": zotero.get("pdf_dir", ""),
        "{project_dir}": str(REPO),
        "{email}": zotero.get("email", "") or cfg.get("unpaywall_email", ""),
    }

    if not TEMPLATE_PATH.exists():
        print("  ✗ SKILL.md.template이 없습니다")
        return False

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    with open(SKILL_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {SKILL_OUTPUT}")

    # .gitignore에 config.json 확인
    if GITIGNORE_PATH.exists():
        gi = GITIGNORE_PATH.read_text(encoding="utf-8")
        if "config.json" not in gi:
            with open(GITIGNORE_PATH, "a", encoding="utf-8") as f:
                f.write("\nconfig.json\n")
            print("  ✓ .gitignore에 config.json 추가")

    return True


def step_install():
    """Step 5: SKILL.md를 Claude Code skills에 설치."""
    print("\n[6/6] SKILL.md 설치")

    if not SKILL_OUTPUT.exists():
        print("  ✗ SKILL.md가 없습니다")
        return False

    SKILL_INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SKILL_OUTPUT, SKILL_INSTALL_DIR / "SKILL.md")
    print(f"  ✓ {SKILL_INSTALL_DIR / 'SKILL.md'}")
    return True


# classify_papers / topic_modeling 이 의존하는 클러스터링 스택 — 이 import 들이
# 실제로 돌 인터프리터(py312) 에서 모두 통과해야 auto-run 이 중간에 안 죽는다.
_CLUSTERING_IMPORTS = "import umap, hdbscan, sentence_transformers, sklearn, numpy, joblib"


def _resolve_py312():
    """topic_modeling/classify 가 실제로 쓸 인터프리터를 run_update_force 와 동일 규칙으로 해석.

    run_update_force._resolve_topic_modeling_python() 를 그대로 재사용해 우선순위
    (PAPER_CURATION_PY312 → 형제 py312 env → which python3.12 → sys.executable)가
    런타임과 어긋나지 않게 한다. import 실패 시 보수적으로 sys.executable 로 fallback.
    """
    try:
        sys.path.insert(0, str(REPO / "pipeline"))
        from run_update_force import _resolve_topic_modeling_python  # type: ignore
        return _resolve_topic_modeling_python()
    except Exception:
        return sys.executable


def _preflight_clustering_env():
    """auto-run 전에 클러스터링 의존성이 py312 인터프리터에서 import 가능한지 확인.

    두 가지 실패 모드를 모두 잡는다:
      (a) py314 단일 env → numba CALL_KW 크래시 (UMAP/HDBSCAN 미라우팅)
      (b) 의존성 미설치 → ModuleNotFoundError
    실패하면 정확한 conda 명령을 안내하고 False 를 반환해 auto-run 을 건너뛴다.
    setup.py 자기 프로세스가 아니라 *실제로 돌 인터프리터* 로 probe 해야 의미가 있다.
    """
    py = _resolve_py312()
    try:
        probe = subprocess.run(
            [py, "-c", _CLUSTERING_IMPORTS],
            capture_output=True, text=True, timeout=120,
        )
    except Exception as e:
        print(f"  ✗ 클러스터링 인터프리터 점검 실패: {e}")
        probe = None

    if probe is not None and probe.returncode == 0:
        if py != sys.executable:
            print(f"  ✓ 클러스터링 인터프리터 확인: {py}")
        return True

    # 실패 — 정확한 복구 명령 안내
    print("  ✗ UMAP/HDBSCAN 클러스터링 환경이 준비되지 않았습니다.")
    print(f"    점검 인터프리터: {py}")
    if probe is not None and probe.stderr.strip():
        # 마지막 줄(주로 ModuleNotFoundError / numba CALL_KW)만 간결히 표시
        last = probe.stderr.strip().splitlines()[-1]
        print(f"    원인: {last}")
    print()
    print("    classify_papers/topic_modeling 은 numba+Python 3.14 충돌을 피하려고")
    print("    별도 py312 conda env 에서 돌아야 합니다. 아래를 실행해 환경을 만드세요:")
    print()
    print("      conda create -n py312 -c conda-forge python=3.12 pip -y")
    print("      conda run -n py312 pip install umap-learn hdbscan sentence-transformers \\")
    print("          joblib numpy scikit-learn anthropic openai")
    print()
    print("    (형제 env 가 아닌 경로면 PAPER_CURATION_PY312 환경변수로 절대 경로 지정)")
    return False


def main():
    parser = argparse.ArgumentParser(description="paper-curation setup")
    parser.add_argument("--no-install", action="store_true",
                        help="SKILL.md 스킬 설치를 건너뜁니다")
    parser.add_argument("--no-run", action="store_true",
                        help="설치만 하고 첫 파이프라인 실행은 건너뜁니다")
    parser.add_argument("--anthropic-auth", choices=("auto", "oauth", "api-key"),
                        default="auto",
                        help="Anthropic 인증 방식: auto(기본), oauth(Claude Code), api-key(Console)")
    config_group = parser.add_mutually_exclusive_group()
    config_group.add_argument("--fresh-config", action="store_true",
                              help="기존 config.json을 백업하고 현재 사용자 설정을 새로 만듭니다")
    config_group.add_argument("--reuse-config", action="store_true",
                              help="기존 config.json이 현재 사용자 것임을 명시하고 재사용합니다")
    args = parser.parse_args()

    print("=" * 50)
    print("  Paper Curation — Setup")
    print("=" * 50)
    dotenv_keys = _load_dotenv()
    if dotenv_keys:
        print(f"  ✓ .env 로드: 비어 있지 않은 설정 {len(dotenv_keys)}개 (값은 표시하지 않음)")

    # Step 1: config.json. Existing ignored files may be fork/worktree residue.
    config_mode = "fresh" if args.fresh_config else "reuse" if args.reuse_config else "prompt"
    cfg = step_config(config_mode)

    # Step 2: Core credentials gate (Zotero/Google required, Anthropic API key or OAuth)
    step_env_check(cfg, args.anthropic_auth)

    # Step 3: Zotero 연결
    step_zotero_test(cfg)

    # Step 4: PaperBanana
    cfg = step_paperbanana(cfg)

    # Step 5: SKILL.md
    step_skill_md(cfg)

    # Step 5: 스킬 설치
    if not args.no_install:
        step_install()
    else:
        print(f"\n[6/6] 스킬 설치 건너뜀 (--no-install)")
        print(f"  수동 설치: cp {SKILL_OUTPUT} ~/.claude/skills/paper-curation/SKILL.md")

    # 요약
    collections = cfg.get("zotero", {}).get("collections", {})
    topics = list(collections.keys())

    print("\n" + "=" * 50)
    print("  설치 완료!")
    print("=" * 50)
    print(f"  Config:  {CONFIG_PATH}")
    if SKILL_OUTPUT.exists():
        print(f"  SKILL:   {SKILL_OUTPUT}")

    # 다음 단계 안내
    print("\n" + "-" * 50)
    print("  다음 단계: 파이프라인 실행")
    print("-" * 50)
    print()
    print("  필수 인증 확인 완료: ZOTERO·GOOGLE + Anthropic(API key 또는 Claude Code OAuth).")
    print("  이제 파이프라인을 실행하여 Zotero 컬렉션의 논문을 리뷰하고")
    print("  웹 페이지로 배포할 수 있습니다.")
    print()
    print("  ⚠ 주의: Zotero 컬렉션의 논문 편수에 따라 시간이 크게 달라집니다 (Anthropic Tier·concurrency 의존).")
    print("    - 10편 이하: 수 분")
    print("    - 50편: ~15분 (Tier 4 default --concurrency 16) ~ 1~2시간 (Tier 1 --concurrency 4)")
    print("    - 500편 이상: 비례 증가. Tier별 권장값은 README 'Concurrency 가이드' 참고.")
    print()
    if topics:
        topic = topics[0]
        print(f"  실행 명령어 (이후에 수동으로 돌릴 때 — 단일 진입점은 run_full.py):")
        print(f"    # 전체 파이프라인 (Zotero에서 가져와서 리뷰 + 분류/인덱스, 배포·vector rebuild 억제)")
        print(f"    PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 PYTHONUTF8=1 python pipeline/run_full.py --topic {topic} --mode curate --source zotero --no-deploy")
        print()
        print(f"    # 주간 운영 (웹 검색으로 신규 논문 추가, 기존 유지, 배포·vector rebuild 억제)")
        print(f"    PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 PYTHONUTF8=1 python pipeline/run_full.py --topic {topic} --mode curate --source web --days 7 --no-deploy")
        print()
        print(f"    # 명시적 vector/full rebuild (시간·비용 ↑, 배포 억제)")
        print(f"    PAPER_CURATION_NO_DEPLOY=1 PYTHONUTF8=1 python pipeline/run_full.py --topic {topic} --mode rebuild --yes --no-deploy")
    print()

    # 배포·이메일은 나중 단계 — 설치 시점에는 자격증명을 묻지 않는다 (deferred)
    print("-" * 50)
    print("  나중 단계: 배포 & Audio Overview 이메일 (지금은 건너뜀)")
    print("-" * 50)
    print()
    print("  Cloudflare/GitHub 배포 자격증명은 설치 때 묻지 않습니다. 처음 배포할 때")
    print("  `run_full.py --mode deploy` 가 필요한 env(CF_API_TOKEN·CLOUDFLARE_ACCOUNT_ID·")
    print("  GitHub 설정)를 그 자리에서 안내합니다. Audio Overview 이메일 발송 기능은")
    print("  워커를 한 번 배포해 두어야 동작하며, 배포된 워커에 시크릿을 등록해야 합니다:")
    print("    npx wrangler secret put GOOGLE_API_KEY   # 워커 측 TTS/Audio Overview 용")
    print("    npx wrangler secret put RESEND_API_KEY   # MP3 첨부 메일 발송용")
    print("  (자세한 내용은 README 'Audio Overview 이메일 발송 — Cloudflare Worker secrets' 참고)")
    print()

    # Step 7: 첫 파이프라인 자동 실행 (--no-run 으로 건너뛸 수 있음)
    if topics and not args.no_run:
        topic = topics[0]
        print("-" * 50)
        print(f"  첫 파이프라인을 자동 실행합니다 (topic: {topic})")
        print("-" * 50)

        # Preflight: classify/topic_modeling 은 UMAP/HDBSCAN 의존 — 별도 py312 env
        # 에서 돌아야 한다 (numba 가 Python 3.14 의 CALL_KW opcode 를 못 다룸).
        # 의존성이 없거나 인터프리터가 py314 단일 env 면 build_papers_index →
        # topic_modeling 에서 CRITICAL_STEP 이 hard-fail 하므로, 깊숙이 들어가
        # 죽기 전에 여기서 미리 막고 정확한 conda 명령을 안내한 뒤 auto-run 을 건너뛴다.
        if not _preflight_clustering_env():
            print()
            print("  (위 환경을 준비한 뒤 'python pipeline/setup.py' 를 다시 실행하세요.)")
        else:
            print("  Zotero에서 논문을 가져와 리뷰 → 분류 → 인덱스까지 진행합니다.")
            print("  Vector/full rebuild는 자동 실행하지 않습니다. 위의 명시적 rebuild 명령을 별도로 실행하세요.")
            print("  Ctrl+C 로 중단할 수 있고, 중단 후에는 --resume 모드로 이어서 진행할 수 있습니다.")
            print()
            try:
                # 문서화된 단일 진입점 run_full.py 사용 — curate/zotero 가 비파괴
                # 기본 경로이며, topic_modeling/classify 의 py312 라우팅은 내부에서 처리.
                subprocess.run(
                    [sys.executable, str(REPO / "pipeline" / "run_full.py"),
                     "--topic", topic, "--mode", "curate", "--source", "zotero",
                     "--concurrency", "4", "--no-deploy"],
                    env={**os.environ, "PAPER_CURATION_NO_DEPLOY": "1", "PAPER_CURATION_NO_VECTOR_REBUILD": "1", "PYTHONUTF8": "1"},
                    cwd=str(REPO),
                )
            except KeyboardInterrupt:
                print("\n  (파이프라인 실행이 중단되었습니다. 나중에 --resume 으로 재개 가능)")
    elif topics and args.no_run:
        print("  (--no-run 지정: 첫 파이프라인 실행은 건너뜁니다)")
    print()


if __name__ == "__main__":
    main()
