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
BINDING_REF = ROOT / "contracts" / "assurance-context-binding.reference.json"

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
BINDING_REQUIRED = {
    "schema_version",
    "handoff_id",
    "source_repository",
    "target_repository",
    "source_artifact_type",
    "source_artifact_id",
    "source_version",
    "reference_only",
    "authority_effect",
}
EXPECTED_BINDING_SOURCE = "fad094618e723acec14a8cdc905d1cfcbdf58813"


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


def _validate_binding_reference(obj: dict) -> None:
    if set(obj) != BINDING_REQUIRED:
        raise SystemExit("unexpected key set on binding reference")
    if obj.get("schema_version") != "1.0.0":
        raise SystemExit("schema_version must be 1.0.0")
    if obj.get("handoff_id") != "foundation-to-toolkit":
        raise SystemExit("handoff_id must be foundation-to-toolkit")
    if obj.get("source_repository") != "ai-governance-os":
        raise SystemExit("source_repository must be ai-governance-os")
    if obj.get("target_repository") != "global-ai-governance-toolkit":
        raise SystemExit("target_repository must be global-ai-governance-toolkit")
    if obj.get("source_artifact_id") != "sample-data/assurance-context-binding.json":
        raise SystemExit("source_artifact_id mismatch")
    if obj.get("source_version") != EXPECTED_BINDING_SOURCE:
        raise SystemExit("source_version must match immutable upstream commit")
    if obj.get("reference_only") is not True:
        raise SystemExit("reference_only must be true")
    if obj.get("authority_effect") != "NONE":
        raise SystemExit("authority_effect must be NONE")
    if not obj.get("source_artifact_type"):
        raise SystemExit("source_artifact_type required")


def main() -> None:
    portfolio = load(PORTFOLIO)
    handoff_doc = load(HANDOFFS)
    schema = load(SCHEMA)
    example = load(EXAMPLE)
    binding_ref = load(BINDING_REF)

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
        ("ai-cyber-resilience-framework", "peace-os"),
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

    # Positive binding reference
    try:
        _validate_binding_reference(binding_ref)
    except SystemExit as exc:
        fail(f"positive binding reference rejected: {exc}")

    # Negative binding references
    negatives = [
        ("changed source", lambda d: d.update({"source_repository": "other"})),
        ("unsupported target", lambda d: d.update({"target_repository": "unknown"})),
        ("incorrect handoff", lambda d: d.update({"handoff_id": "wrong"})),
        ("malformed commit", lambda d: d.update({"source_version": "not-a-sha"})),
        ("false reference_only", lambda d: d.update({"reference_only": False})),
        ("non-NONE authority", lambda d: d.update({"authority_effect": "AUTHORIZE"})),
        ("missing field", lambda d: d.pop("source_artifact_id", None)),
        ("unsupported field", lambda d: d.update({"extra": "bad"})),
    ]
    for name, mutator in negatives:
        bad = json.loads(json.dumps(binding_ref))
        mutator(bad)
        rejected = False
        try:
            _validate_binding_reference(bad)
        except SystemExit:
            rejected = True
        if not rejected:
            fail(f"negative binding test did not reject: {name}")

    print(
        "Integration validation passed: portfolio graph, reciprocal handoffs, "
        "reference-only boundaries, failure behavior, ACRF candidate state, "
        "and Assurance Context Binding reference (positive+negative) are consistent."
    )


if __name__ == "__main__":
    main()
