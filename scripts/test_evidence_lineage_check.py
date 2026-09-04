#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "evidence_lineage_check.py"
spec = importlib.util.spec_from_file_location("evidence_lineage_check", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def must_fail(data: dict, expected: str) -> None:
    try:
        module.validate_run(data)
    except module.ValidationError as error:
        assert expected in str(error), (expected, str(error))
    else:
        raise AssertionError(f"expected validation failure containing: {expected}")


def main() -> int:
    example_path = ROOT / "examples" / "research-run-source-lineage.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    result = module.validate_run(example)
    assert result["ok"] is True
    assert result["source_count"] == 5
    assert result["lineage_count"] == 3
    assert result["duplicate_copies_collapsed"] == 2

    copied_headlines = copy.deepcopy(example)
    copied_headlines["sources"][3]["lineage_id"] = "vendor-announcement-lineage"
    copied_headlines["claims"][0]["evidence_source_ids"] = [
        "vendor-announcement",
        "news-copy-one",
        "news-copy-two",
        "public-api-state",
    ]
    must_fail(copied_headlines, "two independent source lineages")

    inaccessible = copy.deepcopy(example)
    inaccessible["sources"][3]["access_state"] = "login_required"
    must_fail(inaccessible, "uses inaccessible evidence")

    discovery_only = copy.deepcopy(example)
    discovery_only["sources"][3]["source_class"] = "discovery"
    must_fail(discovery_only, "uses discovery-only material as evidence")

    false_counterexample = copy.deepcopy(example)
    false_counterexample["claims"][0]["counterexample_source_ids"] = []
    must_fail(false_counterexample, "says counterexample found but cites none")

    overlapping_counterexample = copy.deepcopy(example)
    overlapping_counterexample["claims"][0]["counterexample_source_ids"] = [
        "vendor-announcement"
    ]
    must_fail(overlapping_counterexample, "same sources as evidence and counterexamples")

    searched_none = copy.deepcopy(example)
    searched_none["claims"][0]["counterexample_source_ids"] = []
    searched_none["claims"][0]["counterexample_status"] = "none_found"
    searched_none["claims"][0]["counterexample_note"] = (
        "Checked public issues and independent reviews; no direct counterexample was found."
    )
    assert module.validate_run(searched_none)["ok"] is True

    credential_url = copy.deepcopy(example)
    credential_url["sources"][0]["url"] = "https://user:password@example.com/private"
    must_fail(credential_url, "without credentials")

    local_url = copy.deepcopy(example)
    local_url["sources"][0]["url"] = "http://127.0.0.1:8080/private"
    must_fail(local_url, "non-public IP address")

    internal_url = copy.deepcopy(example)
    internal_url["sources"][0]["url"] = "https://research.internal/report"
    must_fail(internal_url, "internal host")

    secret_query = copy.deepcopy(example)
    secret_query["sources"][0]["url"] = "https://example.com/report?token=not-a-real-token"
    must_fail(secret_query, "sensitive query fields")

    print(json.dumps({"ok": True, "tested": "evidence_lineage_check"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
