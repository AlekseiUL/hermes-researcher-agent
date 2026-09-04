#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "github_traction_check.py"
spec = importlib.util.spec_from_file_location("github_traction_check", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fake_request(path_or_url: str, token=None, timeout=25):
    if path_or_url == "/repos/example/project":
        return {
            "full_name": "example/project",
            "description": "Example project",
            "html_url": "https://github.com/example/project",
            "homepage": "",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-03T00:00:00Z",
            "pushed_at": "2026-01-02T00:00:00Z",
            "default_branch": "main",
            "fork": False,
            "archived": False,
            "is_template": False,
            "visibility": "public",
            "stargazers_count": 12,
            "subscribers_count": 3,
            "forks_count": 2,
            "open_issues_count": 1,
            "license": {"spdx_id": "MIT"},
            "language": "Python",
            "topics": ["research", "automation"],
        }, {"status": 200, "rate_remaining": "55", "rate_reset": "0"}
    if path_or_url == "/repos/example/project/releases?per_page=5":
        return [{"tag_name": "v0.1.0", "name": "v0.1.0", "published_at": "2026-01-02T00:00:00Z", "prerelease": False, "html_url": "https://github.com/example/project/releases/tag/v0.1.0"}], {"status": 200, "rate_remaining": "54", "rate_reset": "0"}
    if path_or_url == "/repos/example/project/branches?per_page=10":
        return [{"name": "main", "protected": False}], {"status": 200, "rate_remaining": "53", "rate_reset": "0"}
    if path_or_url == "/repos/example/project/commits/main":
        return {"sha": "abcdef1234567890", "commit": {"committer": {"date": "2026-01-02T00:00:00Z"}, "message": "initial release"}, "author": {"login": "example"}}, {"status": 200, "rate_remaining": "52", "rate_reset": "0"}
    raise AssertionError(path_or_url)


def main() -> int:
    setattr(module, "request_json", fake_request)
    assert module.parse_repo("https://github.com/example/project.git") == ("example", "project")
    for invalid in ("https://example.com/example/project", "example/project/extra", "bad owner/project"):
        try:
            module.parse_repo(invalid)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"invalid repository accepted: {invalid}")
    data = module.collect("example", "project")
    assert data["facts"]["name_with_owner"] == "example/project"
    assert data["facts"]["license"] == "MIT"
    assert data["facts"]["recent_releases"][0]["tag_name"] == "v0.1.0"
    assert "GitHub Traction Check" in module.markdown_report(data)
    assert "Stars / forks / watchers: 12 / 2 / 3" in module.markdown_report(data)

    def private_request(path_or_url: str, token=None, timeout=25):
        if path_or_url == "/repos/example/private-project":
            assert token is None
            return {
                "full_name": "example/private-project",
                "visibility": "private",
                "private": True,
            }, {"status": 200, "rate_remaining": "55", "rate_reset": "0"}
        raise AssertionError(path_or_url)

    setattr(module, "request_json", private_request)
    try:
        module.collect("example", "private-project", token="fixture-token")
    except module.FetchError as error:
        assert "not public" in str(error)
    else:
        raise AssertionError("private repository metadata was accepted")
    print(json.dumps({"ok": True, "tested": "github_traction_check"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
