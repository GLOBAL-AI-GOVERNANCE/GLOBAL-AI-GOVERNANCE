#!/usr/bin/env python3
"""Experimental Assurance Delta.

Returns an IMPACT SET for materially changed nodes. The result is not an
authorization, not completed requalification, and not a declaration that
evidence is invalid. It claims nothing beyond the declared graph.

Direction is the explicit table below. It is not inferred from relationship
names at runtime. The same table is stated in docs/ASSURANCE_GRAPH.md.

- DEPENDS_ON and REQUIRES: a change to `to` places `from` in the impact set.
- INVALIDATES and REQUALIFIES: a change to `from` places `to` in the impact set.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "contracts" / "federated-evidence-graph.example.json"

KNOWN_RELATIONSHIPS = {
    "SUPPORTS",
    "QUALIFIES",
    "CONTRADICTS",
    "SUPERSEDES",
    "DEPENDS_ON",
    "REQUIRES",
    "INVALIDATES",
    "RECOVERS_FROM",
    "TRANSFERS_TO",
    "REQUALIFIES",
}

# target: change(to_node) impacts from_node.
# source: change(from_node) impacts to_node.
DIRECTION = {
    "DEPENDS_ON": "target",
    "REQUIRES": "target",
    "INVALIDATES": "source",
    "REQUALIFIES": "source",
}

NOTE = (
    "IMPACT SET only. Experimental. Does not authorize, complete requalification, "
    "declare evidence invalid, or claim causal truth beyond the declared graph."
)


def _result(condition: str, bounded: bool, impact: set[str], note: str = NOTE) -> dict[str, Any]:
    return {
        "experimental": True,
        "condition": condition,
        "bounded": bounded,
        "impact_set": sorted(item for item in impact if item),
        "authority_effect": "NONE",
        "note": note,
    }


def impact_set(changed: list[str], graph: dict[str, Any] | None = None) -> dict[str, Any]:
    if graph is None:
        graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {node["node_id"] for node in graph.get("nodes", []) if isinstance(node, dict)}
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, dict)]
    missing = [node for node in changed if node not in nodes]
    if missing:
        return _result(
            "INVALID_INPUT",
            False,
            set(),
            "Changed node is not in the graph. Result is not a bounded impact set.",
        )

    unknown = [edge for edge in edges if edge.get("relationship") not in KNOWN_RELATIONSHIPS]
    affected = set(changed)
    pending = list(changed)
    guard = 0
    limit = len(nodes) + len(edges) + len(changed) + 1
    while pending:
        guard += 1
        if guard > limit:
            return _result("CONSERVATIVE_REVIEW", False, affected, "Propagation did not terminate inside the graph bound.")
        current = pending.pop()
        for edge in edges:
            direction = DIRECTION.get(edge.get("relationship"))
            if direction == "target" and edge.get("to_node") == current:
                other = edge.get("from_node")
            elif direction == "source" and edge.get("from_node") == current:
                other = edge.get("to_node")
            else:
                continue
            if other not in affected and other in nodes:
                affected.add(other)
                pending.append(other)

    if unknown:
        review = set(affected)
        grew = True
        while grew:
            grew = False
            for edge in unknown:
                ends = {edge.get("from_node"), edge.get("to_node")}
                if review & ends and not ends <= review:
                    review |= {item for item in ends if item in nodes}
                    grew = True
        return _result(
            "CONSERVATIVE_REVIEW",
            False,
            review,
            "Unknown relationship requires conservative review. This is not a bounded impact set.",
        )
    return _result("IMPACT_SET", True, affected)


def main() -> None:
    print(json.dumps(impact_set(sys.argv[1:]), indent=2))


if __name__ == "__main__":
    main()
