# GitHub Release Checklist

**Repository:** <https://github.com/bilgekayali/finsec-llm-eval>
**Initial release commit:** [`53a1ec5`](https://github.com/bilgekayali/finsec-llm-eval/commit/53a1ec531d69215afac34f8549b3a21c10a48336)

## Before creating the repository

- [x] Use the repository name `finsec-llm-eval`.
- [ ] Use the description: `Security and control benchmark for finance-facing LLMs and AI agents.`
- [x] Create the repository without an extra README, license, or `.gitignore`;
      those files are already included.
- [x] Make the first repository public only after inspecting the complete file
      list and confirming that no confidential data is present.

## First push

From the directory containing this project:

```bash
git init
git branch -M main
git add .
git commit -m "Initial release: FinSec-LLM-Eval v0.1.0"
git remote add origin https://github.com/bilgekayali/finsec-llm-eval.git
git push -u origin main
```

## Repository settings

- [x] Confirm that the CI workflow passes on Python 3.11, 3.12, and 3.13.
- [ ] Enable private vulnerability reporting.
- [ ] Enable Dependabot alerts and security updates.
- [ ] Protect `main` and require the CI check before merge.
- [ ] Disable force pushes and branch deletion on `main`.
- [ ] Add the topics listed below.

Suggested topics:

```text
ai-security
financial-services
llm
llm-evaluation
benchmark
prompt-injection
responsible-ai
cybersecurity
```

## First release

- [ ] Create tag `v0.1.0`.
- [ ] Use the title `FinSec-LLM-Eval v0.1.0 — M2 Seed Benchmark`.
- [ ] Attach the repository ZIP only if a separate downloadable archive is
      useful; GitHub already provides source archives.
- [ ] State clearly that the release contains mock results, not a public model
      comparison.
- [ ] Link the dataset card and seed-case review record.

## After publishing

- [x] Add a CI status badge using the final owner and repository name.
- [x] Add the repository URL to `CITATION.cff` and `pyproject.toml`.
- [ ] Review the rendered Mermaid diagram, tables, issue forms, and citation
      panel on GitHub.
