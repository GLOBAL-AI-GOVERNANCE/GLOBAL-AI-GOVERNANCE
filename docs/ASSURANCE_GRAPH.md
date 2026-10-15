# Portfolio Assurance Graph

The portfolio composes independent repositories through references and handoff contracts.

```text
AI Governance Foundations
→ Global AI Governance Toolkit
→ Agentic AI Governance
→ Governed Systems Administration

Global AI Governance Toolkit
→ Verified Vulnerability Governance
→ AI Cyber Resilience Framework
→ Peace OS: Crisis Room
```

The graph does not imply equal maturity, shared runtime state, or automatic authority.

## Assurance thread

Across repositories, a high-consequence claim can be traced conceptually as:

```text
Need
→ governed inventory / decision context
→ authority reference
→ bounded action or nonexecution decision
→ observation / finding
→ evidence / verification
→ configuration-bound assurance
→ operating disposition
→ human decision / learning
```

Each specialist repository owns its local object semantics. Portfolio handoffs carry references; they do not silently redefine foreign objects.

## Fail-closed interoperability

A receiving repository should reject or hold an unsupported handoff rather than infer:

- authority from a reference;
- control effectiveness from a schema;
- verified closure from ticket status;
- current assurance from superseded evidence;
- permission to execute from an analysis result; or
- operational truth from a simulation.

`contracts/handoffs.json` is the machine-readable portfolio graph used by `tools/validate_integration.py`.

## Federated evidence graph

`contracts/federated-evidence-graph.example.json` is a reference graph. Nodes point at native artifacts. They do not copy those artifacts.

Edges may use only neutral relationships: SUPPORTS, QUALIFIES, CONTRADICTS, SUPERSEDES, DEPENDS_ON, REQUIRES, INVALIDATES, RECOVERS_FROM, TRANSFERS_TO, and REQUALIFIES. The graph has no AUTHORIZES relationship. `authority_effect` remains `NONE`.

A contradiction between current artifacts requires an explicit reconciliation reference. A superseded artifact cannot remain current.

