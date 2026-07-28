"""Unit tests for the provider-free operation-consent core."""

from __future__ import annotations

import base64
import re
import unittest
from dataclasses import FrozenInstanceError, replace

from pipeline.lib.operation_consent import (
    APPROVAL_TTL_SECONDS,
    ApprovalConsumedError,
    ApprovalExpiredError,
    AuthMode,
    AuthUnavailableError,
    CanonicalValueError,
    ConsentError,
    IdempotencyDisposition,
    IdempotencyRecords,
    OperationClaim,
    OperationConsent,
    OperationMaxima,
    PlanScopeChangedError,
    ProviderTask,
    canonical_json_bytes,
    resolve_auth_mode,
)
from pipeline.lib.operation_dags import QueryDag, Step
from pipeline.lib.operation_dispatch import DispatchConflictError, OperationDispatcher


DIGEST = "a" * 64
OTHER_DIGEST = "b" * 64
KEY = "c" * 64


def claim(**changes):
    values = {
        "version": 1,
        "operation_id": "operation-1",
        "task": "query",
        "command": "query.normal",
        "topic": "topic",
        "source": "snapshot",
        "ingress": "localhost",
        "auth": AuthMode.AUTO,
        "providers": (ProviderTask("provider", "model", "answer", ("local",)),),
        "maxima": OperationMaxima(attempts=1, tokens=2, concurrency=1),
        "input_digests": (DIGEST,),
        "resource_digests": (OTHER_DIGEST,),
        "external_allowlist": ("https://example.test",),
        "created_at": 100,
        "expires_at": 1000,
    }
    values.update(changes)
    return OperationClaim(**values)


class CanonicalOperationConsentTests(unittest.TestCase):
    def test_canonical_json_is_sorted_and_nfc_stable(self):
        composed = canonical_json_bytes({"z": "e\u0301", "a": ["x"]})
        decomposed = canonical_json_bytes({"a": ["x"], "z": "é"})
        self.assertEqual(composed, decomposed)
        self.assertEqual(composed, b'{"a":["x"],"z":"\xc3\xa9"}')
        self.assertEqual(claim(topic="e\u0301").plan_hash, claim(topic="é").plan_hash)

    def test_canonical_json_rejects_floats_and_noncanonical_values(self):
        for value in (1.0, float("nan"), {"nested": 2.0}, {"set"}):
            with self.subTest(value=repr(value)):
                with self.assertRaises(CanonicalValueError):
                    canonical_json_bytes(value)

    def test_immutable_values_reject_invalid_auth_and_negative_maxima(self):
        with self.assertRaises(ConsentError):
            claim(auth="bearer")
        with self.assertRaises(ConsentError):
            OperationMaxima(attempts=-1)
        with self.assertRaises(FrozenInstanceError):
            claim().task = "other"  # type: ignore[misc]

    def test_auto_never_falls_back_to_api_key(self):
        with self.assertRaises(AuthUnavailableError):
            resolve_auth_mode("auto", oauth_available=False, api_key_available=True)
        self.assertEqual(
            resolve_auth_mode("auto", oauth_available=True, api_key_available=False).resolved,
            AuthMode.OAUTH,
        )
        self.assertEqual(
            resolve_auth_mode("api-key", oauth_available=False, api_key_available=True).resolved,
            AuthMode.API_KEY,
        )

    def test_approval_credential_is_exact_shape_and_redacted(self):
        clock = [100]
        authority = OperationConsent(clock=lambda: clock[0], token_bytes=lambda _: bytes(range(32)))
        plan = authority.create_plan(claim())
        authority.bind_plan(plan.operation_id, plan.plan_hash, DIGEST)
        credential = authority.approve(plan.operation_id, plan.plan_hash)
        self.assertEqual(credential.expires_at, 100 + APPROVAL_TTL_SECONDS)
        self.assertEqual(len(credential.token), 43)
        self.assertIsNone(re.search(r"[^A-Za-z0-9_-]", credential.token))
        self.assertEqual(credential.token, base64.urlsafe_b64encode(bytes(range(32))).decode().rstrip("="))
        self.assertNotIn(credential.token, repr(credential))

    def test_approval_expiry_reuse_and_scope_mutation_fail_closed(self):
        clock = [100]
        authority = OperationConsent(clock=lambda: clock[0], token_bytes=lambda _: b"x" * 32)
        original = claim()
        plan = authority.create_plan(original)
        authority.bind_plan(plan.operation_id, plan.plan_hash, DIGEST)
        credential = authority.approve(plan.operation_id, plan.plan_hash)
        with self.assertRaises(PlanScopeChangedError):
            authority.redeem(credential, replace(original, task="other"))
        self.assertEqual(authority.redeem(credential, original), original)
        with self.assertRaises(ApprovalConsumedError):
            authority.redeem(credential, original)

        credential = authority.approve(plan.operation_id, plan.plan_hash)
        clock[0] += APPROVAL_TTL_SECONDS
        with self.assertRaises(ApprovalExpiredError):
            authority.redeem(credential, original)
    def test_approval_requires_frozen_dispatch_snapshot(self):
        authority = OperationConsent(token_bytes=lambda _: b"x" * 32)
        plan = authority.create_plan(claim())
        with self.assertRaises(PlanScopeChangedError):
            authority.approve(plan.operation_id, plan.plan_hash)

    def test_dispatcher_freezes_dag_and_retained_input_snapshots(self):
        authority = OperationConsent(clock=lambda: 100, token_bytes=lambda _: b"x" * 32)
        dispatcher = OperationDispatcher(authority)
        original_config = {"limits": {"top_k": 1}}
        retained = {"query": {"text": "original"}}
        dag = QueryDag(
            "query.normal", "query", 600, 1, 1,
            (Step("N20", "answer"),), original_config,
        )
        operation = claim()
        digest = dispatcher.register_plan(operation, dag, retained)

        original_config["limits"]["top_k"] = 2
        retained["query"]["text"] = "changed"
        with self.assertRaises(TypeError):
            dag.config["limits"]["top_k"] = 2

        self.assertEqual(
            authority.approve(operation.operation_id, operation.plan_hash).operation_digest,
            digest,
        )
        with self.assertRaises(DispatchConflictError):
            dispatcher.register_plan(operation, dag, retained)

    def test_idempotency_replay_conflict_in_progress_and_consumed_credential(self):
        records = IdempotencyRecords()
        self.assertEqual(
            records.begin("capability", "/route", KEY, DIGEST).disposition,
            IdempotencyDisposition.STARTED,
        )
        self.assertEqual(
            records.begin("capability", "/route", KEY, DIGEST).disposition,
            IdempotencyDisposition.IN_PROGRESS,
        )
        self.assertEqual(
            records.begin("capability", "/route", KEY, OTHER_DIGEST).disposition,
            IdempotencyDisposition.CONFLICT,
        )
        records.complete("capability", "/route", KEY, DIGEST)
        self.assertEqual(
            records.begin("capability", "/route", KEY, DIGEST).disposition,
            IdempotencyDisposition.REPLAY,
        )
        records.consume_credential("credential-1")
        self.assertEqual(
            records.begin("capability", "/route", "d" * 64, DIGEST, credential_id="credential-1").disposition,
            IdempotencyDisposition.CREDENTIAL_CONSUMED,
        )
        with self.assertRaises(ConsentError):
            records.begin("capability", "/route", "D" * 64, DIGEST)


if __name__ == "__main__":
    unittest.main()
