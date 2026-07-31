"""Build reproducible JSON and human-readable Markdown reports."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from finsec_eval.models import CaseResult, Outcome, Severity


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_report(
    *,
    adapter_name: str,
    dataset_path: str | Path,
    results: list[CaseResult],
) -> dict[str, Any]:
    """Create a serializable report with visible critical-failure metrics."""

    outcome_counts = Counter(result.outcome.value for result in results)
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for result in results:
        category_counts[result.category.value][result.outcome.value] += 1

    critical_applicable = [
        result
        for result in results
        if result.severity == Severity.CRITICAL
        and result.outcome != Outcome.NOT_APPLICABLE
    ]
    critical_decided = [
        result
        for result in critical_applicable
        if result.outcome in {Outcome.PASS, Outcome.FAIL}
    ]
    critical_failures = [
        result for result in critical_decided if result.outcome == Outcome.FAIL
    ]
    critical_unresolved = [
        result
        for result in critical_applicable
        if result.outcome not in {Outcome.PASS, Outcome.FAIL}
    ]
    critical_failure_rate = (
        len(critical_failures) / len(critical_decided)
        if critical_decided
        else None
    )
    critical_decision_coverage = (
        len(critical_decided) / len(critical_applicable)
        if critical_applicable
        else None
    )

    return {
        "benchmark": {
            "name": "FinSec-LLM-Eval",
            "version": "0.1.0",
            "adapter": adapter_name,
            "dataset": str(dataset_path),
            "dataset_sha256": sha256_file(dataset_path),
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        "summary": {
            "total_cases": len(results),
            "outcomes": dict(sorted(outcome_counts.items())),
            "critical_cases_applicable": len(critical_applicable),
            "critical_cases_decided": len(critical_decided),
            "critical_failures": len(critical_failures),
            "critical_unresolved": len(critical_unresolved),
            "critical_failure_rate": critical_failure_rate,
            "critical_decision_coverage": critical_decision_coverage,
            "by_category": {
                category: dict(sorted(counts.items()))
                for category, counts in sorted(category_counts.items())
            },
        },
        "results": [result.model_dump(mode="json") for result in results],
    }


def _format_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    benchmark = report["benchmark"]

    lines = [
        "# FinSec-LLM-Eval Run Report",
        "",
        f"- Adapter: `{benchmark['adapter']}`",
        f"- Dataset SHA-256: `{benchmark['dataset_sha256']}`",
        f"- Created: `{benchmark['created_at']}`",
        f"- Total cases: **{summary['total_cases']}**",
        (
            "- Critical Failure Rate: "
            f"**{_format_rate(summary['critical_failure_rate'])}** "
            f"({summary['critical_failures']}/"
            f"{summary['critical_cases_decided']})"
        ),
        (
            "- Critical Decision Coverage: "
            f"**{_format_rate(summary['critical_decision_coverage'])}** "
            f"({summary['critical_cases_decided']}/"
            f"{summary['critical_cases_applicable']})"
        ),
        f"- Unresolved critical cases: **{summary['critical_unresolved']}**",
        "",
        "## Case results",
        "",
        "| Case | Category | Severity | Outcome |",
        "|---|---|---|---|",
    ]

    for result in report["results"]:
        lines.append(
            f"| {result['case_id']} | {result['category']} | "
            f"{result['severity']} | {result['outcome']} |"
        )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "This is a small seed benchmark. Domain approval of its cases is "
            "not evidence of regulatory compliance, general model safety, or "
            "production suitability.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(report: dict[str, Any], output_dir: str | Path) -> tuple[Path, Path]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    json_path = destination / "report.json"
    markdown_path = destination / "report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, markdown_path
