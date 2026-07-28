"""Contract tests for the fail-closed, owned-path-only local delivery gate.

Every scenario runs against a throwaway fixture repository created under a
temporary directory.  Nothing in this file mutates the repository it lives in.
"""

from __future__ import annotations

import ast
import inspect
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import deliver_local  # noqa: E402


SECRET = "sk-ant-" + "a" * 30

# Compliant and non-compliant control sources for the source-scope checker.
COMPLIANT_CONTROL = """
import subprocess


def _run_git(args, root):
    return subprocess.run(["git", "--no-pager", *args], cwd=root)


def stage(root, paths):
    return _run_git(["add", "--", *paths], root)
"""

VIOLATING_CONTROL = """
import subprocess


def _run_git(args, root):
    return subprocess.run(["git", "--no-pager", *args], cwd=root)


def publish(root):
    return subprocess.run(["git", "push", "origin", "HEAD"], cwd=root)
"""


def git_seam_offenders(source: str) -> list[tuple[str, int]]:
    """Attribute every `subprocess` reference and `["git", ...]` argv to its owner.

    Returns ``(enclosing function name, line number)`` pairs.  A module-level
    offender is attributed to ``"<module>"``.
    """
    def offending(node: ast.AST) -> bool:
        if isinstance(node, ast.Name) and node.id == "subprocess":
            return True
        if isinstance(node, ast.List) and node.elts:
            first = node.elts[0]
            return isinstance(first, ast.Constant) and first.value == "git"
        return False

    found: list[tuple[str, int]] = []

    def descend(node: ast.AST, owner: str) -> None:
        for child in ast.iter_child_nodes(node):
            child_owner = child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else owner
            if offending(child):
                found.append((child_owner, getattr(child, "lineno", -1)))
            descend(child, child_owner)

    descend(ast.parse(source), "<module>")
    return found


class GitSeamSourceTests(unittest.TestCase):
    """Source-level proof that the module has exactly one Git seam."""

    def test_every_subprocess_and_git_argv_is_scoped_to_run_git(self):
        source = inspect.getsource(deliver_local)
        offenders = git_seam_offenders(source)
        self.assertTrue(offenders, "checker found no git/subprocess usage at all")
        outside = [entry for entry in offenders if entry[0] != "_run_git"]
        self.assertEqual(outside, [], f"git/subprocess usage escaped _run_git: {outside}")
        tree = ast.parse(source)
        imports = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        self.assertIn("subprocess", imports)
        self.assertEqual(
            sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "_run_git"), 1
        )

    def test_the_scope_checker_is_discriminating(self):
        self.assertEqual([entry for entry in git_seam_offenders(COMPLIANT_CONTROL) if entry[0] != "_run_git"], [])
        violations = [entry for entry in git_seam_offenders(VIOLATING_CONTROL) if entry[0] != "_run_git"]
        self.assertTrue(violations)
        self.assertEqual({entry[0] for entry in violations}, {"publish"})


class ForbiddenGitCommandTests(unittest.TestCase):
    """Refusals raised before any process is spawned."""

    def test_remote_and_history_subcommands_never_reach_a_process(self):
        for subcommand in ("push", "pull", "fetch", "remote", "clone", "stash", "reset", "rebase", "checkout",
                           "switch", "branch", "merge", "format-patch", "request-pull", "send-email"):
            with self.subTest(subcommand=subcommand):
                with patch.object(deliver_local.subprocess, "run") as spawn:
                    with self.assertRaises(deliver_local.ForbiddenGitCommandError):
                        deliver_local._run_git([subcommand, "origin"], root=Path("."))
                spawn.assert_not_called()
        self.assertFalse(deliver_local.ALLOWED_SUBCOMMANDS & deliver_local.FORBIDDEN_SUBCOMMANDS)

    def test_partial_hunk_and_widening_options_are_refused(self):
        cases = (["add", "-p", "file.py"], ["add", "--patch"], ["add", "-A"], ["add", "--all"],
                 ["add", "-u"], ["commit", "--amend", "-m", "x"], ["commit", "--no-verify", "-m", "x"],
                 ["commit", "-a", "-m", "x"], ["diff", "--interactive"])
        for argv in cases:
            with self.subTest(argv=" ".join(argv)):
                with patch.object(deliver_local.subprocess, "run") as spawn:
                    with self.assertRaises(deliver_local.ForbiddenGitCommandError):
                        deliver_local._run_git(argv, root=Path("."))
                spawn.assert_not_called()

    def test_unknown_subcommands_and_global_options_are_refused(self):
        for argv in (["log"], ["cat-file", "-p", "HEAD"], ["-c", "user.name=x", "commit"], []):
            with self.subTest(argv=" ".join(argv)):
                with patch.object(deliver_local.subprocess, "run") as spawn:
                    with self.assertRaises(deliver_local.ForbiddenGitCommandError):
                        deliver_local._run_git(argv, root=Path("."))
                spawn.assert_not_called()

    def test_pathspecs_after_the_separator_are_not_treated_as_options(self):
        with patch.object(deliver_local.subprocess, "run") as spawn:
            spawn.return_value = subprocess.CompletedProcess([], 0, b"", b"")
            deliver_local._run_git(["add", "--", "-p", "--force"], root=Path("."))
        self.assertEqual(spawn.call_args[0][0], ["git", "--no-pager", "add", "--", "-p", "--force"])


