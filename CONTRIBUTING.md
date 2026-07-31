# Contributing to FinSec-LLM-Eval

Contributions are welcome when they improve the benchmark without introducing
real confidential data, unverifiable claims, or hidden scoring behavior.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run the required checks before opening a pull request:

```bash
finsec-eval validate --dataset datasets/v0.2/cases.jsonl
python scripts/build_v0_2_dataset.py
python -m unittest discover -s tests -v
```

The dataset build command must not change committed JSONL bytes unless the
authored case source changed. `--release-ready` is a governance check and is
expected to fail while draft cases remain.

## Proposing a benchmark case

Use the benchmark-case issue form before submitting a large group of cases.
Every accepted case must:

1. use synthetic entities, values, accounts, transactions, and control data;
2. state the expected safe and unsafe behavior clearly;
3. include a severity and one of the six defined risk categories;
4. prefer deterministic evidence for critical failures;
5. identify any semantic judgment that requires qualified human review;
6. include provenance and a compatible license;
7. use a unique `FINSEC_CANARY_` value for synthetic secrets;
8. avoid presenting fictional regulation or internal policy as real.

Do not contribute prompts copied from confidential testing, employer systems,
client engagements, private red-team reports, or restricted datasets.

## Review states

- `draft`: authored but not yet domain-reviewed;
- `reviewed`: examined and annotated by a reviewer;
- `approved`: accepted for the named dataset release.

Approval of a test case does not approve model results produced with that case.
Comparison reports require separate review.

## Code contributions

Keep adapters isolated behind `ModelAdapter`, normalize outputs into
`ModelResponse`, and never execute a real financial transaction tool. A model
adapter may record proposed tool calls for evaluation, but benchmark code must
not connect those calls to production systems.

Adapter configurations may contain environment-variable names but must reject
inline credential values. New remote adapters require contract tests that use
fake clients rather than live credentials.

Changes to scoring must include tests proving that:

- a critical failure cannot be averaged away;
- an unknown evaluator does not silently pass;
- errors and unresolved outcomes remain visible.

## Pull requests

Keep pull requests focused. Explain the risk or methodology change, include the
commands used for validation, and call out any reviewer judgment that remains.

By submitting code or documentation, you agree that your contribution is
licensed under Apache-2.0. By submitting original benchmark data, you agree
that it is licensed under CC BY 4.0.
