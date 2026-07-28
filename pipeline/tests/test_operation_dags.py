"""Offline contract vectors for query operation DAGs."""
import unittest

from pipeline.lib.operation_dags import (
    DagAuthError,
    DagBoundsError,
    DagStateError,
    plan_deeper,
    plan_normal,
    reduce,
    start,
)


class OperationDagTests(unittest.TestCase):
    def test_normal_bounds_and_empty_evidence(self):
        with self.assertRaises(DagBoundsError):
            plan_normal({"query": "q", "retrieval": {"top_k": 101, "candidate_k": 101}, "providers": ["p"]})
        dag = plan_normal({"query": "q", "retrieval": {"mode": "lexical", "top_k": 1, "candidate_k": 1}, "providers": ["p"]})
        state = reduce(start(dag), "N10", {"status": "ok"})
        state = reduce(state, "N13", {"status": "ok", "evidence": []})
        self.assertEqual(state.terminal, "FAILED_EMPTY_EVIDENCE")

    def test_rejects_duplicate_and_undeclared_results(self):
        dag = plan_normal({"query": "q", "retrieval": {"mode": "lexical", "top_k": 1, "candidate_k": 1}, "providers": ["p"]})
        with self.assertRaises(DagStateError):
            reduce(start(dag), "N20", {"status": "ok"})

    def test_deeper_frozen_topology_and_all_fallback_classes(self):
        dag = plan_deeper({
            "query": "q",
            "retrieval": {
                "mode": "lexical",
                "top_k": 1,
                "candidate_k": 1,
                "rerank": False,
            },
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
        frozen_ids = {step.id for step in dag.steps}
        self.assertTrue({
            "D01", "D02", "D10.1", "D13.3", "D15.3", "D20", "D21",
            "D30.1", "D31.1", "D35", "D40", "D41", "D42", "D49",
        } <= frozen_ids)
        self.assertEqual([step.id for step in start(dag).ready], ["D01"])

        with self.assertRaises(DagAuthError):
            reduce(start(dag), "D01", {"status": "failed", "failure": "auth"})

        state = reduce(
            start(dag),
            "D01",
            {"status": "failed", "failure": "provider"},
        )
        state = reduce(state, "D02", {"status": "ok"})
        for aspect in range(1, 4):
            state = reduce(state, f"D10.{aspect}", {"status": "ok"})
            state = reduce(
                state,
                f"D13.{aspect}",
                {"status": "ok", "evidence": [f"e{aspect}"]},
            )
            state = reduce(state, f"D15.{aspect}", {"status": "ok"})

        state = reduce(
            state,
            "D20",
            {"status": "failed", "failure": "provider"},
        )
        state = reduce(state, "D21", {"status": "ok"})
        state = reduce(
            state,
            "D30.1",
            {"status": "failed", "failure": "provider"},
        )
        state = reduce(state, "D31.1", {"status": "ok", "text": "fallback"})
        state = reduce(state, "D30.2", {"status": "ok", "text": "section"})
        draft = {
            "status": "ok",
            "text": "complete",
            "citations": [],
            "references": [],
            "connections": [],
            "figures": [],
        }
        state = reduce(state, "D35", draft)
        state = reduce(
            state,
            "D40",
            {"status": "failed", "failure": "citation"},
        )
        state = reduce(state, "D42", draft)
        state = reduce(state, "D49", {"status": "ok"})
        self.assertEqual(state.terminal, "COMPLETED")
        self.assertEqual(state.final_artifact["payload"]["query"], "q")


if __name__ == "__main__":
    unittest.main()
