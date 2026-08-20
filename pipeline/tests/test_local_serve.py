"""Contract tests for the plan-only local static site server."""

from __future__ import annotations

import http.client
import socket
import tempfile
import unittest
from pathlib import Path

from paper_curation.application.serve import ServeSite, ServeSitePlan, ServeSiteRequest
from paper_curation.integrations.server import LocalStaticServer


class LocalStaticServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "site"
        self.root.mkdir()
        (self.root / "index.html").write_text("<h1>Local site</h1>", encoding="utf-8")
        (self.root / "asset.css").write_text("body { color: black; }", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _plan(self, **overrides: object) -> ServeSitePlan:
        request = ServeSiteRequest(site_root=self.root, port=0, **overrides)
        return ServeSite().plan(request)

    def _request(self, handle: object, path: str) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection(handle.host, handle.port, timeout=2)
        connection.request("GET", path)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_planning_is_read_only_and_does_not_bind(self) -> None:
        sentinel = self.root / "config.json"
        sentinel.write_text('{"provider":"unchanged"}', encoding="utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reserved:
            reserved.bind(("127.0.0.1", 0))
            port = reserved.getsockname()[1]
            plan = ServeSite().plan(ServeSiteRequest(site_root=self.root, port=port))
            self.assertEqual(plan.port, port)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), '{"provider":"unchanged"}')

    def test_serves_index_and_static_file_on_loopback(self) -> None:
        with LocalStaticServer().start(self._plan()) as handle:
            status, headers, body = self._request(handle, "/")
            self.assertEqual(status, 200)
            self.assertEqual(headers["Content-Type"], "text/html; charset=utf-8")
            self.assertEqual(body, b"<h1>Local site</h1>")
            status, headers, body = self._request(handle, "/asset.css")
            self.assertEqual(status, 200)
            self.assertEqual(headers["Content-Type"], "text/css; charset=utf-8")
            self.assertEqual(body, b"body { color: black; }")
            self.assertEqual(handle.host, "127.0.0.1")

    def test_rejects_path_traversal_and_symlink_escape(self) -> None:
        outside = Path(self.temporary.name) / "credential.txt"
        outside.write_text("secret", encoding="utf-8")
        (self.root / "escaped.txt").symlink_to(outside)
        (self.root / "_local_keys.json").write_text('{"key":"secret"}', encoding="utf-8")
        with LocalStaticServer().start(self._plan()) as handle:
            for path in (
                "/../credential.txt",
                "/%2e%2e/credential.txt",
                "/escaped.txt",
                "/_local_keys.json",
            ):
                status, _, body = self._request(handle, path)
                self.assertEqual(status, 404)
                self.assertNotIn(b"secret", body)

    def test_refuses_missing_or_unvalidated_site(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not exist"):
            ServeSiteRequest(site_root=self.root / "missing")
        empty = Path(self.temporary.name) / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(ValueError, "index.html"):
            ServeSiteRequest(site_root=empty)
        with self.assertRaisesRegex(ValueError, "does not exist"):
            LocalStaticServer().start(ServeSitePlan(empty / "missing", "127.0.0.1", 0, False))

    def test_refuses_public_bind_without_explicit_flag(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-loopback"):
            ServeSiteRequest(site_root=self.root, host="0.0.0.0", port=0)
        plan = ServeSite().plan(
            ServeSiteRequest(site_root=self.root, host="0.0.0.0", port=0, allow_public_bind=True)
        )
        self.assertTrue(plan.allow_public_bind)

    def test_clean_shutdown_releases_port(self) -> None:
        handle = LocalStaticServer().start(self._plan())
        port = handle.port
        self.assertTrue(handle.running)
        handle.stop()
        handle.stop()
        self.assertFalse(handle.running)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind(("127.0.0.1", port))


if __name__ == "__main__":
    unittest.main()
