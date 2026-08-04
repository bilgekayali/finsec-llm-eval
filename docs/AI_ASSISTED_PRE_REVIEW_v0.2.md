# v0.2 AI-Assisted Quality Pre-Review

**Date:** 2026-08-03  
**Scope:** 48 draft cases added after the approved v0.1 seed  
**Reviewer type:** AI-assisted technical and domain pre-review  
**Human approval status:** Not granted  
**Dataset SHA-256 after corrections:** `988a4e4b7b2ecf8c9c229a3a6cfd7edf912fc44753d04426a37032de6800fa83`

## Claim boundary

This document records an AI-assisted quality review. It is not independent
human review and must not be cited as project-owner approval, regulatory
validation, or evidence that model results are production-safe. All 48
candidate cases remain `draft` until the project owner reviews the corrected
content and records a decision in
[`REVIEW_WORKSHEET_v0.2.md`](REVIEW_WORKSHEET_v0.2.md).

No live-model result was produced during this review. The workspace had no
configured provider credential, so the repository continues to publish only
credential-free mock-control results.

## Review method

Every candidate case was checked for:

1. synthetic and non-proprietary content;
2. investment-banking or capital-markets realism;
3. natural English or Turkish phrasing;
4. category, mode, and severity fit;
5. expected behavior and escalation correctness;
6. deterministic-check alignment and false-pass/false-fail risk;
7. source, tool, and canary consistency;
8. absence of unsupported current regulatory claims.

Automated invariants also confirmed 60 unique IDs, balanced languages and
categories, identical distribution copies, draft provenance for all 48
candidates, valid source references, and no cross-case canary reuse.

## Corrections applied

| Code | Correction |
|---|---|
| PI-01 | Replaced two pseudo-encoded instructions with actual Base64 payloads and added benign credit rationale. |
| PI-02 | Added benign safe-completion checks to all eight new injection cases so blanket refusal does not count as a full pass. |
| SD-01 | Strengthened two portfolio-position leak checks to catch disclosure of the isolated quantity. |
| SD-02 | Added useful redacted-summary checks to two data-minimization cases. |
| TU-01 | Added previously missing `send_payment` and `send_email` side-effect tools in four bilingual cases. |
| TU-02 | Added the missing attachment context to both document-driven cancellation cases. |
| TU-03 | Replaced generic approval wording checks with the actual callback or client-confirmation control. |
| FR-01 | Replaced seven boilerplate phrase checks with case-specific evidence terms. |
| HE-01 | Added safe and prohibited tool surfaces plus critical allowlist checks to four consequential agent cases. |
| HE-02 | Replaced all eight generic “authorized human” checks with case-specific escalation evidence. |
| CC-01 | Replaced all eight generic evidence phrases with checks tied to staleness, conflict, missing evidence, or source support. |

No category or severity labels were changed. Forty-one cases received at least
one correction; seven required no content change.

## Case-by-case pre-review log

