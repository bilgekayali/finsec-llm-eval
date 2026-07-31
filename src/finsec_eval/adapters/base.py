"""Shared interface implemented by every model or agent adapter."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from finsec_eval.models import ModelResponse, TestCase


class AdapterConfigurationError(ValueError):
    """Raised when an adapter cannot start with the supplied safe configuration."""


class ModelAdapter(ABC):
    """Translate a benchmark case into a system-specific request."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable adapter name written to the run report."""

    @property
    @abstractmethod
    def capabilities(self) -> frozenset[str]:
        """Benchmark capabilities supported by this adapter."""

    @abstractmethod
    def manifest_config(self) -> dict[str, Any]:
        """Return a credential-free configuration for reproducibility."""

    @abstractmethod
    def generate(self, case: TestCase) -> ModelResponse:
        """Execute one case and return normalized text and tool calls."""
