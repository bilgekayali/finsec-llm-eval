---
title: FinSec-LLM-Eval Explorer
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
license: apache-2.0
---

# FinSec-LLM-Eval Explorer

This self-contained Gradio Space lets reviewers inspect the 60 synthetic
English/Turkish cases and run the benchmark's deterministic checks against a
pasted model response.

The Space does not call a model API, execute tools, handle credentials, or
connect to a financial system. Semantic-rubric cases remain `needs_review`.

Source and methodology:
[github.com/bilgekayali/finsec-llm-eval](https://github.com/bilgekayali/finsec-llm-eval)
