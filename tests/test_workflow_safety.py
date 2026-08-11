"""Regression checks for the credential-free GitHub Actions dry run."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "free-dry-run.yml"
OPEN_MODEL_WORKFLOW = (
    ROOT / ".github" / "workflows" / "free-open-model-smoke.yml"
)
OPEN_MODEL_CONFIG = ROOT / "configs" / "comparison.free-open-model-smoke.json"


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


class FreeOpenModelWorkflowSafetyTests(unittest.TestCase):
    def test_workflow_uses_standard_cpu_without_credentials(self) -> None:
        text = OPEN_MODEL_WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("runs-on: ubuntu-latest", text)
        self.assertIn("permissions:\n  contents: write", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn('"device") != "cpu"', text)
        self.assertIn("datasets/v0.1/cases.jsonl", text)
        self.assertIn("provisional; model outputs are not human-adjudicated", text)
        self.assertIn(
            "git add -- reports/v0.2/free-open-model-smoke", text
        )
        self.assertIn("if: always()", text)
        self.assertIn("run-status.json", text)
        self.assertIn("evidence_generated", text)
        self.assertIn("hf_hub_download", text)
        self.assertIn("expected_model_types", text)
        self.assertEqual(text.count("github.token"), 1)
        self.assertNotIn(
            "\n      - reports/v0.2/free-open-model-smoke", text
        )
        for fragment in (
            "secrets.",
            "OPENAI_API_KEY",
            "upload-artifact",
            "environment:",
            "larger-runner",
        ):
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, text)

    def test_config_pins_two_public_local_models(self) -> None:
        import json
        import re

        config = json.loads(OPEN_MODEL_CONFIG.read_text(encoding="utf-8"))
        runs = config["runs"]
        self.assertEqual(len(runs), 2)
        self.assertEqual(
            {run["adapter"] for run in runs}, {"huggingface_local"}
        )
        self.assertTrue(all(run["device"] == "cpu" for run in runs))
        self.assertTrue(all(run["temperature"] == 0 for run in runs))
        self.assertTrue(
            all(
                re.fullmatch(r"[0-9a-f]{40}", run["revision"])
                for run in runs
            )
        )
        self.assertEqual(
            {run["model"]: run["revision"] for run in runs},
            {
                "HuggingFaceTB/SmolLM2-135M-Instruct": (
                    "75fd0ae5b521241aac18793eb0d6cb3598d86055"
                ),
                "Qwen/Qwen2.5-0.5B-Instruct": (
                    "7ae557604adf67be50417f59c2c2f167def9a775"
                ),
            },
        )


if __name__ == "__main__":
    unittest.main()
