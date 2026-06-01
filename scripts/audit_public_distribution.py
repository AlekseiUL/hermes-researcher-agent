#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skip_dirs = {".git", "__pycache__", ".pytest_cache"}
patterns = {
    "private_path": re.compile(r"/Users/[^/\s]+|/home/[^/\s]+/(?:private|internal|workspace)", re.I),
    "secret_assignment": re.compile(
        r"(?i)(api[_-]?key|secret|password|passwd|token|session_string|api_hash)\s*[:=]\s*[\"'][^\"']{6,}[\"']"
    ),
    "private_runtime": re.compile(r"(?i)(auth\.json|state\.db|sessions/|memories/|cron/output|gateway\.log)"),
    "owner_private_context": re.compile(r"(?i)(Telegram ID|private wiki|client data|customer data)"),
    "accusation": re.compile(r"(?i)(\bstolen\b|\btheft\b|\bукрал\b|\bкраж[аеиуой]*\b|\bворов(?:ство|али|ал|ать)?\b)"),
}
findings = []
for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue
    if any(part in skip_dirs for part in path.parts):
        continue
    rel = path.relative_to(root).as_posix()
    if path.suffix in {".pyc", ".pyo"}:
        findings.append(("bytecode", rel, 0, "compiled bytecode file"))
        continue
    data = path.read_bytes()
    if b"\0" in data[:4096]:
        continue
    text = data.decode("utf-8", errors="ignore")
    for i, line in enumerate(text.splitlines(), 1):
        for name, rx in patterns.items():
            # Public docs and this scanner may intentionally mention excluded strings.
            if rel == "scripts/audit_public_distribution.py":
                continue
            if name == "private_runtime" and rel in {".gitignore", "README.md", "SECURITY.md"}:
                continue
            if rx.search(line):
                findings.append((name, rel, i, line[:220]))

if findings:
    for item in findings[:120]:
        print(" | ".join(map(str, item)))
    print(f"findings: {len(findings)}")
    sys.exit(1)
print("public distribution audit: ok")
