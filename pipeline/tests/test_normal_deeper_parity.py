"""Normal/Deeper final-artifact parity vectors."""
import unittest

from pipeline.lib.operation_dags import _final_artifact, plan_deeper, plan_normal, start


class NormalDeeperParityTests(unittest.TestCase):
    def test_normal_and_deeper_retain_query_and_transfer_deterministically(self):
        normal = plan_normal({
            "query": "café",
            "retrieval": {"mode": "lexical", "top_k": 1, "candidate_k": 1},
            "providers": ["p"],
        })
        deeper = plan_deeper({
            "query": "café",
            "retrieval": {"mode": "lexical", "top_k": 1, "candidate_k": 1},
            "deeper": {
                "aspects": 3,
                "sections": 2,
                "max_web_searches": 0,
                "web_per_aspect": 0,
                "graph_max_nodes": 1,
                "graph_max_edges": 0,
                "graph_max_hops": 0,
            },
            "providers": ["p"],
        })
        result = {
            "text": "answer",
            "citations": [],
            "references": [],
            "connections": [],
            "figures": [],
        }

        normal_first = _final_artifact(start(normal), "normal", result)
        normal_second = _final_artifact(start(normal), "normal", result)
        deeper_first = _final_artifact(start(deeper), "deeper", result)
        deeper_second = _final_artifact(start(deeper), "deeper", result)

        self.assertEqual(normal_first["payload"]["query"], "café")
        self.assertEqual(deeper_first["payload"]["query"], "café")
        self.assertEqual(normal_first["transfer_digest"], normal_second["transfer_digest"])
        self.assertEqual(deeper_first["transfer_digest"], deeper_second["transfer_digest"])
        self.assertNotEqual(normal_first["transfer_digest"], deeper_first["transfer_digest"])


if __name__ == "__main__":
    unittest.main()
