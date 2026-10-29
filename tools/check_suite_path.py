#!/usr/bin/env python3
"""Check that every repository README carries the shared navigation block for the suite path.

The expected block is generated from journey.json and portfolio.json, so names, release
versions, previous and next links, and site links stay in one place. Reads each README
through the GitHub API by default, or from local checkouts with --local DIR.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ai-governance.solutions/"
BEGIN = "<!-- gaig:nav -->"
END = "<!-- /gaig:nav -->"
LINKS = (
    f"[Start where you are]({SITE}start.html) · [Connect your agent]({SITE}connect.html#agents) · "
    f"[Specifications]({SITE}connect.html#spec) · [All products]({SITE}#products)"
)


def load() -> tuple[dict, dict, str]:
    journey = json.loads((ROOT / "journey.json").read_text(encoding="utf-8"))
    portfolio = json.loads((ROOT / "portfolio.json").read_text(encoding="utf-8"))
    return journey, portfolio, portfolio["owner"]


def consistency_errors(journey: dict, portfolio: dict) -> list[str]:
    errors = []
    repos = {item["repository"]: item for item in portfolio["repositories"]}
    seen = set()
    for item in journey["sequence"]:
        name = item["repository"]
        if name in seen:
            errors.append(f"{name}: listed twice in journey.json")
        seen.add(name)
        record = repos.get(name)
        if record is None:
            errors.append(f"{name}: not in portfolio.json")
            continue
        version = record.get("version")
        badge = item["badge"]
        if version and not badge.startswith(version + " · "):
            errors.append(f"{name}: badge {badge!r} does not start with portfolio version {version}")
        if version and not record.get("maturity", "").startswith(badge.split(" · ")[0]):
            errors.append(f"{name}: badge {badge!r} disagrees with portfolio maturity")
    if journey["start"] != SITE + "start.html":
        errors.append("journey.json start must be the site's start page")
    return errors


def expected_block(journey: dict, owner: str, index: int) -> str:
    sequence = journey["sequence"]
    item = sequence[index]

    def link(other: dict) -> str:
        return f"[{other['short_name']}](https://github.com/{owner}/{other['repository']})"

    parts = []
    if index > 0:
        parts.append(f"← {link(sequence[index - 1])}")
    if index + 1 < len(sequence):
        parts.append(f"{link(sequence[index + 1])} →")
    path = (
        f"Suite path, step {index + 1} of {len(sequence)}: {item['role']} · "
        + " · ".join(parts)
        + f" · [start anywhere]({journey['start']})"
    )
    return "\n".join(
        [
            BEGIN,
            f"**[Global AI Governance]({SITE})** · `{item['badge']}` · `authority_effect: NONE`",
            "",
            LINKS,
            "",
            path,
            END,
        ]
    )


def readme_from_api(owner: str, repository: str) -> str:
    completed = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repository}/readme"],
        check=True,
        capture_output=True,
        text=True,
    )
    return base64.b64decode(json.loads(completed.stdout)["content"]).decode("utf-8")


def actual_block(readme: str) -> str | None:
    match = re.search(re.escape(BEGIN) + r".*?" + re.escape(END), readme, re.S)
    return match.group(0) if match else None


def manifest_errors(journey: dict, portfolio: dict) -> list[str]:
    """Require suite-manifest.json pins to match portfolio/journey versions."""
    path = ROOT / "suite-manifest.json"
    if not path.is_file():
        return ["suite-manifest.json is missing (run tools/sync_suite_versions.py)"]
    manifest = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    pins = manifest.get("pins") or {}
    repos = {item["repository"]: item for item in portfolio["repositories"]}
    for name, pin in pins.items():
        record = repos.get(name)
        if record is None:
            errors.append(f"{name}: in suite-manifest.json but not portfolio.json")
            continue
        if record.get("published_release") != pin.get("tag") and record.get("version") != pin.get("tag"):
            errors.append(
                f"{name}: suite-manifest tag {pin.get('tag')!r} disagrees with portfolio "
                f"{record.get('published_release')!r}"
            )
    badges = manifest.get("journey_badges") or {}
    for item in journey["sequence"]:
        name = item["repository"]
        if name in badges and badges[name] != item["badge"]:
            errors.append(f"{name}: suite-manifest journey badge disagrees with journey.json")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", type=Path, help="directory holding local checkouts named after each repository")
    parser.add_argument("--print", dest="show", metavar="REPOSITORY", help="print the expected block for one repository")
    args = parser.parse_args()
    journey, portfolio, owner = load()
    names = [item["repository"] for item in journey["sequence"]]
    if args.show:
        print(expected_block(journey, owner, names.index(args.show)))
        return 0
    errors = consistency_errors(journey, portfolio) + manifest_errors(journey, portfolio)
    for index, item in enumerate(journey["sequence"]):
        name = item["repository"]
        readme = (
            (args.local / name / "README.md").read_text(encoding="utf-8")
            if args.local
            else readme_from_api(owner, name)
        )
        block = actual_block(readme)
        if block is None:
            errors.append(f"{name}: README has no {BEGIN} block")
            continue
        badge = f"`{item['badge']}` · `authority_effect: NONE`"
        if badge not in block:
            errors.append(f"{name}: README badge does not read {item['badge']!r}")
        if item.get("readme_managed", True) and block != expected_block(journey, owner, index):
            errors.append(f"{name}: README navigation block differs from journey.json (run with --print {name})")
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print(f"PASS suite path: {len(names)} repositories, names, versions, and previous/next links agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
