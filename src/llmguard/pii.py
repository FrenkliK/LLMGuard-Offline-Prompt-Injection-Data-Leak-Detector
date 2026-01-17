"""PII detection helpers."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class PIIFinding:
    pii_type: str
    evidence: str
    severity: str


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?[0-9][0-9\-\s().]{7,}[0-9]")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
CREDIT_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")


def _luhn_check(number: str) -> bool:
    digits = [int(ch) for ch in number if ch.isdigit()]
    if len(digits) < 13:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def detect_pii(text: str) -> list[PIIFinding]:
    findings: list[PIIFinding] = []
    for match in EMAIL_RE.finditer(text):
        findings.append(PIIFinding("email", match.group(0), "high"))
    for match in PHONE_RE.finditer(text):
        findings.append(PIIFinding("phone", match.group(0), "medium"))
    for match in IBAN_RE.finditer(text):
        findings.append(PIIFinding("iban", match.group(0), "high"))
    for match in CREDIT_CARD_RE.finditer(text):
        candidate = match.group(0)
        if _luhn_check(candidate):
            findings.append(PIIFinding("credit_card", candidate, "critical"))
    return findings
