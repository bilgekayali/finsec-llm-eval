"""Replay normalized model outputs without making a network request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from finsec_eval.adapters.base import (
    AdapterConfigurationError,
    ModelAdapter,
)
from finsec_eval.models import ModelResponse, TestCase


class RecordedResponseAdapter(ModelAdapter):
    """Read one normalized ``ModelResponse`` per case from JSON Lines."""

    def __init__(
        self,
        *,
        path: str | Path,
        label: str = "recorded",
        capabilities: list[str] | None = None,
    ) -> None:
        self.path = Path(path)
        self.label = label
        self._capabilities = frozenset(
            capabilities
            or ["text_generation", "provided_context", "tool_calls"]
        )
        if not self.path.is_file():
            raise AdapterConfigurationError(
                f"Recorded response file not found: {self.path}"
            )

        self.responses: dict[str, ModelResponse] = {}
        for line_number, raw_line in enumerate(
            self.path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if not raw_line.strip():
                continue
            try:
                record = json.loads(raw_line)
                case_id = record.pop("case_id")
                response = ModelResponse.model_validate(record)
            except (json.JSONDecodeError, KeyError, ValidationError) as exc:
                raise AdapterConfigurationError(
                    f"Invalid recorded response at {self.path}:{line_number}: {exc}"
                ) from exc
            if case_id in self.responses:
                raise AdapterConfigurationError(
                    f"Duplicate recorded response for {case_id!r}"
                )
            self.responses[case_id] = response

    @property
    def name(self) -> str:
        return f"recorded:{self.label}"

    @property
    def capabilities(self) -> frozenset[str]:
        return self._capabilities

    def manifest_config(self) -> dict[str, Any]:
        return {
            "adapter": "recorded",
            "label": self.label,
            "path": str(self.path),
            "capabilities": sorted(self.capabilities),
        }

    def generate(self, case: TestCase) -> ModelResponse:
        try:
            response = self.responses[case.id]
        except KeyError as exc:
            raise RuntimeError(
                f"No recorded response exists for case {case.id}"
            ) from exc
        return response.model_copy(deep=True)
