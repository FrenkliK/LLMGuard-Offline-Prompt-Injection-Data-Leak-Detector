"""Report generation utilities."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any


def _normalize_findings(items: list[Any]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in items:
        if is_dataclass(item):
            normalized.append(asdict(item))
        else:
            normalized.append(dict(item))
    return normalized


def _markdown_section(report: dict[str, Any], heading_level: int = 2) -> str:
    summary = report["summary"]
    findings = report["findings"]
    pii = report["pii"]

    prefix = "#" * heading_level
    lines = [f"{prefix} Summary"]
    for key, value in summary.items():
        lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
    lines.append("")

    lines.append(f"{prefix} Findings")
    if not findings:
        lines.append("No prompt injection or policy bypass findings detected.")
    else:
        for finding in findings:
            lines.append(
                f"- **{finding['category']}** ({finding['severity']}): {finding['evidence']}"
            )
    lines.append("")

    lines.append(f"{prefix} PII")
    if not pii:
        lines.append("No PII findings detected.")
    else:
        for finding in pii:
            lines.append(f"- **{finding['pii_type']}** ({finding['severity']}): {finding['evidence']}")

    return "\n".join(lines)


def to_markdown(report: dict[str, Any]) -> str:
    header = ["# LLMGuard Security Report", "", f"Generated: {datetime.utcnow().isoformat()} UTC", ""]
    return "\n".join(header + [_markdown_section(report, heading_level=2)])


def _html_section(report: dict[str, Any]) -> str:
    summary_items = "".join(
        f"<li><strong>{key.replace('_', ' ').title()}</strong>: {value}</li>"
        for key, value in report["summary"].items()
    )
    findings_items = "".join(
        f"<li><strong>{finding['category']}</strong> ({finding['severity']}): {finding['evidence']}</li>"
        for finding in report["findings"]
    )
    pii_items = "".join(
        f"<li><strong>{finding['pii_type']}</strong> ({finding['severity']}): {finding['evidence']}</li>"
        for finding in report["pii"]
    )

    return f"""
  <div class=\"card\">
    <h3>Summary</h3>
    <ul>{summary_items}</ul>
  </div>
  <h3>Findings</h3>
  <ul>{findings_items or '<li>No prompt injection or policy bypass findings detected.</li>'}</ul>
  <h3>PII</h3>
  <ul>{pii_items or '<li>No PII findings detected.</li>'}</ul>
"""


def to_html(report: dict[str, Any]) -> str:
    section = _html_section(report)
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>LLMGuard Security Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    h1, h2, h3 {{ color: #1f2937; }}
    .card {{ background: #f9fafb; padding: 1rem; border-radius: 8px; }}
  </style>
</head>
<body>
  <h1>LLMGuard Security Report</h1>
  <p>Generated: {datetime.utcnow().isoformat()} UTC</p>
  {section}
</body>
</html>
"""


def to_markdown_collection(reports: list[dict[str, Any]]) -> str:
    lines = ["# LLMGuard Security Report", ""]
    for report in reports:
        source = report.get("source", "unknown")
        lines.append(f"## Source: {source}")
        lines.append("")
        lines.append(_markdown_section(report, heading_level=3))
        lines.append("")
    return "\n".join(lines).strip()


def to_html_collection(reports: list[dict[str, Any]]) -> str:
    sections = []
    for report in reports:
        source = report.get("source", "unknown")
        sections.append(f"<section><h2>Source: {source}</h2>{_html_section(report)}</section>")
    sections_html = "\n".join(sections)
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>LLMGuard Security Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    h1, h2, h3 {{ color: #1f2937; }}
    .card {{ background: #f9fafb; padding: 1rem; border-radius: 8px; }}
    section {{ margin-bottom: 2rem; }}
  </style>
</head>
<body>
  <h1>LLMGuard Security Report</h1>
  <p>Generated: {datetime.utcnow().isoformat()} UTC</p>
  {sections_html}
</body>
</html>
"""


def as_json(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "summary": report["summary"],
        "findings": _normalize_findings(report["findings"]),
        "pii": _normalize_findings(report["pii"]),
        "ml": report.get("ml"),
    }
