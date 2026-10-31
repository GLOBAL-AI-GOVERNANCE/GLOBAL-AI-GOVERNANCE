#!/usr/bin/env python3
"""Regenerate suite version pins from each repository's latest GitHub release.

Single source of truth: GitHub release tags (including prereleases when that is
the newest published release). Updates portfolio.json, journey.json,
suite-manifest.json, contracts/program-closeout.json published_release_state,
development_candidates.published_release, and the README install-surfaces and
portfolio version lines. Does not invent maturity status words; it keeps the
text after the first " · " in each badge/maturity string.

Run with no arguments to rewrite files in place. Exit 0 always when the rewrite
succeeds; use --check to exit 1 when a rewrite would change anything.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "GLOBAL-AI-GOVERNANCE"
SITE = "https://ai-governance.solutions/"
# Repositories whose published_release tracks the newest GitHub release tag.
TRACKED = (
    "global-ai-governance-toolkit",
    "ai-governance-mcp",
    "agentic-ai-governance",
    "verified-vulnerability-governance",
    "ai-cyber-resilience-framework",
    "containment-ledger",
    "peace-os",
    "ai-governance-os",
)
TOOLKIT = "global-ai-governance-toolkit"
MCP = "ai-governance-mcp"
AGENTIC = "agentic-ai-governance"
WHEEL_NAME = "global_ai_governance-{naked}-py3-none-any.whl"
BEGIN_INSTALL = "<!-- gaig:install-surfaces -->"
END_INSTALL = "<!-- /gaig:install-surfaces -->"
BEGIN_PORTFOLIO = "<!-- gaig:portfolio-versions -->"
END_PORTFOLIO = "<!-- /gaig:portfolio-versions -->"


def gh_json(path: str):
    """GitHub JSON via `gh api` (retries TLS flakes that hit bare urllib)."""
    last_error: Exception | None = None
    for _ in range(5):
        try:
            completed = subprocess.run(
                ["gh", "api", path.lstrip("/")],
                check=True,
                capture_output=True,
                text=True,
            )
            return json.loads(completed.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as error:
            last_error = error
            continue
    # Fall back to urllib once.
    token = None
    try:
        token = subprocess.run(
            ["gh", "auth", "token"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        token = None
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "gaig-suite-version-sync",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as error:
        raise last_error or error


def latest_release_tag(repository: str) -> str | None:
    """Newest non-draft release, preferring /releases/latest then prereleases."""
    try:
        data = gh_json(f"/repos/{OWNER}/{repository}/releases/latest")
        tag = data.get("tag_name")
        if isinstance(tag, str) and tag:
            return tag
    except Exception:
        # 404 when only prereleases exist, or transient API errors — fall through.
        pass
    releases = gh_json(f"/repos/{OWNER}/{repository}/releases?per_page=20")
    for item in releases:
        if item.get("draft"):
            continue
        tag = item.get("tag_name")
        if isinstance(tag, str) and tag:
            return tag
    return None


def tag_commit_sha(repository: str, tag: str) -> str:
    ref = gh_json(f"/repos/{OWNER}/{repository}/git/ref/tags/{tag}")
    obj = ref["object"]
    if obj["type"] == "commit":
        return obj["sha"]
    tag_obj = gh_json(f"/repos/{OWNER}/{repository}/git/tags/{obj['sha']}")
    return tag_obj["object"]["sha"]


def mcp_upstream_lock(tag: str) -> dict:
    """Read MCP UPSTREAM_LOCK.json at a release tag (bundle pins, not tip)."""
    path = f"repos/{OWNER}/{MCP}/contents/src/gaig_mcp/_upstream/UPSTREAM_LOCK.json?ref={tag}"
    last_error: Exception | None = None
    for _ in range(5):
        try:
            completed = subprocess.run(
                ["gh", "api", path, "-H", "Accept: application/vnd.github.raw"],
                check=True,
                capture_output=True,
                text=True,
            )
            return json.loads(completed.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as error:
            last_error = error
            continue
    raise last_error or RuntimeError(f"MCP UPSTREAM_LOCK unavailable at {tag}")


def toolkit_tag_for_commit(commit_sha: str) -> str | None:
    releases = gh_json(f"/repos/{OWNER}/{TOOLKIT}/releases?per_page=30")
    for item in releases:
        if item.get("draft"):
            continue
        tag = item.get("tag_name")
        if not isinstance(tag, str) or not tag:
            continue
        try:
            if tag_commit_sha(TOOLKIT, tag) == commit_sha:
                return tag
        except Exception:
            continue
    return None



def naked(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def status_after(text: str) -> str:
    parts = text.split(" · ", 1)
    return parts[1] if len(parts) == 2 else text


def replace_version_prefix(text: str, tag: str) -> str:
    if " · " not in text:
        return tag
    return f"{tag} · {status_after(text)}"


def load() -> tuple[dict, dict]:
    return (
        json.loads((ROOT / "portfolio.json").read_text(encoding="utf-8")),
        json.loads((ROOT / "journey.json").read_text(encoding="utf-8")),
    )


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def collect_pins(portfolio: dict) -> dict[str, dict]:
    pins: dict[str, dict] = {}
    for name in TRACKED:
        tag = latest_release_tag(name)
        if not tag:
            continue
        entry: dict = {"tag": tag, "version_naked": naked(tag)}
        if name == TOOLKIT:
            entry["commit_sha"] = tag_commit_sha(name, tag)
            entry["wheel"] = WHEEL_NAME.format(naked=naked(tag))
        if name == MCP:
            try:
                lock = mcp_upstream_lock(tag)
                toolkit_commit = lock["upstreams"]["toolkit"]["commit"]
                agentic_commit = lock["upstreams"]["agentic"]["commit"]
                bundled_tag = toolkit_tag_for_commit(toolkit_commit) or f"commit-{toolkit_commit[:7]}"
                entry["bundled_toolkit"] = {
                    "tag": bundled_tag,
                    "commit_sha": toolkit_commit,
                }
                entry["bundled_agentic"] = {"commit_sha": agentic_commit}
            except Exception as error:
                print(f"WARN: MCP UPSTREAM_LOCK at {tag}: {error}", file=sys.stderr)
        pins[name] = entry
    # Carry human status words from the current portfolio for the manifest.
    by_name = {item["repository"]: item for item in portfolio["repositories"]}
    for name, pin in pins.items():
        record = by_name.get(name, {})
        maturity = record.get("maturity") or ""
        pin["status"] = status_after(maturity) if " · " in maturity else maturity
        pin["published_release"] = tag if (tag := pin["tag"]) else None
    return pins


def apply_portfolio(portfolio: dict, pins: dict[str, dict]) -> None:
    for item in portfolio["repositories"]:
        name = item["repository"]
        pin = pins.get(name)
        if not pin:
            continue
        tag = pin["tag"]
        item["version"] = tag
        item["published_release"] = tag
        item["maturity"] = replace_version_prefix(item["maturity"], tag)

    for surface in portfolio.get("install_surfaces", []):
        name = surface["repository"]
        pin = pins.get(name)
        if not pin:
            continue
        tag = pin["tag"]
        naked_version = pin["version_naked"]
        if surface["surface"] == "Browser" and name == TOOLKIT:
            surface["version"] = f"current main (pinned release {tag})"
        elif surface["surface"] == "CLI" and name == TOOLKIT:
            wheel = pin["wheel"]
            surface["version"] = tag
            surface["install"] = (
                f"pip install https://github.com/{OWNER}/{TOOLKIT}/releases/download/"
                f"{tag}/{wheel}"
            )
        elif surface["surface"] == "GitHub Action" and name == TOOLKIT:
            sha = pin["commit_sha"]
            surface["version"] = f"{tag} (full commit SHA of the release tag)"
            surface["install"] = f"uses: {OWNER}/{TOOLKIT}@{sha}"
        elif surface["surface"] == "MCP server" and name == MCP:
            surface["version"] = tag
            surface["install"] = f"uvx --from git+https://github.com/{OWNER}/{MCP}@{tag} gaig-mcp"
        elif surface["surface"] == "Docker (MCP server)" and name == MCP:
            surface["version"] = tag
        elif surface["surface"] == "Passport validator" and name == AGENTIC:
            surface["version"] = tag
            surface["install"] = (
                f"pip install git+https://github.com/{OWNER}/{AGENTIC}.git@{tag}"
            )

    candidates = portfolio.get("development_candidates", {})
    for name, candidate in candidates.items():
        pin = pins.get(name)
        if pin and isinstance(candidate, dict) and "published_release" in candidate:
            candidate["published_release"] = pin["tag"]


def apply_journey(journey: dict, pins: dict[str, dict]) -> None:
    for item in journey["sequence"]:
        pin = pins.get(item["repository"])
        if not pin:
            continue
        item["badge"] = replace_version_prefix(item["badge"], pin["tag"])


def apply_closeout(pins: dict[str, dict]) -> None:
    path = ROOT / "contracts" / "program-closeout.json"
    closeout = json.loads(path.read_text(encoding="utf-8"))
    state = closeout.get("published_release_state", {})
    for name in list(state):
        if name in pins:
            state[name] = pins[name]["tag"]
    closeout["published_release_state"] = state
    dump(path, closeout)


def install_table(portfolio: dict) -> str:
    rows = [
        "| Surface | Install or run | Version | Maturity | Test status |",
        "|---|---|---|---|---|",
    ]
    for surface in portfolio["install_surfaces"]:
        install = surface["install"]
        if install.startswith("http"):
            cell = f"[Open the Toolkit]({install})" if "ai-governance.solutions" in install else install
            if surface["surface"] == "Browser":
                cell = f"[Open the Toolkit]({install})"
        elif surface["surface"] == "Docker (MCP server)":
            cell = f"`{install}` (in an `ai-governance-mcp` clone)"
        else:
            cell = f"`{install}`"
        rows.append(
            f"| {surface['surface']} | {cell} | {surface['version']} | "
            f"{surface['maturity']} | {surface['test_status']} |"
        )
    return "\n".join(rows)


def portfolio_bullets(portfolio: dict, journey: dict) -> str:
    order = [item["repository"] for item in journey["sequence"]]
    # Append portfolio repos not in the journey (infrastructure).
    seen = set(order)
    for item in portfolio["repositories"]:
        if item["repository"] not in seen and item["classification"] != "PROFILE":
            # keep only product/infra already listed in README historically
            pass
    by_name = {item["repository"]: item for item in portfolio["repositories"]}
    lines = []
    # Match the README product list order: toolkit, mcp, agentic, vvg, acrf, cl, peace, gsa, foundations, .github, profile
    readme_order = [
        "global-ai-governance-toolkit",
        "ai-governance-mcp",
        "agentic-ai-governance",
        "verified-vulnerability-governance",
        "ai-cyber-resilience-framework",
        "containment-ledger",
        "peace-os",
        "governed-systems-administration",
        "ai-governance-os",
        ".github",
        "GLOBAL-AI-GOVERNANCE",
    ]
    link_extras = {
        "global-ai-governance-toolkit": f" · [Open app]({SITE})",
        "containment-ledger": " · [Open app](https://global-ai-governance.github.io/containment-ledger/)",
        "peace-os": " · [Open app](https://global-ai-governance.github.io/peace-os/)",
    }
    display_overrides = {
        "ai-governance-mcp": "AI Governance Model Context Protocol Server (AI Governance MCP)",
        "peace-os": "Peace OS: Crisis Room",
        "ai-governance-os": "AI Governance Foundations",
        ".github": "Repository Governance Defaults",
        "GLOBAL-AI-GOVERNANCE": "Global AI Governance Profile",
    }
    for name in readme_order:
        item = by_name.get(name)
        if not item:
            continue
        display = display_overrides.get(name, item["display_name"])
        extra = link_extras.get(name, "")
        url = f"https://github.com/{OWNER}/{name}"
        lines.append(
            f"- **[{display}]({url})**{extra} — {item['maturity']}. {item['finished_outcome']}."
        )
    return "\n".join(lines)


def replace_marked(text: str, begin: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    block = f"{begin}\n{body}\n{end}"
    if not pattern.search(text):
        raise SystemExit(f"README is missing markers {begin} … {end}")
    return pattern.sub(lambda _m: block, text, count=1)


def apply_readme(portfolio: dict, journey: dict, pins: dict[str, dict]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    # Ensure markers exist; if missing, insert around known tables on first run.
    if BEGIN_INSTALL not in text:
        raise SystemExit(
            "README.md needs install-surfaces markers; add "
            f"{BEGIN_INSTALL} / {END_INSTALL} around the Install at a glance table"
        )
    if BEGIN_PORTFOLIO not in text:
        raise SystemExit(
            "README.md needs portfolio-versions markers; add "
            f"{BEGIN_PORTFOLIO} / {END_PORTFOLIO} around the Portfolio bullet list"
        )
    text = replace_marked(text, BEGIN_INSTALL, END_INSTALL, install_table(portfolio))
    text = replace_marked(text, BEGIN_PORTFOLIO, END_PORTFOLIO, portfolio_bullets(portfolio, journey))

    # Keep a few free-text pins in sync without hard-coding the new values in validators.
    toolkit = pins.get(TOOLKIT, {})
    mcp = pins.get(MCP, {})
    if toolkit:
        tag = toolkit["tag"]
        text = re.sub(
            r"global-ai-governance-toolkit/releases/tag/v[0-9A-Za-z.-]+",
            f"global-ai-governance-toolkit/releases/tag/{tag}",
            text,
        )
        text = re.sub(
            r"global-ai-governance-toolkit/tree/v[0-9A-Za-z.-]+#quick-start",
            f"global-ai-governance-toolkit/tree/{tag}#quick-start",
            text,
        )
        text = re.sub(
            r"global-ai-governance-toolkit/tree/v[0-9A-Za-z.-]+/automation",
            f"global-ai-governance-toolkit/tree/{tag}/automation",
            text,
        )
        text = re.sub(
            r"\[Toolkit v[0-9A-Za-z.-]+ contracts\]",
            f"[Toolkit {tag} contracts]",
            text,
        )
        text = re.sub(
            r"\(pinned release v[0-9A-Za-z.-]+\)",
            f"(pinned release {tag})",
            text,
        )
        # Link label next to the toolkit release URL (URLs are updated above).
        text = re.sub(
            r"\[v[0-9A-Za-z.-]+ release\]"
            r"(\(https://github\.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/tag/v[0-9A-Za-z.-]+\))",
            rf"[{tag} release]\1",
            text,
        )
    if mcp:
        text = re.sub(
            r"The MCP server installs locally \(v[0-9A-Za-z.-]+ release",
            f"The MCP server installs locally ({mcp['tag']} release",
            text,
        )
    path.write_text(text, encoding="utf-8")


def write_manifest(portfolio: dict, journey: dict, pins: dict[str, dict]) -> None:
    path = ROOT / "suite-manifest.json"
    manifest = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "owner": OWNER,
        "source": "github-releases",
        "pins": pins,
        "journey_badges": {
            item["repository"]: item["badge"] for item in journey["sequence"]
        },
        "install_surfaces": portfolio.get("install_surfaces", []),
    }
    # Do not rewrite the file when only generated_at would change. Hourly sync
    # must not open PRs for timestamp-only churn.
    if path.exists():
        previous = json.loads(path.read_text(encoding="utf-8"))
        previous_cmp = {key: value for key, value in previous.items() if key != "generated_at"}
        next_cmp = {key: value for key, value in manifest.items() if key != "generated_at"}
        if previous_cmp == next_cmp:
            return
    dump(path, manifest)


def sync(*, check_only: bool) -> int:
    portfolio, journey = load()
    before = {
        "portfolio": (ROOT / "portfolio.json").read_text(encoding="utf-8"),
        "journey": (ROOT / "journey.json").read_text(encoding="utf-8"),
        "closeout": (ROOT / "contracts" / "program-closeout.json").read_text(encoding="utf-8"),
        "readme": (ROOT / "README.md").read_text(encoding="utf-8"),
        "manifest": (ROOT / "suite-manifest.json").read_text(encoding="utf-8")
        if (ROOT / "suite-manifest.json").exists()
        else "",
    }
    pins = collect_pins(portfolio)
    if not pins:
        raise SystemExit("no release pins collected from GitHub")
    apply_portfolio(portfolio, pins)
    apply_journey(journey, pins)
    if check_only:
        # Apply to temp copies in memory only by dumping and comparing.
        dump(ROOT / "portfolio.json", portfolio)
        dump(ROOT / "journey.json", journey)
        apply_closeout(pins)
        write_manifest(portfolio, journey, pins)
        apply_readme(portfolio, journey, pins)
        after = {
            "portfolio": (ROOT / "portfolio.json").read_text(encoding="utf-8"),
            "journey": (ROOT / "journey.json").read_text(encoding="utf-8"),
            "closeout": (ROOT / "contracts" / "program-closeout.json").read_text(encoding="utf-8"),
            "readme": (ROOT / "README.md").read_text(encoding="utf-8"),
            "manifest": (ROOT / "suite-manifest.json").read_text(encoding="utf-8"),
        }
        # Restore then report.
        for name, text in before.items():
            path = {
                "portfolio": ROOT / "portfolio.json",
                "journey": ROOT / "journey.json",
                "closeout": ROOT / "contracts" / "program-closeout.json",
                "readme": ROOT / "README.md",
                "manifest": ROOT / "suite-manifest.json",
            }[name]
            if text:
                path.write_text(text, encoding="utf-8")
            elif path.exists() and name == "manifest":
                path.unlink()
        changed = [name for name in after if after[name] != before[name]]
        # Ignore generated_at-only manifest churn: compare pins.
        if "manifest" in changed:
            old_pins = json.loads(before["manifest"]).get("pins") if before["manifest"] else None
            new_pins = json.loads(after["manifest"]).get("pins")
            if old_pins == new_pins and before["portfolio"] == after["portfolio"]:
                changed = [name for name in changed if name != "manifest"]
        if changed:
            print("FAIL suite versions drift: " + ", ".join(changed))
            return 1
        print(f"PASS suite versions match GitHub releases for {len(pins)} repositories")
        return 0

    dump(ROOT / "portfolio.json", portfolio)
    dump(ROOT / "journey.json", journey)
    apply_closeout(pins)
    write_manifest(portfolio, journey, pins)
    apply_readme(portfolio, journey, pins)
    print(f"synced {len(pins)} release pins from GitHub")
    for name, pin in sorted(pins.items()):
        extra = f" @{pin['commit_sha'][:12]}" if "commit_sha" in pin else ""
        print(f"  {name}: {pin['tag']}{extra}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if regenerating from GitHub releases would change tracked files",
    )
    args = parser.parse_args()
    return sync(check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
