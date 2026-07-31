# M2 Reference Results

The included reports validate the benchmark pipeline with deterministic mock
adapters. They do not measure a real language model.

## Summary

| Adapter | Pass | Needs review | Fail | Critical failure rate | Critical decision coverage |
|---|---:|---:|---:|---:|---:|
| `mock:safe` | 6 | 6 | 0 | 0% | 100% |
| `mock:leaky` | 0 | 0 | 12 | 100% | 100% |

## Interpretation

`mock:safe` returns controlled responses that avoid synthetic disclosure and
unauthorized tool calls. The six PI, SD, and TU cases receive deterministic
passes. The six FR, HE, and CC cases remain `needs_review` because they contain
semantic rubrics and M2 intentionally has no automatic semantic judge.

`mock:leaky` intentionally exposes synthetic context or proposes unauthorized
actions. All 12 cases fail, including all six critical cases. This proves that
the reporting layer does not hide critical failures behind an average.

## What these results do not establish

The numbers do not establish model quality, regulatory compliance, operational
safety, or expected production performance. A real comparison requires a
versioned model adapter, full run manifest, preserved raw evidence, cost and
latency metadata, and documented human review.

Machine-readable and human-readable reports are available under
[`reports/`](../reports/).
