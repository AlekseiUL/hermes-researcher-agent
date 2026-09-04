#!/usr/bin/env python3
"""Audit the public distribution and reachable Git blobs without exposing matches."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
MAX_FILE_BYTES = 15 * 1024 * 1024
SELF = "scripts/audit_public_distribution.py"

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_like_token": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "private_path": re.compile(
        r"/(?:Users|home)/[^/\s]+/(?:Desktop|Documents|Downloads|\.hermes|private|internal|workspace)(?:/|\b)",
        re.I,
    ),
    "private_runtime": re.compile(
        r"(?i)(auth\.json|state\.db|sessions/|memories/|cron/output|gateway\.log)"
    ),
    "owner_private_context": re.compile(
        r"(?i)(Telegram ID|private wiki|client data|customer data)"
    ),
    "accusation": re.compile(
        r"(?i)(\bstolen\b|\btheft\b|\bукрал\b|\bкраж[аеиуой]*\b|\bворов(?:ство|али|ал|ать)?\b)"
    ),
}
QUOTED_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|secret|password|passwd|token|session_string|api_hash)"
    r"\s*[:=]\s*[\"']([^\"']{6,})[\"']"
)
ENV_SECRET_ASSIGNMENT = re.compile(
    r"(?i)^\s*[A-Z0-9_]*(?:API[_-]?KEY|SECRET|PASSWORD|PASSWD|TOKEN|SESSION_STRING|API_HASH)"
    r"\s*=\s*([^\s#]+)"
)
EMAIL = re.compile(
    r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)
SAFE_VALUE_MARKERS = {
    "[redacted]",
    "changeme",
    "dummy",
    "example",
    "fake",
    "fixture",
    "not-a-real",
    "placeholder",
    "sample",
    "test",
    "your-",
}
SAFE_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "invalid", "test"}
FORBIDDEN_EXACT_PATHS = {".env", "auth.json", "state.db"}
FORBIDDEN_PATH_PARTS = {"memories", "sessions", "logs", "workspace", "cron"}
PRIVATE_RUNTIME_ALLOWLIST = {".gitignore", "README.md", "SECURITY.md"}

Finding = tuple[str, str, int]


def _is_safe_example_value(value: str) -> bool:
    lowered = value.strip("\"'").lower()
    return not lowered or any(marker in lowered for marker in SAFE_VALUE_MARKERS)


def scan_text(text: str, label: str) -> list[Finding]:
    if label == SELF:
        return []
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS.items():
            if name == "private_runtime" and label in PRIVATE_RUNTIME_ALLOWLIST:
                continue
            if pattern.search(line):
                findings.append((name, label, line_number))
        for match in QUOTED_SECRET_ASSIGNMENT.finditer(line):
            if not _is_safe_example_value(match.group(2)):
                findings.append(("secret_assignment", label, line_number))
        if Path(label).suffix.lower() in {".env", ".ini", ".toml", ".yaml", ".yml"}:
            match = ENV_SECRET_ASSIGNMENT.search(line)
            if match and not _is_safe_example_value(match.group(1)):
                findings.append(("secret_assignment", label, line_number))
        for address in EMAIL.findall(line):
            domain = address.rsplit("@", 1)[1].lower()
            if domain not in SAFE_EMAIL_DOMAINS:
                findings.append(("email_address", label, line_number))
    return findings


def scan_bytes(data: bytes, label: str) -> list[Finding]:
    if b"\0" in data[:4096] or data.startswith((b"\xff\xd8\xff", b"\x89PNG")):
        printable_runs = re.findall(rb"[\x20-\x7e]{6,}", data)
        text = "\n".join(run.decode("ascii", errors="ignore") for run in printable_runs)
        return scan_text(text, label)
    return scan_text(data.decode("utf-8", errors="ignore"), label)


def worktree_files() -> Iterable[tuple[str, bytes]]:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.stat().st_size > MAX_FILE_BYTES:
            yield rel, b"__OVERSIZED_PUBLIC_FILE__"
            continue
        yield rel, path.read_bytes()


def worktree_findings() -> list[Finding]:
    findings: list[Finding] = []
    for rel, data in worktree_files():
        path = Path(rel)
        if rel in FORBIDDEN_EXACT_PATHS or any(part in FORBIDDEN_PATH_PARTS for part in path.parts):
            findings.append(("forbidden_runtime_path", rel, 0))
        if data == b"__OVERSIZED_PUBLIC_FILE__":
            findings.append(("oversized_unscanned_file", rel, 0))
            continue
        findings.extend(scan_bytes(data, rel))
    return findings


def _git(*args: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=text,
        check=False,
    )


def history_findings() -> tuple[list[Finding], int]:
    probe = _git("rev-parse", "--is-inside-work-tree", text=True)
    if probe.returncode != 0:
        return [], 0
    objects = _git("rev-list", "--objects", "--all", text=True)
    if objects.returncode != 0:
        return [("git_history_scan_failed", "<git>", 0)], 0
    findings: list[Finding] = []
    scanned = 0
    for row in objects.stdout.splitlines():
        object_id, *rest = row.split(" ", 1)
        label = rest[0] if rest else f"<blob:{object_id[:12]}>"
        kind = _git("cat-file", "-t", object_id, text=True)
        if kind.returncode != 0 or kind.stdout.strip() != "blob":
            continue
        size_result = _git("cat-file", "-s", object_id, text=True)
        if size_result.returncode != 0:
            findings.append(("git_history_scan_failed", label, 0))
            continue
        size = int(size_result.stdout.strip())
        if size > MAX_FILE_BYTES:
            findings.append(("oversized_unscanned_history_blob", label, 0))
            continue
        blob = _git("cat-file", "blob", object_id)
        if blob.returncode != 0:
            findings.append(("git_history_scan_failed", label, 0))
            continue
        scanned += 1
        findings.extend(scan_bytes(blob.stdout, label))
    return findings, scanned


def main() -> int:
    findings = worktree_findings()
    history, blobs_scanned = history_findings()
    findings.extend(history)
    unique = sorted(set(findings))
    if unique:
        for category, path, line in unique[:120]:
            location = f"{path}:{line}" if line else path
            print(f"{category} | {location}")
        print(f"findings: {len(unique)} (values suppressed)")
        return 1
    print(f"public distribution audit: ok; reachable_git_blobs_scanned={blobs_scanned}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
