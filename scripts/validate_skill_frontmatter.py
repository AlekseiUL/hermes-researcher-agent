#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []


def frontmatter_value(fm_text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+?)\s*$", fm_text)
    if not match:
        return None
    return match.group(1).strip().strip('"\'')


for path in sorted(root.glob("skills/*/SKILL.md")):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        errors.append(f"{path}: missing opening frontmatter delimiter at byte 0")
        continue
    match = re.search(r"\n---\s*\n", content[3:])
    if not match:
        errors.append(f"{path}: missing closing frontmatter delimiter")
        continue
    fm_text = content[3 : match.start() + 3]
    for key in ("name", "description"):
        value = frontmatter_value(fm_text, key)
        if not value:
            errors.append(f"{path}: missing {key}")
    description = frontmatter_value(fm_text, "description") or ""
    if len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 chars")
    body = content[match.end() + 3 :].strip()
    if not body:
        errors.append(f"{path}: empty body")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("skill frontmatter: ok")
