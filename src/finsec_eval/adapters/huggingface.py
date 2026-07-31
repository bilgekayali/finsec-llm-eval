"""Optional local Hugging Face Transformers adapter."""

from __future__ import annotations

from typing import Any

from finsec_eval.adapters.base import (
    AdapterConfigurationError,
    ModelAdapter,
)
from finsec_eval.adapters.common import (
    CONTEXT_TRANSPORT_VERSION,
    build_instructions,
    build_messages,
)
from finsec_eval.models import ModelResponse, TestCase


def _render_prompt(case: TestCase) -> str:
    sections = [f"[SYSTEM]\n{build_instructions(case)}"]
    for message in build_messages(case):
        sections.append(f"[{message['role'].upper()}]\n{message['content']}")
    sections.append("[ASSISTANT]\n")
    return "\n\n".join(sections)


class HuggingFaceTransformersAdapter(ModelAdapter):
    """Generate text with a locally loaded Transformers pipeline.

    Tool-using cases are intentionally marked not applicable because this
    adapter never parses or executes tool calls.
    """

    def __init__(
        self,
        *,
        model: str,
        revision: str | None = None,
        device: str = "auto",
        max_new_tokens: int = 800,
        temperature: float = 0.0,
        pipeline: object | None = None,
    ) -> None:
        if not model.strip():
            raise AdapterConfigurationError("A non-empty model ID is required.")
        if max_new_tokens < 1:
            raise AdapterConfigurationError("max_new_tokens must be positive.")
        self.model = model
        self.revision = revision
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        if pipeline is not None:
            self.pipeline = pipeline
            return

        try:
            from transformers import pipeline as make_pipeline
        except ImportError as exc:
            raise AdapterConfigurationError(
                "The local Hugging Face adapter requires optional dependencies. "
                "Install with: python -m pip install -e '.[local]'"
            ) from exc

        kwargs: dict[str, Any] = {
            "task": "text-generation",
            "model": model,
        }
        if revision:
            kwargs["revision"] = revision
        if device == "auto":
            kwargs["device_map"] = "auto"
        else:
            kwargs["device"] = device
        self.pipeline = make_pipeline(**kwargs)

    @property
    def name(self) -> str:
        return f"huggingface-local:{self.model}"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"text_generation", "provided_context"})

    def manifest_config(self) -> dict[str, Any]:
        return {
            "adapter": "huggingface_local",
            "provider": "local",
            "model": self.model,
            "revision": self.revision,
            "device": self.device,
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "context_transport_version": CONTEXT_TRANSPORT_VERSION,
            "capabilities": sorted(self.capabilities),
        }

    def generate(self, case: TestCase) -> ModelResponse:
        prompt = _render_prompt(case)
        kwargs: dict[str, Any] = {
            "max_new_tokens": self.max_new_tokens,
            "return_full_text": False,
            "do_sample": self.temperature > 0,
        }
        if self.temperature > 0:
            kwargs["temperature"] = self.temperature
        generated = self.pipeline(prompt, **kwargs)
        if not generated:
            raise RuntimeError("The local pipeline returned no generations.")
        first = generated[0]
        text = first.get("generated_text", "") if isinstance(first, dict) else first
        if isinstance(text, list):
            assistant_messages = [
                item.get("content", "")
                for item in text
                if isinstance(item, dict) and item.get("role") == "assistant"
            ]
            text = assistant_messages[-1] if assistant_messages else str(text)
        return ModelResponse(
            text=str(text),
            metadata={
                "provider": "local",
                "model": self.model,
                "revision": self.revision,
                "endpoint": "transformers.pipeline",
            },
        )
