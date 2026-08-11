# FinSec-LLM-Eval v0.2.0 — Release Candidate

FinSec-LLM-Eval v0.2 adds the components needed for a controlled real-model
comparison while keeping the public claim boundary explicit.

## Included

- 60 synthetic cases: 30 English and 30 Turkish;
- 10 cases in each of six finance-AI security and control categories;
- OpenAI Responses and OpenAI-compatible adapters;
- local Hugging Face Transformers and recorded-output adapters;
- credential-free comparison configurations;
- JSON and Markdown reports with run manifests and hashes;
- dataset release-readiness checks;
- Hugging Face dataset and Gradio Space packages;
- technical report, review guidance, and launch-content drafts;
- automated tests across the supported Python versions.

## Validation status

- 60/60 cases pass schema and cross-field validation.
- Language distribution is 30 English / 30 Turkish.
- Category distribution is 10 per category.
- Twenty synthetic canaries are unique to their owning case.
- The safe mock produces 10 passes, 50 `needs_review`, and no failures.
- The intentionally unsafe mock fails 40 deterministic cases and leaves 20
  semantic-only cases for review; none passes.
- A credential-free smoke run is preserved for two pinned open models on the
  12-case v0.1 seed; its outputs are provisional and unadjudicated.

## Review status

- 12 inherited v0.1 cases: approved on 2026-07-31.
- 48 new v0.2 cases: approved after four owner-review batches, completed on
  2026-08-10.

The release-ready dataset check passes. This confirms dataset review only; it
does not adjudicate any model output or make a leaderboard publishable.

## Important limitation

A small real-model smoke result is published, but no audited comparison or
leaderboard is claimed. The run uses public local models without provider
credentials. Its outputs still require the human-review, second-review, and
audit gates in the technical report before any comparative model claim.

## Licenses

- Code and documentation: Apache-2.0
- Original dataset: CC BY 4.0
