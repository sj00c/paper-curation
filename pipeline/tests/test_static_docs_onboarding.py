"""Static contracts for truthful, non-deploying first-run documentation."""

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ONBOARDING_DOCS = (
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs" / "setup-guide.md",
)
DOCS = ONBOARDING_DOCS + (ROOT / "docs" / "operations.md", ROOT / "CLAUDE.md")
SKILL_TEMPLATES = (
    ROOT / "SKILL.md.template",
    ROOT / "skills" / "SKILL.md.template",
)
MANIFEST = ROOT / "skills" / "manifest.json"
UNPINNED_CLONE = re.compile(r"^\s*git clone https://github\.com/", re.MULTILINE)
SECRET_ASSIGNMENT = re.compile(
    r"^\s*(?:export\s+(?:CLAUDE_CODE_OAUTH_TOKEN|GOOGLE_API_KEY|GEMINI_API_KEY|"
    r"ZOTERO_API_KEY|ANTHROPIC_API_KEY)=|setx\s+(?:CF_API_TOKEN|"
    r"CLOUDFLARE_API_TOKEN|CLOUDFLARE_ACCOUNT_ID)\b)",
    re.MULTILINE | re.IGNORECASE,
)
UNQUALIFIED_NPX = "npx --yes github:jehyunlee/paper-curation"
SMOKE_COMMAND = "--mode smoke"
HARDCODED_TOPIC_COMMAND = re.compile(r"^\s*(?!#).*--topic\s+(?:ai4s|scisci)\b", re.MULTILINE)
DEFAULT_DIRECT_PYTHON_FLOW = re.compile(
    r"^\s*(?!#).*python\s+pipeline/(?:run_full|search_papers)\.py\b",
    re.MULTILINE,
)
CONFIG_SECRET_KEY = re.compile(r'"(?:api_key|anthropic_api_key|gemini_api_key|google_api_key)"\s*:')
FRESH_CONFIG_COMMAND = "node ./bin/paper-curation.mjs setup --fresh-config"
STALE_LOCAL_SETUP_COMMAND = "npx . setup --auth oauth"


def manifest_contract_text():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fields = []
    for skill in manifest["skills"]:
        fields.extend(str(skill.get(key, "")) for key in ("id", "description", "purpose", "command", "safety"))
    return "\n".join(fields)

def documented_shell_commands(text):
    command = []
    for line in text.splitlines():
        stripped = line.strip()
        if command:
            command.append(stripped.removesuffix("\\").rstrip())
            if not stripped.endswith("\\"):
                yield " ".join(command)
                command = []
        elif stripped.endswith("\\"):
            command = [stripped.removesuffix("\\").rstrip()]
        else:
            yield stripped
    if command:
        yield " ".join(command)


class StaticOnboardingDocsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = {path: path.read_text(encoding="utf-8") for path in DOCS}
        cls.skill_text = {path: path.read_text(encoding="utf-8") for path in SKILL_TEMPLATES}
        cls.manifest_text = manifest_contract_text()

    def test_current_journey_uses_dependency_free_checkout_harness(self):
        for path in ONBOARDING_DOCS:
            with self.subTest(path=path):
                text = self.text[path]
                self.assertIn("node ./bin/paper-curation.mjs skill install", text)
                self.assertIn("node ./bin/paper-curation.mjs setup --fresh-config", text)
                self.assertIn(
                    "node ./bin/paper-curation.mjs doctor --network",
                    text,
                )
                self.assertNotIn("npx . setup --auth oauth", text)

    def test_unqualified_github_npx_is_never_an_executable_command(self):
        for path, text in self.text.items():
            with self.subTest(path=path):
                executable = [
                    line for line in text.splitlines()
                    if UNQUALIFIED_NPX in line
                    and not line.lstrip().startswith(("#", ">", "-", "*"))
                    and "`" not in line
                ]
                self.assertEqual(executable, [])
                self.assertNotIn("APPROVED_REF", text)

    def test_fallbacks_do_not_clone_a_moving_default_branch(self):
        for path in DOCS:
            with self.subTest(path=path):
                self.assertIsNone(UNPINNED_CLONE.search(self.text[path]))

    def test_novice_docs_do_not_put_secrets_in_shell_history(self):
        for path in DOCS:
            with self.subTest(path=path):
                self.assertIsNone(SECRET_ASSIGNMENT.search(self.text[path]))

    def test_fresh_config_examples_do_not_store_api_keys(self):
        for path in ONBOARDING_DOCS:
            with self.subTest(path=path):
                self.assertIsNone(CONFIG_SECRET_KEY.search(self.text[path]))

    def test_smoke_commands_use_both_deploy_suppressors(self):
        for path, text in self.text.items():
            commands = [
                command
                for command in documented_shell_commands(text)
                if SMOKE_COMMAND in command
                and not command.startswith(("#", ">", "-", "*", "|"))
                and "`" not in command
            ]
            for command in commands:
                with self.subTest(path=path, command=command):
                    self.assertIn("PAPER_CURATION_NO_DEPLOY=1", command)
                    self.assertIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
                    self.assertIn("--no-deploy", command)

    def test_local_postprocessing_commands_suppress_deploy(self):
        pattern = re.compile(r"^(?!.*[#`\\|]).*--mode (?:reclassify|retime).*$", re.MULTILINE)
        for path, text in self.text.items():
            for command in pattern.findall(text):
                with self.subTest(path=path, command=command):
                    self.assertIn("PAPER_CURATION_NO_DEPLOY=1", command)
                    self.assertIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
                    self.assertIn("--no-deploy", command)

    def test_local_fallback_recovery_suppresses_deploy(self):
        pattern = re.compile(r"^(?!.*[#`\\|]).*--local-fallback.*$", re.MULTILINE)
        for path, text in self.text.items():
            for command in pattern.findall(text):
                with self.subTest(path=path, command=command):
                    self.assertIn("PAPER_CURATION_NO_DEPLOY=1", command)
                    self.assertIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
                    self.assertIn("--no-deploy", command)

    def test_mismatch_recovery_commands_suppress_deploy(self):
        pattern = re.compile(
            r"^.*(?:"
            r"--mode (?:audit|fix-matching|validate)\b|"
            r"--mode rebuild\b.*--slugs"
            r").*$",
            re.MULTILINE,
        )
        commands = [
            (path, command)
            for path, text in self.text.items()
            for command in pattern.findall(text)
            if not command.lstrip().startswith(("#", ">", "-", "*"))
            and "`" not in command
            and "|" not in command
        ]
        self.assertGreater(len(commands), 0)
        for path, command in commands:
            with self.subTest(path=path, command=command):
                self.assertIn("PAPER_CURATION_NO_DEPLOY=1", command)
                self.assertIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
                self.assertIn("--no-deploy", command)

    def test_fix_matching_prints_safe_followup_commands(self):
        source = (ROOT / "pipeline" / "fix_matching.py").read_text(encoding="utf-8")
        self.assertIn("PAPER_CURATION_NO_DEPLOY=1 PYTHONUTF8=1 ", source)
        self.assertIn("--mode rebuild ", source)
        self.assertIn("--slugs {c} --strict-pdf --no-deploy --yes", source)
        self.assertIn("--mode audit --no-deploy", source)

    def test_setup_local_first_run_paths_suppress_deploy_and_vector_rebuild(self):
        source = (ROOT / "pipeline" / "setup.py").read_text(encoding="utf-8")
        self.assertIn("PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run --", source)
        self.assertIn("--mode curate --source zotero --no-deploy", source)
        self.assertIn("--mode curate --source web --days 7 --no-deploy", source)
        self.assertIn("--mode rebuild --yes --no-deploy", source)
        self.assertIn('"PAPER_CURATION_NO_DEPLOY": "1"', source)
        self.assertIn('"PAPER_CURATION_NO_VECTOR_REBUILD": "1"', source)
        self.assertIn("Vector/full rebuild는 자동 실행하지 않습니다", source)

    def test_docs_expose_preview_only_and_fail_closed_deployment(self):
        for path in ONBOARDING_DOCS:
            with self.subTest(path=path):
                text = self.text[path]
                lowered = text.lower()
                self.assertNotRegex(lowered, r"auto[- ]publish|자동 publish|자동으로 (?:공개|배포)")
                self.assertIn(
                    "node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run",
                    text,
                )
                self.assertRegex(
                    lowered,
                    r"(?:fail-closed|fails closed|거부|unavailable).*(?:deploy|배포)|(?:deploy|배포).*(?:fail-closed|fails closed|거부|unavailable)",
                )

        operations = self.text[ROOT / "docs" / "operations.md"]
        self.assertIn("일반 `run`은 deploy를 승인하거나 실행하지 않", operations)
        self.assertIn("신뢰할 수 있는 deployment approval issuer/executor가 없", operations)

    def test_web_search_preview_keeps_candidate_work_bounded(self):
        source = (ROOT / "pipeline" / "run_full.py").read_text(encoding="utf-8")
        self.assertIn(
            "Web search/register candidate limit only; not a Zotero review or post-processing cap.",
            source,
        )
        self.assertIn('if routing["search"]:', source)
        self.assertIn('"--max-papers", str(args.max_papers)', source)
        self.assertIn('help="실행 계획만 출력, 실제 호출 없음."', source)

    def test_generated_skill_is_generic_and_self_contained(self):
        root_template = self.skill_text[ROOT / "SKILL.md.template"]
        internal_template = self.skill_text[ROOT / "skills" / "SKILL.md.template"]
        self.assertIn("node ./bin/paper-curation.mjs", root_template)
        self.assertIn("setup --fresh-config", root_template)
        self.assertIn("{command}", internal_template)
        for path, template in self.skill_text.items():
            with self.subTest(path=path):
                self.assertNotIn("--topic ai4s", template)
                self.assertNotIn("--topic scisci", template)
                self.assertNotIn("Agent(", template)
                self.assertNotRegex(template, r"PYTHONUTF8=1\s+python\s+pipeline/")
        self.assertIn("<topic>", self.manifest_text)

    def test_manifest_contracts_are_harness_only_and_generic(self):
        self.assertIn("node ./bin/paper-curation.mjs", self.manifest_text)
        self.assertIsNone(HARDCODED_TOPIC_COMMAND.search(self.manifest_text))
        self.assertNotRegex(self.manifest_text, r"python\s+pipeline/")
        self.assertNotIn("API_KEY=", self.manifest_text)

    def test_onboarding_docs_use_aliases_without_sample_topics_or_direct_python_flows(self):
        for path in ONBOARDING_DOCS:
            text = self.text[path]
            with self.subTest(path=path):
                self.assertIsNone(HARDCODED_TOPIC_COMMAND.search(text))
                self.assertIsNone(DEFAULT_DIRECT_PYTHON_FLOW.search(text))
                self.assertIn("<alias>", text)

    def test_operator_copy_uses_fresh_config_and_generic_topic_profiles(self):
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        config_example = (ROOT / "config.example.json").read_text(encoding="utf-8")
        self.assertIn(FRESH_CONFIG_COMMAND, env_example)
        self.assertIn(".env/process env first", env_example)
        self.assertNotIn(STALE_LOCAL_SETUP_COMMAND, env_example)
        self.assertIn("ZOTERO_API_KEY in .env/process env", config_example)
        self.assertNotIn('"api_key": "YOUR_ZOTERO_API_KEY_HERE"', config_example)
        self.assertIn('"topic_profiles"', config_example)
        self.assertIn("domain-neutral", config_example)
        self.assertIn("collection label", config_example)
        self.assertNotIn("ai4s/scisci", config_example)
        self.assertNotIn('"mode": "oauth"', config_example)

    def test_search_cli_copy_uses_generic_topic_profiles(self):
        search_source = (ROOT / "pipeline" / "search_papers.py").read_text(encoding="utf-8")
        build_source = (ROOT / "pipeline" / "build_topic_index.py").read_text(encoding="utf-8")
        self.assertIn("topic_profiles", search_source)
        self.assertIn("collection label/alias", search_source)
        self.assertNotIn("--topic ai4s", search_source)
        self.assertNotIn("--topic scisci", search_source)
        self.assertNotIn("build_topic_index.py ai4s", build_source)
        self.assertNotIn("build_topic_index.py scisci", build_source)

    def test_generated_dashboard_uses_secret_free_local_assets_and_same_origin_actions(self):
        builder = (ROOT / "pipeline" / "build_topic_index.py").read_text(encoding="utf-8")
        runtime = (ROOT / "docs" / "public" / "paper-curation-local.js").read_text(
            encoding="utf-8"
        )
        self.assertIn('href="../public/paper-curation-local.css"', builder)
        self.assertIn('src="../public/paper-curation-local.js" defer', builder)
        self.assertNotIn("BYOK", builder)
        self.assertNotIn("GOOGLE_API_KEY", builder)
        self.assertNotIn("/api/embed", builder)
        self.assertIn("credentials: 'same-origin'", runtime)
        for route in ("/api/action/plan", "/api/action/approve", "/api/action/start"):
            self.assertIn(route, runtime)

    def test_metadata_mismatch_falls_back_to_lexical_without_automatic_rebuild(self):
        source = (ROOT / "pipeline" / "query_search_index.py").read_text(encoding="utf-8")
        normalized = " ".join(source.split())
        self.assertIn(
            "never embeds queries, rebuilds an index, or writes cache",
            source,
        )
        self.assertIn("otherwise retrieval is lexical BM25 only.", normalized)
        self.assertIn('return None, "index metadata invalid: "', source)
        self.assertIn(
            'return None, "legacy index metadata is unbound; dense retrieval disabled"',
            source,
        )
        for path in (
            ROOT / "README.md",
            ROOT / "README.en.md",
            ROOT / "docs" / "operations.md",
        ):
            with self.subTest(path=path):
                text = " ".join(self.text[path].lower().split())
                self.assertIn("lexical", text)
                self.assertIn("rebuild", text)

    def test_active_clis_never_default_to_example_topics(self):
        parser_default = re.compile(
            r"add_argument\([^\n]*(?:--topic|[\"']topic[\"'])[^\n]*"
            r"default=[\"'](?:ai4s|scisci)[\"']"
        )
        for path in (ROOT / "pipeline").glob("*.py"):
            with self.subTest(path=path):
                self.assertIsNone(parser_default.search(path.read_text(encoding="utf-8")))
        pre_push = (ROOT / "scripts" / "pre-push").read_text(encoding="utf-8")
        self.assertNotIn("PAPER_CURATION_TOPIC:-ai4s", pre_push)

    def test_pre_push_secret_detector_redacts_matched_values(self):
        secret = "sk-" + "ant-" + "testsecretmaterial1234567890"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)

            def git(*args):
                completed = subprocess.run(
                    ["git", *args],
                    cwd=repo,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return completed.stdout.strip()

            git("init")
            git("config", "user.email", "test@example.invalid")
            git("config", "commit.gpgsign", "false")
            git("config", "user.name", "Test User")
            (repo / "notes.txt").write_text("safe\n", encoding="utf-8")
            git("add", "notes.txt")
            git("commit", "-m", "initial")
            remote_oid = git("rev-parse", "HEAD")

            scripts = repo / "scripts"
            scripts.mkdir()
            hook = scripts / "pre-push"
            scanner = scripts / "scan-secrets.py"
            shutil.copy2(ROOT / "scripts" / "pre-push", hook)
            shutil.copy2(ROOT / "scripts" / "scan-secrets.py", scanner)

            (repo / "notes.txt").write_text(f"leaked={secret}\n", encoding="utf-8")
            git("add", "notes.txt")
            git("commit", "-m", "leak")
            local_oid = git("rev-parse", "HEAD")
            update = f"refs/heads/main {local_oid} refs/heads/main {remote_oid}\n"

            completed = subprocess.run(
                ["sh", str(hook)],
                cwd=repo,
                input=update,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            scanner.unlink()
            missing_scanner = subprocess.run(
                ["sh", str(hook)],
                cwd=repo,
                input=update,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn("leaked=", completed.stdout)
        self.assertIn("credentials or scanner errors are not safe to push", completed.stdout)
        self.assertNotEqual(missing_scanner.returncode, 0)
        self.assertIn("security scanner is missing; refusing push", missing_scanner.stdout)


if __name__ == "__main__":
    unittest.main()
