"""Tests for visible critical-failure reporting."""

from __future__ import annotations

import unittest
from pathlib import Path

from finsec_eval.adapters import MockAdapter
from finsec_eval.loader import load_cases
from finsec_eval.reporting import build_report, render_markdown
from finsec_eval.runner import run_cases


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_DATASET = PROJECT_ROOT / "datasets" / "v0.1" / "cases.jsonl"


class ReportingTests(unittest.TestCase):
    def test_critical_failure_rate_is_explicit(self) -> None:
        cases = load_cases(SEED_DATASET)
        results = run_cases(MockAdapter("leaky"), cases)
        report = build_report(
            adapter_name="mock:leaky",
            dataset_path=SEED_DATASET,
            results=results,
        )

        self.assertEqual(report["summary"]["critical_failures"], 6)
        self.assertEqual(report["summary"]["critical_failure_rate"], 1.0)
        self.assertEqual(report["summary"]["critical_decision_coverage"], 1.0)
        self.assertEqual(report["summary"]["critical_unresolved"], 0)
        self.assertIn("Critical Failure Rate: **100.0%**", render_markdown(report))
        self.assertIn(
            "Critical Decision Coverage: **100.0%**",
            render_markdown(report),
        )


if __name__ == "__main__":
    unittest.main()
