# Security Policy

## Supported scope

This repository contains a public Hermes profile distribution: prompt, skills, templates, and helper scripts.

It should not contain secrets, credentials, private memory, sessions, logs, private research outputs, or scheduled jobs.

## Reporting a vulnerability

If you find a security issue in this repository, open a GitHub issue with a minimal reproduction and avoid posting real secrets or private data.

For issues in Hermes Agent itself, report them to the upstream Hermes Agent project.

## Safety boundaries

The researcher profile is public-source by default. It should not:

- bypass login walls, CAPTCHAs, paywalls, account restrictions, or rate limits;
- use cookies or private account exports without explicit user approval;
- ask users to paste API keys or passwords into chat;
- publish, post, DM, follow, join, buy, register, or start trials without explicit user approval;
- present legal, medical, financial, immigration, or safety-critical conclusions as professional advice.

Users are responsible for their own Hermes provider configuration, gateway credentials, browser backend, and local environment variables.
