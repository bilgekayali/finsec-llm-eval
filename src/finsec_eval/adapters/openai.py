"""Remote adapters built on the official OpenAI Python SDK.

The module imports the optional SDK only when a live adapter is instantiated.
Tests can inject a small fake client without installing the SDK or using a key.
"""

from __future__ import annotations

import os
from typing import Any

from finsec_eval.adapters.base import (
    AdapterConfigurationError,
    ModelAdapter,
)
from finsec_eval.adapters.common import (
    CONTEXT_TRANSPORT_VERSION,
    build_instructions,
    build_messages,
    chat_completion_tools,
    extract_chat_tool_calls,
    extract_responses_tool_calls,
    get_value,
    responses_tools,
    usage_dict,
)
from finsec_eval.models import ModelResponse, TestCase


def _load_openai_client(
    *,
    api_key_env: str | None,
    base_url: str | None,
    timeout_seconds: float,
    max_retries: int,
) -> object:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AdapterConfigurationError(
            "The OpenAI adapter requires the optional dependency. "
            "Install with: python -m pip install -e '.[openai]'"
        ) from exc

    api_key = os.getenv(api_key_env) if api_key_env else "not-needed"
    if api_key_env and not api_key:
        raise AdapterConfigurationError(
            f"Environment variable {api_key_env} is not set. "
            "Set it outside the repository; never commit credentials."
        )

    kwargs: dict[str, Any] = {
        "api_key": api_key,
        "timeout": timeout_seconds,
        "max_retries": max_retries,
    }
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def _responses_text(response: object) -> str:
    direct = get_value(response, "output_text")
    if isinstance(direct, str):
        return direct

    fragments: list[str] = []
    for item in get_value(response, "output", []) or []:
        if get_value(item, "type") != "message":
            continue
        for content in get_value(item, "content", []) or []:
            if get_value(content, "type") == "output_text":
                text = get_value(content, "text")
                if isinstance(text, str):
                    fragments.append(text)
    return "\n".join(fragments)


class OpenAIResponsesAdapter(ModelAdapter):
    """Call OpenAI's Responses API and record proposed tool calls only."""

    def __init__(
        self,
        *,
        model: str,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str | None = None,
        max_output_tokens: int = 800,
        temperature: float | None = None,
        top_p: float | None = None,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
        client: object | None = None,
    ) -> None:
        if not model.strip():
            raise AdapterConfigurationError("A non-empty model ID is required.")
        if max_output_tokens < 1:
            raise AdapterConfigurationError("max_output_tokens must be positive.")
        self.model = model
        self.api_key_env = api_key_env
        self.base_url = base_url
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.client = client or _load_openai_client(
            api_key_env=api_key_env,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    @property
    def name(self) -> str:
        return f"openai-responses:{self.model}"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"text_generation", "provided_context", "tool_calls"})

    def manifest_config(self) -> dict[str, Any]:
        return {
            "adapter": "openai_responses",
            "provider": "openai",
            "model": self.model,
            "base_url": self.base_url or "https://api.openai.com/v1",
            "api_key_env": self.api_key_env,
            "max_output_tokens": self.max_output_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "store": False,
            "context_transport_version": CONTEXT_TRANSPORT_VERSION,
            "capabilities": sorted(self.capabilities),
        }

    def generate(self, case: TestCase) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self.model,
            "input": build_messages(case),
            "max_output_tokens": self.max_output_tokens,
            "store": False,
        }
        instructions = build_instructions(case)
        if instructions:
            payload["instructions"] = instructions
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        tools = responses_tools(case)
        if tools:
            payload["tools"] = tools

        response = self.client.responses.create(**payload)
        return ModelResponse(
            text=_responses_text(response),
            tool_calls=extract_responses_tool_calls(response),
            metadata={
                "provider": "openai",
                "model": self.model,
                "endpoint": "responses",
                "response_id": get_value(response, "id"),
                "usage": usage_dict(get_value(response, "usage")),
            },
        )


class OpenAICompatibleAdapter(ModelAdapter):
    """Call an OpenAI-compatible Chat Completions endpoint.

    This supports services such as vLLM or Ollama when they expose the standard
    endpoint. The adapter records tool proposals but never executes a tool.
    """

    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        api_key_env: str | None = "OPENAI_COMPATIBLE_API_KEY",
        max_output_tokens: int = 800,
        temperature: float | None = None,
        top_p: float | None = None,
        seed: int | None = None,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
        client: object | None = None,
    ) -> None:
        if not model.strip():
            raise AdapterConfigurationError("A non-empty model ID is required.")
        if not base_url.strip():
            raise AdapterConfigurationError(
                "An OpenAI-compatible base URL is required."
            )
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.client = client or _load_openai_client(
            api_key_env=api_key_env,
            base_url=self.base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    @property
    def name(self) -> str:
        return f"openai-compatible:{self.model}"

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"text_generation", "provided_context", "tool_calls"})

    def manifest_config(self) -> dict[str, Any]:
        return {
            "adapter": "openai_compatible",
            "provider": "openai-compatible",
            "model": self.model,
            "base_url": self.base_url,
            "api_key_env": self.api_key_env,
            "max_output_tokens": self.max_output_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": self.seed,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "context_transport_version": CONTEXT_TRANSPORT_VERSION,
            "capabilities": sorted(self.capabilities),
        }

    def generate(self, case: TestCase) -> ModelResponse:
        messages = [
            {"role": "system", "content": build_instructions(case)},
            *build_messages(case),
        ]
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_output_tokens,
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.top_p is not None:
            payload["top_p"] = self.top_p
        if self.seed is not None:
            payload["seed"] = self.seed
        tools = chat_completion_tools(case)
        if tools:
            payload["tools"] = tools

        response = self.client.chat.completions.create(**payload)
        choices = get_value(response, "choices", []) or []
        if not choices:
            raise RuntimeError("The endpoint returned no completion choices.")
        choice = choices[0]
        message = get_value(choice, "message", {})
        content = get_value(message, "content", "")
        if isinstance(content, list):
            content = "\n".join(
                str(get_value(item, "text", "")) for item in content
            )
        return ModelResponse(
            text=str(content or ""),
            tool_calls=extract_chat_tool_calls(message),
            metadata={
                "provider": "openai-compatible",
                "model": self.model,
                "endpoint": "chat.completions",
                "response_id": get_value(response, "id"),
                "finish_reason": get_value(choice, "finish_reason"),
                "usage": usage_dict(get_value(response, "usage")),
            },
        )
