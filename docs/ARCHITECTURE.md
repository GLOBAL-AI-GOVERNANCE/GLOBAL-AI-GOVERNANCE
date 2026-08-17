# Portfolio Architecture

GLOBAL AI GOVERNANCE is a portfolio of bounded repositories that can stand on their own and compose through a shared governance lifecycle.

The profile repository is the **portfolio control plane**. It records repository identity, maturity, lifecycle role, finished outcome, authority boundary, and intended handoffs. It is not a runtime and does not centralize domain semantics that belong in specialist repositories.

## Shared lifecycle

```text
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

Repositories do not all implement every stage and do not share one maturity level.

## Architectural rules

1. Local value first: a cross-repository change must improve or preserve the target repository on its own.
2. Domain ownership remains local: specialist repositories own their schemas, validators, and evidence boundaries.
3. Shared interfaces are explicit: handoffs should use stable identifiers and documented contracts rather than duplicated semantics.
4. Public claims follow evidence: implementation, validation, and release state must precede stronger public claims.
5. Human authority remains explicit for consequential decisions.
6. Compatibility work must not silently broaden execution, authorization, security, or certification claims.

`portfolio.json` is the machine-readable portfolio manifest. `README.md` remains the human-facing entry point.
