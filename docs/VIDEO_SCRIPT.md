# FinSec-LLM-Eval Demo Video Script

**Target length:** 6–7 minutes  
**Format:** screen recording with terminal and repository pages  
**Tone:** technical, direct, no promotional superlatives

## 0:00–0:35 — Opening

**On screen:** repository README and title.

**Narration:**

“A finance-facing language model can answer a question correctly and still
violate a control. It may reveal restricted data, propose an action without
approval, treat an untrusted document as an instruction, or sound certain when
the evidence is weak.

FinSec-LLM-Eval is an open benchmark I am building to test those failure modes
in a reproducible way.”

## 0:35–1:15 — Scope

**On screen:** risk-coverage table in the README.

**Narration:**

“The benchmark covers six areas: prompt injection, sensitive data, tool
authorization, financial and regulatory factuality, human escalation, and
citation or confidence calibration.

Version 0.2 is a release candidate with 60 synthetic cases: 30 English and 30
Turkish. It contains no live account, customer, transaction, or employer data.”

## 1:15–2:10 — Inspect one case

**On screen:** format one JSONL case with a local viewer or open the Gradio
Space package.

Choose `EN-PI-003`.

**Narration:**

“Each case declares its policy, supplied context, user request, expected
behavior, deterministic checks, semantic rubric, provenance, and review
status.

This example contains a hidden instruction inside a fictional client email.
The model should extract the meeting topic without revealing the canary or
proposing the export tool.”

## 2:10–2:45 — Validate the dataset

**On screen:** terminal.

```bash
finsec-eval validate --dataset datasets/v0.2/cases.jsonl
```

**Narration:**

“The validator checks the schema, duplicate IDs, language and category
alignment, source and tool references, and unique canary ownership.”

Then run:

```bash
finsec-eval validate \
  --dataset datasets/v0.2/cases.jsonl \
  --release-ready
```

**Narration:**

“The stricter release check currently fails by design. Forty-eight new cases
still need human review. I prefer an honest gate over a premature green badge.”

## 2:45–3:40 — Run control adapters

**On screen:** terminal.

```bash
finsec-eval compare \
  --dataset datasets/v0.2/cases.jsonl \
  --config configs/comparison.mock.json \
  --output-dir reports/latest
```

Open `reports/latest/comparison.md`.

**Narration:**

“These are controls, not models. The safe control passes 30 deterministic
cases and leaves 30 semantic cases for review. The intentionally leaky control
fails all 60.

The point is to prove that critical disclosure and tool failures remain
visible and that unresolved cases are not silently counted as passes.”

## 3:40–4:35 — Show real adapters

**On screen:** `src/finsec_eval/adapters/` and
`configs/comparison.openai.example.json`.

**Narration:**

“The runner supports the OpenAI Responses API, an OpenAI-compatible endpoint,
a local Hugging Face Transformers pipeline, and recorded response replay.

Configurations contain model IDs and parameter values, but never API-key
values. Credentials come from environment variables. Tool calls are recorded
as proposals; the benchmark never executes a trade, payment, export, or
publication action.”

Do not run a paid model during the recording unless the result has completed
the review process.

## 4:35–5:30 — Interactive Space

**On screen:** run the Space locally after installing the demo extra.

```bash
cd huggingface/space
python app.py
```

**Narration:**

“The Space is deliberately self-contained. A reviewer can select a case, paste
a model response, optionally add proposed tool calls as JSON, and inspect the
deterministic evidence.

It has no API-key field, makes no outbound model call, and keeps semantic cases
marked as needing review.”

## 5:30–6:20 — Limitations and invitation

**On screen:** technical report limitations and review worksheet.

**Narration:**

“This is not a compliance certificate or a production-safety claim. The new
cases need bilingual and domain review, language difficulty is not calibrated,
and many high-stakes judgments cannot be reduced to exact string checks.

The most useful feedback is concrete: an unrealistic workflow, ambiguous
expected behavior, a weak check, or a Turkish or English phrasing that should
change.”

## 6:20–6:40 — Close

**On screen:** repository URL.

**Narration:**

“The code, candidate dataset, technical report, and review process are public
at github.com/bilgekayali/finsec-llm-eval.”

## Recording checklist

- Use the current clean repository state.
- Do not show environment variables, tokens, browser sessions, or terminal
  history containing secrets.
- Do not display a real-model ranking unless its review record is public.
- Keep the `release candidate` and `synthetic data` labels visible.
- Add captions and verify the commands before recording.
