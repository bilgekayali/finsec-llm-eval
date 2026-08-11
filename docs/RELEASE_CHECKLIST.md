# v0.2 Release Checklist

**Repository:** <https://github.com/bilgekayali/finsec-llm-eval>

## Code and data

- [x] Validate all 60 cases.
- [x] Confirm 30 English and 30 Turkish cases.
- [x] Confirm 10 cases per risk category.
- [x] Confirm unique synthetic canaries.
- [x] Confirm no live or proprietary financial data.
- [x] Test remote adapter contracts without credentials.
- [x] Test local and recorded adapters.
- [x] Generate mock-control comparison reports.
- [x] Record human review of the 48 new cases.
- [x] Pass `finsec-eval validate --release-ready`.

## External model comparison

- [x] Select the first models and record the credential-free CPU-smoke reason.
- [x] Run from an immutable source revision.
- [x] Preserve raw normalized outputs and report hashes.
- [ ] Review every critical, failed, erroneous, and unresolved case.
- [ ] Obtain second review for critical failures and disputes.
- [ ] Audit at least 20% of remaining deterministic passes by language/category.
- [x] Publish limitations and conflicts with the provisional result.

## Hugging Face

- [x] Prepare dataset card and viewer-ready JSONL.
- [x] Prepare self-contained Gradio Space.
- [x] Verify the Space has no credential input or outbound model call.
- [ ] Create the maintainer-owned Hugging Face dataset repository.
- [ ] Push `huggingface/dataset/`.
- [ ] Create the maintainer-owned Space.
- [ ] Push `huggingface/space/`.
- [ ] Verify both hosted pages and replace any placeholder account paths.

## GitHub

- [ ] Set repository description:
      `Security and control benchmark for finance-facing LLMs and AI agents.`
- [ ] Add repository topics.
- [ ] Enable private vulnerability reporting.
- [ ] Protect `main` and require CI before merge.
- [ ] Disable force pushes and branch deletion on `main`.
- [ ] Create a v0.2 release only after CI and rendered-document review.

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

## Communications

- [x] Draft LinkedIn post.
- [x] Draft Medium article.
- [x] Draft demo video script.
- [ ] Publish only claims supported by the current review status.
- [ ] Add Hugging Face URLs only after hosted pages are verified.
