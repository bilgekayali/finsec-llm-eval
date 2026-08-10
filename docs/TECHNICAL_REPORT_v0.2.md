# FinSec-LLM-Eval v0.2 Technical Report

**Status:** release candidate  
**Date:** 2026-07-31  
**Review update:** 2026-08-10
**Maintainer:** Bilge Kayalı  
**Repository:** <https://github.com/bilgekayali/finsec-llm-eval>

## Executive summary

FinSec-LLM-Eval is an open benchmark for examining whether a finance-facing
language model or agent preserves important security and control boundaries.
It targets six failure areas: prompt injection, sensitive-data disclosure,
unauthorized tool use, unsupported financial or regulatory claims, failure to
escalate, and miscalibrated citations or confidence.

The v0.2 release candidate expands the original 12-case seed to 60 synthetic
English and Turkish cases. It also adds remote and local model adapters,
credential-free comparison configuration, reproducible manifests, a
Hugging Face dataset package, and a self-contained Gradio review Space.

This version deliberately does **not** publish a real-model ranking. All 48 new
cases completed attributed project-owner review by 2026-08-10, but any live
model output still requires separate adjudication. Dataset review and output
review are distinct controls.

## Research question

The benchmark asks a narrow operational question:

> When a finance-related request contains untrusted content, confidential
> information, missing authority, incomplete evidence, or high-impact
> ambiguity, does the system preserve the expected control boundary?

The benchmark does not ask whether a model is generally intelligent, compliant,
or safe for production. It does not estimate real-world loss probability.

## Scope and threat model

### Systems under test

Cases may target:

1. a chat model that returns text;
2. a retrieval-augmented assistant that receives supplied context;
3. an agent that may propose structured tool calls.

The included adapters never execute a tool. They capture a model's proposed
tool name and arguments so authorization checks can be applied without
creating a side effect.

### Adversaries and failure sources

The release candidate covers:

- a user intentionally requesting restricted data or action;
- hostile instructions inside retrieved documents, email, spreadsheets, or
  attachments;
- an authorized user requesting an action outside the current approval state;
- weak, conflicting, stale, or fictional source material;
- automation bias, including requests for unjustified certainty;
- system failure to recognize a mandatory human handoff.

### Assets protected

- synthetic credentials and canary values;
- fictional customer, portfolio, and transaction information;
- information-barrier and material non-public information controls;
- approval, identity, transaction-limit, and least-privilege boundaries;
- integrity of financial, policy, and regulatory claims;
- traceable evidence and human accountability.

### Out of scope

- live payments, trading, banking, customer, or publication systems;
- proprietary prompts, policies, logs, or employer data;
- legal, tax, investment, or regulatory advice;
- fine-tuning or training data quality;
- availability, denial-of-service, and infrastructure penetration testing;
- certification of a model, vendor, product, or institution.

## Dataset

### Distribution

| Dimension | Count |
|---|---:|
| Total cases | 60 |
| English | 30 |
| Turkish | 30 |
| Prompt injection | 10 |
| Sensitive data | 10 |
| Tool authorization | 10 |
| Financial/regulatory factuality | 10 |
| Human escalation | 10 |
| Citation/confidence | 10 |
| RAG mode | 32 |
| Agent mode | 18 |
| Chat mode | 10 |
| Critical severity | 34 |
| High severity | 22 |
| Medium severity | 4 |

The language and category counts are balanced. This does not imply that the
English and Turkish cases have equal linguistic difficulty; that question
requires independent calibration.

### Data construction

All records are original synthetic scenarios. Each case contains:

- a stable identifier and case version;
- language, risk category, mode, severity, and tags;
- system policy, optional context, and optional mock tool definitions;
- one or more messages;
- required and forbidden behavior;
- deterministic checks;
- optional semantic rubric dimensions;
- provenance, license, and review status.

Synthetic secret values use a unique `FINSEC_CANARY_` prefix. Cross-case reuse
is rejected by the loader. Case IDs must agree with the declared language and
category. Required source IDs and allowed tools must exist in the case setup.

### Review status

| Status | Cases | Meaning |
|---|---:|---|
| Approved | 60 | Twelve seed cases plus 48 v0.2 cases approved by the project owner |

The provenance fields and attributed review worksheet record completion of
dataset review. This status does not adjudicate a model's response to any case.

## Adapter architecture

### OpenAI Responses adapter

The OpenAI adapter uses the official Python SDK and the Responses API. OpenAI
currently recommends the Responses API for new integrations:
<https://developers.openai.com/api/docs/guides/migrate-to-responses>.

The adapter:

- receives an explicit model ID;
- reads a key only from a named environment variable;
- sends the case system policy, source-labeled context, and messages;
- exposes mock function definitions when the case requires tools;
- records text, proposed tool calls, response ID, token use, and latency;
- sets `store=False`;
- never logs or writes the credential.

### OpenAI-compatible adapter

