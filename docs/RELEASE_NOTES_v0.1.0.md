# FinSec-LLM-Eval v0.1.0 — M2 Seed Benchmark

FinSec-LLM-Eval is an open benchmark for examining security, reliability, and
control behavior in finance-facing language models and AI agents.

This first seed release focuses on methodology and evaluation-pipeline
correctness.

## Included

- 12 synthetic investment-banking and capital-markets cases;
- balanced English and Turkish coverage;
- six risk categories: prompt injection, sensitive data, tool authorization,
  financial and regulatory factuality, human escalation, and confidence
  calibration;
- strict JSONL validation and a published JSON Schema;
- critical-failure-aware deterministic scoring;
- safe and intentionally unsafe mock adapters;
- JSON and Markdown reference reports;
- automated tests across Python 3.11, 3.12, and 3.13;
- documented dataset governance, contribution, security, and licensing rules.

## Validation status

- 12/12 seed cases validate successfully.
- 12/12 cases have project-owner domain approval.
- 6/6 automated tests pass.
- The safe mock produces 6 passes, 6 cases requiring semantic review, and no
  failures.
- The intentionally unsafe mock fails all 12 cases and all six critical cases.

## Important limitation

This release does not include a real-model comparison. Mock results validate
the benchmark pipeline only and are not evidence of model safety, regulatory
compliance, or production suitability.

## Licenses

- Code and project documentation: Apache-2.0
- Original benchmark dataset: CC BY 4.0
