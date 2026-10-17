#!/usr/bin/env python3
"""Read-only owner-scoped Estate Truth check.

Compares portfolio.json with public, non-archived repositories owned by
GLOBAL-AI-GOVERNANCE. The owner is a user account, so the query is the
owner endpoint, not the authenticated account's visible repository list.
Mismatch fails closed. This check does not authorize creation or deletion.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "portfolio.json"
OWNER = "GLOBAL-AI-GOVERNANCE"


def fail(msg: str) -> None:
    print(f"ESTATE TRUTH FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    declared_items = json.loads(PORTFOLIO.read_text(encoding="utf-8"))["repositories"]
    declared_names = [item["repository"] for item in declared_items]
    if len(declared_names) != len(set(declared_names)):
        fail(f"duplicate declared repo: {sorted(declared_names)}")
    declared = set(declared_names)
    try:
        raw = subprocess.check_output(
            ["gh", "api", "--paginate", "/" + "users/" + OWNER + "/repos"],
            text=True,
        )
        items = json.loads(raw)
    except Exception as exc:
        fail(f"unable to query owner repositories: {exc}")
    if not isinstance(items, list):
        fail("owner repository query did not return a list")

    actual: set[str] = set()
    archived: set[str] = set()
    for item in items:
        owner = (item.get("owner") or {}).get("login")
        if owner != OWNER:
            fail(f"wrong owner on {item.get('name')}: {owner}")
        if item.get("private") or item.get("visibility") != "public":
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name:
            fail("public repository is missing a name")
        if item.get("archived") is True:
            archived.add(name)
            continue
        actual.add(name)

    archive_mismatch = sorted(declared & archived)
    if archive_mismatch:
        fail(f"archive-state policy mismatch: {archive_mismatch}")
    missing = sorted(declared - actual)
    extra = sorted(actual - declared)
    if missing:
        fail(f"declared but absent from live public estate: {missing}")
    if extra:
        fail(f"live public repo absent from declaration: {extra}")
    print(json.dumps({
        "valid": True,
        "owner": OWNER,
        "declared": len(declared),
        "actual_public": len(actual),
        "archived_excluded": len(archived),
        "authority_effect": "NONE",
        "note": "Owner-scoped public non-archived inventory match only. Does not authorize creation or deletion.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
