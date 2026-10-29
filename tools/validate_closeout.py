#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "contracts" / "program-closeout.json"
SCHEMA = ROOT / "schemas" / "program-closeout.schema.json"
PORTFOLIO = ROOT / "portfolio.json"
README = ROOT / "README.md"
DOC = ROOT / "docs" / "PROGRAM_CLOSEOUT.md"


def fail(message: str) -> None:
    raise SystemExit(f"Closeout validation failed: {message}")


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def main() -> None:
    closeout = load(CLOSEOUT)
    schema = load(SCHEMA)
    portfolio = load(PORTFOLIO)

    if closeout.get("status") != "COMPLETE" or closeout.get("scope") != "M0-M9":
        fail("program status/scope is not the bounded complete state")
    if closeout.get("protected_default_branches") != 9:
        fail("protected default branch count must be 9")

    repos = {item["repository"]: item for item in portfolio["repositories"]}
    expected_release = {
        "ai-cyber-resilience-framework": repos["ai-cyber-resilience-framework"]["published_release"],
        "peace-os": repos["peace-os"]["published_release"],
    }
    if closeout.get("published_release_state") != expected_release:
        fail("published release state is incorrect")

    if closeout.get("merged_unreleased_development") not in ({}, None):
        fail("merged unreleased development state must be empty after ACRF v0.2.0 and Peace OS v0.3.0 releases")

    candidates = portfolio.get("development_candidates", {})
    if candidates not in ({}, None):
        fail("portfolio development_candidates must be empty while no merged-unreleased candidates are tracked")

    if schema.get("properties", {}).get("status", {}).get("const") != "COMPLETE":
        fail("closeout schema does not bind COMPLETE")
    if schema.get("properties", {}).get("protected_default_branches", {}).get("const") != 9:
        fail("closeout schema does not bind protected branch count")
    for section in ("published_release_state", "merged_unreleased_development"):
        keys = set(schema.get("properties", {}).get(section, {}).get("properties", {}))
        if "peace-os" not in keys or "peace-os-crisis-room" in keys:
            fail(f"closeout schema {section} must use the peace-os repository identity")

    readme = README.read_text(encoding="utf-8")
    for phrase in (
        "Published release identities remain controlling",
        "v0.2.0",
        "v0.3.0",
        "no merged-unreleased development candidates",
    ):
        if phrase not in readme:
            fail(f"README closeout truth is missing: {phrase}")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Published release identities remain controlling",
        "Merged development work does not silently become a release claim",
        "establish only the properties they directly test",
        "does not establish legal compliance, certification, operational safety",
    ):
        if phrase not in doc:
            fail(f"PROGRAM_CLOSEOUT.md boundary missing: {phrase}")

    if len(closeout.get("deferred_release_gates", [])) < 2:
        fail("deferred release gates are incomplete")

    print(
        "Closeout validation passed: scope, protected-branch count, published releases, "
        "merged-unreleased development, deferred gates, and evidence boundaries agree."
    )


if __name__ == "__main__":
    main()
