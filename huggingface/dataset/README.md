---
pretty_name: FinSec-LLM-Eval
license: cc-by-4.0
language:
  - en
  - tr
task_categories:
  - text-generation
tags:
  - finance
  - cybersecurity
  - llm-evaluation
  - prompt-injection
  - responsible-ai
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: test
        path: data/cases.jsonl
---

# FinSec-LLM-Eval

FinSec-LLM-Eval is a bilingual, synthetic benchmark for examining security,
reliability, and control behavior in finance-facing language models and AI
agents.

The v0.2 release candidate contains 60 cases:

- 30 English and 30 Turkish cases;
- 10 cases in each of six risk categories;
- synthetic data only;
- deterministic checks plus explicit semantic-review rubrics;
- no live financial tools, credentials, customer records, or employer data.

## Important review status

This package is a **release candidate**, not a public model leaderboard.
Twelve inherited seed cases are project-owner approved. The 48 new cases are
marked `draft` until bilingual domain review is recorded. Model outputs also
require a separate human review before any public comparison claim.

## Risk categories

| Category | Code | Cases |
|---|---|---:|
| Prompt injection resistance | PI | 10 |
| Sensitive data protection | SD | 10 |
| Tool use and authorization | TU | 10 |
| Financial and regulatory factuality | FR | 10 |
| Human escalation and safe handoff | HE | 10 |
| Citation and confidence calibration | CC | 10 |

## Loading

```python
from datasets import load_dataset

dataset = load_dataset("YOUR_HF_USERNAME/finsec-llm-eval")
print(dataset["test"][0])
```

Replace `YOUR_HF_USERNAME` after the dataset repository is created.

## Intended use

Use the dataset for controlled research, adapter development, security
assurance exercises, reviewer calibration, and teaching. Preserve the
case-level provenance, review status, and synthetic-data boundaries.

Do not use the dataset as:

- evidence of regulatory compliance;
- certification that a model or agent is production-safe;
- investment, legal, tax, or regulatory advice;
- authorization to connect an agent to a live financial system.

## Creation and limitations

All scenarios are original and synthetic. The benchmark emphasizes observable
control failures, but deterministic checks cannot resolve every semantic
failure. English and Turkish counts are balanced; linguistic difficulty has
not yet been independently calibrated. The current domain emphasis is
investment banking and capital markets.

For the full methodology, governance, limitations, and source code, see the
[GitHub repository](https://github.com/bilgekayali/finsec-llm-eval).

## License

The dataset is licensed under CC BY 4.0. Code and documentation in the GitHub
repository use Apache License 2.0.
