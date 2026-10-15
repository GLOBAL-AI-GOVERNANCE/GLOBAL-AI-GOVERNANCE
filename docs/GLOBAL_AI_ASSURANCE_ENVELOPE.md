# Global AI Assurance Envelope

Reference-only interoperability object. It points to native portfolio artifacts without redefining them.

**authority_effect: NONE**

Evidence may support a decision. Evidence does not silently become authority.

## Structure

```text
Subject
  system_id, version, configuration_digest, deployment_context, jurisdiction
Governance
  applicable requirements, risk class, Decision Pack reference
Authority evidence
  Agent Trust Passport (if applicable)
Security / resilience evidence
  VVD closure evidence, ACRF Continuous Assurance Thread
Action evidence
  GSA review artifacts (if applicable)
Independent evaluation
  evaluator, scope, method, competence, conflicts, findings, limitations
Residual risk
Human decision authority
Validity / expiry / revalidation triggers
```

## Minimal reference contract

```json
{
  "source_repository": "...",
  "artifact_type": "...",
  "artifact_id": "...",
  "schema_version": "...",
  "subject_id": "...",
  "artifact_digest": "sha256:...",
  "generated_at": "...",
  "authority_effect": "NONE"
}
```

Native objects remain owned by their repositories. The envelope assembles references only.

## Decision posture (Decision Pack level only)

- PASS — evidence supports proceeding within stated constraints
- WAIT — evidence insufficient, stale, contradictory, or requires remediation
- SAFE STOP — known risk, lack of authority, failed validation, or critical uncertainty prevents proceeding

Underlying native dispositions are preserved.
