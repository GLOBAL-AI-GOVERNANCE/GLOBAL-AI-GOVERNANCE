# Global AI Governance

Governance tools and evidence-driven decision support.

Assess an inventory, examine findings, and prepare a reproducible result for human review and decision. Consequential authority stays with accountable people.

**[Try the Toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/)** — run a sample in the browser. No install.

**[Connect tools](https://global-ai-governance.github.io/global-ai-governance-toolkit/connect.html#agents)** — schemas, commands, or the MCP server.

The browser tools run locally in your browser. The MCP server is available for local installation (v0.1.0 release with wheel, sdist, and `SHA256SUMS`) or operator-hosted self-hosting; **Global AI Governance operates no hosted MCP endpoint**. Outputs are non-authorizing (`authority_effect: NONE`).

**In 10 seconds:** list the AI systems and agents you run, see which ones lack an owner, monitoring, a shutdown path, or evidence, and get a Decision Pack an accountable person uses to decide. Free and open source. The browser check needs no install, upload, or login.

**Pick your path**

- **Founder or team running AI agents:** run the [browser Toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/) on the sample, then on your own inventory from the [blank template](https://global-ai-governance.github.io/global-ai-governance-toolkit/ai-system-inventory-template.csv). Use the [Action Levels](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/blob/main/spec/08-action-authority.md) to decide what each agent may do on its own.
- **Chief of Staff or operations lead:** start with the [Action Levels](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/blob/main/spec/08-action-authority.md) and the [agent passport](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance#five-minute-validation): which agent it covers, who issued it, its conditions, and when it expires.
- **Engineer adding checks to an agent:** run the MCP server with one command (see **Install at a glance** below) and call `check_inventory` with `use_sample=true`.
- **Compliance or risk reviewer:** run **Run example with gaps** in the [browser Toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/) and download the Decision Pack to see the findings and the decision record a named person completes.

Every path is self-serve and non-authorizing: the tools report; people decide.

## Start Here

**Install at a glance**

| Surface | Install or run | Version | Maturity | Test status |
|---|---|---|---|---|
| Browser | [Open the Toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/) | current main (pinned release v2.6.0) | working public reference toolkit | TESTED (hosted CI) |
| CLI | `pip install https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/download/v2.6.0/global_ai_governance_toolkit-2.6.0-py3-none-any.whl` | v2.6.0 | working public reference toolkit | TESTED (release wheel, clean environment) |
| MCP server | `uvx --from git+https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp@v0.1.0 gag-mcp` | v0.1.0 | preview · no hosted endpoint | TESTED (MCP Python SDK client, clean environment) |
| GitHub Action | `uses: GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit@f454bf921b774f17982e70f28ce01a224d3c6410` | v2.6.0 (full commit SHA of the release tag) | released | TESTED (hosted CI self-test) |
| Passport validator | `pip install git+https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance.git` | main, unreleased (after v0.1.0-alpha.2) | experimental public alpha | TESTED (hosted CI, clean environment) |
| Docker (MCP server) | `docker build -f deploy/Dockerfile -t gag-mcp .` (in an `ai-governance-mcp` clone) | v0.1.0 | build locally from Dockerfile · no image published | untested |

TESTED means run by this project's own CI or test runs; it is not independent verification. Every surface is non-authorizing (`authority_effect: NONE`). Machine-readable copy: `install_surfaces` in [portfolio.json](portfolio.json).

### USE

1. Open the [Toolkit](https://global-ai-governance.github.io/global-ai-governance-toolkit/) and select **Run sample** (a synthetic clean inventory) or **Run example with gaps** (a synthetic inventory that shows governance findings). No login or upload is required for the browser workflow.
2. Review the findings and download the AI Governance Decision Pack. Neither example is a real security assessment. The clean sample may pass its bounded checks; a passing result is not a deployment decision and does not authorize deployment.
3. The hosted Toolkit reflects current `main`. For a pinned implementation, use the [v2.6.0 release](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/releases/tag/v2.6.0) and its [quick start](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.6.0#quick-start). v2.5.0 remains the organizational maturity capability release. v2.5.1 is a public-reference integrity patch.

Other browser experiences: [Containment Ledger](https://global-ai-governance.github.io/containment-ledger/) for security-boundary review; [Peace OS: Crisis Room](https://global-ai-governance.github.io/peace-os/) for a fictional crisis-verification exercise.

### INTEGRATE

- [AI Governance MCP](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp) exposes three read-only tools: `check_inventory`, `build_decision_pack`, and `validate_passport`. Every result carries `authority_effect: NONE` and leaves the decision with a human.
- [Install and run locally](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#install-and-run-local) (stdio, no network or token) · [Sample call](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#sample-call) · [Client configuration](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#client-configuration-copy-paste) · [Known limits](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#known-limits)
- The `gag-mcp` command, `gag_mcp` Python package, and `GAG_MCP_*` variables are unchanged since the repository rename.
- [Machine interface](https://global-ai-governance.github.io/global-ai-governance-toolkit/machine-interface.json) · [Agent discovery](https://global-ai-governance.github.io/global-ai-governance-toolkit/llms.txt) · [Toolkit v2.6.0 contracts](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit/tree/v2.6.0/automation) · [Agent authority and passport schemas (v0.1.0-alpha.2)](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance/tree/v0.1.0-alpha.2/schemas)
- [Repository handoff contracts](docs/REPOSITORY_CONTRACTS.md) · [Global AI Assurance Envelope](docs/GLOBAL_AI_ASSURANCE_ENVELOPE.md) · [Portfolio schema](schemas/portfolio.schema.json)

Remote use: on any non-loopback bind the server refuses to start unless `GAG_MCP_ALLOWED_HOSTS` is set to the client-facing hostname and `GAG_MCP_BEARER_TOKEN` is a random secret of at least 32 characters. Serve it only over HTTPS; requests send `Authorization: Bearer TOKEN`. OAuth is not implemented. **Provider connections (Anthropic Claude, OpenAI, xAI Grok): NOT VERIFIED.** Protocol compatibility is tested with the official MCP Python SDK client and the MCP Inspector. ChatGPT on the web is not supported, because it cannot send a static bearer token. [Auth](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#auth) · [Self-hosting](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp#self-hosting-needed-for-every-remote-platform-global-ai-governance-operates-no-endpoint).

Published tags remain controlling for released interfaces; newer merged code is not automatically a released contract. Integrations must preserve the source system's authority and evidence boundaries.

Use of these materials does not imply endorsement or certification. Do not include confidential, personal, regulated, or protected information in public repository surfaces.

<a id="product-map"></a>

## Portfolio

Nine product and reference repositories plus two public infrastructure repositories. Labels below are the current public maturity and outcome from the [machine-readable portfolio](portfolio.json), which also carries lifecycle roles and source-of-truth boundaries.

- **[Global AI Governance Toolkit](https://github.com/GLOBAL-AI-GOVERNANCE/global-ai-governance-toolkit)** · [Open app](https://global-ai-governance.github.io/global-ai-governance-toolkit/) — v2.6.0 · working public reference toolkit. Reproducible Decision Pack, bounded sovereignty assessment, assurance/accountability profiles, and organizational AI maturity evidence assessment.
- **[AI Governance Model Context Protocol Server (AI Governance MCP)](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-mcp)** — v0.1.0 preview · no hosted endpoint. Read-only Model Context Protocol (MCP) tools wrapping the toolkit and passport validator; authority_effect NONE.
- **[Agentic AI Governance](https://github.com/GLOBAL-AI-GOVERNANCE/agentic-ai-governance)** — v0.1.0-alpha.2 · experimental public alpha. Machine-readable authority, evidence, passport, validation, expiry, and revocation artifacts.
- **[Verified Vulnerability Governance](https://github.com/GLOBAL-AI-GOVERNANCE/verified-vulnerability-governance)** — v0.1.3 · verified-closure pre-release. Evidence-linked vulnerability ownership, remediation, retesting, and closure.
- **[AI Cyber Resilience Framework](https://github.com/GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework)** — v0.1.1 · public defensive reference. Boundary assessment, evidence cards, and architecture-hardening backlog.
- **[Containment Ledger](https://github.com/GLOBAL-AI-GOVERNANCE/containment-ledger)** · [Open app](https://global-ai-governance.github.io/containment-ledger/) — Local-only browser instrument for domain/path/evidence marking and human disposition. Independent structural review instrument; shares vocabulary with the AI Cyber Resilience Framework; no code, data, or release dependency; authority_effect NONE.
- **[Peace OS: Crisis Room](https://github.com/GLOBAL-AI-GOVERNANCE/peace-os)** · [Open app](https://global-ai-governance.github.io/peace-os/) — v0.3.0-rc2 · published public browser review candidate · stable, human-validation, Godot, and Windows gates open. Fictional crisis-verification simulation and after-action review.
- **[Governed Systems Administration](https://github.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration)** — Pre-alpha · preimplementation · independent semantic review required · no execution capability. Proposed human-governed administration request, review, validation, and evidence contracts.
- **[AI Governance Foundations](https://github.com/GLOBAL-AI-GOVERNANCE/ai-governance-os)** — v1.1 · foundational governance model and template set. Inventory, ownership, risk, control, monitoring, and reporting foundations.
- **[Repository Governance Defaults](https://github.com/GLOBAL-AI-GOVERNANCE/.github)** — Account-level default repository governance files. Consistent security-boundary, claims-integrity, release-governance, and change-control defaults.
- **[Global AI Governance Profile](https://github.com/GLOBAL-AI-GOVERNANCE/GLOBAL-AI-GOVERNANCE)** — Public Start Here profile for the open-source portfolio. Portfolio truth registry, federated evidence graph, and cross-estate reproduction.

[Repository maturity definitions](docs/MATURITY_MODEL.md) explain what these labels do and do not establish. AI Governance Foundations is the original foundation; Containment Ledger is independent of the AI Cyber Resilience Framework.

## Development Baseline

Published release identities remain controlling. Merged development candidates **do not silently become release claims**. The [portfolio manifest](portfolio.json) records these merged, unreleased candidates; none is a new published release:

- AI Cyber Resilience Framework: **v0.2.0 Continuous Assurance Thread** (published release remains v0.1.1).
- Peace OS: Crisis Room: **Post-RC2 Portfolio Operating Disposition Reference** (published release remains v0.3.0-rc2).
- Agentic AI Governance: OPA Enforcement Bridge and synthetic Agent Incident Readiness lifecycle reference implementations (published release remains v0.1.0-alpha.2).
- Verified Vulnerability Governance: synthetic crypto-migration closure reference (published release remains v0.1.3).

## Shared Governance Lifecycle

Assess → Govern → Authorize → Enforce → Observe → Verify → Contain → Recover → Measure → Learn → Reassess.

Repositories **do not all implement every lifecycle stage** and **do not share one maturity level**. Follow each repository's published maturity and operating boundaries.

## Operating Principles

**Evidence before claims. Accountable ownership before decisions. Verification before closure.** AI assists; humans retain authority.

## Evidence Boundary

The tools produce reference evidence and decision support. Automated checks **do not establish operational safety**, independent real-world assurance, **legal compliance**, **certification**, or **production authorization**. A passing evaluation is not permission to deploy, accept risk, or take consequential action.

For operators and reviewers: [Integrated remediation reference](docs/GOVERNED_VULNERABILITY_REMEDIATION_REFERENCE.md) · [NIST AI RMF mapping](docs/NIST_AI_RMF_1_0_MAPPING.md) · [Source policy](docs/SOURCE_POLICY.md) · [Change policy](docs/CHANGE_POLICY.md) · [Security policy](https://github.com/GLOBAL-AI-GOVERNANCE/.github/blob/main/SECURITY.md).

This profile repository is licensed under the Apache License 2.0; each linked repository states its own license and release terms.
