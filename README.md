# Global AI Governance

**Govern AI before it acts.**

Open-source governance for agent fleets, AI agencies, and AI-run companies, wherever they operate. List the AI systems and agents you run. See which ones lack an owner, monitoring, a shutdown path, or evidence. Get a Decision Pack ready for human review and decision by the person accountable, so trust is earned before autonomy is extended. Framework-neutral and jurisdiction-neutral, with [crosswalks](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/FRONTIER_AND_REGULATORY_CROSSWALK.md) to NIST AI RMF 1.0, ISO/IEC 42001, the EU AI Act, and frontier safety frameworks. The browser check needs no install, upload, or login.

**[Try the Toolkit](https://ai-governance.solutions/)**: run a sample in your browser, nothing to install.

**[Connect your agent](https://ai-governance.solutions/connect.html#agents)**: schemas, commands, or the MCP server any MCP-capable agent can call.

**[Start where you are](https://ai-governance.solutions/start.html)**: open starting points for people using AI apps such as ChatGPT, Claude, Grok, Gemini, or Copilot, for builders of AI organizations and agent fleets, for frontier labs, and for anyone else. You do not need an account, and you can begin at any step. Agents read the same guide at [JOURNEYS.md](https://ai-governance.solutions/JOURNEYS.md).

**Suite path:** [Peace OS](https://github.com/GLOBAL-AI-GOVERNANCE/peace-os) → [Toolkit](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit) → [AI Governance MCP](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) → [Agentic AI Governance](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance) → [Verified Vulnerability Governance](https://github.com/GLOBAL-AI-GOVERNANCE/verified-vulnerability-governance) → [Containment Ledger](https://github.com/GLOBAL-AI-GOVERNANCE/containment-ledger) → [AI Cyber Resilience Framework](https://github.com/GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework) → [AI Governance Foundations](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-os) → [Governed Systems Administration](https://github.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration). This is a suggested reading order, not a required sequence. Each README links its neighbours, and `tools/check_suite_path.py` keeps names, versions, and links in sync with [`journey.json`](journey.json).

No AI system moves faster than ownership, evidence, authority, and control. The tools report; people decide. Every output is non-authorizing (`authority_effect: NONE`). The browser tools run locally. The MCP server installs locally (v0.5.1 release with wheel, sdist, CycloneDX SBOM, `SHA256SUMS`, and build-provenance attestation) or can be self-hosted by an operator; **Global AI Governance operates no hosted MCP endpoint**.

**A few common starting points**

- **Founder or team running AI agents:** run the [browser Toolkit](https://ai-governance.solutions/) on the sample, then on your own inventory from the [blank template](https://ai-governance.solutions/ai-system-inventory-template.csv). Use the [Action Levels](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/blob/main/spec/08-action-authority.md) to decide what each agent may do on its own.
- **Team running a lead agent (orchestrator) that coordinates a fleet:** describe the lead agent's sub-agents and delegations in its [agent passport](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance#five-minute-validation) action graph. v0.1.0-alpha.5 can issue that fleet from an operator policy (`issue-passports`) and run the reference lead agent; the [browser scenario](https://ai-governance.solutions/lead-agent/) does not sign passports. Any declared delegation sets a minimum of Level 3 under the [Action Levels](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/blob/main/spec/08-action-authority.md), so the lead agent is assessed for everything it can reach through other agents. The passport records who issued it, its conditions, and when it expires.
- **Engineer adding checks to an agent:** run the MCP server with one command (see **Install at a glance** below) and call `check_inventory` with `use_sample=true`.
- **Compliance or risk reviewer:** run **Run example with gaps** in the [browser Toolkit](https://ai-governance.solutions/) and download the Decision Pack to see the findings and the decision record a named person completes.

Every path is self-serve and non-authorizing: the tools report; people decide.

## Start Here

**Install at a glance**

<!-- gaig:install-surfaces -->
| Surface | Install or run | Version | Maturity | Test status |
|---|---|---|---|---|
| Browser | [Open the Toolkit](https://ai-governance.solutions/) | current main (pinned release v2.8.2) | stable | TESTED (hosted CI) |
| CLI | `pip install https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/download/v2.8.2/global_ai_governance-2.8.2-py3-none-any.whl` | v2.8.2 | stable | TESTED (release wheel, clean environment) |
| MCP server | `uvx --from git+https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp@v0.5.1 gaig-mcp` | v0.5.1 | released · no hosted endpoint | TESTED (MCP Python SDK client, clean environment) |
| GitHub Action | `uses: GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit@516641b72886762c2ced0f5bc3b2d8205e3d548f` | v2.8.2 (full commit SHA of the release tag) | released | TESTED (hosted CI self-test) |
| Passport validator | `pip install git+https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance.git@v0.1.0-alpha.6` | v0.1.0-alpha.6 | available | TESTED (hosted CI, clean environment) |
| Docker (MCP server) | `docker build -f deploy/Dockerfile -t gaig-mcp .` (in an `ai-governance-mcp` clone) | v0.5.1 | build locally from Dockerfile · no image published | untested |
<!-- /gaig:install-surfaces -->

TESTED means run by this project's own CI or test runs; it is not independent verification. Every surface is non-authorizing (`authority_effect: NONE`). Machine-readable copy: `install_surfaces` in [portfolio.json](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/portfolio.json).

### USE

1. Open the [Toolkit](https://ai-governance.solutions/) and select **Run sample** (a synthetic clean inventory) or **Run example with gaps** (a synthetic inventory that shows governance findings). No login or upload is required for the browser workflow.
2. Review the findings and download the AI Governance Decision Pack. Neither example is a real security assessment. The clean sample may pass its bounded checks; a passing result is not a deployment decision and does not authorize deployment.
3. The hosted Toolkit reflects current `main`. For a pinned implementation, use the [v2.8.1 release](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/tag/v2.8.2) and its [quick start](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.8.2#quick-start). v2.5.0 remains the organizational maturity capability release. v2.5.1 is a public-reference integrity patch.

Other browser experiences: [Containment Ledger](https://global-ai-governance.github.io/containment-ledger/) for security-boundary review; [Peace OS: Crisis Room](https://global-ai-governance.github.io/peace-os/), a crisis-room simulator with synthetic scenarios for rehearsing evidence review, civilian protection, and decisions that stay with people.

### INTEGRATE

- [AI Governance MCP](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) exposes three read-only tools: `check_inventory`, `build_decision_pack`, and `validate_passport`. Every result carries `authority_effect: NONE` and leaves the decision with a human.
- [Install and run locally](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#install-and-run-local) (stdio, no network or token) · [Sample call](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#sample-call) · [Client configuration](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#client-configuration-copy-paste) · [Known limits](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#known-limits)
- The primary command is `gaig-mcp`, with the `gaig_mcp` Python package and `GAIG_MCP_*` variables.
- **AI agents set up from one guide:** [AGENT_SETUP.md](https://ai-governance.solutions/AGENT_SETUP.md) gives every command, the result to expect, MCP client configs, and a done check, with no account, API key, or human step.
- [Machine interface](https://ai-governance.solutions/machine-interface.json) · [Agent discovery](https://ai-governance.solutions/llms.txt) · [Toolkit v2.8.2 contracts](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.8.2/automation) · [Agent authority and passport schemas (v0.1.0-alpha.2)](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/tree/v0.1.0-alpha.2/schemas)
- [Repository handoff contracts](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/REPOSITORY_CONTRACTS.md) · [Global AI Assurance Envelope](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md) · [Portfolio schema](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/schemas/portfolio.schema.json)

Remote use: on any non-loopback bind the server refuses to start unless `GAIG_MCP_ALLOWED_HOSTS` is set to the client-facing hostname and `GAIG_MCP_BEARER_TOKEN` is a random secret of at least 32 characters. Serve it only over HTTPS; requests send `Authorization: Bearer TOKEN`. OAuth is not implemented. **Provider connections (Anthropic Claude, OpenAI, xAI Grok): NOT VERIFIED.** Protocol compatibility is tested with the official MCP Python SDK client and the MCP Inspector. ChatGPT on the web is not supported, because it cannot send a static bearer token. [Auth](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#auth) · [Self-hosting](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#self-hosting-needed-for-every-remote-platform-global-ai-governance-operates-no-endpoint).

Published tags remain controlling for released interfaces; newer merged code is not automatically a released contract. Integrations must preserve the source system's authority and evidence boundaries.

Use of these materials does not imply endorsement or certification. Do not include confidential, personal, regulated, or protected information in public repository surfaces.

<a id="product-map"></a>

## Portfolio

Nine product and reference repositories plus two public infrastructure repositories. Labels below are the current public maturity and outcome from the [machine-readable portfolio](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/portfolio.json), which also carries lifecycle roles and source-of-truth boundaries.

<!-- gaig:portfolio-versions -->
- **[Global AI Governance Toolkit](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit)** · [Open app](https://ai-governance.solutions/) — v2.8.2 · stable. Reproducible Decision Pack, bounded sovereignty assessment, assurance/accountability profiles, and organizational AI maturity evidence assessment.
- **[AI Governance Model Context Protocol Server (AI Governance MCP)](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp)** — v0.5.1 · released · no hosted endpoint. Read-only Model Context Protocol (MCP) tools wrapping the toolkit and passport validator; authority_effect NONE.
- **[Agentic AI Governance](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance)** — v0.1.0-alpha.6 · available. Machine-readable authority, evidence, passport, validation, expiry, and revocation artifacts.
- **[Verified Vulnerability Governance](https://github.com/GLOBAL-AI-GOVERNANCE/verified-vulnerability-governance)** — v0.4.0 · released. Evidence-linked vulnerability ownership, remediation, retesting, and closure.
- **[AI Cyber Resilience Framework](https://github.com/GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework)** — v0.2.0 · released. Boundary assessment, evidence cards, and architecture-hardening backlog.
- **[Containment Ledger](https://github.com/GLOBAL-AI-GOVERNANCE/containment-ledger)** · [Open app](https://global-ai-governance.github.io/containment-ledger/) — v1.0.0 · released · local browser instrument for domain, path, and evidence marking and human disposition. Independent structural review instrument; shares vocabulary with the AI Cyber Resilience Framework; no code, data, or release dependency; authority_effect NONE.
- **[Peace OS: Crisis Room](https://github.com/GLOBAL-AI-GOVERNANCE/peace-os)** · [Open app](https://global-ai-governance.github.io/peace-os/) — v0.3.0 · released for browser use. Crisis-verification simulator with synthetic scenarios and an after-action review.
- **[Governed Systems Administration](https://github.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration)** — specification · no execution. Proposed human-governed administration request, review, validation, and evidence contracts.
- **[AI Governance Foundations](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-os)** — v1.1.1 · stable. Inventory, ownership, risk, control, monitoring, and reporting foundations.
- **[Repository Governance Defaults](https://github.com/GLOBAL-AI-GOVERNANCE/.github)** — Account-level default repository governance files. Consistent security-boundary, claims-integrity, release-governance, and change-control defaults.
- **[Global AI Governance Profile](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE)** — Public Start Here profile for the open-source portfolio. Portfolio truth registry, federated evidence graph, and cross-estate reproduction.
<!-- /gaig:portfolio-versions -->

[Repository maturity definitions](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/MATURITY_MODEL.md) explain what these labels do and do not establish. AI Governance Foundations is the original foundation; Containment Ledger is independent of the AI Cyber Resilience Framework.

## Development Baseline

Published release identities remain controlling. There are no merged-unreleased development candidates. The [portfolio manifest](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/portfolio.json) records repository versions and claim limits. No merged-unreleased development candidates are currently tracked.

- AI Cyber Resilience Framework: **v0.2.0** released (`authority_effect: NONE`).
- Peace OS: Crisis Room: **v0.3.0** released for browser use; Godot, Windows, certification, and operational claims remain HOLD.

## Shared Governance Lifecycle

Assess → Govern → Authorize → Enforce → Observe → Verify → Contain → Recover → Measure → Learn → Reassess.

Repositories **do not all implement every lifecycle stage** and **do not share one maturity level**. Follow each repository's published maturity and operating boundaries.

## Operating Principles

**Evidence before claims. Accountable ownership before decisions. Verification before closure.** AI assists; humans retain authority.

## Evidence Boundary

The tools produce reference evidence and decision support. Automated checks **do not establish operational safety**, independent real-world assurance, **legal compliance**, **certification**, or **production authorization**. A passing evaluation is not permission to deploy, accept risk, or take consequential action.

For operators and reviewers: [Integrated remediation reference](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/GOVERNED_VULNERABILITY_REMEDIATION_REFERENCE.md) · [NIST AI RMF mapping](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/NIST_AI_RMF_1_0_MAPPING.md) · [Frontier safety, EU AI Act, and ISO/IEC 42001 crosswalk](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/FRONTIER_AND_REGULATORY_CROSSWALK.md) · [Source policy](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/SOURCE_POLICY.md) · [Change policy](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE/blob/main/docs/CHANGE_POLICY.md) · [Security policy](https://github.com/GLOBAL-AI-GOVERNANCE/.github/blob/main/SECURITY.md).

This profile repository is licensed under the Apache License 2.0; each linked repository states its own license and release terms.
