"""Execute benchmark cases against a normalized adapter."""

from __future__ import annotations

import hashlib
import json
from time import perf_counter

from finsec_eval.adapters.base import ModelAdapter
from finsec_eval.models import CaseResult, Outcome, TestCase
from finsec_eval.scoring import score_case


def _sha256_json(value: object) -> str:
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def run_cases(
    adapter: ModelAdapter,
    cases: list[TestCase],
) -> list[CaseResult]:
    """Run all cases while preserving per-case errors in the report."""

    results: list[CaseResult] = []

    for case in cases:
        started = perf_counter()
        input_sha256 = _sha256_json(case.model_dump(mode="json"))
        missing_capabilities = sorted(
            set(case.required_capabilities) - set(adapter.capabilities)
        )
        if missing_capabilities:
            results.append(
                CaseResult(
                    case_id=case.id,
                    language=case.language,
                    category=case.category,
                    severity=case.severity,
                    outcome=Outcome.NOT_APPLICABLE,
                    latency_ms=0.0,
                    input_sha256=input_sha256,
                    error=(
                        "Unsupported capabilities: "
                        + ", ".join(missing_capabilities)
                    ),
                )
            )
            continue

        try:
            response = adapter.generate(case)
            result = score_case(case, response)
            result.latency_ms = round((perf_counter() - started) * 1000, 3)
            result.input_sha256 = input_sha256
            result.output_sha256 = _sha256_json(
                response.model_dump(mode="json")
            )
        except Exception as exc:  # A failed case must not abort the whole run.
            result = CaseResult(
                case_id=case.id,
                language=case.language,
                category=case.category,
                severity=case.severity,
                outcome=Outcome.ERROR,
                latency_ms=round((perf_counter() - started) * 1000, 3),
                input_sha256=input_sha256,
                error=f"{type(exc).__name__}: {exc}",
            )
        results.append(result)

    return results
