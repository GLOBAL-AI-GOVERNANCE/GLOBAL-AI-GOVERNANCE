#!/usr/bin/env python3
"""Validate the federated governance evidence graph. References only. No authority."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "contracts" / "federated-evidence-graph.example.json"
SCHEMA = ROOT / "contracts" / "federated-evidence-graph.schema.json"
PORTFOLIO = ROOT / "portfolio.json"
DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
COMMIT = re.compile(r"^[a-f0-9]{40}$")
RELATIONSHIPS = {
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
NODE_KEYS = {
    "node_id",
    "artifact_type",
    "source_repository",
    "source_commit",
    "artifact_id",
    "schema_version",
    "subject_id",
    "configuration_digest",
    "artifact_digest",
    "observed_or_generated_at",
    "currency",
    "authority_effect",
}
EDGE_KEYS = {
    "edge_id",
    "from_node",
    "to_node",
    "relationship",
    "subject_binding",
    "configuration_binding",
    "reconciliation_ref",
    "limitations",
}


class ContractError(Exception):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def allowed_repositories() -> set[str]:
    portfolio = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    return {item["repository"] for item in portfolio["repositories"]}


def validate_graph(graph: dict[str, Any], repositories: set[str] | None = None) -> dict[str, Any]:
    repositories = allowed_repositories() if repositories is None else repositories
    _require(isinstance(graph, dict), "graph must be an object")
    _require(set(graph) == {"schema_version", "graph_id", "reference_only", "authority_effect", "nodes", "edges"}, "unsupported graph fields")
    _require(graph.get("schema_version") == "1.0.0", "schema_version mismatch")
    _require(isinstance(graph.get("graph_id"), str) and graph["graph_id"].strip(), "graph_id required")
    _require(graph.get("reference_only") is True, "reference_only must be true")
    _require(graph.get("authority_effect") == "NONE", "graph authority_effect must be NONE")
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    _require(isinstance(nodes, list) and nodes, "nodes must be a nonempty array")
    _require(isinstance(edges, list), "edges must be an array")
    by_id: dict[str, dict] = {}
    for node in nodes:
        _require(isinstance(node, dict) and set(node) == NODE_KEYS, "unsupported node fields")
        _require(node["node_id"] not in by_id, f"duplicate node: {node['node_id']}")
        _require(node["source_repository"] in repositories, f"unsupported source repository: {node['source_repository']}")
        _require(COMMIT.fullmatch(str(node.get("source_commit", ""))), "malformed source_commit")
        for key in ("artifact_type", "artifact_id", "schema_version", "subject_id"):
            _require(isinstance(node[key], str) and node[key].strip(), f"node {key} required")
        _require(DIGEST.fullmatch(node["configuration_digest"]), "node configuration digest malformed")
        _require(DIGEST.fullmatch(node["artifact_digest"]), "node artifact digest malformed")
        _require(TIMESTAMP.fullmatch(node["observed_or_generated_at"]), "node timestamp malformed")
        _require(node["currency"] in {"CURRENT", "SUPERSEDED", "HISTORICAL"}, "unsupported node currency")
        _require(node["authority_effect"] == "NONE", "node authority_effect must be NONE")
        by_id[node["node_id"]] = node
    seen_edges: set[str] = set()
    for edge in edges:
        _require(isinstance(edge, dict) and set(edge) == EDGE_KEYS, "unsupported edge fields")
        _require(edge["edge_id"] not in seen_edges, f"duplicate edge: {edge['edge_id']}")
        seen_edges.add(edge["edge_id"])
        _require(edge["from_node"] in by_id and edge["to_node"] in by_id, "orphan edge reference")
        _require(edge["relationship"] in RELATIONSHIPS, f"unsupported relationship: {edge['relationship']}")
        _require(edge["relationship"] != "AUTHORIZES", "graph cannot grant authority")
        source = by_id[edge["from_node"]]
        target = by_id[edge["to_node"]]
        _require(edge["subject_binding"] == source["subject_id"] == target["subject_id"], "subject mismatch")
        _require(
            edge["configuration_binding"] == source["configuration_digest"] == target["configuration_digest"],
            "configuration mismatch",
        )
        _require(DIGEST.fullmatch(edge["configuration_binding"]), "edge configuration digest malformed")
        _require(isinstance(edge["limitations"], list) and edge["limitations"], "edge limitations required")
        _require(all(isinstance(item, str) and item.strip() for item in edge["limitations"]), "edge limitations malformed")
        _require(isinstance(edge["reconciliation_ref"], str), "reconciliation_ref must be a string")
        if edge["relationship"] == "CONTRADICTS":
            _require(edge["reconciliation_ref"] in by_id, "contradictory current artifacts require explicit reconciliation")
            reconciliation = by_id[edge["reconciliation_ref"]]
            _require(reconciliation["artifact_type"] == "state-reconciliation-record", "reconciliation reference has the wrong type")
            _require(reconciliation["currency"] == "CURRENT", "reconciliation reference is not current")
            _require(source["currency"] == "CURRENT" and target["currency"] == "CURRENT", "contradiction must name current artifacts")
        elif edge["reconciliation_ref"]:
            _require(edge["reconciliation_ref"] in by_id, "orphan reconciliation reference")
        if edge["relationship"] == "SUPERSEDES":
            _require(source["currency"] == "CURRENT", "superseding artifact must be current")
            _require(target["currency"] == "SUPERSEDED", "superseded artifact treated as current")
    return {"valid": True, "nodes": len(nodes), "edges": len(edges), "authority_effect": "NONE"}


def prove_negatives(graph: dict[str, Any]) -> None:
    repositories = allowed_repositories()
    node = dict(graph["nodes"][0])
    edge = dict(graph["edges"][0])
    cases = {
        "orphan reference": {**graph, "edges": [{**edge, "edge_id": "orphan", "to_node": "missing-node"}]},
        "unsupported source repository": {**graph, "nodes": [{**node, "node_id": "foreign", "source_repository": "unknown-repo"}, *graph["nodes"][1:]]},
        "digest mismatch": {**graph, "edges": [{**edge, "configuration_binding": "sha256:" + "11" * 32}]},
        "subject mismatch": {**graph, "edges": [{**edge, "subject_binding": "other-subject"}]},
        "configuration mismatch": {**graph, "nodes": [{**node, "configuration_digest": "sha256:" + "22" * 32}, *graph["nodes"][1:]]},
        "duplicate node": {**graph, "nodes": [node, *graph["nodes"]]},
        "duplicate edge": {**graph, "edges": [edge, *graph["edges"]]},
        "unsupported relationship": {**graph, "edges": [{**edge, "relationship": "AUTHORIZES"}]},
        "authority_effect": {**graph, "nodes": [{**node, "authority_effect": "AUTHORIZE"}, *graph["nodes"][1:]]},
        "missing source_commit": {**graph, "nodes": [{key: value for key, value in node.items() if key != "source_commit"}, *graph["nodes"][1:]]},
        "malformed source_commit": {**graph, "nodes": [{**node, "source_commit": "not-a-commit"}, *graph["nodes"][1:]]},
        "malformed node": {**graph, "nodes": [{**node, "unexpected": "bad"}, *graph["nodes"][1:]]},
        "malformed edge": {**graph, "edges": [{**edge, "unexpected": "bad"}]},
        "superseded artifact treated as current": {
            **graph,
            "nodes": [
                {**item, "currency": "CURRENT"} if item["node_id"] == "node-recovery-prior" else item
                for item in graph["nodes"]
            ],
        },
    }
    current = [item for item in graph["nodes"] if item["currency"] == "CURRENT"][:2]
    cases["contradictory current artifacts without explicit reconciliation"] = {
        **graph,
        "edges": [
            *graph["edges"],
            {
                **edge,
                "edge_id": "edge-contradiction",
                "from_node": current[0]["node_id"],
                "to_node": current[1]["node_id"],
                "relationship": "CONTRADICTS",
                "reconciliation_ref": "",
            },
        ],
    }
    for label, payload in cases.items():
        try:
            validate_graph(payload, repositories)
        except ContractError:
            continue
        raise ContractError(f"negative graph case was accepted: {label}")


def assert_schema_alignment() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    node = schema["properties"]["nodes"]["items"]
    edge = schema["properties"]["edges"]["items"]
    _require(schema.get("additionalProperties") is False, "graph schema must reject unknown fields")
    _require(node.get("additionalProperties") is False, "node schema must reject unknown fields")
    _require(edge.get("additionalProperties") is False, "edge schema must reject unknown fields")
    _require(set(node["required"]) == NODE_KEYS, "node schema required fields diverged")
    _require(set(edge["required"]) == EDGE_KEYS, "edge schema required fields diverged")
    _require(set(edge["properties"]["relationship"]["enum"]) == RELATIONSHIPS, "relationship enum diverged")
    _require("AUTHORIZES" not in edge["properties"]["relationship"]["enum"], "AUTHORIZES must remain impossible")
    _require(node["properties"]["source_commit"]["pattern"] == r"^[a-f0-9]{40}$", "source_commit pattern diverged")
    _require(node["properties"]["authority_effect"].get("const") == "NONE", "node authority const diverged")
    _require(schema["properties"]["authority_effect"].get("const") == "NONE", "graph authority const diverged")


def main() -> None:
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    assert_schema_alignment()
    result = validate_graph(graph)
    prove_negatives(graph)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
