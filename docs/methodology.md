# Methodology

LLMGuard combines heuristics with optional ML classification.

## Detectors

- Regex patterns for prompt injection, policy bypass, and exfiltration
- PII detection with offline patterns and Luhn checks
- Optional TF-IDF + linear classifier for suspicious intent

## Scoring

Severity is aggregated from findings to provide an overall risk signal.
