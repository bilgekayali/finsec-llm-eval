"""Load and validate JSONL benchmark datasets."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from finsec_eval.models import Category, TestCase


class DatasetValidationError(ValueError):
    """Raised when one or more dataset lines are invalid."""


_CATEGORY_CODES = {
    Category.PROMPT_INJECTION: "PI",
    Category.SENSITIVE_DATA: "SD",
    Category.TOOL_AUTHORIZATION: "TU",
    Category.FINANCIAL_REGULATORY_FACTUALITY: "FR",
    Category.HUMAN_ESCALATION: "HE",
    Category.CONFIDENCE_CITATION: "CC",
}
_CANARY_PATTERN = re.compile(r"FINSEC_CANARY_[A-Z0-9_]+")


def _case_invariant_errors(case: TestCase) -> list[str]:
    errors: list[str] = []
    expected_prefix = f"{case.language.upper()}-{_CATEGORY_CODES[case.category]}-"
    if not case.id.startswith(expected_prefix):
        errors.append(
            f"id {case.id!r} does not match language/category prefix "
            f"{expected_prefix!r}"
        )

    source_ids = {source.source_id for source in case.setup.context}
    missing_sources = sorted(set(case.expected.required_source_ids) - source_ids)
    if missing_sources:
        errors.append(
            "required_source_ids are not present in setup.context: "
            + ", ".join(missing_sources)
        )

    tool_names = {tool.name for tool in case.setup.tools}
    missing_tools = sorted(set(case.expected.allowed_tools) - tool_names)
    if missing_tools:
        errors.append(
            "allowed_tools are not present in setup.tools: "
            + ", ".join(missing_tools)
        )

    if case.mode.value == "agent" and "tool_calls" not in case.required_capabilities:
        errors.append("agent cases must declare the tool_calls capability")

    serialized = case.model_dump_json()
    if "CANARY_" in serialized and not _CANARY_PATTERN.search(serialized):
        errors.append("synthetic canary values must use the FINSEC_CANARY_ prefix")

    return errors


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

            invariant_errors = _case_invariant_errors(case)
            if invariant_errors:
                raise DatasetValidationError(
                    f"Invalid case invariants at {dataset_path}:{line_number}\n- "
                    + "\n- ".join(invariant_errors)
                )

            seen_ids.add(case.id)
            cases.append(case)

    if not cases:
        raise DatasetValidationError(f"Dataset contains no cases: {dataset_path}")

    canary_owners: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        serialized = json.dumps(case.model_dump(mode="json"), ensure_ascii=False)
        for canary in _CANARY_PATTERN.findall(serialized):
            canary_owners[canary].add(case.id)
    reused = {
        canary: sorted(owners)
        for canary, owners in canary_owners.items()
        if len(owners) > 1
    }
    if reused:
        details = "; ".join(
            f"{canary}: {', '.join(owners)}"
            for canary, owners in sorted(reused.items())
        )
        raise DatasetValidationError(
            f"Synthetic canaries must be unique to one case: {details}"
        )

    return cases


def dataset_statistics(cases: list[TestCase]) -> dict[str, Any]:
    """Return stable release and review counts for a validated dataset."""

    return {
        "total_cases": len(cases),
        "languages": dict(sorted(Counter(case.language for case in cases).items())),
        "categories": dict(
            sorted(Counter(case.category.value for case in cases).items())
        ),
        "modes": dict(sorted(Counter(case.mode.value for case in cases).items())),
        "severities": dict(
            sorted(Counter(case.severity.value for case in cases).items())
        ),
        "review_statuses": dict(
            sorted(
                Counter(case.provenance.review_status for case in cases).items()
            )
        ),
    }


def release_readiness_issues(
    cases: list[TestCase],
    *,
    minimum_cases: int = 60,
) -> list[str]:
    """List unmet public-comparison gates that can be checked from the dataset."""

    issues: list[str] = []
    if len(cases) < minimum_cases:
        issues.append(
            f"dataset has {len(cases)} cases; at least {minimum_cases} are required"
        )

    category_counts = Counter(case.category for case in cases)
    missing_categories = [
        category.value for category in Category if not category_counts[category]
    ]
    if missing_categories:
        issues.append("missing categories: " + ", ".join(missing_categories))

    languages = {case.language for case in cases}
    missing_languages = sorted({"en", "tr"} - languages)
    if missing_languages:
        issues.append("missing required languages: " + ", ".join(missing_languages))

    unreviewed = [
        case.id
        for case in cases
        if case.provenance.review_status not in {"reviewed", "approved"}
    ]
    if unreviewed:
        issues.append(
            f"{len(unreviewed)} cases still require human review "
            f"(first: {', '.join(unreviewed[:5])})"
        )

    return issues
