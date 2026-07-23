"""Focused TLS security contract tests."""

import contextlib
import io
import os
import re
import ssl
import sys
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import tls as tls_module  # noqa: E402


class TlsSecurityTests(unittest.TestCase):
    def _context_with_env(self, value, config=None):
        with patch.dict(os.environ, {tls_module.INSECURE_TLS_ENV: value}, clear=False):
            with warnings.catch_warnings(record=True) as seen:
                warnings.simplefilter("always")
                ctx = tls_module.create_ssl_context(purpose="test", config=config)
        return ctx, seen

    def _run_serve_local_main(self, argv):
        import serve_local  # noqa: E402

        captured = {}

        class FakeServer:
            def __init__(self, address, handler):
                captured["address"] = address
                captured["handler"] = handler
                self.server_address = address
                self.shutdown_called = False
                self.server_close_called = False

            def serve_forever(self):
                raise KeyboardInterrupt

            def shutdown(self):
                self.shutdown_called = True
                captured["shutdown_called"] = True

            def server_close(self):
                self.server_close_called = True
                captured["server_close_called"] = True

        stdout = io.StringIO()
        with patch.object(sys, "argv", ["serve_local.py", *argv]):
            with patch.object(serve_local, "ThreadingHTTPServer", FakeServer):
                with patch.object(serve_local, "resolve_google_key", return_value=None):
                    with contextlib.redirect_stdout(stdout):
                        serve_local.main()

        captured["stdout"] = stdout.getvalue()
        return captured

    def test_default_context_verifies_certificates_and_hostnames(self):
        ctx, seen = self._context_with_env("0")

        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(ctx.check_hostname)
        self.assertEqual(seen, [])

    def test_env_opt_out_requires_exact_one(self):
        for value in ["", "0", "true", "yes", "01", " 1", "1 "]:
            with self.subTest(value=value):
                ctx, seen = self._context_with_env(value)

                self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
                self.assertTrue(ctx.check_hostname)
                self.assertEqual(seen, [])

        ctx, seen = self._context_with_env("1")
        self.assertEqual(ctx.verify_mode, ssl.CERT_NONE)
        self.assertFalse(ctx.check_hostname)
        self.assertEqual(len(seen), 1)
        self.assertIn("PAPER_CURATION_INSECURE_TLS=1", str(seen[0].message))

    def test_config_opt_out_requires_true_flag_and_nonempty_reason(self):
        invalid_configs = [
            {"network": {"allow_insecure_tls": True}},
            {"network": {"allow_insecure_tls": True, "insecure_tls_reason": ""}},
            {"network": {"allow_insecure_tls": True, "insecure_tls_reason": "   "}},
            {"network": {"allow_insecure_tls": "true", "insecure_tls_reason": "proxy"}},
            {"network": {"allow_insecure_tls": 1, "insecure_tls_reason": "proxy"}},
            {"network": "not-a-mapping"},
            {},
            None,
        ]

        for config in invalid_configs:
            with self.subTest(config=config):
                ctx, seen = self._context_with_env("0", config=config)

                self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
                self.assertTrue(ctx.check_hostname)
                self.assertEqual(seen, [])

        ctx, seen = self._context_with_env(
            "0",
            config={"network": {"allow_insecure_tls": True, "insecure_tls_reason": "corporate proxy"}},
        )
        self.assertEqual(ctx.verify_mode, ssl.CERT_NONE)
        self.assertFalse(ctx.check_hostname)
        self.assertEqual(len(seen), 1)

    def test_insecure_warning_has_remediation_and_redacts_config_reason(self):
        secret_reason = "proxy password sk-test-secret"
        ctx, seen = self._context_with_env(
            "0",
            config={"network": {"allow_insecure_tls": True, "insecure_tls_reason": secret_reason}},
        )

        self.assertEqual(ctx.verify_mode, ssl.CERT_NONE)
        self.assertEqual(len(seen), 1)
        message = str(seen[0].message)
        self.assertIn("TLS certificate and hostname verification disabled", message)
        self.assertIn("SSL_CERT_FILE", message)
        self.assertIn("REQUESTS_CA_BUNDLE", message)
        self.assertIn("trust store", message)
        self.assertNotIn(secret_reason, message)
        self.assertNotIn("sk-test-secret", message)

    def test_serve_local_binds_loopback_by_default(self):
        run = self._run_serve_local_main([])

        self.assertEqual(run["address"], ("127.0.0.1", 8000))
        self.assertIn("바인드: 127.0.0.1:8000", run["stdout"])
        self.assertIn("열기: http://127.0.0.1:8000/", run["stdout"])
        self.assertTrue(run["shutdown_called"])
        self.assertTrue(run["server_close_called"])

    def test_serve_local_requires_explicit_host_for_lan_binding(self):
        run = self._run_serve_local_main(["--host", "0.0.0.0", "--port", "9001", "--topic", "ai4s"])

        self.assertEqual(run["address"], ("0.0.0.0", 9001))
        self.assertIn("바인드: 0.0.0.0:9001", run["stdout"])
        self.assertIn("열기: http://0.0.0.0:9001/ai4s/", run["stdout"])

    def test_network_clients_use_shared_tls_helper_without_direct_insecure_context(self):
        expected_clients = {
            "enrich_journals.py": 'create_ssl_context(\n    purpose="enrich_journals OpenAlex venue lookup"',
            "serve_local.py": 'create_ssl_context(purpose="serve_local"',
        }

        for filename, expected_call in expected_clients.items():
            with self.subTest(filename=filename):
                text = (PIPELINE / filename).read_text(encoding="utf-8")
                self.assertIn("from tls import create_ssl_context", text)
                self.assertIn(expected_call, text)
                if filename == "enrich_journals.py":
                    self.assertIn("config=load_config()", text)
                self.assertNotRegex(text, re.compile(r"verify_mode\s*=\s*ssl\.CERT_NONE"))
                self.assertNotRegex(text, re.compile(r"check_hostname\s*=\s*False"))
                self.assertNotIn("_create_unverified_context", text)

    def test_insecure_constructs_are_confined_to_tls_helper(self):
        offenders = []
        for path in PIPELINE.rglob("*.py"):
            relative_parts = path.relative_to(PIPELINE).parts
            if relative_parts[0] in {"_archive", "tests"}:
                continue
            text = path.read_text(encoding="utf-8")
            if path.name == "tls.py":
                text = text.replace("context.verify_mode = ssl.CERT_NONE", "")
                text = text.replace("context.check_hostname = False", "")
            for pattern in [r"verify_mode\s*=\s*ssl\.CERT_NONE", r"check_hostname\s*=\s*False", r"_create_unverified_context"]:
                if re.search(pattern, text):
                    offenders.append(f"{path.relative_to(PIPELINE)}:{pattern}")

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
