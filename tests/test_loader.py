"""Tests for dataset validation and duplicate detection."""

from __future__ import annotations

import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from finsec_eval.loader import DatasetValidationError, load_cases
from finsec_eval.models import TestCase


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_DATASET = PROJECT_ROOT / "datasets" / "v0.1" / "cases.jsonl"
TEST_CASE_SCHEMA = PROJECT_ROOT / "schemas" / "test-case.schema.json"


class LoaderTests(unittest.TestCase):
    def test_seed_dataset_is_valid(self) -> None:
        cases = load_cases(SEED_DATASET)
        self.assertEqual(len(cases), 12)
        self.assertEqual(
            {case.language for case in cases},
            {"tr", "en"},
        )
        category_counts = Counter(case.category.value for case in cases)
        self.assertEqual(set(category_counts.values()), {2})
        self.assertTrue(
            all(case.provenance.review_status == "approved" for case in cases)
        )
        self.assertTrue(
            all(
                case.provenance.last_reviewed_at == "2026-07-31"
                for case in cases
            )
        )

    def test_committed_schema_matches_model(self) -> None:
        committed_schema = json.loads(
            TEST_CASE_SCHEMA.read_text(encoding="utf-8")
        )
        self.assertEqual(committed_schema, TestCase.model_json_schema())

    def test_duplicate_ids_are_rejected(self) -> None:
        first_line = SEED_DATASET.read_text(encoding="utf-8").splitlines()[0]
        with tempfile.TemporaryDirectory() as temp_dir:
            duplicate_path = Path(temp_dir) / "duplicates.jsonl"
            duplicate_path.write_text(
                f"{first_line}\n{first_line}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(DatasetValidationError, "Duplicate case id"):
                load_cases(duplicate_path)


if __name__ == "__main__":
    unittest.main()
