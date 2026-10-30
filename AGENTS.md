# AGENTS.md

Instructions for coding agents working in this public profile repository.

## Setup and checks

```bash
python3 -B tools/check_history_privacy.py
python3 -B tools/validate_profile.py
GH_TOKEN="$(gh auth token)" python3 -B tools/verify_estate_truth.py
GH_TOKEN="$(gh auth token)" python3 -B tools/check_suite_path.py
GH_TOKEN="$(gh auth token)" python3 -B tools/sync_suite_versions.py --check
python3 -B -m unittest tests/test_assurance_delta.py -v
python3 -B tools/check_schema_ids.py
python3 -B tools/validate_integration.py
python3 -B tools/validate_closeout.py
python3 -B tools/validate_final_internal_reference.py
```

`Profile Checks` on GitHub Actions runs the same suite, including the suite-version check on pull requests.

## Rules

- `GLOBAL-AI-GOVERNANCE` is a GitHub User account, not a GitHub Organization. Do not describe it as an organization in site, README, or metadata copy.
- Every public result keeps `authority_effect: "NONE"`. Do not add a path that approves, certifies, or authorizes.
- Version pins come from live GitHub releases via `tools/sync_suite_versions.py`. Do not hand-edit suite versions in README, portfolio, journey, or suite-manifest without running that tool.
- Prefer squash-merge through green CI. Do not force-push `main`.

## Setup guide

End-to-end local setup for the toolkit and MCP: [AGENT_SETUP](https://ai-governance.solutions/AGENT_SETUP.html).
