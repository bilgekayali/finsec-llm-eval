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

`--release-ready` now passes because all 60 cases have completed attributed
dataset review. It does not approve a later model run:

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

### Credential-free GitHub Actions dry run

Maintainers can start the manual **Free deterministic dry run** workflow to
verify benchmark wiring without contacting a model provider. It uses the
reviewed-in `configs/comparison.mock.json` configuration and runs only the
`mock:safe` and `mock:leaky` controls.

To run it:

1. open **Actions → Free deterministic dry run**;
2. select **Run workflow**;
3. open the completed run summary to review the deterministic comparison.

No GitHub environment or API key is required. The workflow does not reference
secrets, install the OpenAI dependency, call an external model endpoint, or
upload an artifact. A runtime guard rejects the run if the comparison config
contains any adapter other than `mock`.

Real-model evaluation is intentionally unavailable in GitHub Actions. Run the
local commands above only after explicitly approving API usage and applying an
appropriate project hard spend limit.

### Credential-free open-model smoke comparison

The **Free open-model smoke comparison** workflow is the exception to the paid
provider boundary above. It does not call a hosted inference API. It downloads
two public Apache-2.0 model snapshots and runs them locally on a standard
GitHub-hosted CPU runner:

- `HuggingFaceTB/SmolLM2-135M-Instruct` at commit
  `75fd0ae5b521241aac18793eb0d6cb3598d86055`;
- `Qwen/Qwen2.5-0.5B-Instruct` at commit
  `4a7e54c8b8a89aa1a38cff2b97395dd455338167`.

The run uses the approved 12-case v0.1 seed, a 96-token generation cap,
temperature zero, and the text-only local adapter. The two tool-authorization
cases are reported as `not_applicable`; they are not silently treated as
passes. No API key, repository secret, paid model endpoint, larger runner, or
workflow artifact is used.

GitHub documents standard hosted runners as free for public repositories:
<https://docs.github.com/en/actions/reference/runners/github-hosted-runners#standard-github-hosted-runners-for-public-repositories>.
The selected model cards and licenses are available at:

- <https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct>;
- <https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct>.

The workflow writes the compact comparison to the job summary, prints raw
review evidence to the job log, and commits the generated JSON and Markdown
reports back to its source branch. Checkout credentials are not persisted; the
short-lived workflow token is exposed only to the final publication step. It
deliberately uploads no artifact. Any output remains a provisional smoke result
until the human-review procedure in section 8 is completed; the workflow cannot
declare a winner.

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

The manual GitHub Actions dry run exercises mock controls only. It cannot
produce or publish real-model results.
