import unittest

from pipeline.lib.operation_consent import OperationClaim, OperationConsent, canonical_json_bytes, sha256_hex
from pipeline.lib.operation_dags import QueryDag, Step
from pipeline.lib.operation_dispatch import DispatchCredentialError, OperationDispatcher


class AudioDeliveryTests(unittest.TestCase):
    def test_final_requires_exact_capability_credential_and_allows_one_retry(self):
        now = 100
        consent = OperationConsent(clock=lambda: now, token_bytes=lambda _: b"y" * 32)
        dispatcher = OperationDispatcher(consent, clock=lambda: now)
        claim = OperationClaim(1, "operation", "test", "query.normal", "topic", "retained", "localhost", "oauth", created_at=now, expires_at=700)
        dispatcher.register_plan(claim, QueryDag("query.normal", "q", 600, 1, 1, (Step("N20", "answer"),), {}), {"query": "q"})
        ready = dispatcher.redeem(consent.approve("operation", claim.plan_hash), claim)[0]
        result = {"text": "answer", "citations": [], "references": [], "connections": [], "figures": []}
        raw = canonical_json_bytes(result)
        dispatcher.accept("operation", "N20", ready.credential, {"type": "completed", "digest": sha256_hex(raw), "length": len(raw), "metadata": {}, "ref": "retained", "result": result}, idempotency_key="a" * 64)
        delivery = dispatcher.final_delivery("operation")
        with self.assertRaises(ConnectionError):
            dispatcher.get_final("operation", delivery.capability, delivery.credential, idempotency_key="b" * 64, interrupted=True)
        headers, payload = dispatcher.get_final("operation", delivery.capability, delivery.credential, idempotency_key="b" * 64)
        self.assertEqual(headers["Accept-Ranges"], "none")
        self.assertEqual(int(headers["Content-Length"]), len(payload))
        with self.assertRaises(DispatchCredentialError):
            dispatcher.get_final("operation", delivery.capability, delivery.credential, idempotency_key="b" * 64)


if __name__ == "__main__":
    unittest.main()
