#!/usr/bin/env python3
"""Validate the public profile README and machine-readable portfolio manifest."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PORTFOLIO = ROOT / "portfolio.json"
SCHEMA = ROOT / "schemas" / "portfolio.schema.json"

REQUIRED_HEADINGS = (
    "# Global AI Governance",
    "## Start Here",
    "### Govern One AI System",
    "## Portfolio",
    "## Development Baseline",
    "## Shared Governance Lifecycle",
    "## Operating Principles",
    "## Evidence Boundary",
)

REQUIRED_BOUNDARIES = (
    "human review and decision",
    "no execution capability",
    "do not all implement every lifecycle stage",
    "do not share one maturity level",
    "do not establish operational safety",
    "legal compliance",
    "certification",
    "production authorization",
)

FORBIDDEN_TEXT = (
    "global-ai-governance-solutions",
    "peace-governance-crisis-room",
    "Peace Governance Crisis Room",
    "v0.2.2 · source-readiness pre-release · runtime not yet tested",
    "all repositories are production-ready",
    "fully compliant",
    "certified ai governance",
)

REQUIRED_REPOSITORY_KEYS = {
    "repository",
    "display_name",
    "lifecycle_roles",
    "version",
    "maturity",
    "finished_outcome",
    "authority_boundary",
    "upstream",
    "downstream",
}


def fail(message: str) -> None:
    raise SystemExit(f"Profile validation failed: {message}")


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"required JSON file is missing: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def validate_manifest(manifest: dict) -> list[dict]:
    if manifest.get("schema_version") != "1.0.0":
        fail("portfolio schema_version must be 1.0.0")
    if manifest.get("owner") != "GLOBAL-AI-GOVERNANCE":
        fail("portfolio owner is incorrect")
    if manifest.get("profile_repository") != "GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE":
        fail("profile_repository is incorrect")

    if manifest.get("integration_contract_version") != "1.0.0":
        fail("integration_contract_version must be 1.0.0")
    expected_candidate = {
        "candidate": "v0.2.0 Continuous Assurance Thread",
        "status": "MERGED_UNRELEASED",
        "published_release": "v0.1.1",
    }
    candidates = manifest.get("development_candidates", {})
    if candidates.get("ai-cyber-resilience-framework") != expected_candidate:
        fail("ACRF development candidate record is incorrect")

    expected_peace_candidate = {
        "candidate": "Post-RC2 Portfolio Operating Disposition Reference",
        "status": "MERGED_UNRELEASED",
        "published_release": "v0.3.0-rc2",
    }
    if candidates.get("peace-os-crisis-room") != expected_peace_candidate:
        fail("Peace OS development candidate record is incorrect")

    lifecycle = manifest.get("shared_lifecycle")
    if not isinstance(lifecycle, list) or not lifecycle:
        fail("shared_lifecycle must be a non-empty list")
    if len(lifecycle) != len(set(lifecycle)):
        fail("shared_lifecycle contains duplicates")

    repos = manifest.get("repositories")
    if not isinstance(repos, list) or not repos:
        fail("repositories must be a non-empty list")

    names: list[str] = []
    for index, item in enumerate(repos, start=1):
        if not isinstance(item, dict):
            fail(f"repository entry {index} must be an object")
        if set(item) != REQUIRED_REPOSITORY_KEYS:
            fail(f"repository entry {index} has an unexpected key set")
        for key in ("repository", "display_name", "maturity", "finished_outcome", "authority_boundary"):
            if not isinstance(item[key], str) or not item[key].strip():
                fail(f"repository entry {index} has invalid {key}")
        for key in ("lifecycle_roles", "upstream", "downstream"):
            if not isinstance(item[key], list) or any(not isinstance(v, str) or not v for v in item[key]):
                fail(f"repository entry {index} has invalid {key}")
            if len(item[key]) != len(set(item[key])):
                fail(f"repository entry {index} has duplicate values in {key}")
        if item["version"] is not None and not isinstance(item["version"], str):
            fail(f"repository entry {index} has invalid version")
        names.append(item["repository"])

    if len(names) != len(set(names)):
        fail("portfolio contains duplicate repository names")
    if manifest.get("flagship_repository") not in names:
        fail("flagship_repository is not present in repositories")

    known = set(names)
    for item in repos:
        for relation in (*item["upstream"], *item["downstream"]):
            if relation not in known:
                fail(f"unknown repository relation: {relation}")

    gsa = next((item for item in repos if item["repository"] == "governed-systems-administration"), None)
    if gsa is None or gsa["lifecycle_roles"] != ["DESIGN ENFORCEMENT"]:
        fail("GSA lifecycle role must remain DESIGN ENFORCEMENT until execution capability exists")

    return repos


def main() -> None:
    if not README.is_file():
        fail("README.md is missing")

    text = README.read_text(encoding="utf-8")
    lowered = text.lower()
    manifest = load_json(PORTFOLIO)
    load_json(SCHEMA)
    repositories = validate_manifest(manifest)

    for heading in REQUIRED_HEADINGS:
        if text.count(heading) != 1:
            fail(f"heading must appear exactly once: {heading}")

    for item in repositories:
        repository = item["repository"]
        url = f"https://github.com/GLOBAL-AI-GOVERNANCE/{repository}"
        if url not in text:
            fail(f"repository link is missing: {repository}")
        if item["maturity"] not in text:
            fail(f"README maturity does not match manifest: {repository}")
        if item["finished_outcome"] not in text:
            fail(f"README finished outcome does not match manifest: {repository}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary.lower() not in lowered:
            fail(f"evidence boundary is missing: {boundary}")

    for forbidden in FORBIDDEN_TEXT:
        if forbidden.lower() in lowered:
            fail(f"forbidden or stale claim found: {forbidden}")

    lifecycle_section = text.split("## Shared Governance Lifecycle", 1)[1].split(
        "## Operating Principles", 1
    )[0]
    positions = []
    for stage in manifest["shared_lifecycle"]:
        position = lifecycle_section.find(stage)
        if position < 0:
            fail(f"lifecycle stage is missing: {stage}")
        positions.append(position)
    if positions != sorted(positions):
        fail("lifecycle stages are out of order")

    if not re.search(
        r"\bv2\.1\.0\b.*working public reference toolkit",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        fail("toolkit release and maturity are not connected")

    if "Pre-alpha" not in text or "independent semantic review" not in text:
        fail("GSA pre-alpha review boundary is missing")

    if not re.search(
        r"peace-os-crisis-room.*v0\.3\.0-rc2.*published public browser review candidate",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        fail("Peace OS RC2 repository and bounded maturity are not connected")

    if "\t" in text:
        fail("README contains tab characters")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            fail(f"trailing whitespace on line {line_number}")

    print(
        "Profile validation passed: README, portfolio manifest, lifecycle, maturity, "
        "repository outcomes, and evidence boundaries are consistent."
    )


if __name__ == "__main__":
    main()
