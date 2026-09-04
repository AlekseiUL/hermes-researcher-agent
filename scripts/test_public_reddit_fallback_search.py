#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "public_reddit_fallback_search.py"
spec = importlib.util.spec_from_file_location("public_reddit_fallback_search", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def must_reject(value: str, expected: str) -> None:
    try:
        module.validate_public_query(value)
    except SystemExit as error:
        assert expected in str(error)
    else:
        raise AssertionError(f"private query was accepted: {expected}")


def main() -> int:
    assert module.validate_public_query("Hermes Agent research workflow") == (
        "Hermes Agent research workflow"
    )
    assert module.validate_public_query("compare 2025 and 2026 releases") == (
        "compare 2025 and 2026 releases"
    )
    must_reject("contact owner" + "@example.com", "email address")
    must_reject("inspect /" + "Users/person/private", "local path")
    must_reject("inspect C:" + "\\private\\notes", "local path")
    must_reject("key gh" + "p_" + ("A" * 24), "API/token-shaped value")
    must_reject("call +1 202 555 0199", "phone-like number")

    assert module.validate_limit(1) == 1
    assert module.validate_limit(25) == 25
    for invalid in (0, 26):
        try:
            module.validate_limit(invalid)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"invalid limit accepted: {invalid}")

    items = [
        {"reddit_url": "https://reddit.com/r/test/comments/one"},
        {"reddit_url": "https://reddit.com/r/test/comments/one"},
    ]
    assert len(module.dedupe(items)) == 1
    print(json.dumps({"ok": True, "tested": "public_reddit_fallback_search"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())