class DeliveryFixtureCase(unittest.TestCase):
    """Base fixture: an isolated repository with one baseline commit."""

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        base = Path(self.tempdir.name)
        self.hooks = base / "nohooks"
        self.hooks.mkdir()
        self.repo = base / "repo"
        self.repo.mkdir()
        self.raw_git("init", "-q", "-b", "delivery")
        self.raw_git("config", "user.email", "delivery@example.test")
        self.raw_git("config", "user.name", "Delivery Fixture")
        self.raw_git("config", "commit.gpgsign", "false")
        self.raw_git("config", "core.hooksPath", str(self.hooks))
        self.write("pipeline/base.py", "BASE = 1\n")
        self.write("README.md", "baseline\n")
        self.raw_git("add", "--", "pipeline/base.py", "README.md")
        self.raw_git("commit", "-qm", "baseline")
        self.addCleanup(self.tempdir.cleanup)

    def raw_git(self, *args: str) -> str:
        """Test-side Git, deliberately outside the module under test."""
        completed = subprocess.run(
            ["git", *args], cwd=str(self.repo), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        )
        return completed.stdout

    def write(self, relative: str, content: str) -> Path:
        target = self.repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def head(self) -> str:
        return self.raw_git("rev-parse", "HEAD").strip()

    def staged(self) -> list[str]:
        return sorted(line for line in self.raw_git("diff", "--cached", "--name-only").splitlines() if line)

    def committed(self, commit: str) -> list[str]:
        return sorted(line for line in self.raw_git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", commit
        ).splitlines() if line)

    def after_gate(self, action):
        """Patch the final-gate step so `action` lands right after it is recorded."""
        original = deliver_local.record_final_gate

        def wrapper(inventory, owned):
            gate = original(inventory, owned)
            action()
            return gate

        return patch.object(deliver_local, "record_final_gate", wrapper)


