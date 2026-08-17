# Repository Contracts

These contracts define how repositories should compose without becoming one monolith.

## Shared invariants

- No inventory, no governance.
- No owner, no deployment.
- No evidence, no claim.
- No verification, no closure.
- No shutdown path, no frontier release.
- AI may assist. Humans retain authority.

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

## Independence contract

Every repository should remain understandable and testable from its own README, local artifacts, and validation commands. Portfolio integration is additive, not a prerequisite for basic comprehension.
