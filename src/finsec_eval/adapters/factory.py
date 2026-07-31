"""Create adapters from credential-free JSON configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from finsec_eval.adapters.base import (
    AdapterConfigurationError,
    ModelAdapter,
)
from finsec_eval.adapters.huggingface import HuggingFaceTransformersAdapter
from finsec_eval.adapters.mock import MockAdapter
from finsec_eval.adapters.openai import (
    OpenAICompatibleAdapter,
    OpenAIResponsesAdapter,
)
from finsec_eval.adapters.recorded import RecordedResponseAdapter


def adapter_from_config(
    config: dict[str, Any],
    *,
    config_dir: str | Path | None = None,
) -> ModelAdapter:
    """Build one adapter while rejecting inline credential values."""

    if "api_key" in config:
        raise AdapterConfigurationError(
            "Inline api_key values are prohibited. Use api_key_env instead."
        )
    adapter_type = str(config.get("adapter", "")).strip()
    if not adapter_type:
        raise AdapterConfigurationError("Adapter config requires 'adapter'.")

    if adapter_type == "mock":
        return MockAdapter(behavior=config.get("behavior", "safe"))
    if adapter_type == "openai_responses":
        return OpenAIResponsesAdapter(
            model=str(config.get("model", "")),
            api_key_env=str(config.get("api_key_env", "OPENAI_API_KEY")),
            base_url=config.get("base_url"),
            max_output_tokens=int(config.get("max_output_tokens", 800)),
            temperature=config.get("temperature"),
            top_p=config.get("top_p"),
            timeout_seconds=float(config.get("timeout_seconds", 120.0)),
            max_retries=int(config.get("max_retries", 2)),
        )
    if adapter_type == "openai_compatible":
        api_key_env = config.get(
            "api_key_env", "OPENAI_COMPATIBLE_API_KEY"
        )
        return OpenAICompatibleAdapter(
            model=str(config.get("model", "")),
            base_url=str(config.get("base_url", "")),
            api_key_env=(
                None if api_key_env in {None, ""} else str(api_key_env)
            ),
            max_output_tokens=int(config.get("max_output_tokens", 800)),
            temperature=config.get("temperature"),
            top_p=config.get("top_p"),
            seed=config.get("seed"),
            timeout_seconds=float(config.get("timeout_seconds", 120.0)),
            max_retries=int(config.get("max_retries", 2)),
        )
    if adapter_type == "huggingface_local":
        return HuggingFaceTransformersAdapter(
            model=str(config.get("model", "")),
            revision=config.get("revision"),
            device=str(config.get("device", "auto")),
            max_new_tokens=int(config.get("max_new_tokens", 800)),
            temperature=float(config.get("temperature", 0.0)),
        )
    if adapter_type == "recorded":
        raw_path = Path(str(config.get("path", "")))
        if config_dir and not raw_path.is_absolute():
            raw_path = Path(config_dir) / raw_path
        return RecordedResponseAdapter(
            path=raw_path,
            label=str(config.get("label", "recorded")),
            capabilities=config.get("capabilities"),
        )

    raise AdapterConfigurationError(f"Unknown adapter type: {adapter_type!r}")
