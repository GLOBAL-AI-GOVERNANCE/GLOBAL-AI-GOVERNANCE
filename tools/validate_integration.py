#!/usr/bin/env python3
"""Validate the portfolio handoff graph and integration boundaries."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "portfolio.json"
HANDOFFS = ROOT / "contracts" / "handoffs.json"
SCHEMA = ROOT / "contracts" / "portfolio-handoff.schema.json"
EXAMPLE = ROOT / "contracts" / "portfolio-handoff.example.json"

ALLOWED_FAILURE = {
    "FAIL_CLOSED",
    "REJECT_UNSUPPORTED",
    "HOLD_FOR_HUMAN_REVIEW",
    "REVERIFICATION_REQUIRED",
}
REQUIRED_HANDOFF_KEYS = {
    "handoff_id",
    "source_repository",
    "target_repository",
    "source_artifact",
    "target_input",
    "reference_only",
    "failure_behavior",
    "authority_boundary",
}


def fail(message: str) -> None:
    raise SystemExit(f"Integration validation failed: {message}")


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} root must be an object")
    return value


def main() -> None:
    portfolio = load(PORTFOLIO)
    handoff_doc = load(HANDOFFS)
    schema = load(SCHEMA)
    example = load(EXAMPLE)

    if portfolio.get("integration_contract_version") != "1.0.0":
        fail("portfolio integration_contract_version must be 1.0.0")

    candidates = portfolio.get("development_candidates", {})
    acrf = candidates.get("ai-cyber-resilience-framework", {})
    expected_acrf = {
        "candidate": "v0.2.0 Continuous Assurance Thread",
        "status": "MERGED_UNRELEASED",
        "published_release": "v0.1.1",
    }
    if acrf != expected_acrf:
        fail("ACRF merged-unreleased candidate record is missing or incorrect")

    if handoff_doc.get("schema_version") != "1.0.0":
        fail("handoff schema_version must be 1.0.0")
    if handoff_doc.get("contract_version") != portfolio["integration_contract_version"]:
        fail("handoff contract version does not match portfolio manifest")

    repositories = {item["repository"]: item for item in portfolio["repositories"]}
    ids: set[str] = set()

    for item in handoff_doc.get("handoffs", []):
        if set(item) != REQUIRED_HANDOFF_KEYS:
            fail(f"handoff {item.get('handoff_id')} has unexpected key set")
        hid = item["handoff_id"]
        if hid in ids:
            fail(f"duplicate handoff_id: {hid}")
        ids.add(hid)

        source = item["source_repository"]
        target = item["target_repository"]
        if source not in repositories or target not in repositories:
            fail(f"{hid}: unknown source or target repository")
        if target not in repositories[source]["downstream"]:
            fail(f"{hid}: target missing from source downstream declaration")
        if source not in repositories[target]["upstream"]:
            fail(f"{hid}: source missing from target upstream declaration")
        if item["reference_only"] is not True:
            fail(f"{hid}: portfolio handoff must be reference-only")
        if item["failure_behavior"] not in ALLOWED_FAILURE:
            fail(f"{hid}: unsupported failure behavior")
        if not item["authority_boundary"].strip():
            fail(f"{hid}: authority boundary missing")

    required_edges = {
        ("ai-governance-os", "global-ai-governance-toolkit"),
        ("global-ai-governance-toolkit", "agentic-ai-governance"),
        ("agentic-ai-governance", "governed-systems-administration"),
        ("global-ai-governance-toolkit", "verified-vulnerability-governance"),
        ("verified-vulnerability-governance", "ai-cyber-resilience-framework"),
        ("ai-cyber-resilience-framework", "peace-os-crisis-room"),
    }
    actual_edges = {
        (item["source_repository"], item["target_repository"])
        for item in handoff_doc["handoffs"]
    }
    if actual_edges != required_edges:
        fail("handoff graph does not exactly match the bounded portfolio graph")

    if set(example) != REQUIRED_HANDOFF_KEYS:
        fail("portfolio handoff example key set is invalid")
    if example["reference_only"] is not True:
        fail("portfolio handoff example must be reference-only")

    schema_props = schema.get("properties", {})
    if schema_props.get("reference_only", {}).get("const") is not True:
        fail("portfolio-handoff schema must require reference_only=true")

    print(
        "Integration validation passed: portfolio graph, reciprocal handoffs, "
        "reference-only boundaries, failure behavior, and ACRF candidate state are consistent."
    )


if __name__ == "__main__":
    main()
