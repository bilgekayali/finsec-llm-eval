"""End-to-end comparison report tests with deterministic controls."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from finsec_eval.comparison import run_comparison


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET = PROJECT_ROOT / "datasets" / "v0.2" / "cases.jsonl"
CONFIG = PROJECT_ROOT / "configs" / "comparison.mock.json"


class ComparisonTests(unittest.TestCase):
    def test_mock_comparison_writes_reproducible_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path, markdown_path = run_comparison(
                dataset_path=DATASET,
                config_path=CONFIG,
                output_dir=temp_dir,
                source_revision="test-revision",
            )
            comparison = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(len(comparison["runs"]), 2)
            self.assertEqual(
                comparison["runs"][0]["summary"]["outcomes"]["pass"],
                10,
            )
            self.assertEqual(
                comparison["runs"][1]["summary"]["outcomes"]["fail"],
                60,
            )
            self.assertIn(
                "human-review gates",
                markdown_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
