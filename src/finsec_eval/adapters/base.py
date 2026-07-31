"""Shared interface implemented by every model or agent adapter."""

from __future__ import annotations

from abc import ABC, abstractmethod

from finsec_eval.models import ModelResponse, TestCase


class ModelAdapter(ABC):
    """Translate a benchmark case into a system-specific request."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable adapter name written to the run report."""

    @abstractmethod
    def generate(self, case: TestCase) -> ModelResponse:
        """Execute one case and return normalized text and tool calls."""
