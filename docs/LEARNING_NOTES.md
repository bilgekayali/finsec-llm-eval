# Learning Notes: M1 Execution Path

These notes are written for contributors who can read and modify Python scripts
but are new to package architecture.

## The five-step path

When you run:

```bash
finsec-eval run \
  --dataset datasets/v0.1/cases.jsonl \
  --mock-behavior safe \
  --output-dir reports/safe
```

the program follows this path:

1. `cli.py` reads and validates the command-line arguments.
2. `loader.py` converts each JSONL line into a strict `TestCase`.
3. `MockAdapter.generate()` produces a normalized `ModelResponse`.
4. `scoring.py` evaluates the response against deterministic checks.
5. `reporting.py` writes the raw JSON evidence and a readable Markdown report.

Keeping these concerns separate lets us add real providers without rewriting
the dataset or scoring logic.

## Why Pydantic is used

Benchmark data is evidence. A misspelled field or unexpected type can change a
result, so `models.py` rejects undocumented fields instead of guessing what
the author meant.

Try changing `severity` in one dataset line to `urgent`. Validation should fail
and point to the exact line.

## Why there are two mock behaviors

`mock:safe` and `mock:leaky` test the benchmark pipeline, not an AI model.

- The safe mock passes the six deterministic PI/SD/TU cases. The six semantic
  FR/HE/CC cases remain `needs_review`, because the benchmark refuses to invent
  a semantic verdict.
- The unsafe mock discloses synthetic canaries, requests unauthorized actions,
  or fails the required evidence/escalation checks. All 12 seed cases fail.

If this contrast does not appear, the evaluator itself is broken.

## Why unknown checks do not pass

`evaluate_check()` returns `passed=None` for an unimplemented check. The case
then becomes `needs_review`.

This is an important safety rule: absence of an evaluator is not evidence that
the tested model behaved correctly.

## Suggested reading order

1. `datasets/v0.1/cases.jsonl`
2. `src/finsec_eval/models.py`
3. `src/finsec_eval/loader.py`
4. `src/finsec_eval/adapters/mock.py`
5. `src/finsec_eval/scoring.py`
6. `src/finsec_eval/runner.py`
7. `src/finsec_eval/reporting.py`
8. `src/finsec_eval/cli.py`
9. `tests/`

## Small exercises

1. Add a non-critical `required_substring` check to a new synthetic case.
2. Add a third mock behavior that fails only one risk category.
3. Change a case ID to an invalid format and inspect the validation error.
4. Explain why a single average score could hide a critical data leak.

Do not publish new cases until their expected behavior, provenance, and safety
checks have been reviewed.
