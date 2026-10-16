#!/usr/bin/env python3
"""Synthetic tests for experimental assurance delta direction and bounds."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.assurance_delta import impact_set


def _node(node_id: str) -> dict:
    return {"node_id": node_id}


def _edge(from_node: str, to_node: str, relationship: str) -> dict:
    return {"from_node": from_node, "to_node": to_node, "relationship": relationship}


def _graph(edges: list[dict], nodes: list[str] | None = None) -> dict:
    names = set(nodes or [])
    for edge in edges:
        names.add(edge["from_node"])
        names.add(edge["to_node"])
    return {"nodes": [_node(name) for name in sorted(names)], "edges": edges}


class AssuranceDeltaTests(unittest.TestCase):
    def test_depends_on_change_impacts_dependent_only(self) -> None:
        graph = _graph([
            _edge("A", "B", "DEPENDS_ON"),
        ], ["A", "B", "C"])
        result = impact_set(["B"], graph)
        self.assertEqual(result["condition"], "IMPACT_SET")
        self.assertTrue(result["bounded"])
        self.assertEqual(result["impact_set"], ["A", "B"])
        self.assertNotIn("C", result["impact_set"])
        self.assertEqual(result["authority_effect"], "NONE")
        self.assertTrue(result["experimental"])

    def test_unrelated_change_stays_local(self) -> None:
        graph = _graph([_edge("A", "B", "DEPENDS_ON")], ["A", "B", "C"])
        result = impact_set(["C"], graph)
        self.assertEqual(result["impact_set"], ["C"])
        self.assertNotIn("A", result["impact_set"])
        self.assertNotIn("B", result["impact_set"])

    def test_requires_direction(self) -> None:
        graph = _graph([_edge("A", "B", "REQUIRES")], ["A", "B", "C"])
        result = impact_set(["B"], graph)
        self.assertEqual(result["impact_set"], ["A", "B"])
        self.assertNotIn("C", result["impact_set"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_multi_hop_dependency(self) -> None:
        graph = _graph([
            _edge("A", "B", "DEPENDS_ON"),
            _edge("B", "C", "DEPENDS_ON"),
        ])
        result = impact_set(["C"], graph)
        self.assertEqual(result["impact_set"], ["A", "B", "C"])
        self.assertTrue(result["bounded"])

    def test_invalidates_and_requalifies_use_declared_source_direction(self) -> None:
        invalidates = impact_set(["A"], _graph([_edge("A", "B", "INVALIDATES")], ["A", "B", "C"]))
        requalifies = impact_set(["A"], _graph([_edge("A", "B", "REQUALIFIES")], ["A", "B", "C"]))
        self.assertEqual(invalidates["impact_set"], ["A", "B"])
        self.assertEqual(requalifies["impact_set"], ["A", "B"])
        self.assertNotIn("C", invalidates["impact_set"])

    def test_unknown_conservative(self) -> None:
        graph = _graph([
            _edge("A", "B", "DEPENDS_ON"),
            _edge("B", "D", "NOT_A_RELATIONSHIP"),
        ], ["A", "B", "C", "D"])
        result = impact_set(["B"], graph)
        self.assertEqual(result["condition"], "CONSERVATIVE_REVIEW")
        self.assertFalse(result["bounded"])
        self.assertIn("A", result["impact_set"])
        self.assertIn("D", result["impact_set"])
        self.assertNotIn("C", result["impact_set"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_nonexistent_changed_node_is_invalid(self) -> None:
        graph = _graph([_edge("A", "B", "DEPENDS_ON")])
        result = impact_set(["missing"], graph)
        self.assertEqual(result["condition"], "INVALID_INPUT")
        self.assertFalse(result["bounded"])
        self.assertEqual(result["impact_set"], [])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_cycle_terminates(self) -> None:
        graph = _graph([
            _edge("A", "B", "DEPENDS_ON"),
            _edge("B", "A", "DEPENDS_ON"),
        ])
        result = impact_set(["A"], graph)
        self.assertEqual(result["condition"], "IMPACT_SET")
        self.assertEqual(result["impact_set"], ["A", "B"])
        self.assertTrue(result["bounded"])
        self.assertEqual(result["authority_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
