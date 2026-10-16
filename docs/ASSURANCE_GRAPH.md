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

`contracts/federated-evidence-graph.example.json` is a reference graph. Nodes point at native artifacts by repository, 40-character source commit, and digest. They do not copy those artifacts. JSON Schema defines node and edge structure. `tools/validate_evidence_graph.py` enforces binding, supersession, and contradiction rules. Schema validity alone does not establish a relationship.

Edges may use only neutral relationships: SUPPORTS, QUALIFIES, CONTRADICTS, SUPERSEDES, DEPENDS_ON, REQUIRES, INVALIDATES, RECOVERS_FROM, TRANSFERS_TO, and REQUALIFIES. The graph has no AUTHORIZES relationship. `authority_effect` remains `NONE`.

Experimental assurance delta uses one declared direction table. It does not infer direction from relationship names at runtime.

| Relationship | Direction | Impact |
|---|---|---|
| DEPENDS_ON | `from` depends on `to` | A change to `to` places `from` in the impact set |
| REQUIRES | `from` requires `to` | A change to `to` places `from` in the impact set |
| INVALIDATES | `from` invalidates `to` | A change to `from` places `to` in the impact set |
| REQUALIFIES | `from` requalifies `to` | A change to `from` places `to` in the impact set |

SUPPORTS, QUALIFIES, CONTRADICTS, SUPERSEDES, RECOVERS_FROM, and TRANSFERS_TO are known and do not propagate impact. An unknown relationship requires conservative review. The output is an impact set only. It does not authorize, complete requalification, declare evidence invalid, or claim causal truth beyond the declared graph.

A contradiction between current artifacts requires an explicit reconciliation reference. A superseded artifact cannot remain current.

## Federated mission bindings

A golden-thread subject binding relates a native subject and configuration to the synthetic mission thread without changing the native object.

`SAME_SUBJECT` means the native and thread identifiers are identical. `COMPONENT_OF` is an explicit synthetic component relationship. `SUPPORTING_EVIDENCE_FOR` is an explicit synthetic evidence relationship. None of these grants authority or establishes external authenticity. Clean-environment reproduction verifies the declared binding; it does not verify a real-world relationship.
