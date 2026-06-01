# Contributing

Contributions are welcome if they preserve the safety model:

- public-source research only by default;
- no private data, secrets, cookies, sessions, logs, or owner-specific artifacts;
- no cron jobs enabled by default;
- no scripts that bypass access controls or scrape behind login;
- claims must be source-backed and caveated.

Before opening a pull request, run:

```bash
python3 scripts/audit_public_distribution.py
python3 scripts/validate_skill_frontmatter.py
```
