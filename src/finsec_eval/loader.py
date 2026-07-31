"""Load and validate JSONL benchmark datasets."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from finsec_eval.models import TestCase


class DatasetValidationError(ValueError):
    """Raised when one or more dataset lines are invalid."""


def load_cases(path: str | Path) -> list[TestCase]:
    """Load a UTF-8 JSONL dataset and return validated cases.

    The error includes the source line number so a dataset author can correct
    the input without searching the whole file.
    """

    dataset_path = Path(path)
    if not dataset_path.is_file():
        raise DatasetValidationError(f"Dataset not found: {dataset_path}")

    cases: list[TestCase] = []
    seen_ids: set[str] = set()

    with dataset_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                case = TestCase.model_validate_json(line)
            except ValidationError as exc:
                raise DatasetValidationError(
                    f"Invalid case at {dataset_path}:{line_number}\n{exc}"
                ) from exc

            if case.id in seen_ids:
                raise DatasetValidationError(
                    f"Duplicate case id {case.id!r} at "
                    f"{dataset_path}:{line_number}"
                )

            seen_ids.add(case.id)
            cases.append(case)

    if not cases:
        raise DatasetValidationError(f"Dataset contains no cases: {dataset_path}")

    return cases
