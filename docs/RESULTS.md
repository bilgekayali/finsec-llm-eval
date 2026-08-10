# v0.2 Control Results

The committed results validate the benchmark pipeline with deterministic
controls. They do not measure a real language model.

## Summary

| Adapter | Pass | Needs review | Fail | Critical failure rate | Critical decision coverage |
|---|---:|---:|---:|---:|---:|
| `mock:safe` | 10 | 50 | 0 | 0% | 88.2% |
| `mock:leaky` | 0 | 20 | 40 | 100% | 94.1% |

## Interpretation

`mock:safe` protects canaries and proposes no prohibited tool call. Ten cases
without semantic rubrics receive deterministic passes. The other 50 remain
`needs_review` because their rubrics cannot be responsibly reduced to
substring checks.

`mock:leaky` exposes synthetic context, proposes unauthorized actions, or
returns deliberately unsupported claims. Forty cases contain deterministic
failure evidence. Twenty semantic-only cases remain `needs_review`; none is
silently counted as a pass.

## Real model results

No real-model comparison is published in v0.2-rc. A public result requires:

- completed dataset review of all 60 cases;
- immutable model and configuration metadata;
- a complete run manifest;
- human review of all critical and unresolved outputs;
- second review for critical failures and disputes;
- a stratified audit of deterministic passes.

Until those gates are complete, an empty results table is more accurate than a
premature ranking.

Machine-readable and Markdown control reports are under
[`reports/v0.2/mock-controls/`](../reports/v0.2/mock-controls/).
