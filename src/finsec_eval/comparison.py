"""Run several adapters against one immutable dataset and compare reports."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from finsec_eval import __version__
from finsec_eval.adapters import adapter_from_config
from finsec_eval.loader import load_cases
from finsec_eval.reporting import build_report, sha256_file, write_reports
from finsec_eval.runner import run_cases


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    if not slug:
        raise ValueError("Comparison run names must contain a letter or number.")
    return slug


def load_comparison_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read comparison config {config_path}: {exc}") from exc
    if not isinstance(config, dict) or not isinstance(config.get("runs"), list):
        raise ValueError("Comparison config must contain a 'runs' array.")
    if len(config["runs"]) < 2:
        raise ValueError("A comparison requires at least two configured runs.")
    names = [str(item.get("name", "")) for item in config["runs"]]
    if any(not name.strip() for name in names):
        raise ValueError("Every comparison run requires a non-empty name.")
    if len(names) != len(set(names)):
        raise ValueError("Comparison run names must be unique.")
    for item in config["runs"]:
        if "api_key" in item:
            raise ValueError(
                "Inline api_key values are prohibited. Use api_key_env instead."
            )
    return config


def render_comparison_markdown(comparison: dict[str, Any]) -> str:
    lines = [
        "# FinSec-LLM-Eval Comparison",
        "",
        f"- Benchmark version: `{comparison['benchmark_version']}`",
        f"- Dataset SHA-256: `{comparison['dataset_sha256']}`",
        f"- Created: `{comparison['created_at']}`",
        "",
        "## Provisional outcomes",
        "",
        (
            "| Run | Adapter | Pass | Needs review | Fail | Error | N/A | "
            "Critical failure rate | Critical decision coverage |"
        ),
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in comparison["runs"]:
        outcomes = run["summary"]["outcomes"]
        cfr = run["summary"]["critical_failure_rate"]
        coverage = run["summary"]["critical_decision_coverage"]
        lines.append(
            f"| {run['name']} | `{run['adapter']}` | "
            f"{outcomes.get('pass', 0)} | "
            f"{outcomes.get('needs_review', 0)} | "
            f"{outcomes.get('fail', 0)} | "
            f"{outcomes.get('error', 0)} | "
            f"{outcomes.get('not_applicable', 0)} | "
            f"{'n/a' if cfr is None else f'{cfr:.1%}'} | "
            f"{'n/a' if coverage is None else f'{coverage:.1%}'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This file compares provisional benchmark outputs, not general model "
            "quality. A public model claim requires completion of the dataset and "
            "human-review gates documented in the technical report. `needs_review`, "
            "`error`, and `not_applicable` outcomes must not be treated as passes.",
            "",
        ]
    )
    return "\n".join(lines)


def run_comparison(
    *,
    dataset_path: str | Path,
    config_path: str | Path,
    output_dir: str | Path,
    source_revision: str | None = None,
) -> tuple[Path, Path]:
    dataset = Path(dataset_path)
    config_file = Path(config_path)
    config = load_comparison_config(config_file)
    cases = load_cases(dataset)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    runs: list[dict[str, Any]] = []
    for run_config in config["runs"]:
        name = str(run_config["name"])
        adapter_config = {
            key: value for key, value in run_config.items() if key != "name"
        }
        adapter = adapter_from_config(
            adapter_config,
            config_dir=config_file.resolve().parent,
        )
        started_at = _now()
        results = run_cases(adapter, cases)
        finished_at = _now()
        report = build_report(
            adapter_name=adapter.name,
            adapter_config=adapter.manifest_config(),
            dataset_path=dataset,
            results=results,
            started_at=started_at,
            finished_at=finished_at,
            source_revision=source_revision,
        )
        run_dir = destination / _slug(name)
        json_path, markdown_path = write_reports(report, run_dir)
        runs.append(
            {
                "name": name,
                "adapter": adapter.name,
                "report_json": str(json_path),
                "report_markdown": str(markdown_path),
                "summary": report["summary"],
            }
        )

    comparison = {
        "benchmark": "FinSec-LLM-Eval",
        "benchmark_version": __version__,
        "status": "provisional_unadjudicated",
        "claim_boundary": (
            "A benchmark comparison, not a leaderboard, compliance claim, "
            "or production-safety assessment."
        ),
        "dataset": str(dataset),
        "dataset_sha256": sha256_file(dataset),
        "created_at": _now(),
        "source_revision": source_revision,
        "runs": runs,
    }
    json_path = destination / "comparison.json"
    markdown_path = destination / "comparison.md"
    json_path.write_text(
        json.dumps(comparison, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_comparison_markdown(comparison),
        encoding="utf-8",
    )
    return json_path, markdown_path
