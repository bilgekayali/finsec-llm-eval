# Learning Notes: v0.2 Execution Path

These notes are for contributors who can read Python scripts but are new to
package architecture.

## A single run

When you run:

```bash
finsec-eval run \
  --dataset datasets/v0.2/cases.jsonl \
  --adapter mock \
  --mock-behavior safe \
  --output-dir reports/latest/safe
```

the program follows this path:

1. `cli.py` validates command-line arguments and builds a credential-free
   adapter configuration.
2. `loader.py` validates every JSONL case and its cross-field invariants.
3. `adapters/factory.py` creates the selected `ModelAdapter`.
4. `runner.py` checks capabilities, calls the adapter, times the case, and
   hashes the normalized input/output.
5. `scoring.py` applies deterministic checks.
6. `reporting.py` writes the run manifest, raw evidence, summary metrics, and
   Markdown report.

## A comparison

`comparison.py` loads two or more configurations, runs them against the same
dataset, keeps an individual report for each adapter, and creates one aggregate
comparison.

Configurations may name an environment variable such as `OPENAI_API_KEY`.
They must never contain the credential value.

## Why Pydantic is used

Benchmark data is evidence. A misspelled field or unexpected type can change a
result, so `models.py` rejects undocumented fields instead of guessing.

The loader then checks relationships that JSON Schema alone does not express:
ID/language/category agreement, source references, tool references, agent
capabilities, duplicate IDs, and cross-case canary ownership.

## Why there are two mock behaviors

`mock:safe` and `mock:leaky` test the benchmark pipeline, not an AI model.

- The safe control passes 30 deterministic PI/SD/TU cases. Thirty semantic
  FR/HE/CC cases remain `needs_review`.
- The leaky control discloses synthetic context, proposes unauthorized tools,
  or misses mandatory control language. All 60 cases fail.

If this contrast does not appear, the evaluator itself is broken.

## Why unsupported cases are not failures

The local Transformers adapter does not produce structured tool calls. Agent
cases requiring `tool_calls` therefore become `not_applicable`.

Treating an unsupported capability as a pass or failure would distort the
comparison.

## Why unknown checks do not pass

`evaluate_check()` returns `passed=None` for an unimplemented check. The case
becomes `needs_review`.

Absence of an evaluator is not evidence that the tested model behaved
correctly.

## Suggested reading order

1. `datasets/v0.2/cases.jsonl`
2. `src/finsec_eval/models.py`
3. `src/finsec_eval/loader.py`
4. `src/finsec_eval/adapters/base.py`
5. `src/finsec_eval/adapters/mock.py`
6. `src/finsec_eval/adapters/openai.py`
7. `src/finsec_eval/adapters/huggingface.py`
8. `src/finsec_eval/scoring.py`
9. `src/finsec_eval/runner.py`
10. `src/finsec_eval/reporting.py`
11. `src/finsec_eval/comparison.py`
12. `tests/`

## Small exercises

1. Add a non-critical deterministic check to a new synthetic case.
2. Add a fake-client response shape to `test_adapters.py`.
3. Change a case ID so it conflicts with its language and inspect the error.
4. Explain why `needs_review` must not appear in the pass column.

Do not mark a new case as reviewed or publish a model ranking without the
evidence required by the human-review guide.
