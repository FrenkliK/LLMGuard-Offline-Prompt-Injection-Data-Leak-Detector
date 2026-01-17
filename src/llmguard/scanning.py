"""Scanning orchestration."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from llmguard import detectors
from llmguard.ml import classify
from llmguard.pii import detect_pii


SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _aggregate_severity(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "none"
    max_level = max(SEVERITY_ORDER.get(item["severity"], 0) for item in findings)
    for name, level in SEVERITY_ORDER.items():
        if level == max_level:
            return name
    return "none"


def scan_text(text: str, enable_ml: bool = True) -> dict[str, Any]:
    raw_findings = detectors.detect_all(text)
    pii_findings = detect_pii(text)

    findings = [asdict(finding) for finding in raw_findings]
    pii = [asdict(finding) for finding in pii_findings]

    ml_results = None
    if enable_ml:
        ml_results = [asdict(result) for result in classify([text])]

    summary = {
        "findings_count": len(findings),
        "pii_count": len(pii),
        "overall_severity": _aggregate_severity(findings + pii),
    }

    return {
        "summary": summary,
        "findings": findings,
        "pii": pii,
        "ml": ml_results,
    }


def scan_path(path: Path, enable_ml: bool = True) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    report = scan_text(text, enable_ml=enable_ml)
    report["source"] = str(path)
    return report


def scan_directory(directory: Path, enable_ml: bool = True) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file():
            reports.append(scan_path(file_path, enable_ml=enable_ml))
    return reports
