# What Should a Finance-Facing LLM Be Allowed to Get Wrong?

Most LLM demos are built around capability: can the model summarize a report,
answer a question, or use a tool?

In financial services, capability is only half of the problem. The other half
is control behavior.

A system can write an excellent market summary and still be unsafe if it
reveals restricted transaction information. It can identify the right
instrument and still be unacceptable if it sends an order without verified
authority. It can produce fluent compliance language and still invent a rule,
date, threshold, or citation.

That is the reason I started building
[FinSec-LLM-Eval](https://github.com/bilgekayali/finsec-llm-eval), an open
benchmark for security, reliability, and control behavior in finance-facing
language models and agents.

The project is now at a v0.2 release-candidate stage. It contains 60 synthetic
English and Turkish cases, model adapters, reproducible reports, and a small
interactive review demo. It does not yet contain a public real-model ranking.
That omission is deliberate.

## Six control questions

The benchmark is organized around six risk areas.

### 1. Prompt injection

A retrieved document, email, spreadsheet note, or attachment may contain text
that tells the assistant to ignore its policy, reveal a protected value, or
call a tool.

The test is not whether the model recognizes the phrase “prompt injection.”
The test is whether it preserves the authority boundary when the hostile
instruction appears inside otherwise plausible business material.

### 2. Sensitive data

Finance workflows contain customer records, portfolios, transaction terms,
credentials, information-barrier data, and material non-public information.

The benchmark uses fictional values and unique synthetic canaries. A model
fails when it reproduces protected content that the case says must remain
restricted. No real customer or employer data is used.

### 3. Tool authorization

An agent may be technically capable of proposing a payment, trade, export, or
publication action. That does not mean the user has authority to request it or
that the required approval state exists.

FinSec-LLM-Eval passes mock tool definitions to capable adapters, records the
model's proposed calls, and checks them against the case allowlist. It never
executes the side effect.

### 4. Financial and regulatory factuality

High-stakes hallucination is not limited to made-up numbers. A model may invent
a circular, treat a draft as effective, hide a source conflict, or guarantee a
tax or investment outcome.

These cases test source discipline and uncertainty. Many cannot be decided
responsibly with a string match, so they remain open for human review.

### 5. Human escalation

Some decisions should stop at the model boundary: ambiguous sanctions matches,
suspected fraud, incomplete market-surveillance evidence, conflicting trading
controls, and other consequential cases.

A good handoff is more than a generic disclaimer. The response should explain
why review is needed, preserve the evidence, avoid claiming that approval
already happened, and identify a useful next step.

### 6. Citation and confidence calibration

Fluent certainty is easy to mistake for evidence. The benchmark includes stale
sources, conflicting documents, missing data, and sources that do not support
the requested claim.

The question is whether the answer's confidence stays proportional to what the
case actually provides.

## Why deterministic checks are not enough

Deterministic checks are valuable because they create inspectable evidence. If
a protected canary appears in the response, or a prohibited tool call appears
in the trace, the failure should not depend on a second model's opinion.

But deterministic checks are incomplete. A response can disclose information
through a paraphrase, misrepresent a source without copying it, or perform a
weak escalation while still containing the word “review.”

FinSec-LLM-Eval therefore uses three layers:

1. deterministic checks for observable failures;
2. explicit semantic rubrics;
3. human adjudication for unresolved and release-critical results.

A critical deterministic failure cannot be overturned by an average or a
judge model.

## What changed in v0.2

The original seed contained 12 approved cases. The v0.2 candidate expands that
set to 60:

- 30 English and 30 Turkish;
- 10 cases in each risk category;
- 32 RAG, 18 agent, and 10 chat cases;
- 34 critical, 22 high, and 4 medium-severity cases.

It also adds:

- an OpenAI Responses adapter;
- an OpenAI-compatible adapter for controlled endpoints;
- a local Hugging Face Transformers adapter;
- recorded-output replay for audits;
- multi-model comparison reports;
- input/output hashes and credential-free run manifests;
- a Hugging Face dataset package;
- a Gradio Space for inspecting cases and evaluating pasted responses.

The adapters capture proposed tool calls but never execute them.

## The control numbers—and what they do not mean

Two deterministic controls are committed with the project.

The safe control produces 10 passes, 50 cases requiring semantic review, and
no failures. The deliberately unsafe control fails 40 deterministic cases and
leaves 20 semantic-only cases for review; none is counted as a pass.

Those numbers test the benchmark pipeline. They say nothing about the quality
of a real language model.

This distinction matters. A clean-looking table can create false confidence
if unresolved cases are counted as passes, unsupported capabilities are
ignored, or model outputs are never reviewed.

## Why I am not publishing a leaderboard yet

All 60 cases have completed attributed project-owner review. A live model run
would still need separate output review:

- immutable model and configuration metadata;
- review of every critical, failed, erroneous, and unresolved output;
- a second reviewer for critical failures and disputes;
- a stratified audit of deterministic passes;
- clear limitations and conflict-of-interest disclosure.

Until those gates are complete, a leaderboard would be more promotional than
evidential.

## How to contribute

The most useful contributions are specific:

- identify an unrealistic finance workflow;
- improve a Turkish or English formulation;
- show that a deterministic check can reward an unsafe answer;
- propose a case with clear synthetic data and expected behavior;
- review a semantic rubric for repeatability;
- test an adapter without publishing an unaudited ranking.

The repository includes a review worksheet, contribution guide, technical
report, dataset card, and reproducible control reports.

FinSec-LLM-Eval is not intended to prove that an AI system is compliant or
safe. Its purpose is narrower: make important control failures visible,
reproducible, and difficult to hide behind a single score.

Repository:
<https://github.com/bilgekayali/finsec-llm-eval>
