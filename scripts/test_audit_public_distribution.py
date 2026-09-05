#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_public_distribution.py"
spec = importlib.util.spec_from_file_location("audit_public_distribution", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def categories(text: str, label: str = "fixture.txt") -> set[str]:
    return {finding[0] for finding in module.scan_text(text, label)}


def main() -> int:
    private_key = "-----BEGIN " + "PRIVATE KEY-----\nfixture\n-----END PRIVATE KEY-----"
    assert "private_key" in categories(private_key)

    github_token = "gh" + "p_" + ("A" * 24)
    assert "github_token" in categories(github_token)

    assignment = "API_KEY" + ' = "real-looking-value-123456"'
    assert "secret_assignment" in categories(assignment, "config.py")

    env_assignment = "SERVICE_TOKEN" + "=real-looking-value-123456"
    assert "secret_assignment" in categories(env_assignment, "settings.env")

    private_path = "/" + "Users" + "/person/Desktop/private.txt"
    assert "private_path" in categories(private_path)

    assert "email_address" not in categories("owner@example.com")
    assert module.scan_text("OPENAI_API_KEY=", ".env.EXAMPLE") == []

    binary = b"\xff\xd8\xff" + b"\x00" * 30 + github_token.encode("ascii")
    assert "github_token" in {finding[0] for finding in module.scan_bytes(binary, "image.jpg")}

    stderr = io.StringIO()
    with redirect_stderr(stderr):
        module.audit_event("completed", outcome="success", finding_count=0)
    event = json.loads(stderr.getvalue())
    assert event == {
        "component": "public_distribution_audit",
        "finding_count": 0,
        "operation": "public_distribution_scan",
        "outcome": "success",
        "phase": "completed",
        "schema_version": "operation-audit/v1",
    }

    print(json.dumps({"ok": True, "tested": "audit_public_distribution"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())