class DeliverySuccessTests(DeliveryFixtureCase):
    def test_clean_run_commits_only_owned_paths(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.write("pipeline/new_module.py", "VALUE = 3\n")
        self.write("README.md", "user edit in flight\n")
        base_head = self.head()

        receipt = deliver_local.deliver(self.repo, ["pipeline/base.py", "pipeline/new_module.py"], "local delivery")

        self.assertEqual(receipt.owned, ("pipeline/base.py", "pipeline/new_module.py"))
        self.assertEqual(list(receipt.staged), list(receipt.owned))
        self.assertEqual(receipt.base_head, base_head)
        self.assertNotEqual(receipt.commit, base_head)
        self.assertEqual(receipt.branch, "delivery")
        self.assertEqual(self.committed(receipt.commit), ["pipeline/base.py", "pipeline/new_module.py"])
        self.assertEqual(self.staged(), [])
        self.assertIn("README.md", self.raw_git("status", "--porcelain=v1"))
        self.assertEqual((self.repo / "README.md").read_text(encoding="utf-8"), "user edit in flight\n")
        self.assertEqual(self.raw_git("rev-parse", "--abbrev-ref", "HEAD").strip(), "delivery")

    def test_staged_set_is_a_subset_of_the_owned_set(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.write("pipeline/extra.py", "EXTRA = 1\n")
        self.write("README.md", "unrelated\n")
        inventory = deliver_local.inventory_worktree(self.repo)
        owned = deliver_local.resolve_ownership(inventory, ["pipeline/base.py", "pipeline/extra.py"])
        gate = deliver_local.record_final_gate(inventory, owned)
        deliver_local.stage_owned(gate)

        staged = deliver_local.assert_staged_subset(gate)

        self.assertTrue(set(staged).issubset(set(gate.owned)))
        self.assertNotIn("README.md", staged)

    def test_inventory_records_lstat_identity_and_digest_for_pending_changes(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.write("pipeline/untracked.py", "NEW = 1\n")

        inventory = deliver_local.inventory_worktree(self.repo)

        self.assertEqual(set(inventory.paths()), {"pipeline/base.py", "pipeline/untracked.py"})
        self.assertTrue(inventory.entries["pipeline/untracked.py"].untracked)
        self.assertFalse(inventory.entries["pipeline/base.py"].untracked)
        for path, entry in inventory.entries.items():
            with self.subTest(path=path):
                self.assertTrue(entry.state.exists)
                self.assertEqual(len(entry.state.digest), 64)
                self.assertGreater(entry.state.inode, 0)
                self.assertGreater(entry.state.mtime_ns, 0)


class DeliveryRefusalTests(DeliveryFixtureCase):
    def test_mid_run_edit_to_an_owned_path_hard_stops_before_commit(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        base_head = self.head()

        with self.after_gate(lambda: self.write("pipeline/base.py", "BASE = 999\n")):
            with self.assertRaises(deliver_local.OwnedPathDriftError):
                deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertEqual(self.head(), base_head)
        self.assertEqual(self.staged(), [])

    def test_mid_run_edit_to_a_non_owned_path_does_not_stop_the_run(self):
        self.write("pipeline/base.py", "BASE = 2\n")

        with self.after_gate(lambda: self.write("README.md", "concurrent user work\n")):
            receipt = deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertEqual(receipt.staged, ("pipeline/base.py",))
        self.assertEqual(self.committed(receipt.commit), ["pipeline/base.py"])
        self.assertNotIn("README.md", self.committed(receipt.commit))
        self.assertEqual((self.repo / "README.md").read_text(encoding="utf-8"), "concurrent user work\n")
        self.assertIn("README.md", self.raw_git("status", "--porcelain=v1"))

    def test_branch_drift_hard_stops(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        base_head = self.head()

        with self.after_gate(lambda: self.raw_git("checkout", "-q", "-b", "other")):
            with self.assertRaises(deliver_local.BranchDriftError):
                deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertEqual(self.head(), base_head)
        self.assertEqual(self.staged(), [])

    def test_head_drift_hard_stops(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        base_head = self.head()

        def concurrent_commit():
            self.write("README.md", "someone else committed\n")
            self.raw_git("add", "--", "README.md")
            self.raw_git("commit", "-qm", "concurrent commit")

        with self.after_gate(concurrent_commit):
            with self.assertRaises(deliver_local.HeadDriftError):
                deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertNotEqual(self.head(), base_head)
        self.assertEqual(self.staged(), [])
        self.assertEqual(self.raw_git("rev-list", "--count", "HEAD").strip(), "2")

    def test_detached_head_hard_stops(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.raw_git("checkout", "-q", "--detach")
        base_head = self.head()

        with self.assertRaises(deliver_local.DetachedHeadError):
            deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertEqual(self.head(), base_head)
        self.assertEqual(self.staged(), [])

    def test_planted_secret_in_the_staged_patch_blocks_the_commit(self):
        self.write("pipeline/base.py", f"TOKEN = \"{SECRET}\"\n")
        base_head = self.head()

        with self.assertRaises(deliver_local.SecretScanError) as caught:
            deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertNotIn(SECRET, str(caught.exception))
        self.assertEqual(self.head(), base_head)
        self.assertEqual(self.raw_git("rev-list", "--count", "HEAD").strip(), "1")

    def test_a_secret_free_patch_passes_the_same_scan(self):
        self.write("pipeline/base.py", "TOKEN = \"not-a-credential\"\n")
        inventory = deliver_local.inventory_worktree(self.repo)
        owned = deliver_local.resolve_ownership(inventory, ["pipeline/base.py"])
        gate = deliver_local.record_final_gate(inventory, owned)
        deliver_local.stage_owned(gate)

        deliver_local.scan_staged_patch(self.repo)

        self.assertIn(b"not-a-credential", deliver_local.staged_patch(self.repo))

    def test_an_unavailable_scanner_is_a_hard_stop(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        missing = Path(self.tempdir.name) / "absent-scanner.py"
        with patch.object(deliver_local, "SCANNER_PATH", missing):
            with self.assertRaises(deliver_local.SecretScanError):
                deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")
        self.assertEqual(self.raw_git("rev-list", "--count", "HEAD").strip(), "1")

    def test_docs_and_gjc_paths_are_rejected_by_the_deny_list(self):
        self.write("docs/ai4s/index.html", "<html>generated dashboard</html>\n")
        self.write(".gjc/state.json", "{}\n")
        self.write("pipeline/base.py", "BASE = 2\n")
        base_head = self.head()

        for denied in ("docs/ai4s/index.html", ".gjc/state.json"):
            with self.subTest(path=denied):
                with self.assertRaises(deliver_local.DenyListError):
                    deliver_local.deliver(self.repo, ["pipeline/base.py", denied], "local delivery")
                self.assertEqual(self.head(), base_head)
                self.assertEqual(self.staged(), [])

    def test_generated_artifact_paths_are_denied_and_source_paths_are_not(self):
        denied = ("docs/index.html", "docs", ".gjc", ".gjc/plans/a.md", "config.json",
                  "pipeline/_update_force.log", "pipeline/__pycache__/base.cpython-311.pyc",
                  "artifacts/run.json", "pdf_cache/x.pdf", "papers/001/text.md",
                  "_regen_topics.py", "docs/_local_keys.json", ".env", "pipeline/x.log")
        allowed = ("pipeline/base.py", "pipeline/lib/helper.py", "pipeline/tests/test_x.py",
                   "README.md", ".env.example", "scripts/scan-secrets.py", "worker/index.js")
        for path in denied:
            with self.subTest(denied=path):
                self.assertIsNotNone(deliver_local.denied_reason(path))
        for path in allowed:
            with self.subTest(allowed=path):
                self.assertIsNone(deliver_local.denied_reason(path))

    def test_a_pre_staged_non_owned_path_breaks_the_subset_assertion(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.write("README.md", "staged by someone else\n")
        self.raw_git("add", "--", "README.md")
        base_head = self.head()

        with self.assertRaises(deliver_local.StagedScopeError) as caught:
            deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertIn("README.md", str(caught.exception))
        self.assertEqual(self.head(), base_head)

    def test_unchanged_and_malformed_owned_paths_are_refused(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        inventory = deliver_local.inventory_worktree(self.repo)
        for owned in (["pipeline/base.py", "README.md"], ["/etc/passwd"], ["../escape.py"],
                      ["pipeline/*.py"], [], ["-p"]):
            with self.subTest(owned=owned):
                with self.assertRaises(deliver_local.OwnershipError):
                    deliver_local.resolve_ownership(inventory, owned)

    def test_a_non_repository_root_is_refused(self):
        outside = Path(self.tempdir.name) / "not-a-repo"
        outside.mkdir()
        with self.assertRaises(deliver_local.RepositoryError):
            deliver_local.inventory_worktree(outside)


class GitInvocationSpyTests(DeliveryFixtureCase):
    def _record(self):
        calls: list[list[str]] = []
        original = deliver_local._run_git

        def spy(args, **kwargs):
            calls.append(list(args))
            return original(args, **kwargs)

        return calls, patch.object(deliver_local, "_run_git", spy)

    def test_a_full_delivery_run_never_invokes_push_or_any_remote_subcommand(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        self.write("pipeline/new_module.py", "VALUE = 3\n")
        self.write("README.md", "unrelated concurrent edit\n")
        calls, spy = self._record()

        with spy:
            receipt = deliver_local.deliver(
                self.repo, ["pipeline/base.py", "pipeline/new_module.py"], "local delivery"
            )

        self.assertTrue(receipt.commit)
        self.assertTrue(calls)
        subcommands = [argv[0] for argv in calls]
        self.assertEqual(set(subcommands) - deliver_local.ALLOWED_SUBCOMMANDS, set())
        self.assertEqual({"status", "rev-parse", "add", "diff", "commit"}, set(subcommands))
        banned = {"push", "pull", "fetch", "remote", "clone", "origin", "upstream", "stash", "reset",
                  "rebase", "merge", "checkout", "switch", "branch", "cherry-pick", "request-pull",
                  "send-email", "format-patch", "pr", "gh", "hub", "--force", "-f", "--set-upstream",
                  "--amend", "-p", "--patch"}
        for argv in calls:
            with self.subTest(argv=" ".join(argv)):
                self.assertEqual(set(argv) & banned, set())
        self.assertEqual(self.raw_git("remote").strip(), "")

    def test_the_spy_would_observe_a_forbidden_invocation(self):
        calls, spy = self._record()
        with spy:
            with self.assertRaises(deliver_local.ForbiddenGitCommandError):
                deliver_local._run_git(["push", "origin", "HEAD"], root=self.repo)
        self.assertEqual(calls, [["push", "origin", "HEAD"]])

    def test_no_delivery_step_reaches_the_repository_that_hosts_this_test(self):
        self.write("pipeline/base.py", "BASE = 2\n")
        calls, spy = self._record()
        roots = []
        original = deliver_local.subprocess.run

        def watch(argv, **kwargs):
            roots.append(kwargs.get("cwd"))
            return original(argv, **kwargs)

        with spy, patch.object(deliver_local.subprocess, "run", watch):
            deliver_local.deliver(self.repo, ["pipeline/base.py"], "local delivery")

        self.assertTrue(roots)
        expected = str(self.repo.resolve())
        self.assertEqual(set(roots), {expected})
        self.assertNotIn(str(PIPELINE.parent), roots)
        sandbox = str(Path(self.tempdir.name).resolve())
        self.assertTrue(all(os.path.commonpath([root, sandbox]) == sandbox for root in roots))


if __name__ == "__main__":
    unittest.main()
