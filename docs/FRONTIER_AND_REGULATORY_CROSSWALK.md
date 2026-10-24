# Frontier Safety and Regulatory Crosswalk

**Mapping date:** 2026-10-24

This is an informative engineering crosswalk for AI safety, governance, and policy teams. It shows where the portfolio's artifacts can supply **deployment-side evidence** (inventories, owners, authority limits, human decision records, incident and remediation records) alongside the frameworks that frontier developers and enterprises deploying agents already use. The NIST AI RMF 1.0 crosswalk is maintained separately in [NIST_AI_RMF_1_0_MAPPING.md](NIST_AI_RMF_1_0_MAPPING.md).

**What the portfolio does not do:** it does not evaluate model capabilities (for example CBRN, cyber-offense, autonomy, or manipulation evaluations), test safeguard effectiveness, secure model weights, or decide whether a threshold has been crossed. Those remain with the developer's own evaluations, safeguards, and governance bodies.

## Frontier safety frameworks

Each framework below links capability thresholds to required safeguards and to an accountable internal decision before development or deployment continues. The portfolio maps only to the record-keeping and decision-support parts of that loop.

| Framework element | Portfolio artifacts | Boundary |
|---|---|---|
| Know which models, systems, and agents are in scope | Toolkit system inventory with owner, monitoring, shutdown-path, and evidence findings; AI Governance Foundations registers | Inventory completeness depends on what the operator declares. |
| Limit what deployed agents may do | Agentic AI Governance Action Levels, action graph (including `SUBAGENT` nodes and `DELEGATES` edges), and agent passports with conditions, expiry, and revocation | Declared authority is validated; runtime behavior is not observed or enforced. |
| Record an accountable go / no-go decision with its evidence | Toolkit Decision Pack with a human decision record; `authority_effect: NONE` on every output | The record supports a decision; it is not the decision and grants no permission. |
| Incident readiness and response records | Agentic AI Governance synthetic Agent Incident Readiness lifecycle reference (current main, unreleased) | Synthetic reference only; not an operational incident process. |
| Security boundaries, containment, and recovery | AI Cyber Resilience Framework boundary assessment and evidence cards; Containment Ledger boundary review; Verified Vulnerability Governance remediation and verified closure | Reference and review instruments; they do not establish a security level. |

## EU AI Act

| Provision (Regulation (EU) 2024/1689) | Portfolio artifacts | Boundary |
|---|---|---|
| Art. 53(1)(a)-(b): GPAI technical documentation and information for downstream providers | Toolkit inventory and Decision Pack as structured, exportable records of systems, owners, and evidence | Does not produce the documentation the Act requires of a GPAI provider. |
| Art. 55(1)(a): model evaluation and adversarial testing (systemic-risk GPAI) | None | Out of scope: the portfolio performs no model evaluation. |
| Art. 55(1)(b): assess and mitigate systemic risks | Toolkit findings and human decision records; Agentic authority limits for agentic deployments | Supports recording risk decisions; does not assess systemic risk. |
| Art. 55(1)(c): track, document, and report serious incidents | Agent Incident Readiness reference (synthetic) | No reporting channel to the AI Office or any authority. |
| Art. 55(1)(d): cybersecurity protection | Verified Vulnerability Governance closure records; AI Cyber Resilience Framework; Containment Ledger | Does not protect a model or its infrastructure. |
| Arts. 14 and 26: human oversight and deployer use of high-risk AI systems | Named accountable owner and human decision record (Toolkit); passport conditions and expiry (Agentic) | Does not determine whether a system is high-risk or meets these Articles. |

The General-Purpose AI Code of Practice is a voluntary tool that the Commission and the AI Board have assessed as adequate for demonstrating GPAI obligations; the portfolio is not a signatory and is not an alternative adequate means.

## ISO/IEC 42001:2023

| Clause or Annex A area | Portfolio artifacts | Boundary |
|---|---|---|
| Clause 6.1: actions to address risks and opportunities | Toolkit findings, risk tiers, and Decision Pack | Organization-level risk criteria remain the operator's. |
| Clause 8: operation | Agentic passports, Action Levels, and expiry/revocation for agent deployments | Declared controls only. |
| Clause 9: performance evaluation | Toolkit validation reports; organizational AI maturity evidence assessment | Not an internal audit or management review. |
| A.3.2 AI roles and responsibilities | Named owner per system (Toolkit); passport issuer (Agentic) | Records roles; does not assign them. |
| A.5 Assessing impacts of AI systems | Toolkit impact fields (people, money, security, rights, safety), findings, and human decision record | Not a complete impact assessment. |
| A.6.2 AI system life cycle (verification, deployment, operation and monitoring, event logs) | Toolkit monitoring and shutdown-path findings; Verified Vulnerability Governance retest and closure | No runtime event logging is provided. |
| A.10 Third-party and customer relationships | Toolkit inventory `Vendor / Internal` field per system | Records the source; does not assess suppliers. |

## Non-claim

This crosswalk **does not establish compliance, conformity, certification, legal sufficiency, adoption, endorsement, or partnership** with respect to any framework, regulation, standard, or organization named here. Framework owners may revise their documents; re-check the sources below before relying on any row.

## Authoritative sources

- Regulation (EU) 2024/1689 (Artificial Intelligence Act): https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- European Commission, The General-Purpose AI Code of Practice (published July 10, 2025): https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai
- AI Act Service Desk, obligations of GPAI model providers: https://ai-act-service-desk.ec.europa.eu/en/ai-act/faq/what-legal-obligations-do-providers-general-purpose-ai-models-face-under-ai-act-2-august
- ISO/IEC 42001:2023, Information technology - Artificial intelligence - Management system: https://www.iso.org/standard/42001
- Anthropic, Responsible Scaling Policy (Version 3.4, effective July 8, 2026): https://www.anthropic.com/responsible-scaling-policy
- OpenAI, Preparedness Framework (Version 2, last updated April 15, 2025): https://openai.com/index/updating-our-preparedness-framework/
- Google DeepMind, Frontier Safety Framework (Version 3.1, April 17, 2026): https://deepmind.google/blog/strengthening-our-frontier-safety-framework/
