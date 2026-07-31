"""Command-line interface for validation, schema generation, and smoke runs."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

from finsec_eval.adapters import MockAdapter
from finsec_eval.loader import DatasetValidationError, load_cases
from finsec_eval.models import TestCase
from finsec_eval.reporting import build_report, write_reports
from finsec_eval.runner import run_cases


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="finsec-eval",
        description="Evaluate security controls in finance-facing LLM systems.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a JSONL benchmark dataset.",
    )
    validate_parser.add_argument("--dataset", required=True, type=Path)

    schema_parser = subparsers.add_parser(
        "schema",
        help="Generate the formal test-case JSON Schema.",
    )
    schema_parser.add_argument("--output", required=True, type=Path)

    run_parser = subparsers.add_parser(
        "run",
        help="Run the dataset with a deterministic mock adapter.",
    )
    run_parser.add_argument("--dataset", required=True, type=Path)
    run_parser.add_argument(
        "--mock-behavior",
        choices=("safe", "leaky"),
        default="safe",
    )
    run_parser.add_argument("--output-dir", required=True, type=Path)

    return parser


def _validate_command(dataset: Path) -> int:
    cases = load_cases(dataset)
    categories = Counter(case.category.value for case in cases)
    print(f"Validated {len(cases)} cases from {dataset}")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")
    return 0


def _schema_command(output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(TestCase.model_json_schema(), indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote schema to {output}")
    return 0


def _run_command(dataset: Path, behavior: str, output_dir: Path) -> int:
    cases = load_cases(dataset)
    adapter = MockAdapter(behavior=behavior)
    results = run_cases(adapter, cases)
    report = build_report(
        adapter_name=adapter.name,
        dataset_path=dataset,
        results=results,
    )
    json_path, markdown_path = write_reports(report, output_dir)

    outcomes = report["summary"]["outcomes"]
    print(
        f"Completed {len(results)} cases with {adapter.name}: "
        + ", ".join(f"{key}={value}" for key, value in outcomes.items())
    )
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            return _validate_command(args.dataset)
        if args.command == "schema":
            return _schema_command(args.output)
        if args.command == "run":
            return _run_command(
                args.dataset,
                args.mock_behavior,
                args.output_dir,
            )
    except DatasetValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    raise AssertionError(f"Unhandled command: {args.command}")


def entrypoint() -> None:
    raise SystemExit(main())
