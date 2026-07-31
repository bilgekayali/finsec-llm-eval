"""Command-line interface for validation, model runs, and comparisons."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from finsec_eval.adapters import (
    AdapterConfigurationError,
    adapter_from_config,
)
from finsec_eval.comparison import run_comparison
from finsec_eval.loader import (
    DatasetValidationError,
    dataset_statistics,
    load_cases,
    release_readiness_issues,
)
from finsec_eval.models import TestCase
from finsec_eval.reporting import build_report, write_reports
from finsec_eval.runner import run_cases


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    validate_parser.add_argument(
        "--release-ready",
        action="store_true",
        help="Also enforce the machine-checkable public-comparison gates.",
    )

    schema_parser = subparsers.add_parser(
        "schema",
        help="Generate the formal test-case JSON Schema.",
    )
    schema_parser.add_argument("--output", required=True, type=Path)

    run_parser = subparsers.add_parser(
        "run",
        help="Run one mock, remote, local, or recorded adapter.",
    )
    run_parser.add_argument("--dataset", required=True, type=Path)
    run_parser.add_argument("--output-dir", required=True, type=Path)
    run_parser.add_argument(
        "--adapter",
        choices=(
            "mock",
            "openai",
            "openai-compatible",
            "huggingface",
            "recorded",
        ),
        default="mock",
    )
    run_parser.add_argument(
        "--mock-behavior",
        choices=("safe", "leaky"),
        default="safe",
    )
    run_parser.add_argument("--model")
    run_parser.add_argument("--base-url")
    run_parser.add_argument("--api-key-env")
    run_parser.add_argument(
        "--no-api-key",
        action="store_true",
        help="For a trusted local OpenAI-compatible endpoint only.",
    )
    run_parser.add_argument("--responses-file", type=Path)
    run_parser.add_argument("--label", default="recorded")
    run_parser.add_argument("--revision")
    run_parser.add_argument("--device", default="auto")
    run_parser.add_argument("--max-output-tokens", type=int, default=800)
    run_parser.add_argument("--temperature", type=float)
    run_parser.add_argument("--top-p", type=float)
    run_parser.add_argument("--seed", type=int)
    run_parser.add_argument("--timeout-seconds", type=float, default=120.0)
    run_parser.add_argument("--max-retries", type=int, default=2)
    run_parser.add_argument("--source-revision")

    compare_parser = subparsers.add_parser(
        "compare",
        help="Run two or more credential-free adapter configurations.",
    )
    compare_parser.add_argument("--dataset", required=True, type=Path)
    compare_parser.add_argument("--config", required=True, type=Path)
    compare_parser.add_argument("--output-dir", required=True, type=Path)
    compare_parser.add_argument("--source-revision")

    return parser


def _validate_command(dataset: Path, release_ready: bool) -> int:
    cases = load_cases(dataset)
    statistics = dataset_statistics(cases)
    print(f"Validated {len(cases)} cases from {dataset}")
    for category, count in statistics["categories"].items():
        print(f"  {category}: {count}")
    print(
        "  languages: "
        + ", ".join(
            f"{language}={count}"
            for language, count in statistics["languages"].items()
        )
    )
    print(
        "  review: "
        + ", ".join(
            f"{status}={count}"
            for status, count in statistics["review_statuses"].items()
        )
    )

    if release_ready:
        issues = release_readiness_issues(cases)
        if issues:
            print("Public-comparison dataset gates are not complete:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            return 3
        print("Machine-checkable public-comparison dataset gates passed.")
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


def _single_run_config(args: argparse.Namespace) -> dict[str, Any]:
    if args.adapter == "mock":
        return {"adapter": "mock", "behavior": args.mock_behavior}
    if args.adapter == "openai":
        return {
            "adapter": "openai_responses",
            "model": args.model or "",
            "base_url": args.base_url,
            "api_key_env": args.api_key_env or "OPENAI_API_KEY",
            "max_output_tokens": args.max_output_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "timeout_seconds": args.timeout_seconds,
            "max_retries": args.max_retries,
        }
    if args.adapter == "openai-compatible":
        return {
            "adapter": "openai_compatible",
            "model": args.model or "",
            "base_url": args.base_url or "",
            "api_key_env": (
                None
                if args.no_api_key
                else args.api_key_env or "OPENAI_COMPATIBLE_API_KEY"
            ),
            "max_output_tokens": args.max_output_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "seed": args.seed,
            "timeout_seconds": args.timeout_seconds,
            "max_retries": args.max_retries,
        }
    if args.adapter == "huggingface":
        return {
            "adapter": "huggingface_local",
            "model": args.model or "",
            "revision": args.revision,
            "device": args.device,
            "max_new_tokens": args.max_output_tokens,
            "temperature": args.temperature or 0.0,
        }
    if args.adapter == "recorded":
        return {
            "adapter": "recorded",
            "path": str(args.responses_file or ""),
            "label": args.label,
        }
    raise AssertionError(f"Unhandled adapter: {args.adapter}")


def _run_command(args: argparse.Namespace) -> int:
    cases = load_cases(args.dataset)
    adapter = adapter_from_config(_single_run_config(args))
    started_at = _now()
    results = run_cases(adapter, cases)
    finished_at = _now()
    report = build_report(
        adapter_name=adapter.name,
        adapter_config=adapter.manifest_config(),
        dataset_path=args.dataset,
        results=results,
        started_at=started_at,
        finished_at=finished_at,
        source_revision=args.source_revision,
    )
    json_path, markdown_path = write_reports(report, args.output_dir)

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
            return _validate_command(args.dataset, args.release_ready)
        if args.command == "schema":
            return _schema_command(args.output)
        if args.command == "run":
            return _run_command(args)
        if args.command == "compare":
            json_path, markdown_path = run_comparison(
                dataset_path=args.dataset,
                config_path=args.config,
                output_dir=args.output_dir,
                source_revision=args.source_revision,
            )
            print(f"Comparison JSON: {json_path}")
            print(f"Comparison Markdown: {markdown_path}")
            return 0
    except (
        AdapterConfigurationError,
        DatasetValidationError,
        ValueError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    raise AssertionError(f"Unhandled command: {args.command}")


def entrypoint() -> None:
    raise SystemExit(main())
