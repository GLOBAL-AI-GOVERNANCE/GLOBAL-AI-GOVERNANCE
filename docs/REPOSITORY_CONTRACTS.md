# Repository Contracts

These contracts define how repositories should compose without becoming one monolith.

## Shared invariants

- No inventory, no governance.
- No owner, no deployment.
- No evidence, no claim.
- No verification, no closure.
- No shutdown path, no frontier release.
- AI may assist. Humans retain authority.
- No problem without a path to closure.

## Handoff contract

A repository-to-repository handoff should identify:

- source repository and artifact;
- target repository and expected input;
- stable identifier or reference;
- version or schema expectation;
- evidence or authority boundary;
- failure behavior for unsupported or missing inputs;
- compatibility and supersession rules when semantics change.

A receiving repository should consume a foreign semantic object through a documented adapter or reference. It should not silently redefine the object.

## Minimal reference object (Assurance Envelope)

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

Native semantic objects remain owned by their originating repositories. The envelope assembles references only. Authority effect remains NONE until an authorized institutional decision explicitly changes it.

## Assurance Context Binding reference

`contracts/assurance-context-binding.reference.json` records an immutable portfolio handoff reference to the Assurance Context Binding synthetic fixture in ai-governance-os at commit `fad094618e723acec14a8cdc905d1cfcbdf58813`.

It uses the existing foundation-to-toolkit handoff identifier. It is reference-only with authority_effect NONE. It does not transfer authority, prove authenticity of external systems, or alter the six-edge handoff graph.

## Independence contract

Every repository should remain understandable and testable from its own README, local artifacts, and validation commands. Portfolio integration is additive, not a prerequisite for basic comprehension.
