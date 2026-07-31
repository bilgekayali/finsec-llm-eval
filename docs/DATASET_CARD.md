# FinSec-LLM-Eval Dataset Card

## Dataset summary

FinSec-LLM-Eval v0.1.0 is a small, synthetic seed set for evaluating the
security and control behavior of finance-facing language models and agents.
It contains 12 cases: one English and one Turkish case in each of six risk
categories.

| Property | Value |
|---|---|
| Release | 0.1.0 |
| Cases | 12 |
| Languages | English, Turkish |
| Domain | Investment banking and capital markets |
| Data format | JSON Lines |
| Source type | Original synthetic scenarios |
| Case review | Project-owner approved on 2026-07-31 |
| Dataset license | CC BY 4.0 |

## Category distribution

| Category | Code | Cases |
|---|---|---:|
| Prompt injection | PI | 2 |
| Sensitive data | SD | 2 |
| Tool authorization | TU | 2 |
| Financial and regulatory factuality | FR | 2 |
| Human escalation | HE | 2 |
| Citation and confidence calibration | CC | 2 |

Six cases are marked `critical` and six are marked `high` severity.

## Data fields

Each JSONL record contains:

- stable case identity, version, language, category, mode, and severity;
- synthetic setup context and optional mock tool definitions;
- user and system messages;
- expected required and forbidden behaviors;
- deterministic checks and optional semantic-rubric dimensions;
- provenance, license, and review metadata.

The formal contract is available in
[`schemas/test-case.schema.json`](../schemas/test-case.schema.json).

## Intended uses

The seed set is suitable for:

- developing and testing evaluation pipelines;
- demonstrating critical-failure-aware reporting;
- teaching LLM security and assurance concepts;
- comparing adapter behavior during controlled development;
- collecting reviewer feedback before the benchmark is expanded.

## Out-of-scope uses

Do not use v0.1.0 as:

- proof of regulatory compliance;
- certification of a model, agent, vendor, or financial institution;
- a statistically representative model leaderboard;
- a substitute for legal, compliance, risk, or security review;
- authorization to connect an agent to a production financial tool.

## Data creation

All scenarios are original and synthetic. Names, issuers, transactions,
policies, values, canaries, and tool calls are fictional. No production logs,
customer data, employer material, or confidential testing prompts were used.

The scenarios were designed to make severe failures observable through exact
canary checks, forbidden-value checks, and tool-call allowlists where possible.
Cases requiring semantic judgment remain unresolved until reviewed.

## Review and governance

The project owner approved the scenario realism and expected control behavior
for all 12 M2 cases on 2026-07-31. Independent reviewer calibration has not yet
been completed. Model outputs and comparison reports require their own review;
dataset approval does not transfer to later results.

Contributed cases move through `draft`, `reviewed`, and `approved` states.
Every release must preserve provenance and review metadata.

## Known limitations

- Twelve cases are too few for broad ranking claims.
- The sector coverage is limited to investment-banking and capital-markets
  examples.
- English and Turkish coverage is balanced by count, not by independent
  linguistic difficulty calibration.
- Semantic rubrics have not been calibrated across multiple reviewers.
- No real-model baseline is included in M2.
- Current deterministic checks emphasize visible failure evidence and do not
  cover every indirect disclosure or misleading answer.

## Licensing and citation

The dataset is released under CC BY 4.0. See
[`DATA_LICENSE.md`](../DATA_LICENSE.md) for attribution guidance and
[`CITATION.cff`](../CITATION.cff) for project citation metadata.
