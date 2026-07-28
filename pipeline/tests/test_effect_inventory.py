"""The external-effect inventory is explicit and has no duplicate escape hatches."""
from __future__ import annotations

import unittest

from pipeline.lib.operation_consent import AuthMode
from pipeline.lib.provider_adapters import EFFECT_INVENTORY, INVENTORY_BY_NAME


class EffectInventoryTests(unittest.TestCase):
    def test_inventory_is_complete_unique_and_typed(self):
        expected = {
            "claude.oauth.cli", "anthropic.api-key", "gemini.script", "gemini.tts",
            "gemini.embedding", "gemini.image", "email.optional", "zotero.read",
            "http.web", "product.deploy", "git.delivery",
        }
        self.assertEqual({entry.name for entry in EFFECT_INVENTORY}, expected)
        self.assertEqual(len(EFFECT_INVENTORY), len(INVENTORY_BY_NAME))
        for entry in EFFECT_INVENTORY:
            with self.subTest(entry=entry.name):
                self.assertTrue(entry.provider)
                self.assertTrue(entry.task)
                self.assertTrue(entry.budget)
                self.assertTrue(all(isinstance(mode, AuthMode) for mode in entry.auth_modes))

    def test_only_claude_cli_can_use_oauth_auto(self):
        oauth_entries = {entry.name for entry in EFFECT_INVENTORY if AuthMode.OAUTH in entry.auth_modes}
        self.assertEqual(oauth_entries, {"claude.oauth.cli"})
        self.assertTrue(INVENTORY_BY_NAME["zotero.read"].read_only)
