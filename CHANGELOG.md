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
  safe-completion, and rubric improvements, then recorded final owner approval
  of all eight prompt-injection candidates.
- Recorded owner review of all eight sensitive-data candidates and applied the
  requested leakage-detection, data-minimization, secure-alternative, and
  information-barrier escalation improvements, then recorded final owner
  approval of all eight corrected cases.
- Recorded the initial owner review of all eight tool-authorization candidates
  and applied the requested neutral/localized tool descriptions, realistic
  synthetic transaction details, semantic authorization checks, data-
  minimization controls, document trust boundaries, and escalation rubrics.
  Final owner approval of all eight corrected cases was then recorded.
- Completed owner review of the remaining 24 financial/regulatory factuality,
  human-escalation, and citation/confidence cases in English and Turkish.
- Replaced fragile required-keyword checks in those semantic cases with
  evidence-based rubrics, neutral localized tool descriptions, realistic
  synthetic document metadata, and explicit verification or escalation paths.
- Recorded all 60 cases as approved and passed the dataset release-ready gate.
- Added a credential-free GitHub Actions smoke comparison for two pinned,
  Apache-2.0 open models on the approved v0.1 seed, with CPU-only execution,
  no user-managed secrets or artifacts, an explicit unadjudicated-result
  boundary, and branch-scoped publication of the generated evidence.

### Planned

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
