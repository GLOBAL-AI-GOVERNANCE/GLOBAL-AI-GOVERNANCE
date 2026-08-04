#!/usr/bin/env python3
"""Validate the public profile README and its evidence boundaries."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

REQUIRED_HEADINGS = (
    "# Global AI Governance",
    "## Start Here",
    "### Govern One AI System",
    "## Portfolio",
    "## Shared Governance Lifecycle",
    "## Operating Principles",
    "## Evidence Boundary",
)

REQUIRED_REPOSITORIES = (
    "global-ai-governance-toolkit",
    "agentic-ai-governance",
    "governed-systems-administration",
    "verified-vulnerability-governance",
    "ai-cyber-resilience-framework",
    "peace-os-crisis-room",
    "ai-governance-os",
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

LIFECYCLE = (
    "Govern",
    "Authorize",
    "Enforce",
    "Observe",
    "Verify",
    "Contain",
    "Recover",
    "Measure",
    "Learn",
)


def fail(message: str) -> None:
    raise SystemExit(f"Profile validation failed: {message}")


def main() -> None:
    if not README.is_file():
        fail("README.md is missing.")

    text = README.read_text(encoding="utf-8")
    lowered = text.lower()

    for heading in REQUIRED_HEADINGS:
        if text.count(heading) != 1:
            fail(f"heading must appear exactly once: {heading}")

    for repository in REQUIRED_REPOSITORIES:
        url = (
            "https://github.com/GLOBAL-AI-GOVERNANCE/"
            f"{repository}"
        )
        if url not in text:
            fail(f"repository link is missing: {repository}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary.lower() not in lowered:
            fail(f"evidence boundary is missing: {boundary}")

    for forbidden in FORBIDDEN_TEXT:
        if forbidden.lower() in lowered:
            fail(f"forbidden or stale claim found: {forbidden}")

    lifecycle_section = text.split(
        "## Shared Governance Lifecycle",
        1,
    )[1].split("## Operating Principles", 1)[0]

    positions = []
    for stage in LIFECYCLE:
        position = lifecycle_section.find(stage)
        if position < 0:
            fail(f"lifecycle stage is missing: {stage}")
        positions.append(position)

    if positions != sorted(positions):
        fail("lifecycle stages are out of order.")

    if not re.search(
        r"\bv2\.1\.0\b.*working public reference toolkit",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        fail("toolkit release and maturity are not connected.")

    if "Pre-alpha" not in text or "independent semantic review" not in text:
        fail("GSA pre-alpha review boundary is missing.")
    if not re.search(
        r"peace-os-crisis-room.*v0\.3\.0-rc2.*"
        r"published public browser review candidate",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        fail("Peace OS RC2 repository and bounded maturity are not connected.")

    if "\t" in text:
        fail("README contains tab characters.")

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            fail(f"trailing whitespace on line {line_number}")

    print(
        "Profile validation passed: "
        "flagship path, portfolio links, lifecycle, maturity, "
        "and evidence boundaries verified."
    )


if __name__ == "__main__":
    main()
