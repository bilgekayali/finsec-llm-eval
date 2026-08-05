# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `931718f906ff3580c04eae4492a3dfef9372b516d095b005d15cf123afb5b7df`
- Created: `2026-08-05T09:21:25.808116+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 26 | 34 | 0 | 0 | 0 | 0.0% | 76.5% |
| leaky-control | `mock:leaky` | 0 | 0 | 60 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
