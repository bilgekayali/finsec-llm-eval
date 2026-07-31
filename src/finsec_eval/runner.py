"""Execute benchmark cases against a normalized adapter."""

from __future__ import annotations

from time import perf_counter

from finsec_eval.adapters.base import ModelAdapter
from finsec_eval.models import CaseResult, Outcome, TestCase
from finsec_eval.scoring import score_case


def run_cases(
    adapter: ModelAdapter,
    cases: list[TestCase],
) -> list[CaseResult]:
    """Run all cases while preserving per-case errors in the report."""

    results: list[CaseResult] = []

    for case in cases:
        started = perf_counter()
        try:
            response = adapter.generate(case)
            result = score_case(case, response)
            result.latency_ms = round((perf_counter() - started) * 1000, 3)
        except Exception as exc:  # A failed case must not abort the whole run.
            result = CaseResult(
                case_id=case.id,
                category=case.category,
                severity=case.severity,
                outcome=Outcome.ERROR,
                latency_ms=round((perf_counter() - started) * 1000, 3),
                error=f"{type(exc).__name__}: {exc}",
            )
        results.append(result)

    return results
