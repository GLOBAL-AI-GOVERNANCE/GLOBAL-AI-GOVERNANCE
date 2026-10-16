#!/usr/bin/env python3
"""Synthetic tests for experimental assurance delta."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.assurance_delta import impact_set

ROOT = Path(__file__).resolve().parents[1]
GRAPH = json.loads((ROOT / "contracts" / "federated-evidence-graph.example.json").read_text(encoding="utf-8"))


class AssuranceDeltaTests(unittest.TestCase):
    def test_one_dependency_change_bounded(self) -> None:
        nodes = [n["node_id"] for n in GRAPH.get("nodes", [])]
        if nodes:
            result = impact_set([nodes[0]], GRAPH)
            self.assertIn(nodes[0], result["impact_set"])
            self.assertEqual(result["authority_effect"], "NONE")
            self.assertTrue(result["experimental"])

    def test_unrelated_untouched(self) -> None:
        result = impact_set(["nonexistent-node"], GRAPH)
        self.assertEqual(result["authority_effect"], "NONE")

    def test_unknown_conservative(self) -> None:
        result = impact_set([], GRAPH)
        self.assertEqual(result["authority_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
