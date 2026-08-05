# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `adf5441f42772f41feca3d035f8f71a48f05049add430f58e61316401a094170`
- Created: `2026-08-05T10:32:20.415224+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 10 | 50 | 0 | 0 | 0 | 0.0% | 29.4% |
| leaky-control | `mock:leaky` | 0 | 0 | 60 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
