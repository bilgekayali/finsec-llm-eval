"""Tests proving that critical leaks and tool calls cannot be averaged away."""

from __future__ import annotations

import unittest
from pathlib import Path

from finsec_eval.adapters import MockAdapter
from finsec_eval.loader import load_cases
from finsec_eval.models import Outcome
from finsec_eval.runner import run_cases


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_DATASET = PROJECT_ROOT / "datasets" / "v0.1" / "cases.jsonl"


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases(SEED_DATASET)

    def test_safe_mock_has_no_failures(self) -> None:
        results = run_cases(MockAdapter("safe"), self.cases)
        outcome_counts = {
            outcome: sum(result.outcome == outcome for result in results)
            for outcome in Outcome
        }
        self.assertEqual(outcome_counts[Outcome.FAIL], 0)
        self.assertEqual(outcome_counts[Outcome.PASS], 6)
        self.assertEqual(outcome_counts[Outcome.NEEDS_REVIEW], 6)

    def test_unsafe_mock_fails_all_seed_cases(self) -> None:
        results = run_cases(MockAdapter("leaky"), self.cases)
        self.assertTrue(all(result.outcome == Outcome.FAIL for result in results))
        critical_results = [
            result for result in results if result.severity.value == "critical"
        ]
        self.assertEqual(len(critical_results), 6)
        self.assertTrue(
            all(
                any(check.critical and check.passed is False for check in result.checks)
                for result in critical_results
            )
        )


if __name__ == "__main__":
    unittest.main()
