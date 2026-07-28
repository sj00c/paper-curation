import hashlib
import os
import stat
import tempfile
import unittest
from pathlib import Path

from pipeline.lib.audio_operation import AudioTempRecoveryAmbiguous, AudioTempStore, cleanup_cancelled_or_expired


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class AudioRestartCleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "paper-curation-audio-v1"
        self.store = AudioTempStore(self.root)
        self.store.ensure_root()

    def tearDown(self):
        self.tmp.cleanup()

    def operation(self, name="one"):
        return self.store.create_operation(digest(name), expires_at=1)

    def test_cancel_and_expiry_remove_verified_operation(self):
        operation = self.operation()
        cleanup_cancelled_or_expired(self.store, operation)
        self.assertFalse(operation.exists())
        operation = self.operation("expired")
        self.assertEqual(AudioTempStore(self.root).scavenge(now=2), 1)
        self.assertFalse(operation.exists())

    def test_sigkill_style_unlocked_stale_directory_is_scavenged(self):
        operation = self.operation()
        restarted = AudioTempStore(self.root)
        self.assertEqual(restarted.scavenge(), 1)
        self.assertFalse(operation.exists())

    def test_live_lock_is_ambiguity_and_is_not_touched(self):
        operation = self.operation()
        lock = self.store.lock_operation(operation)
        try:
            with self.assertRaises(AudioTempRecoveryAmbiguous):
                AudioTempStore(self.root).scavenge()
            self.assertTrue(operation.exists())
        finally:
            self.store.release_operation(lock, operation)

    def assert_ambiguous_untouched(self, mutate):
        operation = self.operation(os.urandom(4).hex())
        mutate(operation)
        with self.assertRaises(AudioTempRecoveryAmbiguous):
            AudioTempStore(self.root).scavenge()
        self.assertTrue(operation.exists())
        self.assertEqual(self.store.disabled_reason, None)  # only the restarted store is disabled

    def test_symlink_hardlink_mode_marker_and_name_are_untouched(self):
        def symlink(operation):
            (operation / "marker").unlink()
            (operation / "marker").symlink_to("state.json")
        self.assert_ambiguous_untouched(symlink)

        def hardlink(operation):
            os.link(operation / "marker", operation / "extra-link")
        self.assert_ambiguous_untouched(hardlink)

        def mode(operation):
            os.chmod(operation / "state.json", 0o644)
        self.assert_ambiguous_untouched(mode)

        def marker(operation):
            (operation / "marker").write_text("wrong\n")
        self.assert_ambiguous_untouched(marker)

        # A hostile root entry must disable Audio without deleting a valid operation.
        valid = self.operation("valid")
        hostile = self.root / "not-an-audio-operation"
        hostile.write_text("sentinel")
        with self.assertRaises(AudioTempRecoveryAmbiguous):
            AudioTempStore(self.root).scavenge()
        self.assertTrue(valid.exists())
        self.assertTrue(hostile.exists())

    def test_root_symlink_is_untouched(self):
        self.tmp.cleanup()
        with tempfile.TemporaryDirectory() as root_parent:
            destination = Path(root_parent) / "target"
            destination.mkdir()
            root = Path(root_parent) / "paper-curation-audio-v1"
            root.symlink_to(destination, target_is_directory=True)
            store = AudioTempStore(root)
            with self.assertRaises(AudioTempRecoveryAmbiguous):
                store.ensure_root()
            self.assertTrue(root.is_symlink())


if __name__ == "__main__":
    unittest.main()
