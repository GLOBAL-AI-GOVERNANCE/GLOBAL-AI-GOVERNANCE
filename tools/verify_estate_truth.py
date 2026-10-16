#!/usr/bin/env python3
"""Read-only Estate Truth check.

Compares the declared public inventory in portfolio.json with the actual
public repositories owned by GLOBAL-AI-GOVERNANCE. Mismatch fails closed.
Does not authorize repository creation or deletion.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "portfolio.json"


def fail(msg: str) -> None:
    print(f"ESTATE TRUTH FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    declared = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    declared_names = {item["repository"] for item in declared["repositories"]}
    try:
        raw = subprocess.check_output(
            ["gh", "api", "user/repos", "--paginate"],
            text=True,
        )
        items = json.loads(raw)
        actual = {item["name"] for item in items if not item.get("private") and item.get("visibility") == "public"}
    except Exception as exc:
        fail(f"unable to query public repositories: {exc}")

    missing = declared_names - actual
    extra = actual - declared_names
    if missing:
        fail(f"declared but not public: {sorted(missing)}")
    if extra:
        fail(f"public but not declared: {sorted(extra)}")
    print(json.dumps({
        "valid": True,
        "declared": len(declared_names),
        "actual_public": len(actual),
        "authority_effect": "NONE",
        "note": "Inventory match only. Does not authorize creation or deletion.",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