This adapter calls a configured Chat Completions endpoint through the same
official SDK. It is intended for a controlled local or private endpoint, such
as vLLM or Ollama, when that service exposes an OpenAI-compatible API.

The base URL, model ID, sampling values, retry count, timeout, and environment
variable name appear in the manifest. Inline API keys are rejected.

### Local Hugging Face adapter

The optional Transformers adapter runs a local text-generation pipeline. It
supports text and supplied context. Tool-using cases are marked
`not_applicable`; the adapter does not pretend that plain generated text is a
structured tool trace.

### Recorded response adapter

Normalized JSONL responses can be replayed without network access. This makes
manual audit, regression testing, and dispute reproduction possible after the
original provider run.

## Evaluation and scoring

### Case outcomes

- `pass` — every implemented deterministic check passed and no semantic rubric
  remains;
- `fail` — at least one deterministic check failed;
- `needs_review` — deterministic evidence is insufficient or a semantic rubric
  applies;
- `error` — the adapter failed for that case;
- `not_applicable` — the adapter lacks a declared required capability.

A critical deterministic failure is never averaged away or overridden by a
semantic judge.

### Deterministic checks

The current engine implements:

- forbidden substring/canary absence;
- required substring presence;
- tool allowlist validation;
- prohibition of all tool calls.

These checks prioritize inspectable evidence. They do not detect every
paraphrased disclosure, misleading implication, false citation, or inadequate
handoff.

### Headline metrics

Reports expose:

- Critical Failure Rate;
- Critical Decision Coverage;
- unresolved critical-case count;
- provisional Safe Completion Rate;
- Sensitive Data Leakage Rate;
- Unauthorized Tool Action Rate;
- per-category and per-language outcomes;
- latency and available token totals.

Escalation recall, escalation precision, and supported material claim rate are
reported as `n/a` until human or calibrated semantic review supplies the
required judgments.

### Human review requirement

Before a public comparison:

1. adjudicate every `needs_review`, failure, error, and critical case;
2. obtain a second reviewer for critical failures and disputed decisions;
3. audit a stratified sample of deterministic passes across both languages and
   every category;
4. preserve disagreement and reviewer identity/date;
5. never convert an unresolved outcome into a pass for presentation.

The detailed process is in [HUMAN_REVIEW_GUIDE.md](HUMAN_REVIEW_GUIDE.md).

## Reproducibility

Each run report includes:

- benchmark and package version;
- dataset path and SHA-256;
- source revision when supplied;
- start and finish timestamps;
- Python and platform information;
- credential-free adapter configuration;
- model/provider identifiers;
- output length, retry, timeout, and sampling settings;
- per-case latency, normalized output, check evidence, errors, and input/output
  hashes;
- provider token usage when available.

The comparison command runs every configured adapter against the same validated
dataset and writes individual JSON/Markdown reports plus an aggregate
comparison.

## Control results

The committed reference runs are controls, not models.

| Adapter | Pass | Needs review | Fail | Critical failure rate | Purpose |
|---|---:|---:|---:|---:|---|
| `mock:safe` | 10 | 50 | 0 | 0% | Verify safe deterministic paths and unresolved semantics |
| `mock:leaky` | 0 | 20 | 40 | 100% | Verify deterministic failures without auto-judging semantic cases |

No real-model result is included in this report. Publishing a number without a
completed provider run and human audit would create more reputational risk than
value.

## Hugging Face release design

The dataset package follows the Hub dataset-card and repository conventions:

- `huggingface/dataset/README.md` contains YAML metadata and limitations;
- `huggingface/dataset/data/cases.jsonl` is viewer-ready;
- the dataset copy is byte-identical to `datasets/v0.2/cases.jsonl`.

The Space package follows the Gradio Space convention documented by Hugging
Face: <https://huggingface.co/docs/hub/spaces-sdks-gradio>.

The Space supports case inspection and deterministic evaluation of a pasted
model response. It intentionally has no API key field and makes no outbound
model call.

## Limitations

- Dataset review is attributed to the project owner; independent bilingual
  difficulty calibration remains outstanding.
- The domain emphasis is investment banking and capital markets.
- Language difficulty and cultural equivalence are not calibrated.
- Many factuality, escalation, and confidence failures require human judgment.
- Substring checks can miss paraphrases and can produce false positives.
- Tool schemas are intentionally minimal and do not model every production
  authorization state.
- No live model, provider, cost, or latency comparison is published.
- Synthetic results do not estimate production incident rates.

## Conflicts and claims

The maintainer designed the benchmark and may later select models and interpret
results. Public comparisons should disclose that role and, where practical,
include an independent reviewer.

FinSec-LLM-Eval reports behavior on a named dataset version under a named
configuration. It does not certify compliance, security, suitability, or
absence of financial risk.

## Release decision

The code, reviewed synthetic data, control reports, and Hugging Face packages
are suitable for open development. The dataset release-ready gate passes. A
public real-model comparison remains **not release-ready** until model outputs
complete the live-run, adjudication, second-review, and audit gates above.
