# Change Policy

Substantive portfolio changes should be bounded, reviewable, recoverable, and evidence-producing.

## Change record

A consequential change should identify:

1. **Need** — why the change is required.
2. **Impact** — repositories, schemas, interfaces, evidence, releases, and public claims affected.
3. **Proof** — tests, validators, builds, or reviews actually performed.
4. **Boundary** — what the evidence does not prove.
5. **Recovery** — how the change can be reverted, superseded, or revalidated.
6. **Disposition** — merge, hold, rework, or renewed authorization.

## Automation boundary

Automation may perform deterministic maintenance and validation. High-impact changes involving security semantics, authority, cryptography, breaking schemas, execution capability, recovery behavior, releases, or public claims require deliberate human authorization even when CI is green.
