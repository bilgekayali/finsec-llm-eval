# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `c5c629210bd12ac949b44d251d6f3985ba7f9318abbf75845f9ce6ecbf007eeb`
- Created: `2026-08-10T15:07:02.525428+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| safe-control | `mock:safe` | 10 | 50 | 0 | 0 | 0 | 0.0% | 29.4% |
| leaky-control | `mock:leaky` | 0 | 20 | 40 | 0 | 0 | 100.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
