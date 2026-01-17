"""Detectors for prompt injection and policy bypass patterns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import re


@dataclass
class Finding:
    category: str
    pattern: str
    evidence: str
    severity: str


PROMPT_INJECTION_PATTERNS = [
    ("prompt_injection", r"ignore (all|previous|prior) instructions", "high"),
    ("prompt_injection", r"system prompt", "medium"),
    ("prompt_injection", r"reveal (the )?(system|developer) instructions", "high"),
    ("prompt_injection", r"you are now", "medium"),
    ("prompt_injection", r"override (safety|policy)", "high"),
]

POLICY_BYPASS_PATTERNS = [
    ("policy_bypass", r"jailbreak", "high"),
    ("policy_bypass", r"do anything now", "high"),
    ("policy_bypass", r"bypass (filters|guardrails)", "high"),
    ("policy_bypass", r"dev mode", "medium"),
]

EXFILTRATION_PATTERNS = [
    ("data_exfiltration", r"exfiltrate", "high"),
    ("data_exfiltration", r"send (all|the) data", "high"),
    ("data_exfiltration", r"export (the )?database", "high"),
    ("data_exfiltration", r"leak (credentials|secrets)", "high"),
]


def _run_patterns(text: str, patterns: Iterable[tuple[str, str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    for category, pattern, severity in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            findings.append(
                Finding(
                    category=category,
                    pattern=pattern,
                    evidence=match.group(0),
                    severity=severity,
                )
            )
    return findings


def detect_prompt_injection(text: str) -> list[Finding]:
    return _run_patterns(text, PROMPT_INJECTION_PATTERNS)


def detect_policy_bypass(text: str) -> list[Finding]:
    return _run_patterns(text, POLICY_BYPASS_PATTERNS)


def detect_exfiltration(text: str) -> list[Finding]:
    return _run_patterns(text, EXFILTRATION_PATTERNS)


def detect_all(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for detector in (detect_prompt_injection, detect_policy_bypass, detect_exfiltration):
        findings.extend(detector(text))
    return findings
