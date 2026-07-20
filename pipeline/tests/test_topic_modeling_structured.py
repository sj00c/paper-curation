"""Focused no-network tests for topic-modeling structured Claude calls."""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import topic_modeling as tm  # noqa: E402


class FakeMessages:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        value = self.outputs.pop(0)
        return SimpleNamespace(
            content=[SimpleNamespace(type="tool_use", input=value)]
        )


class FakeClient:
    def __init__(self, outputs):
        self.messages = FakeMessages(outputs)

    def with_options(self, **_kwargs):
        return self


class TopicModelingStructuredTests(unittest.TestCase):
    def test_sub_topic_names_use_required_tool_schema(self):
        client = FakeClient([{
            "7": {"name": "Robot Learning", "description": "Learning for robots."}
        }])

        with patch.object(tm.time, "sleep", return_value=None):
            result = tm.name_sub_topics(
                {7: [("robot", 1.0), ("learning", 0.8)]},
                [7, 7],
                client,
            )

        self.assertEqual(result[7]["name"], "Robot Learning")
        call = client.messages.calls[0]
        self.assertEqual(call["tool_choice"]["name"], "name_sub_topics")
        schema = call["tools"][0]["input_schema"]
        self.assertEqual(schema["required"], ["7"])
        self.assertFalse(schema["additionalProperties"])

    def test_connections_use_structured_result_without_text_parsing(self):
        client = FakeClient([{
            "001": [{
                "target": "002",
                "relation": "foundation",
                "reason": "두 논문의 핵심 방법이 직접 연결된다.",
            }]
        }])
        papers = [
            {"slug": "001_First", "title": "First", "essence": "One"},
            {"slug": "002_Second", "title": "Second", "essence": "Two"},
        ]

        result = tm.generate_connections_from_candidates(
            {"001_First": [("002_Second", 0.9)]},
            papers,
            client,
            batch_size=1,
            deadline_s=5,
            max_rounds=1,
        )

        self.assertEqual(result["001_First"][0]["slug"], "002_Second")
        call = client.messages.calls[0]
        self.assertEqual(call["tool_choice"]["name"], "select_paper_connections")
        schema = call["tools"][0]["input_schema"]
        self.assertEqual(schema["required"], ["001"])
        relation = schema["properties"]["001"]["items"]["properties"]["relation"]
        self.assertIn("foundation", relation["enum"])

    def test_missing_tool_result_fails_visibly(self):
        response = SimpleNamespace(
            content=[SimpleNamespace(type="text", text='{"1": {}}')]
        )
        with self.assertRaisesRegex(RuntimeError, "no structured tool result"):
            tm._anthropic_tool_input(response)


if __name__ == "__main__":
    unittest.main()
