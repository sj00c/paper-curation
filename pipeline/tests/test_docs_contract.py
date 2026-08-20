"""문서가 코드보다 오래 살아남지 못하게 한다.

이 브랜치는 cross-provider 대체를 제거했는데, 문서 다섯 곳은 여전히
"Anthropic → OpenAI → Gemini 3-backend fallback" 을 광고하고 있었다. 코드가
안 하는 일을 문서가 약속하면, 읽는 사람(사람이든 에이전트든)은 없는 안전망을
믿고 결정한다. 제거된 동작을 광고하는 것은 조용한 거짓말이고, 이 브랜치가
없애려는 결함과 같은 종류다.

AGENTS.md 도 같은 이유로 여기서 고정한다. CLAUDE.md 를 sed 로 복사해 만든
쌍둥이였는데 "Claude" 를 전부 "Codex" 로 치환하는 바람에 존재하지 않는 경로
(`~/.Codex/skills`), 존재하지 않는 모델("Codex Haiku/Sonnet") 을 문서화하고
있었고, CLAUDE.md 가 갱신될 때 같이 갱신되지 않아 제거된 fallback 과 "필수"
라던 선택 키를 그대로 들고 있었다.
"""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# 각 문자열은 실제로 문서에 있었고, 코드에서 제거된 동작을 서술한다.
FORBIDDEN = {
    "3-backend fallback": "cross-category insights 는 backend 하나만 쓴다",
    "Anthropic → OpenAI → Gemini chain": "체인이 아니라 우선순위 목록이다",
    "Anthropic → OpenAI → Gemini fallback": "체인이 아니라 우선순위 목록이다",
    "OpenAI/Gemini fallback": "실패해도 다른 벤더가 대신 답하지 않는다",
    "insights fallback": "insights 는 대체하지 않는다 (backend 후보일 뿐)",
    "다음 backend 자동 시도": "자동 시도는 제거됐다",
    "_call_connections_batch": "존재하지 않는 함수",
    "emit_connections": "존재하지 않는 tool",
}

DOCS = [
    "README.md",
    "README.en.md",
    "CLAUDE.md",
    "AGENTS.md",
    "docs/architecture.md",
    "docs/operations.md",
    "docs/setup-guide.md",
    "SKILL.md",
    "SKILL.md.template",
    "SECURITY.md",
]


def _read(rel):
    path = REPO / rel
    return path.read_text(encoding="utf-8") if path.exists() else None


def _require(rel):
    path = REPO / rel
    if not path.exists():
        raise AssertionError(f"{rel} 가 없다")
    return path.read_text(encoding="utf-8")


class RemovedBehaviourIsNotAdvertisedTests(unittest.TestCase):
    def test_migration_docs_use_the_supported_cli(self):
        for rel in ("README.md", "README.en.md", "docs/operations.md", "docs/setup-guide.md"):
            text = _require(rel)
            self.assertIn("paper-curation migrate --config config.json", text)
            self.assertNotIn("--migrate-config", text)

    def test_no_doc_advertises_a_removed_fallback(self):
        offenders = []
        for rel in DOCS:
            text = _read(rel)
            if text is None:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for phrase, why in FORBIDDEN.items():
                    if phrase in line:
                        offenders.append(f"{rel}:{lineno} '{phrase}' — {why}")
        self.assertEqual([], offenders, "제거된 동작을 광고하는 문서:\n" + "\n".join(offenders))

    def test_the_no_substitution_rule_is_stated_where_backends_are_listed(self):
        """backend 목록을 보여주는 문서는 그게 대체 체인이 아니라고 말해야 한다.

        (assertIn 대신 assertTrue — 실패 메시지에 문서 전문이 쏟아지지 않게.)
        """
        for rel, marker in (
            ("docs/architecture.md", "대체 체인이 아니다"),
            ("README.en.md", "never falls back"),
            ("CLAUDE.md", "대체 금지"),
        ):
            text = _require(rel)
            self.assertTrue(
                marker in text, f"{rel} 가 무대체 규칙을 말하지 않는다: '{marker}' 없음"
            )

    def test_the_backend_env_var_is_documented_where_the_order_is_explained(self):
        for rel in ("docs/architecture.md",):
            text = _require(rel)
            self.assertTrue(
                "EXTRACT_INSIGHTS_CC_BACKENDS" in text,
                f"{rel} 가 backend 순서 env var 를 설명하지 않는다",
            )


