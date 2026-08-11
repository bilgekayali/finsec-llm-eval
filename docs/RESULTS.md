# v0.2 Control Results

The committed results include deterministic pipeline controls and a small,
credential-free real-model smoke comparison. The model outputs remain
provisional and unadjudicated.

## Summary

| Adapter | Pass | Needs review | Fail | Critical failure rate | Critical decision coverage |
|---|---:|---:|---:|---:|---:|
| `mock:safe` | 10 | 50 | 0 | 0% | 29.4% |
| `mock:leaky` | 0 | 20 | 40 | 100% | 100% |

## Interpretation

`mock:safe` protects canaries and proposes no prohibited tool call. Ten cases
without semantic rubrics receive deterministic passes. The other 50 remain
`needs_review` because their rubrics cannot be responsibly reduced to
substring checks.

`mock:leaky` exposes synthetic context, proposes unauthorized actions, or
returns deliberately unsupported claims. Forty cases contain deterministic
failure evidence. Twenty semantic-only cases remain `needs_review`; none is
silently counted as a pass.

## Real model results

The first smoke comparison ran two immutable public model snapshots locally on
a standard GitHub-hosted CPU runner. It used no API key or paid inference API
and evaluated the approved 12-case v0.1 seed.

| Model | Pass | Fail | N/A | Critical failures | Critical decision coverage |
|---|---:|---:|---:|---:|---:|
| SmolLM2-135M-Instruct | 4 | 6 | 2 | 0/4 | 100% |
| Qwen2.5-0.5B-Instruct | 3 | 7 | 2 | 1/4 | 100% |

The N/A outcomes are the two tool-authorization cases, which a text-only local
adapter cannot execute or evaluate. Qwen also triggered a deterministic
sensitive-data failure in one of two seed cases. These numbers are useful as
review evidence, but they are not a leaderboard or a production-safety claim.

An audited public comparison still requires:

- completed dataset review of all 60 cases;
- immutable model and configuration metadata;
- a complete run manifest (now preserved for this smoke run);
- human review of all critical and unresolved outputs;
- second review for critical failures and disputes;
- a stratified audit of deterministic passes.

Until the remaining review gates are complete, the smoke table must retain its
`provisional_unadjudicated` label and must not be used to declare a winner.

Machine-readable and Markdown control reports are under
[`reports/v0.2/mock-controls/`](../reports/v0.2/mock-controls/). The real-model
smoke evidence is under
[`reports/v0.2/free-open-model-smoke/`](../reports/v0.2/free-open-model-smoke/).
