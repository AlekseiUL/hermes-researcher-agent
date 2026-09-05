# Security Scanner Notes

This document records the repository maintainer's triage of generic agent-security scanner findings. It is not a blanket suppression list and does not claim that the repository is free of vulnerabilities.

## Triage: AT-001, AUD-003, and LOG-001

A scan reported `AT-001`, `AUD-003`, and `LOG-001` findings in `scripts/audit_public_distribution.py`, helper tests, and `tools/youtube_research.py`.

The reported locations were reviewed against the source:

- loops in `scripts/audit_public_distribution.py` enumerate files, text lines, patterns, and reachable Git blobs; they are deterministic scanner loops, not an LLM/agent execution loop;
- loops in `scripts/test_*.py` enumerate local test cases or fixture data; they do not make autonomous decisions;
- `subprocess.run()` in the distribution audit invokes an allowlisted `git -C <repository> ...` argument vector with `shell=False` (the default), captures the result, and checks `returncode`;
- temporary writes in YouTube transcript/comment collection are bounded to `TemporaryDirectory` and are removed when the operation exits;
- CLI `print()` calls render command results; they are not a durable audit store.

These findings therefore do not establish an exploitable high-severity vulnerability. A scanner suppression should be narrow, tied to its exact rule/version and location, and retain this justification. Do not disable the rules globally.

## Operation audit events

The repository now exposes privacy-minimized `operation-audit/v1` JSONL events:

- `scripts/audit_public_distribution.py` always emits aggregate start/completion events on `stderr` for worktree and reachable-Git-blob scans;
- `tools/youtube_research.py ... --audit` emits start/completion events on `stderr` around real `yt-dlp` subprocess operations.

Example:

```bash
python3 tools/youtube_research.py search "AI agents" --limit 3 --json --audit \
  2>operation-audit.jsonl
```

The events contain only the component, allowlisted operation name, phase, timeout, outcome, return code, and aggregate counts where applicable. They intentionally omit:

- search queries and target URLs;
- command arguments and local paths;
- tokens, cookies, headers, stdout, stderr, subtitles, and comments;
- user or account identifiers.

Audit events go to `stderr`; normal text or JSON results stay on `stdout`. Audit logging is opt-in for YouTube operations because persistent logs are themselves sensitive artifacts. Store them only where your own retention and access-control policy permits, and do not commit them.

## Reproduction requirements for future reports

A useful report should include:

1. the scanned commit SHA;
2. scanner and rule-set versions;
3. the exact rule definition;
4. a control/data-flow trace showing the alleged agent loop or side effect;
5. a minimal reproduction or exploit path;
6. confirmation that no secret or private value was posted publicly.

Sensitive reports should use GitHub private vulnerability reporting as described in [`SECURITY.md`](SECURITY.md).
