"""Dependency-free checks for the Hugging Face Space scoring core."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = PROJECT_ROOT / "huggingface" / "space" / "space_core.py"
SPEC = importlib.util.spec_from_file_location("finsec_space_core", CORE_PATH)
assert SPEC and SPEC.loader
SPACE_CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPACE_CORE)


class SpaceTests(unittest.TestCase):
    def test_space_loads_all_cases(self) -> None:
        self.assertEqual(len(SPACE_CORE.CASES), 60)
        self.assertEqual(len(SPACE_CORE.CHOICES), 60)

    def test_forbidden_canary_fails(self) -> None:
        selection = next(
            choice for choice in SPACE_CORE.CHOICES if choice.startswith("EN-PI-002")
        )
        headline, details = SPACE_CORE.evaluate_response(
            selection,
            "FINSEC_CANARY_EN_PI_002",
            "[]",
        )
        self.assertIn("fail", headline)
        self.assertEqual(details["outcome"], "fail")

    def test_semantic_case_stays_unresolved(self) -> None:
        selection = next(
            choice for choice in SPACE_CORE.CHOICES if choice.startswith("EN-CC-004")
        )
        response = SPACE_CORE.safe_control_response(selection)
        headline, details = SPACE_CORE.evaluate_response(
            selection,
            response,
            "[]",
        )
        self.assertIn("needs_review", headline)
        self.assertEqual(details["outcome"], "needs_review")


if __name__ == "__main__":
    unittest.main()
