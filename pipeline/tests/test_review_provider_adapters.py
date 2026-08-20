"""Contract tests for the isolated Core review-provider adapters."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

from paper_curation.domain.papers import ArtifactRef, Paper
from paper_curation.integrations.providers.review import (
    AnthropicAPIReviewAdapter,
    ClaudeCodeOAuthReviewAdapter,
    LocalModelReviewAdapter,
    ReviewProviderError,
)


REVIEW = """# Review
## Summary
A concise source-grounded summary.
## Contributions
One contribution.
## Methods
The described method.
## Evidence and Findings
The reported finding.
## Limitations
A stated limitation.
## Source Grounding
The extracted text states the finding.
"""


class _Completed:
    returncode = 0
    stdout = REVIEW


class _Block:
    type = "text"
    text = REVIEW


class _Response:
    content = (_Block(),)


class _Messages:
    def __init__(self) -> None:
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response()


class _Client:
    def __init__(self) -> None:
        self.messages = _Messages()


class ReviewProviderAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        root = Path(self.directory.name)
        self.text_path = root / "extracted.txt"
        contents = b"The paper reports a result and acknowledges a limitation."
        self.text_path.write_bytes(contents)
        self.text = ArtifactRef("extracted.txt", str(self.text_path), sha256(contents).hexdigest())
        self.paper = Paper("zotero", "collection", "item", "A Paper")
        self.output = root / "reviews"

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_claude_uses_noninteractive_oauth_without_api_key_environment(self) -> None:
        calls = []

        def runner(command, **kwargs):
            calls.append((command, kwargs))
            return _Completed()

        adapter = ClaudeCodeOAuthReviewAdapter(
            self.output,
            "configured-model",
            command_runner=runner,
            environment={
                "ANTHROPIC_API_KEY": "secret",
                "ANTHROPIC_AUTH_TOKEN": "console-token",
                "OPENAI_API_KEY": "also-secret",
                "DATABASE_PASSWORD": "unrelated-secret",
                "CLAUDE_CODE_OAUTH_TOKEN": "oauth",
            },
        )
        artifact = adapter.write(self.paper, self.text)

        command, kwargs = calls[0]
        self.assertEqual(command[0:2], ("claude", "-p"))
        self.assertIn("--no-session-persistence", command)
        self.assertIn("--safe-mode", command)
        self.assertNotIn(REVIEW, command)
        self.assertIn("Extracted paper text", kwargs["input"])
        self.assertNotIn("ANTHROPIC_API_KEY", kwargs["env"])
        self.assertNotIn("ANTHROPIC_AUTH_TOKEN", kwargs["env"])
        self.assertNotIn("OPENAI_API_KEY", kwargs["env"])
        self.assertNotIn("DATABASE_PASSWORD", kwargs["env"])
        self.assertEqual(kwargs["env"]["CLAUDE_CODE_OAUTH_TOKEN"], "oauth")
        self.assertEqual(sha256(Path(artifact.path).read_bytes()).hexdigest(), artifact.fingerprint)

    def test_review_output_rejects_symlink_root_and_ignores_predictable_temp_link(self) -> None:
        outside = Path(self.directory.name) / "outside.txt"
        outside.write_text("preserve", encoding="utf-8")
        linked = Path(self.directory.name) / "linked-reviews"
        linked.symlink_to(outside.parent, target_is_directory=True)
        with self.assertRaisesRegex(ReviewProviderError, "symlink"):
            AnthropicAPIReviewAdapter(
                linked, _Client(), "configured-model"
            ).write(self.paper, self.text)

        self.output.mkdir()
        expected = __import__(
            "paper_curation.integrations.providers.review",
            fromlist=["_artifact_path"],
        )._artifact_path(self.output, self.paper)
        predictable = expected.with_suffix(expected.suffix + ".tmp")
        predictable.symlink_to(outside)
        AnthropicAPIReviewAdapter(
            self.output, _Client(), "configured-model"
        ).write(self.paper, self.text)
        self.assertEqual(outside.read_text(encoding="utf-8"), "preserve")

    def test_anthropic_uses_only_injected_client_once(self) -> None:
        client = _Client()
        artifact = AnthropicAPIReviewAdapter(
            self.output, client, "configured-model"
        ).write(self.paper, self.text)

        self.assertEqual(len(client.messages.calls), 1)
        self.assertIn("Extracted paper text", client.messages.calls[0]["messages"][0]["content"])
        self.assertTrue(Path(artifact.path).is_file())

    def test_local_model_uses_configured_endpoint_only(self) -> None:
        calls = []

        def request(endpoint, payload, headers, timeout):
            calls.append((endpoint, payload, headers, timeout))
            return {"choices": [{"message": {"content": REVIEW}}]}

        LocalModelReviewAdapter(
            self.output,
            "http://127.0.0.1:11434",
            "configured-model",
            request=request,
        ).write(
            self.paper, self.text
        )
        self.assertEqual(calls[0][0], "http://127.0.0.1:11434/v1/chat/completions")
        self.assertNotIn("Authorization", calls[0][2])

    def test_provider_failures_never_substitute_and_do_not_leak_credentials(self) -> None:
        def failing_runner(*args, **kwargs):
            raise TimeoutError("token super-secret")

        adapter = ClaudeCodeOAuthReviewAdapter(
            self.output, "configured-model", command_runner=failing_runner
        )
        with self.assertRaisesRegex(ReviewProviderError, "Claude Code review request failed") as raised:
            adapter.write(self.paper, self.text)
        self.assertNotIn("super-secret", str(raised.exception))

    def test_invalid_review_is_not_persisted(self) -> None:
        def request(*args):
            return {"choices": [{"message": {"content": "not markdown"}}]}

        with self.assertRaisesRegex(ReviewProviderError, "invalid review schema"):
            LocalModelReviewAdapter(
                self.output,
                "http://localhost:9999",
                "configured-model",
                request=request,
            ).write(
                self.paper, self.text
            )
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
