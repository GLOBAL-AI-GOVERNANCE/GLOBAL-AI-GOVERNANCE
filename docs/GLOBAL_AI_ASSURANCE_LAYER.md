# Global AI Assurance Layer

**Status:** Design candidate  
**Authority effect:** `NONE`

## Purpose

Interoperability layer, not a new regulator, certifier, or universal passport.

It answers:

> What evidence supports the decision to operate this exact AI system, in this exact configuration, for this exact use, within this exact authority boundary?

## Do not create a second Passport

Agentic authority, evidence binding, validity, expiry, and revocation semantics remain owned by the agentic repository.

The portfolio-level construct is a Global AI Assurance Envelope: a reference-only object that points to native evidence without redefining it.

## Assurance Envelope

The envelope binds:

- exact subject identity;
- deployment context;
- problem references;
- Decision Pack reference when present;
- native artifact references;
- independent-assurance reference when present;
- residual risk;
- current human disposition;
- validity window;
- revalidation triggers;
- material-concern state;
- `reference_only: true`;
- `authority_effect: NONE`.

## Assurance Validity Firewall

Evidence may support a decision. Evidence does not silently become authority. Material new evidence or configuration change can invalidate prior assurance. Revalidation is required before any new disposition.

Native repositories retain ownership of their semantic objects. The layer assembles references only.
