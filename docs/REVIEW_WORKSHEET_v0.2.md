# v0.2 Dataset Review Worksheet

This worksheet covers the 48 cases added after the approved v0.1 seed. All 48
completed attributed project-owner review by 2026-08-10. Dataset approval is
separate from model-output adjudication.

## AI-assisted pre-review

An AI-assisted quality pre-review was completed on 2026-08-03 and is recorded
in [`AI_ASSISTED_PRE_REVIEW_v0.2.md`](AI_ASSISTED_PRE_REVIEW_v0.2.md).
It corrected content and check-design defects but did not fill the human
reviewer or decision fields below. At that stage, all 48 candidate cases
remained `draft`.

## Review fields

For each case, review:

1. synthetic/non-proprietary content;
2. domain realism;
3. natural English or Turkish phrasing;
4. category and severity fit;
5. expected behavior and escalation label;
6. deterministic checks and rubric;
7. canary uniqueness where applicable;
8. absence of an unsupported current regulatory claim.

Decision values: `approved`, `changes_requested`, or `rejected`.

## Case log

| Case | Language | Category | Reviewer | Date | Decision | Notes/change reference |
|---|---|---|---|---|---|---|
| TR-PI-002 | tr | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; corrected Turkish control and finance wording approved after final review. |
| TR-PI-003 | tr | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; neutral Turkish tool description and revised system instruction approved after final review. |
| TR-PI-004 | tr | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; relaxed check, `trend_fidelity`, and revised system instruction approved after final review. |
| TR-PI-005 | tr | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; revised tool/control/task wording and `evidence_fidelity` approved after final review. |
| EN-PI-002 | en | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Approved as written; an unlabeled harder variant remains a possible future enhancement. |
| EN-PI-003 | en | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; neutral tool description approved after final review. |
| EN-PI-004 | en | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; relaxed check and `trend_fidelity` approved after final review. |
| EN-PI-005 | en | Prompt injection | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; revised tool/task wording and `evidence_fidelity` approved after final review. |
| TR-SD-002 | tr | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; transformed-disclosure coverage, stronger identifier checks, and Turkish wording approved after final review. |
| TR-SD-003 | tr | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; token controls, secure-alternative guidance, and revised wording approved after final review. |
| TR-SD-004 | tr | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; client-name protection and semantic minimization checks approved after final review. |
| TR-SD-005 | tr | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; partial-disclosure controls and information-barrier escalation approved after final review. |
| EN-SD-002 | en | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; transformed-disclosure coverage and stronger identifier checks approved after final review. |
| EN-SD-003 | en | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; token controls, secure-alternative guidance, and revised wording approved after final review. |
| EN-SD-004 | en | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; client-name protection and semantic minimization checks approved after final review. |
| EN-SD-005 | en | Sensitive data | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; partial-disclosure controls and information-barrier escalation approved after final review. |
| TR-TU-002 | tr | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; neutral/localized tools and semantic authorization-boundary and safe-next-step rubrics approved after final review. |
| TR-TU-003 | tr | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; synthetic payment details, verification sequencing, and safe-next-step rubrics approved after final review. |
| TR-TU-004 | tr | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; metadata-only preview and authorization, minimization, and escalation rubrics approved after final review. |
| TR-TU-005 | tr | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; synthetic order data and document-trust, authorization, and safe-next-step rubrics approved after final review. |
| EN-TU-002 | en | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; neutral tools and semantic authorization-boundary and safe-next-step rubrics approved after final review. |
| EN-TU-003 | en | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; synthetic payment details, verification sequencing, and safe-next-step rubrics approved after final review. |
| EN-TU-004 | en | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; metadata-only preview and authorization, minimization, and escalation rubrics approved after final review. |
| EN-TU-005 | en | Tool authorization | Bilge Kayalı | 2026-08-05 | approved | Initially `changes_requested`; synthetic order data and document-trust, authorization, and safe-next-step rubrics approved after final review. |
| TR-FR-002 | tr | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Initially `changes_requested`; realistic non-directive note plus source-authenticity, scope/effective-date, and escalation rubrics approved. |
| TR-FR-003 | tr | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Initially `changes_requested`; document identity, ownership, approval, effective-date, conflict, and escalation controls approved. |
| TR-FR-004 | tr | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Naturalized tax-guarantee scenario with fact/jurisdiction and qualified-handoff rubrics approved. |
| TR-FR-005 | tr | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Settlement scope, source status, and authoritative-verification rubrics approved. |
| EN-FR-002 | en | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Initially `changes_requested`; realistic non-directive note plus source-authenticity, scope/effective-date, and escalation rubrics approved. |
| EN-FR-003 | en | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Initially `changes_requested`; document identity, ownership, approval, effective-date, conflict, and escalation controls approved. |
| EN-FR-004 | en | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Tax-guarantee scenario with fact/jurisdiction and qualified-handoff rubrics approved. |
| EN-FR-005 | en | Financial/regulatory factuality | Bilge Kayalı | 2026-08-10 | approved | Settlement scope, source status, and authoritative-verification rubrics approved. |
| TR-HE-002 | tr | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Neutral tools plus payment containment, evidence-specificity, and authorized-escalation rubrics approved. |
| TR-HE-003 | tr | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Procedural fairness, evidence preservation, confidentiality, and investigation handoff approved. |
| TR-HE-004 | tr | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Neutral tools plus halt-control integrity, verification sequence, and market-operations escalation approved. |
| TR-HE-005 | tr | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Identity uncertainty, disposition control, and Compliance handoff approved. |
| EN-HE-002 | en | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Neutral tools plus payment containment, evidence-specificity, and authorized-escalation rubrics approved. |
| EN-HE-003 | en | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Procedural fairness, evidence preservation, confidentiality, and investigation handoff approved. |
| EN-HE-004 | en | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Neutral tools plus halt-control integrity, verification sequence, and market-operations escalation approved. |
| EN-HE-005 | en | Human escalation | Bilge Kayalı | 2026-08-10 | approved | Identity uncertainty, disposition control, and Compliance handoff approved. |
| TR-CC-002 | tr | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Temporal calibration, historical claim support, and precise citation rubrics approved. |
| TR-CC-003 | tr | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Source-conflict disclosure, evidence weighting, and citation fidelity approved. |
| TR-CC-004 | tr | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Useful abstention, confidence calibration, and evidence-request rubrics approved. |
| TR-CC-005 | tr | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Citation entailment, numeric-claim control, and evidence-path rubrics approved. |
| EN-CC-002 | en | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Temporal calibration, historical claim support, and precise citation rubrics approved. |
| EN-CC-003 | en | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Source-conflict disclosure, evidence weighting, and citation fidelity approved. |
| EN-CC-004 | en | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Useful abstention, confidence calibration, and evidence-request rubrics approved. |
| EN-CC-005 | en | Citation/confidence | Bilge Kayalı | 2026-08-10 | approved | Citation entailment, numeric-claim control, and evidence-path rubrics approved. |

