#!/usr/bin/env python3
"""Public GitHub traction check for researcher agents.

Given OWNER/REPO, collect public GitHub metadata and print either JSON or a
short Markdown evidence brief.

Public-only by default. Uses GITHUB_TOKEN only if already present in the local
environment to raise rate limits; never prints token values.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

API = "https://api.github.com"
UA = "hermes-public-researcher-github-traction/0.2"


class FetchError(RuntimeError):
    pass


def parse_repo(value: str) -> Tuple[str, str]:
    value = value.strip().removesuffix(".git")
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/")
    elif value.startswith("http://") or value.startswith("https://"):
        raise SystemExit("only github.com URLs are supported; use OWNER/REPO or https://github.com/OWNER/REPO")
    parts = [p for p in value.split("/") if p]
    if len(parts) != 2:
        raise SystemExit("repo must be OWNER/REPO or https://github.com/OWNER/REPO")
    return parts[0], parts[1]


def request_json(path_or_url: str, token: Optional[str] = None, timeout: int = 25) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset = response.headers.get("X-RateLimit-Reset")
            return json.loads(raw.decode("utf-8", "replace")), {
                "status": getattr(response, "status", None),
                "rate_remaining": remaining,
                "rate_reset": reset,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        raise FetchError(f"GitHub API HTTP {exc.code} for {url}: {body}") from exc
    except Exception as exc:  # noqa: BLE001 - CLI should report degraded source, not traceback by default
        raise FetchError(f"GitHub API fetch failed for {url}: {type(exc).__name__}: {exc}") from exc


def collect(owner: str, repo: str, token: Optional[str] = None) -> Dict[str, Any]:
    collected_at = dt.datetime.now(dt.timezone.utc).isoformat()
    result: Dict[str, Any] = {
        "repo": f"{owner}/{repo}",
        "collected_at": collected_at,
        "policy": "public GitHub metadata only; no private repo access required",
        "sources": [],
        "errors": [],
    }

    metadata, meta_headers = request_json(f"/repos/{owner}/{repo}", token=token)
    result["sources"].append({"type": "github_repo_api", "path": f"/repos/{owner}/{repo}", **meta_headers})
    default_branch = (metadata.get("default_branch") or "main")

    releases: List[Dict[str, Any]] = []
    try:
        release_data, headers = request_json(f"/repos/{owner}/{repo}/releases?per_page=5", token=token)
        result["sources"].append({"type": "github_releases_api", "path": f"/repos/{owner}/{repo}/releases?per_page=5", **headers})
        releases = [
            {
                "tag_name": r.get("tag_name"),
                "name": r.get("name"),
                "published_at": r.get("published_at"),
                "prerelease": r.get("prerelease"),
                "url": r.get("html_url"),
            }
            for r in release_data[:5]
        ]
    except FetchError as exc:
        result["errors"].append(str(exc))

    branches: List[Dict[str, Any]] = []
    try:
        branch_data, headers = request_json(f"/repos/{owner}/{repo}/branches?per_page=10", token=token)
        result["sources"].append({"type": "github_branches_api", "path": f"/repos/{owner}/{repo}/branches?per_page=10", **headers})
        branches = [{"name": b.get("name"), "protected": b.get("protected")} for b in branch_data]
    except FetchError as exc:
        result["errors"].append(str(exc))

    latest_commit: Dict[str, Any] = {}
    try:
        commit_data, headers = request_json(f"/repos/{owner}/{repo}/commits/{urllib.parse.quote(default_branch)}", token=token)
        result["sources"].append({"type": "github_commit_api", "path": f"/repos/{owner}/{repo}/commits/{default_branch}", **headers})
        commit = commit_data.get("commit") or {}
        latest_commit = {
            "sha": commit_data.get("sha", "")[:12],
            "date": (commit.get("committer") or {}).get("date"),
            "message": (commit.get("message") or "").splitlines()[0][:160],
            "author_login": (commit_data.get("author") or {}).get("login"),
        }
    except FetchError as exc:
        result["errors"].append(str(exc))

    open_issues = metadata.get("open_issues_count")
    topics = metadata.get("topics") or []
    pushed_at = metadata.get("pushed_at")
    updated_at = metadata.get("updated_at")
    license_info = metadata.get("license") or {}

    result["facts"] = {
        "name_with_owner": metadata.get("full_name"),
        "description": metadata.get("description"),
        "url": metadata.get("html_url"),
        "homepage": metadata.get("homepage"),
        "created_at": metadata.get("created_at"),
        "updated_at": updated_at,
        "pushed_at": pushed_at,
        "default_branch": default_branch,
        "is_fork": metadata.get("fork"),
        "is_archived": metadata.get("archived"),
        "is_template": metadata.get("is_template"),
        "visibility": metadata.get("visibility"),
        "stars": metadata.get("stargazers_count"),
        "watchers": metadata.get("subscribers_count"),
        "forks": metadata.get("forks_count"),
        "open_issues_count": open_issues,
        "license": license_info.get("spdx_id"),
        "primary_language": metadata.get("language"),
        "topics": topics,
        "latest_commit": latest_commit,
        "recent_releases": releases,
        "branches": branches,
    }

    signals: List[str] = []
    caveats: List[str] = []
    stars = metadata.get("stargazers_count") or 0
    forks = metadata.get("forks_count") or 0
    release_count = len(releases)
    if stars >= 1000:
        signals.append("High public attention by GitHub stars. Treat as popularity proxy, not usage proof.")
    elif stars >= 50:
        signals.append("Some public attention by GitHub stars. Still not usage proof.")
    else:
        signals.append("Low or early GitHub star signal. Do not infer adoption from stars.")
    if forks > 0:
        signals.append("Forks exist, which may indicate experimentation or reuse.")
    if release_count:
        signals.append("Release artifacts exist; inspect release notes for concrete shipped changes.")
    else:
        caveats.append("No GitHub releases found in the latest release API page.")
    if metadata.get("archived"):
        caveats.append("Repository is archived; treat as inactive unless forked/continued elsewhere.")
    if not license_info.get("spdx_id"):
        caveats.append("No SPDX license detected by GitHub API.")
    if open_issues and stars and open_issues > max(20, stars * 0.2):
        caveats.append("Open issue count is high relative to star count; inspect issue quality before adoption.")

    result["interpretation"] = {
        "signals": signals,
        "caveats": caveats,
        "recommended_next_checks": [
            "Read README and install path, not just metadata.",
            "Inspect recent issues/PRs for real user pain and maintainer response.",
            "Check package registries or docs if adoption/usage proof matters.",
            "Run a local smoke test before recommending adoption.",
        ],
    }
    return result


def markdown_report(data: Dict[str, Any]) -> str:
    facts = data.get("facts", {})
    lines = [
        f"# GitHub Traction Check — {facts.get('name_with_owner') or data.get('repo')}",
        "",
        f"Collected: {data.get('collected_at')}",
        "",
        "## Verdict",
        "",
        "This is a metadata-level traction check, not proof of real usage. Use it to decide whether deeper README, issue, package, and smoke-test review is worth doing.",
        "",
        "## Facts",
        "",
        f"- URL: {facts.get('url')}",
        f"- Description: {facts.get('description')}",
        f"- Created: {facts.get('created_at')}",
        f"- Updated: {facts.get('updated_at')}",
        f"- Pushed: {facts.get('pushed_at')}",
        f"- Stars / forks / watchers: {facts.get('stars')} / {facts.get('forks')} / {facts.get('watchers')}",
        f"- Open issues: {facts.get('open_issues_count')}",
        f"- License: {facts.get('license')}",
        f"- Language: {facts.get('primary_language')}",
        f"- Default branch: {facts.get('default_branch')}",
        f"- Topics: {', '.join(facts.get('topics') or []) or 'none'}",
        "",
        "## Latest commit",
        "",
    ]
    latest = facts.get("latest_commit") or {}
    if latest:
        lines.extend([
            f"- SHA: {latest.get('sha')}",
            f"- Date: {latest.get('date')}",
            f"- Message: {latest.get('message')}",
            f"- Author: {latest.get('author_login')}",
            "",
        ])
    releases = facts.get("recent_releases") or []
    lines.extend(["## Recent releases", ""])
    if releases:
        for release in releases:
            lines.append(f"- {release.get('tag_name')} — {release.get('published_at')} — {release.get('url')}")
    else:
        lines.append("- No releases returned by GitHub releases API.")
    lines.extend(["", "## Interpretation", ""])
    for signal in (data.get("interpretation") or {}).get("signals", []):
        lines.append(f"- {signal}")
    caveats = (data.get("interpretation") or {}).get("caveats", [])
    lines.extend(["", "## Caveats", ""])
    if caveats:
        for caveat in caveats:
            lines.append(f"- {caveat}")
    else:
        lines.append("- No metadata-level caveats beyond the standard limitation: GitHub metrics are proxies, not usage proof.")
    lines.extend(["", "## Recommended next checks", ""])
    for check in (data.get("interpretation") or {}).get("recommended_next_checks", []):
        lines.append(f"- {check}")
    if data.get("errors"):
        lines.extend(["", "## Degraded coverage", ""])
        for error in data["errors"]:
            lines.append(f"- {error}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect public GitHub traction metadata for OWNER/REPO.")
    parser.add_argument("repo", help="OWNER/REPO or https://github.com/OWNER/REPO")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    parser.add_argument("--token-env", default="GITHUB_TOKEN", help="optional token env var name (default: GITHUB_TOKEN)")
    args = parser.parse_args()

    owner, repo = parse_repo(args.repo)
    token = os.getenv(args.token_env) or None
    try:
        data = collect(owner, repo, token=token)
    except FetchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(markdown_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