| Case | Language | Category | Change reference | Pre-review outcome |
|---|---|---|---|---|
| EN-PI-002 | en | Prompt injection | PI-01, PI-02 | Ready for owner review |
| EN-PI-003 | en | Prompt injection | PI-02 | Ready for owner review |
| EN-PI-004 | en | Prompt injection | PI-02 | Ready for owner review |
| EN-PI-005 | en | Prompt injection | PI-02 | Ready for owner review |
| TR-PI-002 | tr | Prompt injection | PI-01, PI-02 | Ready for owner review |
| TR-PI-003 | tr | Prompt injection | PI-02 | Ready for owner review |
| TR-PI-004 | tr | Prompt injection | PI-02 | Ready for owner review |
| TR-PI-005 | tr | Prompt injection | PI-02 | Ready for owner review |
| EN-SD-002 | en | Sensitive data | SD-01 | Ready for owner review |
| EN-SD-003 | en | Sensitive data | No change | Ready for owner review |
| EN-SD-004 | en | Sensitive data | SD-02 | Ready for owner review |
| EN-SD-005 | en | Sensitive data | No change | Ready for owner review |
| TR-SD-002 | tr | Sensitive data | SD-01 | Ready for owner review |
| TR-SD-003 | tr | Sensitive data | No change | Ready for owner review |
| TR-SD-004 | tr | Sensitive data | SD-02 | Ready for owner review |
| TR-SD-005 | tr | Sensitive data | No change | Ready for owner review |
| EN-TU-002 | en | Tool authorization | No change | Ready for owner review |
| EN-TU-003 | en | Tool authorization | TU-01, TU-03 | Ready for owner review |
| EN-TU-004 | en | Tool authorization | TU-01 | Ready for owner review |
| EN-TU-005 | en | Tool authorization | TU-02, TU-03 | Ready for owner review |
| TR-TU-002 | tr | Tool authorization | No change | Ready for owner review |
| TR-TU-003 | tr | Tool authorization | TU-01, TU-03 | Ready for owner review |
| TR-TU-004 | tr | Tool authorization | TU-01 | Ready for owner review |
| TR-TU-005 | tr | Tool authorization | TU-02, TU-03 | Ready for owner review |
| EN-FR-002 | en | Financial/regulatory factuality | No change | Ready for owner review |
| EN-FR-003 | en | Financial/regulatory factuality | FR-01 | Ready for owner review |
| EN-FR-004 | en | Financial/regulatory factuality | FR-01 | Ready for owner review |
| EN-FR-005 | en | Financial/regulatory factuality | FR-01 | Ready for owner review |
| TR-FR-002 | tr | Financial/regulatory factuality | FR-01 | Ready for owner review |
| TR-FR-003 | tr | Financial/regulatory factuality | FR-01 | Ready for owner review |
| TR-FR-004 | tr | Financial/regulatory factuality | FR-01 | Ready for owner review |
| TR-FR-005 | tr | Financial/regulatory factuality | FR-01 | Ready for owner review |
| EN-HE-002 | en | Human escalation | HE-01, HE-02 | Ready for owner review |
| EN-HE-003 | en | Human escalation | HE-02 | Ready for owner review |
| EN-HE-004 | en | Human escalation | HE-01, HE-02 | Ready for owner review |
| EN-HE-005 | en | Human escalation | HE-02 | Ready for owner review |
| TR-HE-002 | tr | Human escalation | HE-01, HE-02 | Ready for owner review |
| TR-HE-003 | tr | Human escalation | HE-02 | Ready for owner review |
| TR-HE-004 | tr | Human escalation | HE-01, HE-02 | Ready for owner review |
| TR-HE-005 | tr | Human escalation | HE-02 | Ready for owner review |
| EN-CC-002 | en | Citation/confidence | CC-01 | Ready for owner review |
| EN-CC-003 | en | Citation/confidence | CC-01 | Ready for owner review |
| EN-CC-004 | en | Citation/confidence | CC-01 | Ready for owner review |
| EN-CC-005 | en | Citation/confidence | CC-01 | Ready for owner review |
| TR-CC-002 | tr | Citation/confidence | CC-01 | Ready for owner review |
| TR-CC-003 | tr | Citation/confidence | CC-01 | Ready for owner review |
| TR-CC-004 | tr | Citation/confidence | CC-01 | Ready for owner review |
| TR-CC-005 | tr | Citation/confidence | CC-01 | Ready for owner review |

## Validation evidence

- Python syntax check for the dataset builder: passed.
- Three generated JSONL copies: byte-identical.
- Standard-library test suite: 19/19 passed.
- Safe mock: no failed cases.
- Intentionally unsafe mock: all 60 cases failed.
- Candidate provenance: 48/48 remain `draft`.

## Required human action

The project owner must review the corrected dataset, fill the reviewer, date,
decision, and notes fields in the official worksheet, and confirm the final
content rather than the earlier draft. Only then may the 48 records be changed
to `approved` and the release-ready gate be treated as satisfied.
