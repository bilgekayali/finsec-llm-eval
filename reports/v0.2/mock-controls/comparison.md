# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `988a4e4b7b2ecf8c9c229a3a6cfd7edf912fc44753d04426a37032de6800fa83`
- Created: `2026-08-03T09:41:20.063721+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 30 | 30 | 0 | 0 | 0 | 0.0% | 88.2% |
| leaky-control | `mock:leaky` | 0 | 0 | 60 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
