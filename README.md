# Global AI Governance

**Novel governance solutions the world needs now.**

Open, non-authorizing governance infrastructure that AI agents and the teams behind them can call: evidence in, decision-ready outcomes out, humans in charge.

**[Connect your agent](#for-ai-agents)** · **[Run a pilot](#for-labs-and-teams)** · **[Read the spec](docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md)** · [Live toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/)

Every Global AI Governance output carries `authority_effect: NONE`. The tools prepare evidence and decision support; approval, deployment, risk acceptance, and shutdown stay with accountable humans.

## For AI agents

Compatible with Model Context Protocol (MCP) based agents. MCP is an open standard that lets AI assistants call external tools. Not affiliated with or endorsed by any AI lab or platform.

**Read first:** [`llms.txt`](https://global-ai-governance.github.io/global-ai-governance-toolkit/llms.txt) and [`machine-interface.json`](https://global-ai-governance.github.io/global-ai-governance-toolkit/machine-interface.json) describe the versioned contracts, schemas, and entry points without scraping prose.

**Use it in your agent in 5 minutes** with the [AI Governance Model Context Protocol Server](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) (AI Governance MCP), a read-only server with three tools: `check_inventory`, `build_decision_pack`, and `validate_passport`.

```bash
git clone https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp && cd ai-governance-mcp
python3 -m venv .venv && . .venv/bin/activate && pip install -e .
./scripts/fetch_upstreams.sh   # pinned, read-only copies of the reference repositories
gag-mcp                        # stdio; or: gag-mcp --http --port 8000
```

The repository was renamed from `gag-mcp` (the old URL redirects). The command `gag-mcp`, the Python package `gag_mcp`, and the `GAG_MCP_*` environment variables are unchanged.

Local use (stdio) needs no network or token. Any remote use needs an HTTPS endpoint you host yourself, `GAG_MCP_ALLOWED_HOSTS` set to the hostname clients use, and `GAG_MCP_BEARER_TOKEN` set to a random secret of at least 32 characters; the server refuses to start on a network-reachable bind without both. Every remote request must send `Authorization: Bearer TOKEN`. The token is a static shared secret, not OAuth. Replace `/ABS/PATH`, `YOUR-HOST`, and `TOKEN` with your own values.

```bash
export GAG_MCP_ALLOWED_HOSTS=YOUR-HOST
export GAG_MCP_BEARER_TOKEN=TOKEN
gag-mcp --http --host 0.0.0.0 --port 8000
```

**Provider connections: NOT VERIFIED.** Protocol compatibility is tested with the official MCP Python SDK client and the MCP Inspector. None of the provider recipes below has been tested against a live provider.

<details>
<summary><b>Claude Desktop</b> (local, stdio)</summary>

```json
{
  "mcpServers": {
    "gag": { "command": "/ABS/PATH/ai-governance-mcp/.venv/bin/gag-mcp" }
  }
}
```

Remote (NOT VERIFIED): the Anthropic Messages API MCP connector with `"authorization_token": "TOKEN"`. A Claude.ai custom connector works only if your organization can add an `authorization: Bearer TOKEN` request header; otherwise it cannot connect, because this server does not implement OAuth.
</details>

<details>
<summary><b>OpenAI Responses API</b> (remote MCP, NOT VERIFIED)</summary>

```json
{
  "type": "mcp",
  "server_label": "gag",
  "server_url": "https://YOUR-HOST/mcp",
  "headers": { "Authorization": "Bearer TOKEN" },
  "allowed_tools": ["check_inventory", "build_decision_pack", "validate_passport"],
  "require_approval": "never"
}
```

ChatGPT on the web (developer mode or custom apps) is **not supported**: it offers OAuth or no authentication and cannot send the static bearer token this server requires.
</details>

<details>
<summary><b>xAI API</b> (remote MCP, NOT VERIFIED)</summary>

```json
{
  "type": "mcp",
  "server_label": "gag",
  "server_url": "https://YOUR-HOST/mcp",
  "headers": { "Authorization": "Bearer TOKEN" },
  "allowed_tools": ["check_inventory", "build_decision_pack", "validate_passport"]
}
```

grok.com consumer connectors: whether they can send a static `Authorization: Bearer` header is unverified. If they cannot, they cannot connect to this server.
</details>

No hosted Global AI Governance endpoint exists. Full per-platform setup, the auth model, and self-hosting options are in the [AI Governance MCP README](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#readme).

## For labs and teams

**Run a pilot:** one authorized AI system inventory, one accountable owner, one Decision Pack, and one documented decision boundary. Pilots can cover agent authority and passports, vulnerability closure evidence, cyber-resilience boundaries, or wiring AI Governance MCP into an internal agent platform.

**Contact:** start with the [Pilots and integrations: start here](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/discussions/29) thread, or open a new thread in [GitHub Discussions](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/discussions) with your use case. Do not post confidential, personal, or regulated information.

## Product Map

| Product | What you get | Status | Open |
|---|---|---|---|
| Toolkit | Inventory to findings to human Decision Pack | v2.3.0 · released | [Site](https://global-ai-governance.github.io/global-ai-governance-toolkit/) · [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit) |
| AI Governance MCP | Toolkit and passport checks inside any MCP-based agent | v0.1.0 · preview | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) |
| Agentic AI Governance | Agent authority, passport, expiry, and revocation schemas | v0.1.0-alpha.2 · experimental | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance) |
| Verified Vulnerability Governance | Evidence-linked remediation and verified closure | v0.1.3 · pre-release | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/verified-vulnerability-governance) |
| AI Cyber Resilience Framework | Boundary assessment and hardening backlog | v0.1.1 · reference framework | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework) |
| Containment Ledger: Security Boundary Review | Local browser review of security domains, boundary paths, evidence marks, and a human disposition | Unreleased · public instrument | [Site](https://global-ai-governance.github.io/containment-ledger/) · [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/containment-ledger) |
| Peace OS: Crisis Room | Fictional crisis-verification exercise | v0.3.0-rc2 · review candidate | [Site](https://global-ai-governance.github.io/peace-os/) · [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/peace-os) |
| Governed Systems Administration | Proposed governed administration contracts | Pre-alpha · design only | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration) |
| AI Governance Foundations | The original foundation: governance model, registers, and templates | v1.1 · foundational | [Repo](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-os) |

AI Governance Foundations (`ai-governance-os`, first published as AI Governance OS v1.1 in May 2026) is the portfolio's original foundation; the toolkit and later repositories build on its doctrine, registers, and templates. Containment Ledger is independent of the AI Cyber Resilience Framework and records a review only: it does not enforce boundaries or verify evidence.

Lifecycle roles, controlling maturity, and evidence boundaries for each repository are in the Portfolio table below.

## Start Here

Choose one public path. Each route names the capability and maturity that exist today.

### USE

Open the [live local-first governance browser](https://global-ai-governance.github.io/global-ai-governance-toolkit/). The hosted browser reflects current `main`. The controlling tagged reference is [v2.3.0 - Assurance & Accountability Profiles](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/tag/v2.3.0).

```
AI system inventory
→ normalization and schema validation
→ preliminary risk tier
→ policy-driven findings
→ machine-readable governance outputs
→ AI Governance Decision Pack
→ human review and decision
```

1. Open the live browser and select **Run sample**.
2. Review normalization, findings, machine outputs, and the Decision Pack.
3. Load one authorized CSV when appropriate; approval, restrictions, risk acceptance, rollback, and shutdown remain human-owned.

For a reproducible tagged reference path, use the released [v2.3.0 five-minute workflow](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.3.0#quick-start).

v2.3.0 preserves the bounded sovereignty assessment and adds optional Auditable AI, Quantum-AI synthetic assurance, and CISO accountability profiles. These profiles produce non-authorizing evidence and decision support; they do not establish provider attestation, certification, compliance, production authorization, quantum advantage, or operating authority.

### INTEGRATE

Use only the versioned public contracts that fit your boundary:

- [Toolkit v2.3.0 automation](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.3.0/automation) for inventory checks, policy findings, reports, and a human Decision Pack.
- [Agentic AI Governance v0.1.0-alpha.2 schemas](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/tree/v0.1.0-alpha.2/schemas) for experimental authority, passport, evidence, validation, expiry, and revocation artifacts.
- [Portfolio repository contracts](docs/REPOSITORY_CONTRACTS.md) for reference-only handoffs that do not transfer approval, truth, certification, or operational authority.
- [Global AI Assurance Envelope](docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md) for the portfolio-level reference-only interoperability object (authority_effect: NONE).

Published tags remain controlling. Merged or local development work is not a released interface until its own release gate passes.

### PARTNER

Start with one bounded, evidence-producing pilot: one authorized inventory, one accountable human owner, one Decision Pack, and one documented decision boundary. Use the flagship's [public contribution process](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/blob/v2.3.0/CONTRIBUTING.md) to propose a reproducible use case, fixture, documentation improvement, or integration adapter.

Partnership does not imply endorsement, certification, production authorization, compliance, or acceptance of submitted claims. Do not include confidential, personal, regulated, or otherwise protected information in public contributions.

## Portfolio

[Understand repository maturity → Maturity Model](docs/MATURITY_MODEL.md)

| Lifecycle role | Repository | Current maturity | Finished outcome |
|---|---|---|---|
| **GOVERN + MEASURE** | [Global AI Governance Toolkit](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit) | **v2.3.0 · working public reference toolkit** | Reproducible Decision Pack, bounded sovereignty assessment, and optional assurance/accountability profiles |
| **AUTHORIZE** | [Agentic AI Governance](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance) | **v0.1.0-alpha.2 · experimental public alpha** | Machine-readable authority, evidence, passport, validation, expiry, and revocation artifacts |
| **DESIGN ENFORCEMENT** | [Governed Systems Administration](https://github.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration) | **Pre-alpha · preimplementation · independent semantic review required · no execution capability** | Proposed human-governed administration request, review, validation, and evidence contracts |
| **OBSERVE + VERIFY + CLOSE** | [Verified Vulnerability Governance](https://github.com/GLOBAL-AI-GOVERNANCE/verified-vulnerability-governance) | **v0.1.3 · verified-closure pre-release** | Evidence-linked vulnerability ownership, remediation, retesting, and closure |
| **CONTAIN + RECOVER** | [AI Cyber Resilience Framework](https://github.com/GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework) | **v0.1.1 · public defensive reference** | Boundary assessment, evidence cards, and architecture-hardening backlog |
| **DECIDE + LEARN** | [Peace OS: Crisis Room](https://github.com/GLOBAL-AI-GOVERNANCE/peace-os) | **v0.3.0-rc2 · published public browser review candidate · stable, human-validation, Godot, and Windows gates open** | Fictional crisis-verification simulation and after-action review |
| **FOUNDATION** | [AI Governance Foundations](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-os) | **v1.1 · foundational governance model and template set** | Inventory, ownership, risk, control, monitoring, and reporting foundations |
| **ADJUNCT** | [Containment Ledger](https://github.com/GLOBAL-AI-GOVERNANCE/containment-ledger) | **Local-only browser instrument for domain/path/evidence marking and human disposition** | Independent structural review instrument; shares vocabulary with the AI Cyber Resilience Framework; no code, data, or release dependency; authority_effect NONE |
| **ADJUNCT** | [AI Governance Model Context Protocol Server](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) | **v0.1.0 preview · source only · no hosted endpoint** | Read-only Model Context Protocol (MCP) tools wrapping the toolkit and passport validator; authority_effect NONE |
| **GOVERNANCE META** | [Community Health](https://github.com/GLOBAL-AI-GOVERNANCE/.github) | **Account-level default community health and repository governance files** | Consistent contribution, support, and security-reporting boundaries |
| **PROFILE CONTROL** | [Global AI Governance](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE) | **Public Start Here profile for the open-source portfolio** | Portfolio truth registry, federated evidence graph, and cross-estate reproduction |

## Development Baseline

Published release identities remain controlling. Merged development work is tracked separately so development state does not silently become a release claim.

- **Agentic AI Governance:** the bounded OPA Enforcement Bridge and synthetic Agent Incident Readiness lifecycle reference implementations are merged and unreleased with current-main status `DEFINED / VERIFIED`. The lifecycle demonstrates authorized, policy-denied, revoked, rollback-rejected, and distinct new-passport reauthorized states while preserving terminal revocation of the original passport. It performs no external enforcement. The published release remains `v0.1.0-alpha.2`.
- **Verified Vulnerability Governance:** the bounded synthetic crypto-migration closure reference is merged and unreleased. It uses the existing governed-remediation contract and does not evidence real migration, deployment, or independent retesting. The published pre-release identity remains `v0.1.3`.
- **AI Cyber Resilience Framework:** `v0.2.0 Continuous Assurance Thread`, including the optional synthetic crypto-agility reference, is merged and unreleased. The published release remains `v0.1.1`.
- **Peace OS: Crisis Room:** `Post-RC2 Portfolio Operating Disposition Reference` is merged and unreleased. The published browser review candidate remains `v0.3.0-rc2`, and its documented stable-release holds remain open.

These development handoffs are reference-only. They do not silently become release claims, production authorization, certification, operational truth, or permission to act.

## Integrated Reference Proof

The portfolio demonstrates bounded interoperability across repositories without transferring authority or truth between them.

- [Governed Vulnerability Remediation integrated reference](docs/GOVERNED_VULNERABILITY_REMEDIATION_REFERENCE.md)
- [NIST AI RMF 1.0 bounded portfolio mapping](docs/NIST_AI_RMF_1_0_MAPPING.md)
- [Global AI Assurance Envelope](docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md)
- [Problem-Solving Model](docs/PROBLEM_SOLVING_MODEL.md)
- [Independent Validation Pattern](docs/INDEPENDENT_VALIDATION_PATTERN.md)

The references are synthetic and reference-only. They do not prove real remediation, independent retesting, operational assurance, compliance, certification, or permission to act.

## Shared Governance Lifecycle

```
Govern
→ Authorize
→ Enforce
→ Observe
→ Verify
→ Contain
→ Recover
→ Measure
→ Learn
```

The repositories are complementary. They do not all implement every lifecycle stage, and they do not share one maturity level.

## Operating Principles

- No inventory, no governance.
- No owner, no deployment.
- No evidence, no claim.
- No verification, no closure.
- No shutdown path, no frontier release.
- No sovereignty, no strategic AI.
- No problem without a path to closure.
- AI may assist. Humans retain authority.

## Evidence Boundary

This portfolio includes a working public reference toolkit, an experimental alpha specification, verified-closure and public-browser-review prereleases, a pre-alpha design, a defensive reference framework, and foundational governance templates.

Repository checks establish bounded technical consistency for the included artifacts. They do not establish operational safety, factual truth of submitted declarations, legal compliance, certification, production authorization, institutional approval, or fitness for every environment.

**Start narrow. Govern one system. Produce one decision-ready outcome. Capture proof. Repeat.**

Repository content is provided under the Apache License 2.0 unless a linked repository states its own license.

<details>
<summary>A note from the founder</summary>

Global AI Governance exists to bring novel solutions, from out of this world, to problems the world needs solved now: AI that is visible, owned, evidenced, and answerable to people. The work is offered openly so any team, lab, or agent can build on it.
</details>
