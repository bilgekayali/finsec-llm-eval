"""Model adapters supplied by FinSec-LLM-Eval."""

from finsec_eval.adapters.base import AdapterConfigurationError, ModelAdapter
from finsec_eval.adapters.factory import adapter_from_config
from finsec_eval.adapters.huggingface import HuggingFaceTransformersAdapter
from finsec_eval.adapters.mock import MockAdapter
from finsec_eval.adapters.openai import (
    OpenAICompatibleAdapter,
    OpenAIResponsesAdapter,
)
from finsec_eval.adapters.recorded import RecordedResponseAdapter

__all__ = [
    "AdapterConfigurationError",
    "HuggingFaceTransformersAdapter",
    "MockAdapter",
    "ModelAdapter",
    "OpenAICompatibleAdapter",
    "OpenAIResponsesAdapter",
    "RecordedResponseAdapter",
    "adapter_from_config",
]