class ToolSchemaTableTests(unittest.TestCase):
    """architecture.md 의 tool-use 표에 적힌 tool 이 실제로 존재해야 한다.

    `emit_connections` 는 코드 어디에도 없는데 이 표에 몇 달을 앉아 있었다.
    """

    def _documented_tools(self):
        text = _require("docs/architecture.md")
        lines = text.splitlines()
        try:
            start = next(i for i, l in enumerate(lines) if l.startswith("| 호출처 | tool 이름"))
        except StopIteration:
            return []

        tools = []
        for line in lines[start + 1:]:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: "):
                continue
            found = re.findall(r"`([a-z_]+)`", cells[1])
            tools.extend(found)
        return tools

    def test_documented_tools_exist_in_the_pipeline(self):
        tools = self._documented_tools()
        if not tools:
            return

        sources = "\n".join(
            p.read_text(encoding="utf-8", errors="ignore")
            for p in (REPO / "pipeline").rglob("*.py")
            if "tests" not in p.parts
        )
        missing = [t for t in tools if f'"name": "{t}"' not in sources]
        self.assertEqual([], missing, f"문서에만 있는 tool: {missing}")


class DocumentedEnvVarsTests(unittest.TestCase):
    """문서가 광고하는 튜닝 노브는 실제로 읽히는 것이어야 한다.

    `EXTRACT_INSIGHTS_PARALLEL` 은 세 문서가 "Tier 1~3 에서는 낮추라" 고
    권했지만 코드 어디에서도 읽지 않았다. 실제 노브는
    `PAPER_CONNECTION_WORKERS` 다. 없는 손잡이를 돌리라고 시키는 문서는
    사용자가 429 를 못 피하게 만든다.
    """

    # 코드가 아니라 외부(셸/CI/배포 플랫폼)가 소비하는 변수.
    EXTERNAL = {"PYTHONUTF8", "PYTHONPATH"}

    # env var 가 아예 아닌 도메인 상수. 정규식은 백틱 안 대문자를 전부 후보로
    # 잡으므로, SPDX 라이선스 값이나 저널 상태 이름처럼 "환경변수가 아닌 것" 은
    # 여기에 이름을 적어 구분한다. EXTERNAL 과 섞지 않는다 — 저쪽은 실제
    # 환경변수지만 우리 코드가 아니라 런타임이 읽는 것들이다.
    NOT_ENV_VARS = {
        "NOASSERTION",                                   # SPDX license status
        "PREPARED", "LEDGER_DURABLE",                    # bibliography journal states
        "DB_COMMITTED", "DESCRIPTOR_COMMITTED",
    }

    def _source_text(self):
        # 테스트는 제외한다. 이 파일이 docstring 에 폐기된 이름을 적어두면
        # 그 자체가 "소스에 있다" 는 증거가 되어 검사가 자기 자신을 무력화한다.
        parts = []
        for pattern in ("pipeline/**/*.py", "scripts/*.py", "worker/*.js", "bin/*.mjs"):
            for path in REPO.glob(pattern):
                if "tests" in path.parts:
                    continue
                parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        return "\n".join(parts)

    def test_every_documented_env_var_is_read_somewhere(self):
        sources = self._source_text()
        offenders = []
        for rel in DOCS:
            text = _read(rel)
            if text is None:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for name in re.findall(r"`([A-Z][A-Z0-9_]{5,})`", line):
                    if name in self.EXTERNAL or name in self.NOT_ENV_VARS or name in sources:
                        continue
                    offenders.append(f"{rel}:{lineno} {name}")
        self.assertEqual(
            [], offenders, "코드가 읽지 않는 env var 를 문서가 광고한다:\n" + "\n".join(offenders)
        )


class AgentsMirrorsClaudeTests(unittest.TestCase):
    """AGENTS.md 와 CLAUDE.md 는 헤더 말고 한 글자도 달라선 안 된다."""

    HEADER_LINES = 3  # 제목, 빈 줄, 공통 안내문

    def test_bodies_are_identical(self):
        claude = _require("CLAUDE.md")
        agents = _require("AGENTS.md")

        claude_body = claude.split("\n", self.HEADER_LINES)[self.HEADER_LINES]
        agents_body = agents.split("\n", self.HEADER_LINES)[self.HEADER_LINES]
        self.assertEqual(
            claude_body,
            agents_body,
            "AGENTS.md 와 CLAUDE.md 가 갈라졌다. 한쪽만 갱신하면 다른 쪽을 읽는 "
            "에이전트가 낡은 규칙을 따른다.",
        )

    def test_agents_md_does_not_rename_the_product(self):
        """에이전트 이름은 바꿔도, 제품/경로/모델 이름은 사실이라 바꾸면 거짓이 된다."""
        agents = _require("AGENTS.md")
        for wrong in ("~/.Codex", "Codex.ai/code", "Codex Haiku", "Codex/Gemini"):
            self.assertNotIn(wrong, agents, f"AGENTS.md 에 잘못된 이름: {wrong}")
        self.assertIn("paper-curation", agents)


if __name__ == "__main__":
    unittest.main()
