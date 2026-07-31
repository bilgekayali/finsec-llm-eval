"""Gradio application for reviewing cases and pasted model outputs."""

from __future__ import annotations

import gradio as gr

from space_core import CHOICES, case_view, evaluate_response, safe_control_response


with gr.Blocks(title="FinSec-LLM-Eval Explorer") as demo:
    gr.Markdown(
        """
# FinSec-LLM-Eval Explorer

Inspect a synthetic finance-security case, paste a model response, and run
deterministic checks. The result is provisional: semantic cases still require
human review, and no result is a compliance or production-safety claim.
"""
    )

    case_selector = gr.Dropdown(
        choices=CHOICES,
        value=CHOICES[0],
        label="Benchmark case",
    )
    case_json = gr.JSON(label="Case and review rubric", value=case_view(CHOICES[0]))

    with gr.Row():
        response_text = gr.Textbox(
            label="Model response",
            lines=10,
            placeholder="Paste the model response here.",
        )
        tool_calls = gr.Textbox(
            label="Proposed tool calls (optional JSON)",
            lines=10,
            value="[]",
            placeholder='[{"name": "tool_name", "arguments": {}}]',
        )

    with gr.Row():
        load_control = gr.Button("Load safe control response")
        evaluate = gr.Button("Evaluate response", variant="primary")

    outcome_markdown = gr.Markdown()
    result_json = gr.JSON(label="Deterministic evidence")

    case_selector.change(
        fn=case_view,
        inputs=case_selector,
        outputs=case_json,
    )
    load_control.click(
        fn=safe_control_response,
        inputs=case_selector,
        outputs=response_text,
    )
    evaluate.click(
        fn=evaluate_response,
        inputs=[case_selector, response_text, tool_calls],
        outputs=[outcome_markdown, result_json],
    )

    gr.Markdown(
        """
The Space does not call model APIs, execute tools, or accept credentials.
[View the methodology and source](https://github.com/bilgekayali/finsec-llm-eval).
"""
    )


if __name__ == "__main__":
    demo.launch()
