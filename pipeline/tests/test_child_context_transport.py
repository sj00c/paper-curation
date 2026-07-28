"""Offline contract tests for the anonymous fd3 child-context transport."""
from __future__ import annotations

import os
import struct
import sys
import threading
import unittest
from unittest import mock

from pipeline.lib import child_context as transport


DIGEST = "a" * 64
OTHER_DIGEST = "b" * 64
POLICY = transport.ChildContextPolicy("operation-1", DIGEST, ("normal",), {"items": 2})
CONTEXT = transport.ChildOperationContext("operation-1", DIGEST, "normal", {"items": 1})
def _mutated_frame(child, changes):
    frame = child._signed(CONTEXT.canonical_value(), 456)
    frame.update(changes)
    return frame



class ChildContextTransportTests(unittest.TestCase):
    def setUp(self):
        self.pair = transport.Fd3Socketpair.create()
        self.parent = transport.ParentChildContext.open(self.pair.parent, parent_pid=123)
        bootstrap = transport._recv_frame(self.pair.child, 0.1, None)
        self.child = transport.ChildParentContext(
            self.pair.child,
            transport._b64_decode(bootstrap["key"], "key", transport.KEY_BYTES),
            transport._b64_decode(bootstrap["nonce"], "nonce", transport.NONCE_BYTES),
        )

    def tearDown(self):
        self.parent.close()
        self.child.close()
        self.pair.close()

    @unittest.skipUnless(hasattr(os, "fork"), "requires fork-capable Unix")
    def test_forked_fd3_exchange_verifies_pid_and_parent_lineage(self):
        pair = transport.Fd3Socketpair.create()
        parent = transport.ParentChildContext.open(pair.parent)
        child_pid = os.fork()
        if child_pid == 0:
            try:
                pair.close_parent()
                pair.install_child_fd3()
                child = transport.ChildParentContext.from_fd3()
                child.send(CONTEXT)
                child.close()
                os._exit(0)
            except BaseException:
                os._exit(1)
        pair.close_child()
        try:
            self.assertEqual(parent.receive(POLICY, expected_child_pid=child_pid, timeout=1), CONTEXT)
            _, status = os.waitpid(child_pid, 0)
            self.assertEqual(status, 0)
        finally:
            parent.close()
            pair.close()
    def test_valid_exchange_is_bound_to_policy(self):
        self.child.send(CONTEXT, pid=456)
        self.assertEqual(self.parent.receive(POLICY, expected_child_pid=456), CONTEXT)

    def test_replayed_reordered_and_skipped_sequences_fail_closed(self):
        frame = self.child._signed(CONTEXT.canonical_value(), 456)
        transport._send_frame(self.child._channel, frame)
        self.parent.receive(POLICY, expected_child_pid=456)
        transport._send_frame(self.child._channel, frame)
        with self.assertRaises(transport.ChildContextVerificationError):
            self.parent.receive(POLICY, expected_child_pid=456)
        self.assertTrue(self.parent._closed)

    def test_skipped_sequence_fails_closed(self):
        self.child._outgoing = 1
        transport._send_frame(self.child._channel, self.child._signed(CONTEXT.canonical_value(), 456))
        with self.assertRaises(transport.ChildContextVerificationError):
            self.parent.receive(POLICY, expected_child_pid=456)

    def test_bad_mac_nonce_digest_pid_member_and_budget_fail_closed(self):
        cases = (
            ("mac", lambda: _mutated_frame(self.child, {"mac": "A" * 43})),
            ("nonce", lambda: _mutated_frame(self.child, {"nonce": "A" * 43})),
            ("digest", lambda: self.child._signed({**CONTEXT.canonical_value(), "subclaim_digest": OTHER_DIGEST}, 456)),
            ("pid", lambda: self.child._signed(CONTEXT.canonical_value(), 999)),
            ("member", lambda: self.child._signed({**CONTEXT.canonical_value(), "member": "deeper"}, 456)),
            ("budget", lambda: self.child._signed({**CONTEXT.canonical_value(), "budget": {"items": 3}}, 456)),
        )
        for name, frame_factory in cases:
            with self.subTest(name=name):
                self.tearDown()
                self.setUp()
                transport._send_frame(self.child._channel, frame_factory())
                with self.assertRaises(transport.ChildContextVerificationError):
                    self.parent.receive(POLICY, expected_child_pid=456)
                self.assertTrue(self.parent._closed)

    def test_missing_fd3_fails_closed(self):
        with mock.patch.object(transport.os, "fstat", side_effect=OSError):
            with self.assertRaises(transport.ChildContextUnavailableError):
                transport.ChildParentContext.from_fd3(expected_parent_pid=123)

    def test_parent_lineage_mismatch_fails_closed(self):
        pair = transport.Fd3Socketpair.create()
        parent = transport.ParentChildContext.open(pair.parent, parent_pid=123)
        try:
            with mock.patch.object(transport, "_check_socket_fd", return_value=pair.child), mock.patch.object(transport.os, "getppid", return_value=321):
                with self.assertRaises(transport.ChildContextVerificationError):
                    transport.ChildParentContext.from_fd3()
        finally:
            parent.close()
            pair.close()
    def test_eof_timeout_and_cancel_close_parent(self):
        self.child.close()
        with self.assertRaises(transport.ChildContextEOFError):
            self.parent.receive(POLICY, expected_child_pid=456, timeout=0.1)
        self.assertTrue(self.parent._closed)

        self.tearDown()
        self.setUp()
        with self.assertRaises(transport.ChildContextTimeoutError):
            self.parent.receive(POLICY, expected_child_pid=456, timeout=0)
        self.assertTrue(self.parent._closed)

        self.tearDown()
        self.setUp()
        cancelled = threading.Event()
        cancelled.set()
        with self.assertRaises(transport.ChildContextCancelledError):
            self.parent.receive(POLICY, expected_child_pid=456, cancel=cancelled)
        self.assertTrue(self.parent._closed)

    def test_oversize_frame_and_cleanup(self):
        self.child._channel.sendall(struct.pack("!I", transport.MAX_FRAME_BYTES + 1))
        with self.assertRaises(transport.ChildContextFrameError):
            self.parent.receive(POLICY, expected_child_pid=456)
        self.assertTrue(self.parent._closed)
        self.assertEqual(self.parent._channel.fileno(), -1)

    def test_socketpair_fd3_installation_and_secret_redaction(self):
        argv_before = tuple(sys.argv)
        env_before = dict(os.environ)
        self.assertNotIn(bytes(self.parent._key).hex(), repr(self.parent))
        self.assertNotIn(bytes(self.parent._key).hex(), repr(self.pair))
        self.assertNotIn(DIGEST, repr(CONTEXT))
        self.assertEqual(tuple(sys.argv), argv_before)
        self.assertEqual(dict(os.environ), env_before)

        # Installation is exercised in an isolated descriptor slot and leaves fd3 inheritable.
        extra = transport.Fd3Socketpair.create()
        original = os.dup(transport.FD3)
        try:
            extra.install_child_fd3()
            self.assertTrue(os.get_inheritable(transport.FD3))
        finally:
            os.dup2(original, transport.FD3)
            os.close(original)
            extra.close()


if __name__ == "__main__":
    unittest.main()
