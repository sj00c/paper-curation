"""Regression tests for the bundled originality trigger resource."""

import unittest

from pipeline.lib.originality_extractor import _extract_rule_based, load_triggers


class OriginalityTriggerTests(unittest.TestCase):
    def test_default_trigger_resource_loads(self):
        triggers = load_triggers()

        self.assertIn("rule_base_novelty", triggers["categories"])
        self.assertIn("we propose", triggers["all"])

    def test_default_triggers_extract_author_stated_contribution(self):
        triggers = load_triggers()
        text = (
            "Prior systems require expensive labels. "
            "In this work, we propose a new framework for label-free molecular search. "
            "The framework improves retrieval accuracy on three benchmarks."
        )

        result = _extract_rule_based(text, triggers)

        self.assertIn("we propose a new framework", result.lower())


if __name__ == "__main__":
    unittest.main()
