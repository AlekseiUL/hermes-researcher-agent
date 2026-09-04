#!/usr/bin/env python3
"""Guard English/Russian README parity for current public capabilities."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RU_MARKER = "# Hermes Researcher Agent — исследовательский агент для Hermes"

CAPABILITY_PAIRS = (
    ("v0.4.0", "v0.4.0"),
    ("research-run/v1", "research-run/v1"),
    ("Source-lineage checks", "Проверка происхождения источников"),
    ("Counterexample gate", "Поиск контрпримеров"),
    ("MarkItDown", "MarkItDown"),
    ("GitHub", "GitHub"),
    ("Reddit", "Reddit"),
    ("YouTube Research Pack", "YouTube Research Pack"),
    ("youtube-intelligence-stack", "youtube-intelligence-stack"),
    ("PASS_AFTER_FIX", "PASS_AFTER_FIX"),
    ("BLOCKED", "BLOCKED"),
)

YOUTUBE_COMMANDS = (
    "youtube_research.py doctor",
    "youtube_research.py search",
    "youtube_research.py video",
    "youtube_research.py channel",
    "youtube_research.py playlist",
    "youtube_research.py transcript",
    "youtube_research.py comments",
)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    if text.count(RU_MARKER) != 1:
        raise AssertionError("README must contain exactly one Russian-section marker")
    english, russian = text.split(RU_MARKER, 1)

    for english_term, russian_term in CAPABILITY_PAIRS:
        if english_term not in english:
            raise AssertionError(f"English README is missing current capability term: {english_term}")
        if russian_term not in russian:
            raise AssertionError(f"Russian README is missing current capability term: {russian_term}")

    for command in YOUTUBE_COMMANDS:
        if english.count(command) != 1:
            raise AssertionError(f"English README must document exactly one {command} example")
        if russian.count(command) != 1:
            raise AssertionError(f"Russian README must document exactly one {command} example")

    if "## Source coverage at a glance" not in english:
        raise AssertionError("English README is missing source coverage summary")
    if "## Какие источники поддерживаются" not in russian:
        raise AssertionError("Russian README is missing source coverage summary")

    print("bilingual README capability parity: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
