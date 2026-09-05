# Security Policy

## Supported scope

This repository contains a public Hermes profile distribution: prompt, skills, templates, and helper scripts.

It should not contain secrets, credentials, private memory, sessions, logs, private research outputs, or scheduled jobs.

## Reporting a vulnerability

If the issue involves secrets, credentials, private data, or an exploit path, do **not** paste sensitive material into a public issue. Use GitHub's private vulnerability reporting / Security Advisories when available, or open a minimal public issue that says private details are available to maintainers.

For non-sensitive bugs, open a GitHub issue with a minimal reproduction.

Generic scanner reports should include the scanned commit SHA, scanner and
rule-set versions, rule definition, and a reproducible control/data-flow trace.
See [`SECURITY-SCANNER-NOTES.md`](SECURITY-SCANNER-NOTES.md) for the current
triage and the privacy-minimized operation-audit contract.

For issues in Hermes Agent itself, report them to the upstream Hermes Agent project.

## Safety boundaries

The researcher profile is public-source by default. It should not:

- bypass login walls, CAPTCHAs, paywalls, account restrictions, or rate limits;
- use cookies or private account exports without explicit user approval;
- ask users to paste API keys or passwords into chat;
- publish, post, DM, follow, join, buy, register, or start trials without explicit user approval;
- present legal, medical, financial, immigration, or safety-critical conclusions as professional advice.

Users are responsible for their own Hermes provider configuration, gateway credentials, browser backend, and local environment variables.
