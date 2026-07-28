import http.client
import json
import threading
import unittest
from unittest import mock

from pipeline import serve_local


class ActionWireProtocolTests(unittest.TestCase):
    def setUp(self):
        self.server = serve_local.ThreadingHTTPServer(("127.0.0.1", 0), serve_local.LocalHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]
        self.cookie = self.request("GET", "/api/bootstrap")[1]["set-cookie"].split(";", 1)[0]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, headers=None):
        headers = dict(headers or {})
        headers.setdefault("Host", "127.0.0.1:%d" % self.port)
        if method == "POST":
            headers.setdefault("Origin", "http://127.0.0.1:%d" % self.port)
            headers.setdefault("Content-Type", "application/json")
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        payload = response.read()
        return response.status, {key.lower(): value for key, value in response.getheaders()}, json.loads(payload)

    def plan(self):
        body = json.dumps({"schema": 1, "command": "query.normal", "topic_alias": "topic", "input": {"auth_mode": "auto", "query": "hello"}, "limits": {}})
        with mock.patch.object(serve_local, "oauth_available", return_value=True):
            return self.request("POST", "/api/action/plan", body, {"Cookie": self.cookie})

    def test_auto_never_falls_back_to_api_key(self):
        body = json.dumps({"schema": 1, "command": "query.normal", "topic_alias": "topic", "input": {"auth_mode": "auto", "query": "hello"}, "limits": {}})
        with mock.patch.object(serve_local, "oauth_available", return_value=False), mock.patch.object(serve_local, "api_key_available", return_value=True):
            status, _, payload = self.request("POST", "/api/action/plan", body, {"Cookie": self.cookie})
        self.assertEqual(status, 401)
        self.assertEqual(payload["error"]["code"], "AUTH_UNAVAILABLE")

    def test_plan_names_exact_provider_model_work_and_unavailable_dispatch(self):
        status, _, planned = self.plan()
        self.assertEqual(status, 200)
        preview = planned["preview"]
        self.assertEqual(preview["requested_auth"], "auto")
        self.assertEqual(preview["resolved_auth"], "oauth")
        self.assertEqual(preview["cost"], "PRICE_UNAVAILABLE")
        self.assertEqual(preview["dispatch_state"], "UNAVAILABLE")
        self.assertEqual(preview["expected_work"], ["query.normal"])
        self.assertEqual(
            preview["providers"],
            [{
                "fallbacks": [],
                "model": "claude-sonnet-5",
                "provider": "claude",
                "task": "query.normal",
            }],
        )

    def test_start_fails_closed_without_consuming_approval(self):
        status, _, planned = self.plan()
        self.assertEqual(status, 200)
        approval = {"schema": 1, "operation_id": planned["operation_id"], "plan_hash": planned["plan_hash"], "decision": "approve"}
        status, _, approved = self.request("POST", "/api/action/approve", json.dumps(approval), {"Cookie": self.cookie})
        self.assertEqual(status, 200)
        start = json.dumps({"schema": 1, "operation_id": planned["operation_id"], "plan_hash": planned["plan_hash"]})
        headers = {"Cookie": self.cookie, "Idempotency-Key": "a" * 64, "X-PC-Redeem": approved["redeem_credential"]}
        status, _, rejected = self.request("POST", "/api/action/start", start, headers)
        self.assertEqual((status, rejected["error"]["code"]), (503, "DISPATCH_UNAVAILABLE"))
        headers["Idempotency-Key"] = "b" * 64
        status, _, retried = self.request("POST", "/api/action/start", start, headers)
        self.assertEqual((status, retried["error"]["code"]), (503, "DISPATCH_UNAVAILABLE"))
        approval_state = self.server.operation_wire_state.consent._approvals[approved["redeem_credential"]]
        self.assertFalse(approval_state.consumed)

    def test_unknown_keys_and_scope_mutation_fail_closed(self):
        status, _, planned = self.plan()
        self.assertEqual(status, 200)
        body = {"schema": 1, "operation_id": planned["operation_id"], "plan_hash": "0" * 64, "decision": "approve"}
        status, _, payload = self.request("POST", "/api/action/approve", json.dumps(body), {"Cookie": self.cookie})
        self.assertEqual((status, payload["error"]["code"]), (409, "PLAN_SCOPE_CHANGED"))
        malformed = json.dumps({"schema": 1, "command": "query.normal", "topic_alias": "topic", "input": {"auth_mode": "oauth", "query": "x", "extra": True}, "limits": {}})
        status, _, payload = self.request("POST", "/api/action/plan", malformed, {"Cookie": self.cookie})
        self.assertEqual((status, payload["error"]["code"]), (400, "INVALID_SCHEMA"))
