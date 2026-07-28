import unittest

from pipeline.lib.operation_consent import OperationClaim, OperationConsent, canonical_json_bytes, sha256_hex
from pipeline.lib.operation_dags import QueryDag, Step
from pipeline.lib.operation_dispatch import (
    DispatchConflictError,
    DispatchCredentialError,
    DispatchError,
    OperationDispatcher,
)


class OperationRaceTests(unittest.TestCase):
    def setUp(self):
        self.now = 100
        self.consent = OperationConsent(clock=lambda: self.now, token_bytes=lambda _: b"x" * 32)
        self.dispatcher = OperationDispatcher(self.consent, clock=lambda: self.now)
        self.claim = OperationClaim(1, "operation", "test", "query.normal", "topic", "retained", "localhost", "oauth", created_at=100, expires_at=700)
        self.dispatcher.register_plan(self.claim, QueryDag("query.normal", "q", 600, 1, 1, (Step("N20", "answer"),), {}), {"query": "q"})
        self.ready = self.dispatcher.redeem(self.consent.approve("operation", self.claim.plan_hash), self.claim)[0]

    def completed(self, result):
        raw = canonical_json_bytes(result)
        return {"type": "completed", "digest": sha256_hex(raw), "length": len(raw), "metadata": {}, "ref": "retained", "result": result}

    def test_same_key_replay_changed_bytes_and_consumed_step_credential(self):
        result = {"text": "answer", "citations": [], "references": [], "connections": [], "figures": []}
        body = self.completed(result)
        first = self.dispatcher.accept("operation", "N20", self.ready.credential, body, idempotency_key="a" * 64)
        self.assertEqual(first["state"], "COMPLETED")
        self.assertEqual(self.dispatcher.accept("operation", "N20", self.ready.credential, body, idempotency_key="a" * 64), first)
        changed = dict(body, ref="other")
        with self.assertRaises(DispatchConflictError):
            self.dispatcher.accept("operation", "N20", self.ready.credential, changed, idempotency_key="a" * 64)
        with self.assertRaises(DispatchCredentialError):
            self.dispatcher.get_final("operation", "operation", "bad", idempotency_key="b" * 64)

    def test_invalid_body_or_credential_does_not_poison_idempotency_key(self):
        result = {
            "text": "answer",
            "citations": [],
            "references": [],
            "connections": [],
            "figures": [],
        }
        body = self.completed(result)
        key = "c" * 64
        with self.assertRaises(DispatchCredentialError):
            self.dispatcher.accept(
                "operation",
                "N20",
                "bad",
                body,
                idempotency_key=key,
            )
        with self.assertRaises(DispatchError):
            self.dispatcher.accept(
                "operation",
                "N20",
                self.ready.credential,
                {"type": "unknown"},
                idempotency_key=key,
            )
        accepted = self.dispatcher.accept(
            "operation",
            "N20",
            self.ready.credential,
            body,
            idempotency_key=key,
        )
        self.assertEqual(accepted["state"], "COMPLETED")

    def test_expiry_cancels_ready_work(self):
        self.now = 700
        with self.assertRaises(Exception):
            self.dispatcher.ready_steps("operation")


if __name__ == "__main__":
    unittest.main()