## Prompt-injection batch status

Bilge Kayalı completed the first human review of the eight v0.2 prompt-
injection candidates on 2026-08-05. One case was approved as written and seven
received `changes_requested`. After the requested corrections were applied,
the reviewer confirmed the final content of all seven cases on the same date.
All eight prompt-injection candidates are now approved; the remaining 40 v0.2
candidates retain `draft` status.

## Sensitive-data batch status

Bilge Kayalı completed the first human review of the eight v0.2 sensitive-data
candidates on 2026-08-05. All eight received `changes_requested`. After the
requested corrections were applied, the reviewer confirmed the final content
of all eight cases on the same date. All eight are now approved; the remaining
32 v0.2 candidates retain `draft` status.

## Tool-authorization batch status

Bilge Kayalı completed the first human review of the eight v0.2 tool-
authorization candidates on 2026-08-05. All eight received
`changes_requested`. After the requested corrections were applied, the reviewer
confirmed the final content of all eight cases on the same date. All eight are
now approved; the remaining 24 v0.2 candidates retain `draft` status.

## Final semantic batch status

Bilge Kayalı approved the remaining 24 English and Turkish cases on
2026-08-10 after the requested financial/regulatory corrections and a final
quality pass across human-escalation and citation/confidence cases. Fragile
required-keyword checks were removed from all 24 semantic cases. The final
cases use explicit evidence-based rubrics, realistic synthetic document
metadata, neutral localized tools, and concrete verification or escalation
paths. All 60 dataset records are now approved.

## Completion rule

The completed review followed this rule:

1. apply requested edits;
2. update each case's provenance in the dataset source;
3. rebuild all three JSONL copies;
4. run the full test suite;
5. have the reviewer confirm the final content, not an earlier draft;
6. run `finsec-eval validate --release-ready`.

The release-ready command checks recorded status; it cannot prove that a
review actually happened. The signed/attributed worksheet is the audit record.
