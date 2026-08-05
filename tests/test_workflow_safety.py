"""Regression checks for the credential-free GitHub Actions dry run."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "free-dry-run.yml"


class FreeDryRunWorkflowSafetyTests(unittest.TestCase):
    def test_workflow_is_manual_and_mock_only(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", text)
        self.assertIn("configs/comparison.mock.json", text)
        self.assertIn('adapters != {"mock"}', text)

    def test_workflow_cannot_access_paid_openai_path(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        forbidden_fragments = (
            "secrets.",
            "OPENAI_API_KEY",
            "comparison.openai",
            '.[openai]',
            "environment:",
            "upload-artifact",
        )

        for fragment in forbidden_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
