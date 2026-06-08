#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "source_reach_doctor.py"
spec = importlib.util.spec_from_file_location("source_reach_doctor", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def fake_fetch(url: str, timeout: int = 20, max_bytes: int = 6000):
    if "r.jina.ai/http://example.com" in url:
        return 200, "Example Domain"
    if "api.github.com/repos/octocat/Hello-World" in url:
        return 200, json.dumps({"full_name": "octocat/Hello-World"})
    if "reddit.com/r/LocalLLaMA/hot.json" in url:
        return 403, "blocked"
    if "r.jina.ai/http://old.reddit.com/r/LocalLLaMA/" in url:
        return 200, "LocalLLaMA via reader"
    raise AssertionError(url)


def main() -> int:
    checks = []
    module.check_jina(checks, fetcher=fake_fetch)
    module.check_github_public_api(checks, fetcher=fake_fetch)
    module.check_reddit_public_fallback(checks, fetcher=fake_fetch)
    assert [check.status for check in checks] == ["PASS", "PASS", "PASS"], checks
    assert checks[2].name == "Reddit public fallback"
    assert "Jina/old.reddit fallback works" in checks[2].note

    module.check_markitdown(
        checks,
        runner=lambda args, timeout: (0, "markitdown 0.1.test") if args[:2] == ["/usr/bin/markitdown", "--version"] else (1, "unexpected"),
        finder=lambda name: "/usr/bin/markitdown" if name == "markitdown" else None,
    )
    assert checks[-1].name == "MarkItDown document ingestion"
    assert checks[-1].status == "PASS"

    module_fallback_checks = []
    module.check_markitdown(
        module_fallback_checks,
        runner=lambda args, timeout: (0, "python module available") if args[:2] == ["python3", "-c"] else (1, "unexpected"),
        finder=lambda name: None,
    )
    assert module_fallback_checks[0].status == "PASS"
    assert "Python module available" in module_fallback_checks[0].note

    fallback_checks = []
    module.check_markitdown(
        fallback_checks,
        runner=lambda args, timeout: (1, "missing"),
        finder=lambda name: None,
    )
    assert fallback_checks[0].status == "WARN"

    text, code = module.verdict(checks)
    assert code == 0
    assert text.startswith("PASS")

    degraded = [module.Check("GitHub public API", "WARN", "HTTP 403")]
    text, code = module.verdict(degraded)
    assert code == 0
    assert "PASS_AFTER_FIX" in text

    redacted = module.redact("token=abc123456 secret: qwerty password=hidden Authorization: Bearer dont_print_me")
    assert "abc123456" not in redacted
    assert "qwerty" not in redacted
    assert "hidden" not in redacted
    assert "dont_print_me" not in redacted
    print(json.dumps({"ok": True, "tested": "source_reach_doctor"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
