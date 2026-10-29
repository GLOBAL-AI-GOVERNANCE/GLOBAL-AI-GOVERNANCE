# Releasing and suite version sync

Product release tags are the single source of truth for suite version pins. Do not hand-edit version numbers in the profile README, `portfolio.json`, `journey.json`, or the Toolkit site docs when cutting a release.

## What to release

1. Tag and publish the product release in its own repository (CI-attested assets as that repo requires).
2. Within an hour, or sooner via `workflow_dispatch` / `repository_dispatch` (`suite-release`), the profile workflow **Sync suite versions** regenerates:
   - `portfolio.json` and `journey.json`
   - `suite-manifest.json` (machine-readable pins, commit SHAs, wheel names)
   - `contracts/program-closeout.json` published-release fields that track those tags
   - README install-surfaces and portfolio version blocks (between `gaig:*` markers)
3. The workflow opens a squash PR and enables auto-merge when checks are green.
4. Consuming repos (Toolkit site pins, README `gaig:nav` blocks, social preview PNGs) read `suite-manifest.json` and regenerate the same way. Social PNG upload stays a browser step for the operator.

## Checks instead of hard-coded versions

- `tools/sync_suite_versions.py --check` fails when regenerating from GitHub would change tracked files.
- `tools/check_suite_path.py` requires README nav blocks and `suite-manifest.json` to agree with `journey.json` / `portfolio.json`.
- Profile validators derive expected release links and closeout pins from `portfolio.json`.

## Cross-repo trigger without new secrets

`GITHUB_TOKEN` cannot start workflows in other repositories. Prefer:

- **Scheduled pull** in each consuming repo (hourly), or
- **`workflow_dispatch`** on the consumer after you publish, or
- **`repository_dispatch` type `suite-release`** on this profile repo when a product release workflow is allowed to call it with the default token targeting this same repo only.

## First automated run

The initial `suite-manifest.json` was generated from the live GitHub releases that already pinned Toolkit `v2.8.1`, MCP `v0.5.1`, and Peace OS `v0.3.0-rc3`. Later releases propagate through the same path.
