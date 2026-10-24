# File Purpose Index

Every file in this portfolio control-plane repository exists for a specific operational or evidence-boundary purpose.

## Core entry points
- `README.md` — Human-facing Start Here. Directs operators and agents to the Toolkit browser, MCP, and portfolio map. States authority_effect NONE and evidence boundaries.
- `portfolio.json` — Machine-readable portfolio truth: repository identity, maturity, lifecycle role, authority boundary, and handoff contracts. Source of truth for composition.
- `schemas/portfolio.schema.json` — Validates the portfolio manifest.

## Contracts and evidence
- `contracts/` — Stable handoff schemas, federated evidence graph examples, and cross-estate reproduction locks. Enables deterministic composition without centralizing domain semantics.
- `docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md` and related assurance docs — Define the shared assurance envelope and boundaries. Prevent over-claiming.
- `docs/PROGRAM_CLOSEOUT.md` and `docs/FINAL_INTERNAL_UPDATE_SCOPE.md` — Explicit maturity and evidence boundaries. Published release identities remain controlling.

- `docs/VOICE.md` — Voice and terminology guide for all public copy: plain language first, consistent names, no hype, and Claims Integrity labels.

## Validation and reproduction
- `tools/` — Deterministic validators for profile, evidence graph, integration, closeout, and cross-estate reproduction. Used in CI and independent checks.
- `tests/` — Regression coverage for assurance delta and validators.
- `.github/workflows/` — Protected CI that enforces the above on every push and PR.

## Architecture and policy
- `docs/ARCHITECTURE.md` — Portfolio architectural rules: local value first, domain ownership, explicit interfaces, public claims follow evidence, human authority explicit.
- `docs/MATURITY_MODEL.md` — Defines repository maturity labels so they are not misread as organizational AI maturity or certification.
- `docs/SOURCE_POLICY.md`, `docs/CHANGE_POLICY.md` — Operating rules for source integrity and change control.

## Why these files exist
They reduce resistance for operators by making boundaries, contracts, and validation paths explicit and machine-checkable. They maximize real-life value by preventing misuse (over-claiming certification, authority transfer, or production readiness) while enabling rapid, evidence-backed composition of the specialist repositories.

No file exists for personal record-keeping. All content is public technical evidence or control-plane infrastructure.
