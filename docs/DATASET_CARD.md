# FinSec-LLM-Eval Dataset Card

## Dataset summary

FinSec-LLM-Eval v0.2.0-rc is a synthetic benchmark for evaluating security and
control behavior in finance-facing language models and agents.

| Property | Value |
|---|---|
| Release | 0.2.0 release candidate |
| Cases | 60 |
| Languages | 30 English, 30 Turkish |
| Domain | Investment banking and capital markets |
| Data format | UTF-8 JSON Lines |
| Source type | Original synthetic scenarios |
| Review status | 60 approved |
| Dataset license | CC BY 4.0 |

## Category distribution

| Category | Code | Cases |
|---|---|---:|
| Prompt injection | PI | 10 |
| Sensitive data | SD | 10 |
| Tool authorization | TU | 10 |
| Financial and regulatory factuality | FR | 10 |
| Human escalation | HE | 10 |
| Citation and confidence calibration | CC | 10 |

Severity distribution is 34 critical, 22 high, and 4 medium cases. Mode
distribution is 32 RAG, 18 agent, and 10 chat cases.

## Data fields

Each record contains stable identity, language, category, mode, severity,
synthetic setup context, optional mock tools, messages, expected behavior,
deterministic checks, semantic rubric, and provenance.

The formal contract is
[`schemas/test-case.schema.json`](../schemas/test-case.schema.json).
Cross-field invariants and unique-canary ownership are enforced by the Python
loader.

## Intended uses

- evaluation-pipeline and adapter development;
- controlled LLM security research;
- human-review calibration;
- finance-sector assurance exercises;
- teaching prompt injection, data protection, authorization, escalation, and
  evidence discipline.

## Out-of-scope uses

Do not use this release candidate as:

- proof of regulatory compliance;
- certification of a model, agent, vendor, or institution;
- a production-safety statement;
- investment, legal, tax, or regulatory advice;
- permission to connect an agent to a live financial tool;
- a public model leaderboard before review gates are complete.

## Creation and safety

All scenarios are original and synthetic. Names, accounts, issuers,
transactions, policies, documents, and canaries are fictional. No production
logs, customer data, employer material, or confidential prompts were used.

Synthetic secrets use unique `FINSEC_CANARY_` values. Agent tools are mock
definitions only; the benchmark never executes a transaction or side effect.

## Review and governance

The 12 v0.1 seed cases were project-owner approved on 2026-07-31. The 48 added
v0.2 cases completed bilingual project-owner review in four batches, with the
final 24 financial/regulatory factuality, human-escalation, and
citation/confidence cases approved on 2026-08-10. Dataset approval does not
approve later model outputs.

Public model results also require manual adjudication, independent review of
critical failures and disputes, and a stratified audit of deterministic passes.

## Known limitations

- English and Turkish counts are balanced, but difficulty is not calibrated.
- Sector coverage emphasizes investment banking and capital markets.
- Semantic rubrics require human judgment.
- Exact-string checks cannot detect every paraphrased failure.
- A 12-case open-model smoke result is included as provisional, unadjudicated
  evidence; no audited ranking is included.

## Licensing and citation

The dataset is released under CC BY 4.0. See
[`DATA_LICENSE.md`](../DATA_LICENSE.md) and
[`CITATION.cff`](../CITATION.cff).
