#!/usr/bin/env python3
"""Experimental Assurance Delta.

Deterministic research utility. Given materially changed node(s), returns the
affected nodes/claims requiring reassessment (IMPACT SET).

Rules:
- INVALIDATES and dependency relationships propagate impact.
- Unrelated evidence remains untouched.
- Unknown graph relationships fail conservatively.
- Tool never changes authority.
- Tool never declares requalification complete.
- Marked experimental.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "contracts" / "federated-evidence-graph.example.json"
PROPAGATING = {"INVALIDATES", "DEPENDS_ON", "REQUIRES", "REQUALIFIES"}


def impact_set(changed: list[str], graph: dict[str, Any] | None = None) -> dict[str, Any]:
    if graph is None:
        graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {n["node_id"]: n for n in graph.get("nodes", [])}
    edges = graph.get("edges", [])
    affected = set(changed)
    unknown = False
    # Conservative propagation
    changed_flag = True
    while changed_flag:
        changed_flag = False
        for edge in edges:
            rel = edge.get("relationship")
            if rel not in PROPAGATING and rel not in {"SUPPORTS", "QUALIFIES", "CONTRADICTS", "SUPERSEDES", "RECOVERS_FROM", "TRANSFERS_TO"}:
                unknown = True
            if edge.get("from_node") in affected and rel in PROPAGATING:
                to = edge.get("to_node")
                if to not in affected:
                    affected.add(to)
                    changed_flag = True
    if unknown:
        # Conservative: require review of all connected
        for edge in edges:
            if edge.get("from_node") in affected or edge.get("to_node") in affected:
                affected.add(edge.get("from_node"))
                affected.add(edge.get("to_node"))
    return {
        "experimental": True,
        "impact_set": sorted(affected),
        "authority_effect": "NONE",
        "note": "IMPACT SET only. Does not complete requalification or change authority. Unknown relationships fail conservatively.",
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps(impact_set([]), indent=2))
        return
    print(json.dumps(impact_set(sys.argv[1:]), indent=2))


if __name__ == "__main__":
    main()
