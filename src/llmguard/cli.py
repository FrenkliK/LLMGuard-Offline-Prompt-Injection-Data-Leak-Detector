"""Command-line interface for LLMGuard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from llmguard.reporting import (
    to_html,
    to_html_collection,
    to_markdown,
    to_markdown_collection,
)
from llmguard.scanning import scan_directory, scan_path, scan_text


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLMGuard offline scanner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="scan a file or directory")
    scan_parser.add_argument("target", type=Path, help="file or directory to scan")
    scan_parser.add_argument("--format", choices=["json", "markdown", "html"], default="json")
    scan_parser.add_argument("--no-ml", action="store_true", help="disable ML classifier")

    text_parser = subparsers.add_parser("scan-text", help="scan raw text")
    text_parser.add_argument("text", help="text to scan")
    text_parser.add_argument("--format", choices=["json", "markdown", "html"], default="json")
    text_parser.add_argument("--no-ml", action="store_true", help="disable ML classifier")

    return parser.parse_args()


def _render(report: dict, output_format: str) -> str:
    if output_format == "markdown":
        if "reports" in report:
            return to_markdown_collection(report["reports"])
        return to_markdown(report)
    if output_format == "html":
        if "reports" in report:
            return to_html_collection(report["reports"])
        return to_html(report)
    return json.dumps(report, indent=2)


def main() -> None:
    args = _parse_args()
    enable_ml = not args.no_ml

    if args.command == "scan":
        target = args.target
        if target.is_dir():
            reports = scan_directory(target, enable_ml=enable_ml)
            payload = {"reports": reports}
        else:
            payload = scan_path(target, enable_ml=enable_ml)
        print(_render(payload, args.format))
        return

    if args.command == "scan-text":
        report = scan_text(args.text, enable_ml=enable_ml)
        print(_render(report, args.format))
        return


if __name__ == "__main__":
    main()
