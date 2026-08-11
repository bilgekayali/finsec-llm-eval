# FinSec-LLM-Eval Comparison

- Benchmark version: `0.2.0`
- Dataset SHA-256: `c8dea5a4314d3a23ca23a3cc1f3c7ea423393d4fb22c0d92645887db111d9dd3`
- Created: `2026-08-11T12:47:22.987485+00:00`

## Provisional outcomes

| Run | Adapter | Pass | Needs review | Fail | Error | N/A | Critical failure rate | Critical decision coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| smollm2-135m-instruct | `huggingface-local:HuggingFaceTB/SmolLM2-135M-Instruct` | 4 | 0 | 6 | 0 | 2 | 0.0% | 100.0% |
| qwen2-5-0-5b-instruct | `huggingface-local:Qwen/Qwen2.5-0.5B-Instruct` | 3 | 0 | 7 | 0 | 2 | 25.0% | 100.0% |

## Interpretation boundary

This file compares provisional benchmark outputs, not general model quality. A public model claim requires completion of the dataset and human-review gates documented in the technical report. `needs_review`, `error`, and `not_applicable` outcomes must not be treated as passes.
