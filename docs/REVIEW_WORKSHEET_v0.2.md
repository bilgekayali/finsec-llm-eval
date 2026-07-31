# v0.2 Dataset Review Worksheet

This worksheet covers the 48 cases added after the approved v0.1 seed. Do not
change a case's provenance from `draft` until a real reviewer completes the
checks below and records a decision.

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
| TR-PI-002 | tr | Prompt injection |  |  |  |  |
| TR-PI-003 | tr | Prompt injection |  |  |  |  |
| TR-PI-004 | tr | Prompt injection |  |  |  |  |
| TR-PI-005 | tr | Prompt injection |  |  |  |  |
| EN-PI-002 | en | Prompt injection |  |  |  |  |
| EN-PI-003 | en | Prompt injection |  |  |  |  |
| EN-PI-004 | en | Prompt injection |  |  |  |  |
| EN-PI-005 | en | Prompt injection |  |  |  |  |
| TR-SD-002 | tr | Sensitive data |  |  |  |  |
| TR-SD-003 | tr | Sensitive data |  |  |  |  |
| TR-SD-004 | tr | Sensitive data |  |  |  |  |
| TR-SD-005 | tr | Sensitive data |  |  |  |  |
| EN-SD-002 | en | Sensitive data |  |  |  |  |
| EN-SD-003 | en | Sensitive data |  |  |  |  |
| EN-SD-004 | en | Sensitive data |  |  |  |  |
| EN-SD-005 | en | Sensitive data |  |  |  |  |
| TR-TU-002 | tr | Tool authorization |  |  |  |  |
| TR-TU-003 | tr | Tool authorization |  |  |  |  |
| TR-TU-004 | tr | Tool authorization |  |  |  |  |
| TR-TU-005 | tr | Tool authorization |  |  |  |  |
| EN-TU-002 | en | Tool authorization |  |  |  |  |
| EN-TU-003 | en | Tool authorization |  |  |  |  |
| EN-TU-004 | en | Tool authorization |  |  |  |  |
| EN-TU-005 | en | Tool authorization |  |  |  |  |
| TR-FR-002 | tr | Financial/regulatory factuality |  |  |  |  |
| TR-FR-003 | tr | Financial/regulatory factuality |  |  |  |  |
| TR-FR-004 | tr | Financial/regulatory factuality |  |  |  |  |
| TR-FR-005 | tr | Financial/regulatory factuality |  |  |  |  |
| EN-FR-002 | en | Financial/regulatory factuality |  |  |  |  |
| EN-FR-003 | en | Financial/regulatory factuality |  |  |  |  |
| EN-FR-004 | en | Financial/regulatory factuality |  |  |  |  |
| EN-FR-005 | en | Financial/regulatory factuality |  |  |  |  |
| TR-HE-002 | tr | Human escalation |  |  |  |  |
| TR-HE-003 | tr | Human escalation |  |  |  |  |
| TR-HE-004 | tr | Human escalation |  |  |  |  |
| TR-HE-005 | tr | Human escalation |  |  |  |  |
| EN-HE-002 | en | Human escalation |  |  |  |  |
| EN-HE-003 | en | Human escalation |  |  |  |  |
| EN-HE-004 | en | Human escalation |  |  |  |  |
| EN-HE-005 | en | Human escalation |  |  |  |  |
| TR-CC-002 | tr | Citation/confidence |  |  |  |  |
| TR-CC-003 | tr | Citation/confidence |  |  |  |  |
| TR-CC-004 | tr | Citation/confidence |  |  |  |  |
| TR-CC-005 | tr | Citation/confidence |  |  |  |  |
| EN-CC-002 | en | Citation/confidence |  |  |  |  |
| EN-CC-003 | en | Citation/confidence |  |  |  |  |
| EN-CC-004 | en | Citation/confidence |  |  |  |  |
| EN-CC-005 | en | Citation/confidence |  |  |  |  |

## Completion rule

When all decisions are approved:

1. apply requested edits;
2. update each case's provenance in the dataset source;
3. rebuild all three JSONL copies;
4. run the full test suite;
5. have the reviewer confirm the final content, not an earlier draft;
6. run `finsec-eval validate --release-ready`.

The release-ready command checks recorded status; it cannot prove that a
review actually happened. The signed/attributed worksheet is the audit record.
