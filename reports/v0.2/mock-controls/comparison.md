# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `37780a0438c883e9b19a0c1e5fa6de5be1fc644b474febc02ebcf8db0e8e8b08`
- Created: `2026-07-31T09:12:30.812798+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 30 | 30 | 0 | 0 | 0 | 0.0% | 88.2% |
| leaky-control | `mock:leaky` | 0 | 0 | 60 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
