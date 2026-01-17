# Threat Model

LLMGuard targets offline detection of prompt injection, policy bypass, and data exfiltration in LLM application logs.

## Assets

- System prompts and developer instructions
- Secrets and credentials in tool outputs
- Customer PII in prompts, outputs, or logs

## Adversaries

- External users attempting prompt injection
- Insider abuse to extract confidential data
- Automated bots probing for bypasses

## Assumptions

- Logs are available locally
- No network calls to model APIs
- Scanning can run in CI or local environments
