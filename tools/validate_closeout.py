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

    expected_release = {
        "ai-cyber-resilience-framework": "v0.1.1",
        "peace-os-crisis-room": "v0.3.0-rc2",
    }
    if closeout.get("published_release_state") != expected_release:
        fail("published release state is incorrect")

    expected_dev = {
        "ai-cyber-resilience-framework": "v0.2.0 Continuous Assurance Thread",
        "peace-os-crisis-room": "Post-RC2 Portfolio Operating Disposition Reference",
    }
    if closeout.get("merged_unreleased_development") != expected_dev:
        fail("merged unreleased development state is incorrect")

    candidates = portfolio.get("development_candidates", {})
    if candidates.get("ai-cyber-resilience-framework") != {
        "candidate": "v0.2.0 Continuous Assurance Thread",
        "status": "MERGED_UNRELEASED",
        "published_release": "v0.1.1",
    }:
        fail("ACRF portfolio candidate is inconsistent with closeout")
    if candidates.get("peace-os-crisis-room") != {
        "candidate": "Post-RC2 Portfolio Operating Disposition Reference",
        "status": "MERGED_UNRELEASED",
        "published_release": "v0.3.0-rc2",
    }:
        fail("Peace OS portfolio candidate is inconsistent with closeout")

    if schema.get("properties", {}).get("status", {}).get("const") != "COMPLETE":
        fail("closeout schema does not bind COMPLETE")
    if schema.get("properties", {}).get("protected_default_branches", {}).get("const") != 9:
        fail("closeout schema does not bind protected branch count")

    readme = README.read_text(encoding="utf-8")
    for phrase in (
        "Published release identities remain controlling",
        "v0.2.0 Continuous Assurance Thread",
        "Post-RC2 Portfolio Operating Disposition Reference",
        "do not silently become release claims",
    ):
        if phrase not in readme:
            fail(f"README closeout truth is missing: {phrase}")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in (
        "COMPLETE for the current portfolio hardening and assurance-integration scope",
        "does not mean every repository is production-ready",
        "separate reviewed release gate",
        "not failures of this closeout",
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
