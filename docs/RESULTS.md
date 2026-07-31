# v0.2 Control Results

The committed results validate the benchmark pipeline with deterministic
controls. They do not measure a real language model.

## Summary

| Adapter | Pass | Needs review | Fail | Critical failure rate | Critical decision coverage |
|---|---:|---:|---:|---:|---:|
| `mock:safe` | 30 | 30 | 0 | 0% | 88.2% |
| `mock:leaky` | 0 | 0 | 60 | 100% | 100% |

## Interpretation

`mock:safe` protects canaries, proposes no prohibited tool call, and returns
the required control language. The 30 PI, SD, and TU cases receive
deterministic passes. The 30 FR, HE, and CC cases remain `needs_review`
because their semantic rubrics cannot be responsibly reduced to substring
checks.

`mock:leaky` exposes synthetic context or proposes unauthorized actions. All
60 cases fail, demonstrating that the reporting layer does not hide critical
failures behind an average.

## Real model results

No real-model comparison is published in v0.2-rc. A public result requires:

- human approval of the 48 draft cases;
- immutable model and configuration metadata;
- a complete run manifest;
- human review of all critical and unresolved outputs;
- second review for critical failures and disputes;
- a stratified audit of deterministic passes.

Until those gates are complete, an empty results table is more accurate than a
premature ranking.

Machine-readable and Markdown control reports are under
[`reports/v0.2/mock-controls/`](../reports/v0.2/mock-controls/).
