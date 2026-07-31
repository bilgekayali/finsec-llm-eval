"""Release-candidate coverage, provenance, and control-baseline tests."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter, defaultdict
from pathlib import Path

from finsec_eval.adapters import MockAdapter
from finsec_eval.loader import (
    load_cases,
    release_readiness_issues,
)
from finsec_eval.models import Outcome
from finsec_eval.runner import run_cases


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET = PROJECT_ROOT / "datasets" / "v0.2" / "cases.jsonl"
HF_DATASET = (
    PROJECT_ROOT / "huggingface" / "dataset" / "data" / "cases.jsonl"
)
HF_SPACE_DATASET = PROJECT_ROOT / "huggingface" / "space" / "cases.jsonl"
CANARY_PATTERN = re.compile(r"FINSEC_CANARY_[A-Z0-9_]+")


class DatasetV02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases(DATASET)

    def test_distribution_is_balanced(self) -> None:
        self.assertEqual(len(self.cases), 60)
        self.assertEqual(
            Counter(case.language for case in self.cases),
            {"en": 30, "tr": 30},
        )
        self.assertEqual(
            set(Counter(case.category.value for case in self.cases).values()),
            {10},
        )

    def test_review_status_is_not_overstated(self) -> None:
        statuses = Counter(
            case.provenance.review_status for case in self.cases
        )
        self.assertEqual(statuses, {"approved": 12, "draft": 48})
        issues = release_readiness_issues(self.cases)
        self.assertTrue(
            any("48 cases still require human review" in issue for issue in issues)
        )

    def test_canaries_are_unique_to_cases(self) -> None:
        owners: dict[str, set[str]] = defaultdict(set)
        for case in self.cases:
            serialized = json.dumps(
                case.model_dump(mode="json"),
                ensure_ascii=False,
            )
            for canary in CANARY_PATTERN.findall(serialized):
                owners[canary].add(case.id)
        self.assertEqual(len(owners), 20)
        self.assertTrue(all(len(case_ids) == 1 for case_ids in owners.values()))

    def test_hugging_face_copies_are_exact(self) -> None:
        content = DATASET.read_bytes()
        self.assertEqual(HF_DATASET.read_bytes(), content)
        self.assertEqual(HF_SPACE_DATASET.read_bytes(), content)

    def test_mock_controls_cover_all_cases(self) -> None:
        safe = run_cases(MockAdapter("safe"), self.cases)
        safe_counts = Counter(result.outcome for result in safe)
        self.assertEqual(safe_counts[Outcome.PASS], 30)
        self.assertEqual(safe_counts[Outcome.NEEDS_REVIEW], 30)
        self.assertEqual(safe_counts[Outcome.FAIL], 0)

        leaky = run_cases(MockAdapter("leaky"), self.cases)
        self.assertTrue(all(result.outcome == Outcome.FAIL for result in leaky))


if __name__ == "__main__":
    unittest.main()
