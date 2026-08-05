# Changelog

All notable project changes are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project uses semantic versioning for code and dataset releases.

## [Unreleased]

### Changed

- Completed an AI-assisted quality pre-review of all 48 v0.2 candidate cases.
- Corrected encoded-instruction realism, missing tool/attachment surfaces, and
  brittle deterministic checks while preserving all candidate records as draft.
- Regenerated the repository and Hugging Face JSONL copies and revalidated the
  mock controls.
- Recorded the first owner human-review batch for eight prompt-injection cases:
  one approved case and seven cases with requested corrections.
- Applied the requested prompt-injection wording, tool-description,
  safe-completion, and rubric improvements while retaining corrected cases as
  draft pending final reviewer confirmation.

### Planned

- Final reviewer confirmation of seven corrected prompt-injection cases and
  human review of the remaining 40 v0.2 candidates.
- First audited real-model comparison.
- External Hugging Face dataset and Space publication.

## [0.2.0] - 2026-07-31

### Added

- Sixty-case release-candidate dataset with 30 English and 30 Turkish cases.
- Ten cases in each of the six benchmark risk categories.
- OpenAI Responses and OpenAI-compatible adapters using the official SDK.
- Optional local Hugging Face Transformers adapter.
- Recorded-response replay for deterministic audit.
- Credential-free multi-adapter comparison configurations.
- Reproducible manifests, input/output hashes, latency, and token summaries.
- Machine-checkable dataset release gates and unique-canary validation.
- Push-ready Hugging Face dataset and Gradio Space packages.
- Technical report, live-run guide, human-review guide, and review worksheet.
- LinkedIn, Medium, and demo-video drafts with explicit claim boundaries.
- Expanded standard-library test suite.

### Governance

- Preserved the 12 approved v0.1 seed cases unchanged.
- Marked all 48 new cases as draft pending real bilingual/domain review.
- Published mock-control results only; no real-model ranking is claimed.

## [0.1.0] - 2026-07-31

### Added

- Strict Pydantic schema and JSONL loader.
- Six finance-security risk categories.
- Twelve English and Turkish synthetic seed cases.
- Safe and intentionally unsafe deterministic mock adapters.
- Critical-failure-aware scoring and report generation.
- JSON and Markdown reference reports.
- Automated tests and GitHub Actions validation.
- Dataset card, contribution guide, security policy, and citation metadata.

### Reviewed

- Project-owner domain approval for the 12 M2 seed cases.
