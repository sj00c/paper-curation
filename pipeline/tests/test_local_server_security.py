import http.client
import json
import threading
import unittest

from pipeline import serve_local


class LocalServerSecurityTests(unittest.TestCase):
    def setUp(self):
        self.server = serve_local.ThreadingHTTPServer(("127.0.0.1", 0), serve_local.LocalHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request(method, path, body=body, headers=headers or {})
        response = conn.getresponse()
        raw = response.read()
        return response.status, {key.lower(): value for key, value in response.getheaders()}, json.loads(raw)

    def test_bootstrap_has_exact_loopback_cookie_and_security_headers(self):
        status, headers, body = self.request("GET", "/api/bootstrap", headers={"Host": "127.0.0.1:%d" % self.port})
        self.assertEqual(status, 200)
        self.assertEqual(body["audio_capability"]["feature"], "audio_overview")
        self.assertIn("HttpOnly", headers["set-cookie"])
        self.assertIn("SameSite=Strict", headers["set-cookie"])
        self.assertIn("Path=/api", headers["set-cookie"])
        self.assertNotIn("Domain=", headers["set-cookie"])
        self.assertEqual(headers["cache-control"], "no-store")
        self.assertEqual(headers["x-content-type-options"], "nosniff")
        self.assertEqual(headers["referrer-policy"], "no-referrer")
        self.assertEqual(headers["x-frame-options"], "DENY")

    def test_alias_forwarded_and_origin_are_rejected_before_body_parse(self):
        payload = b"not-json"
        status, _, result = self.request("POST", "/api/action/plan", payload, {"Host": "localhost:%d" % self.port, "Origin": "http://127.0.0.1:%d" % self.port, "Content-Type": "application/json", "Content-Length": str(len(payload))})
        self.assertEqual((status, result["error"]["code"]), (400, "INVALID_AUTHORITY"))
        status, _, result = self.request("POST", "/api/action/plan", payload, {"Host": "127.0.0.1:%d" % self.port, "Origin": "http://localhost:%d" % self.port, "Content-Type": "application/json", "Content-Length": str(len(payload))})
        self.assertEqual((status, result["error"]["code"]), (403, "INVALID_ORIGIN"))
        status, _, result = self.request("POST", "/api/action/plan", payload, {"Host": "127.0.0.1:%d" % self.port, "Origin": "http://127.0.0.1:%d" % self.port, "X-Forwarded-Host": "example.test", "Content-Type": "application/json", "Content-Length": str(len(payload))})
        self.assertEqual((status, result["error"]["code"]), (400, "INVALID_AUTHORITY"))

    def test_legacy_effect_routes_are_not_available(self):
        headers = {"Host": "127.0.0.1:%d" % self.port, "Origin": "http://127.0.0.1:%d" % self.port, "Content-Type": "application/json"}
        status, _, result = self.request("POST", "/api/embed", b"{}", headers)
        self.assertEqual((status, result["error"]["code"]), (404, "NOT_FOUND"))
        status, _, result = self.request("POST", "/api/audio-email", b"{}", headers)
        self.assertEqual((status, result["error"]["code"]), (404, "NOT_FOUND"))
