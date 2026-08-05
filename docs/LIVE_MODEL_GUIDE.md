# Live Model Run Guide

This guide runs real models without putting credentials or unreviewed claims
in the repository.

## 1. Create an isolated environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[openai]"
```

For a local Transformers model:

```bash
python -m pip install -e ".[local]"
```

## 2. Configure credentials outside the repository

The OpenAI adapter reads `OPENAI_API_KEY` by default. Set the variable in the
shell, a secret manager, or CI secret storage. Do not paste the value into a
JSON config, command argument, report, issue, or commit.

The repository ignores `.env` and `.env.*`, but the runner does not
automatically load those files. This avoids hidden configuration.

## 3. Validate the candidate dataset

```bash
finsec-eval validate --dataset datasets/v0.2/cases.jsonl
```

`--release-ready` is expected to fail until the 48 draft cases receive real
human review:

```bash
finsec-eval validate \
  --dataset datasets/v0.2/cases.jsonl \
  --release-ready
```

## 4. Run one OpenAI model

Choose a model ID deliberately based on account access, cost, latency, and the
experiment question. Do not silently replace a model in an existing baseline.

```bash
finsec-eval run \
  --dataset datasets/v0.2/cases.jsonl \
  --adapter openai \
  --model YOUR_EXPLICIT_MODEL_ID \
  --max-output-tokens 800 \
  --output-dir reports/latest/openai-model \
  --source-revision YOUR_GIT_COMMIT
```

The integration uses the Responses API, which OpenAI recommends for new
projects:
<https://developers.openai.com/api/docs/guides/migrate-to-responses>.

## 5. Compare two models

Copy the example without adding key values:

```bash
cp \
  configs/comparison.openai.example.json \
  configs/comparison.openai.local.json
```

Edit model IDs and non-secret parameters, then run:

```bash
finsec-eval compare \
  --dataset datasets/v0.2/cases.jsonl \
  --config configs/comparison.openai.local.json \
  --output-dir reports/latest/openai-comparison \
  --source-revision YOUR_GIT_COMMIT
```

The `.gitignore` rule for `*.local.json` keeps the local experiment
configuration out of commits.

### Controlled GitHub Actions run

Maintainers can also start the manual **Experimental real-model evaluation**
workflow. It uses the reviewed-in configuration at
`configs/comparison.openai.example.json`, currently comparing
`gpt-5.6-luna` and `gpt-5.6-terra` through the Responses API.

Before the first run:

1. create the protected GitHub environment `finsec-experimental-eval`;
2. add `OPENAI_API_KEY` as an environment secret;
3. optionally require a maintainer approval for that environment;
4. open **Actions → Experimental real-model evaluation → Run workflow**;
5. type `EXPERIMENTAL` when prompted.

The workflow does not commit or publish results. It stores raw reports as a
private GitHub Actions artifact for 14 days and records whether the public
release gate is still incomplete. Never paste an API key into a workflow
input, issue, pull request, config file, or report.

## 6. Run a controlled OpenAI-compatible endpoint

```bash
finsec-eval run \
  --dataset datasets/v0.2/cases.jsonl \
  --adapter openai-compatible \
  --model YOUR_SERVED_MODEL_ID \
  --base-url http://127.0.0.1:8000/v1 \
  --no-api-key \
  --temperature 0 \
  --seed 42 \
  --output-dir reports/latest/local-endpoint
```

Use `--no-api-key` only for a trusted local endpoint. For an authenticated
service, pass the **environment variable name** with `--api-key-env`, never the
credential value.

## 7. Run a local Hugging Face model

```bash
finsec-eval run \
  --dataset datasets/v0.2/cases.jsonl \
  --adapter huggingface \
  --model YOUR_HUGGING_FACE_MODEL_ID \
  --revision YOUR_IMMUTABLE_REVISION \
  --temperature 0 \
  --output-dir reports/latest/huggingface-local
```

Agent cases requiring structured tool calls are reported as
`not_applicable`.

## 8. Review before publishing

Do not publish the generated comparison table immediately.

- Review every critical result.
- Review every failure, error, and `needs_review`.
- Obtain a second review for critical failures and disputes.
- Audit deterministic passes across both languages and all categories.
- Record model terms/version, date, source commit, dataset hash, and any
  conflicts of interest.
- Keep raw evidence, but remove any accidental secrets before sharing.

Only then prepare a public results document.

The manual GitHub Actions workflow intentionally cannot bypass this section.
Its artifact is evidence for review, not a leaderboard or release result.
