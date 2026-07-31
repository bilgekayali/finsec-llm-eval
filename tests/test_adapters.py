"""Contract tests for remote, local, and recorded adapters."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from finsec_eval.adapters import (
    HuggingFaceTransformersAdapter,
    OpenAICompatibleAdapter,
    OpenAIResponsesAdapter,
    RecordedResponseAdapter,
)
from finsec_eval.loader import load_cases
from finsec_eval.models import Outcome
from finsec_eval.runner import run_cases


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET = PROJECT_ROOT / "datasets" / "v0.2" / "cases.jsonl"


class _ResponsesEndpoint:
    def __init__(self) -> None:
        self.payload = None

    def create(self, **kwargs):
        self.payload = kwargs
        return SimpleNamespace(
            id="resp_test",
            output_text="Approval is required.",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="order_lookup",
                    arguments='{"account":"TEST"}',
                )
            ],
            usage=SimpleNamespace(
                input_tokens=10,
                output_tokens=4,
                total_tokens=14,
            ),
        )


class _ChatEndpoint:
    def __init__(self) -> None:
        self.payload = None

    def create(self, **kwargs):
        self.payload = kwargs
        message = SimpleNamespace(
            content="Authorization is required.",
            tool_calls=[],
        )
        return SimpleNamespace(
            id="chat_test",
            choices=[
                SimpleNamespace(
                    message=message,
                    finish_reason="stop",
                )
            ],
            usage=SimpleNamespace(
                prompt_tokens=11,
                completion_tokens=3,
                total_tokens=14,
            ),
        )


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases(DATASET)

    def test_openai_responses_payload_and_normalization(self) -> None:
        endpoint = _ResponsesEndpoint()
        client = SimpleNamespace(responses=endpoint)
        adapter = OpenAIResponsesAdapter(
            model="test-model",
            client=client,
        )
        case = next(case for case in self.cases if case.id == "EN-TU-001")
        response = adapter.generate(case)

        self.assertFalse(endpoint.payload["store"])
        self.assertEqual(endpoint.payload["model"], "test-model")
        self.assertIn("tools", endpoint.payload)
        self.assertEqual(response.tool_calls[0].name, "order_lookup")
        self.assertEqual(response.metadata["usage"]["total_tokens"], 14)
        self.assertNotIn("api_key", adapter.manifest_config())

    def test_openai_compatible_payload_and_normalization(self) -> None:
        endpoint = _ChatEndpoint()
        client = SimpleNamespace(
            chat=SimpleNamespace(completions=endpoint)
        )
        adapter = OpenAICompatibleAdapter(
            model="served-model",
            base_url="http://127.0.0.1:8000/v1",
            api_key_env=None,
            client=client,
            temperature=0,
            seed=42,
        )
        case = next(case for case in self.cases if case.id == "EN-TU-004")
        response = adapter.generate(case)

        self.assertEqual(endpoint.payload["seed"], 42)
        self.assertEqual(endpoint.payload["temperature"], 0)
        self.assertEqual(response.text, "Authorization is required.")
        self.assertEqual(response.metadata["finish_reason"], "stop")

    def test_local_adapter_marks_tool_cases_not_applicable(self) -> None:
        def fake_pipeline(prompt, **kwargs):
            self.assertIn("[ASSISTANT]", prompt)
            self.assertFalse(kwargs["do_sample"])
            return [{"generated_text": "Supporting evidence is insufficient."}]

        adapter = HuggingFaceTransformersAdapter(
            model="local-test-model",
            pipeline=fake_pipeline,
        )
        text_case = next(case for case in self.cases if case.id == "EN-CC-004")
        response = adapter.generate(text_case)
        self.assertIn("Supporting evidence", response.text)

        tool_case = next(case for case in self.cases if case.id == "EN-TU-001")
        result = run_cases(adapter, [tool_case])[0]
        self.assertEqual(result.outcome, Outcome.NOT_APPLICABLE)
        self.assertIn("tool_calls", result.error)

    def test_recorded_adapter_replays_normalized_output(self) -> None:
        case = self.cases[0]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "responses.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "case_id": case.id,
                        "text": "Recorded response",
                        "tool_calls": [],
                        "metadata": {"source": "test"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            adapter = RecordedResponseAdapter(path=path, label="fixture")
            response = adapter.generate(case)
            self.assertEqual(response.text, "Recorded response")
            self.assertEqual(adapter.name, "recorded:fixture")


if __name__ == "__main__":
    unittest.main()
