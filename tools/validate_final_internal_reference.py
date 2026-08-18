#!/usr/bin/env python3
"""Validate the final internal synthetic reference and bounded mapping."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "contracts" / "final-internal-reference.json"
GVR_DOC = ROOT / "docs" / "GOVERNED_VULNERABILITY_REMEDIATION_REFERENCE.md"
NIST_DOC = ROOT / "docs" / "NIST_AI_RMF_1_0_MAPPING.md"
SCOPE_DOC = ROOT / "docs" / "FINAL_INTERNAL_UPDATE_SCOPE.md"
README = ROOT / "README.md"

EXPECTED_STAGES = [
    ("GOVERN_MEASURE", "global-ai-governance-toolkit", "automation/fixtures/governance-decision-handoff.example.json"),
    ("AUTHORIZE", "agentic-ai-governance", "examples/passports/signed-unrevoked.json"),
    ("DESIGN_ENFORCEMENT", "governed-systems-administration", "tests/golden/administration-evidence-record.json"),
    ("OBSERVE_VERIFY_CLOSE", "verified-vulnerability-governance", "examples/governed-remediation/reference.json"),
    ("CONTAIN_RECOVER", "ai-cyber-resilience-framework", "examples/secure-inference-cell/reference-bundle.json"),
    ("DECIDE_LEARN", "peace-os-crisis-room", "examples/portfolio/operating-disposition-reference.json"),
]

def fail(message: str) -> None:
    raise SystemExit(f"Final internal reference validation failed: {message}")

def main() -> None:
    try:
        reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))

    exact_top = {
        "schema_version": "1.0.0",
        "reference_only": True,
        "synthetic_only": True,
        "authority_effect": "NONE",
        "authority_transfer": False,
        "event_occurrence_assumed": False,
        "current_validity_assumed": False,
        "human_decision_required": True,
        "failure_behavior": "FAIL_CLOSED",
        "artifact_resolution": "PATH_PLUS_GATE_EVIDENCE_DIGEST",
    }
    for key, expected in exact_top.items():
        if reference.get(key) != expected:
            fail(f"{key} must be {expected!r}")

    foundation = reference.get("foundation", {})
    if foundation != {
        "repository": "ai-governance-os",
        "artifact_path": "README.md",
        "role": "FOUNDATION",
    }:
        fail("foundation reference is incorrect")

    actual = [
        (item.get("stage"), item.get("repository"), item.get("artifact_path"))
        for item in reference.get("stages", [])
    ]
    if actual != EXPECTED_STAGES:
        fail("stage/repository/artifact sequence is incorrect")

    agentic = reference["stages"][1]
    if agentic.get("current_authority_assumed") is not False:
        fail("Agentic reference may not assume current authority")
    if agentic.get("artifact_semantics") != "SIGNED_SYNTHETIC_REFERENCE_ONLY":
        fail("Agentic artifact semantics are not explicit")

    gsa = reference["stages"][2]
    if gsa.get("execution_assumed") is not False:
        fail("GSA reference may not assume execution")

    gvr = GVR_DOC.read_text(encoding="utf-8")
    for phrase in (
        "reference-only",
        "synthetic",
        "never assumes that the sample is currently valid",
        "does not prove that a real vulnerability was remediated",
        "does not execute commands",
    ):
        if phrase.lower() not in gvr.lower():
            fail(f"GVR boundary text missing: {phrase}")

    nist = NIST_DOC.read_text(encoding="utf-8")
    for phrase in (
        "AI RMF 1.0 is being revised",
        "Govern",
        "Map",
        "Measure",
        "Manage",
        "does not establish NIST compliance",
    ):
        if phrase.lower() not in nist.lower():
            fail(f"NIST mapping boundary text missing: {phrase}")

    scope = SCOPE_DOC.read_text(encoding="utf-8")
    for phrase in (
        "independent human review",
        "external contributors",
        "does not create or promote a release",
        "Published release identities remain controlling",
    ):
        if phrase.lower() not in scope.lower():
            fail(f"scope boundary text missing: {phrase}")

    readme = README.read_text(encoding="utf-8")
    for path in (
        "docs/GOVERNED_VULNERABILITY_REMEDIATION_REFERENCE.md",
        "docs/NIST_AI_RMF_1_0_MAPPING.md",
        "docs/FINAL_INTERNAL_UPDATE_SCOPE.md",
    ):
        if path not in readme:
            fail(f"README link missing: {path}")

    print(
        "Final internal reference validation passed: synthetic/reference-only "
        "boundaries, time-validity non-assumption, integrated stage references, "
        "NIST mapping, and scope limits are consistent."
    )

if __name__ == "__main__":
    main()
