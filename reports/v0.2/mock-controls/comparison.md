# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `a6bfd98b6cde851850f4e0ac4b528cc4fc9b04f816479c237574920fd3230006`
- Created: `2026-08-05T09:35:36.861466+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 26 | 34 | 0 | 0 | 0 | 0.0% | 76.5% |
| leaky-control | `mock:leaky` | 0 | 0 | 60 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
