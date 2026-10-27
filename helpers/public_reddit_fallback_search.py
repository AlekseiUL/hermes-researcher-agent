#!/usr/bin/env python3
"""Public Reddit fallback search for research agents.

Purpose: when reddit.com public JSON returns 401/403, do not treat it as
"no signal". Search public archive fallbacks best-effort, then return normalized
candidates for later live browser/web verification.

No cookies, no login, no secrets, no private Reddit/session scraping.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List

UA = "hermes-public-researcher/0.1 (+public-source research; no cookies)"
PRIVATE_QUERY_PATTERNS = {
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "local path": re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\)"),
    "API/token-shaped value": re.compile(
        r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|"
        r"xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})"
    ),
    "phone-like number": re.compile(r"(?<!\d)\+?\d[\d ()-]{8,}\d(?!\d)"),
}


def validate_public_query(query: str) -> str:
    query = query.strip()
    if not query:
        raise SystemExit("query must not be empty")
    if len(query) > 300:
        raise SystemExit("query is too long; keep public fallback queries under 301 characters")
    for label, pattern in PRIVATE_QUERY_PATTERNS.items():
        if pattern.search(query):
            raise SystemExit(f"query looks like it contains a {label}; refusing public transmission")
    return query


def validate_limit(value: int) -> int:
    if not 1 <= value <= 25:
        raise SystemExit("limit must be between 1 and 25")
    return value


def fetch_json(url: str, timeout: int = 20) -> Dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json,text/plain;q=0.9,*/*;q=0.8"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        return {"ok": True, "status": getattr(r, "status", None), "url": url, "json": json.loads(raw.decode("utf-8", "replace"))}


def fetch_text(url: str, timeout: int = 20) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(2048)
        return {"ok": True, "status": getattr(r, "status", None), "url": url, "text_sample": raw.decode("utf-8", "replace")}


def safe_call(fn, url: str) -> Dict[str, Any]:
    try:
        return fn(url)
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "url": url, "error": f"HTTPError: {e.reason}"}
    except Exception as e:  # collector must not die on one degraded source
        return {"ok": False, "status": None, "url": url, "error": f"{type(e).__name__}: {e}"}


def reddit_json_probe(query: str, limit: int) -> Dict[str, Any]:
    q = urllib.parse.quote(query)
    probes = [
        f"https://www.reddit.com/search.json?q={q}&limit={limit}&sort=new",
        f"https://old.reddit.com/search.json?q={q}&limit={limit}&sort=new",
    ]
    attempts = [safe_call(fetch_json, u) for u in probes]
    ok = [a for a in attempts if a.get("ok")]
    blocked = bool(attempts) and not ok and any(a.get("status") in (401, 403) for a in attempts)
    return {"source": "reddit_json", "ok": bool(ok), "blocked": blocked, "attempts": attempts}


def normalize_pullpush_item(item: Dict[str, Any], kind: str) -> Dict[str, Any]:
    created = item.get("created_utc")
    try:
        created_iso = dt.datetime.fromtimestamp(float(created), tz=dt.timezone.utc).isoformat()
    except Exception:
        created_iso = None
    permalink = item.get("permalink")
    reddit_url = ("https://reddit.com" + permalink) if permalink else item.get("url")
    title = item.get("title") or ""
    body = item.get("selftext") or item.get("body") or ""
    text = title if kind == "submission" else body
    return {
        "source": "pullpush",
        "kind": kind,
        "status": "archive-only-needs-live-check",
        "subreddit": item.get("subreddit"),
        "author": item.get("author"),
        "created_iso": created_iso,
        "title": title or None,
        "text_snippet": " ".join(str(text).split())[:280] if text else None,
        "reddit_url": reddit_url,
        "score": item.get("score"),
        "num_comments": item.get("num_comments"),
        "raw_id": item.get("id"),
    }


def pullpush_search(query: str, limit: int) -> Dict[str, Any]:
    q = urllib.parse.quote(query)
    out: Dict[str, Any] = {"source": "pullpush", "ok": False, "attempts": [], "items": []}
    for kind in ("submission", "comment"):
        url = f"https://api.pullpush.io/reddit/search/{kind}/?q={q}&size={limit}&sort=desc&sort_type=created_utc"
        res = safe_call(fetch_json, url)
        out["attempts"].append(res)
        if res.get("ok"):
            out["ok"] = True
            for item in (res.get("json") or {}).get("data", [])[:limit]:
                out["items"].append(normalize_pullpush_item(item, kind))
    return out


def arctic_shift_probe(query: str, limit: int) -> Dict[str, Any]:
    q = urllib.parse.quote(query)
    candidates = [
        f"https://arctic-shift.photon-reddit.com/search?q={q}",
        f"https://arctic-shift.photon-reddit.com/api/search?query={q}&limit={limit}",
    ]
    attempts = []
    for url in candidates:
        attempts.append(safe_call(fetch_text if "/search?" in url else fetch_json, url))
        time.sleep(0.2)
    return {"source": "arctic_shift", "ok": any(a.get("ok") for a in attempts), "attempts": attempts, "items": []}


def dedupe(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for item in items:
        key = item.get("reddit_url") or (item.get("source"), item.get("raw_id"), item.get("text_snippet"))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search Reddit with public-only fallback sources.",
        epilog="The query is sent to Reddit and public archive endpoints (PullPush and Arctic Shift). Do not use private identifiers.",
    )
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    query = validate_public_query(args.query)
    limit = validate_limit(args.limit)
    reddit = reddit_json_probe(query, limit)
    pullpush = pullpush_search(query, limit)
    arctic = arctic_shift_probe(query, limit)
    items = dedupe(pullpush.get("items") or [])
    result = {
        "query": query,
        "collected_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "policy": "public-only; query sent to Reddit, PullPush, and Arctic Shift; no login/cookies; archive hits require live browser verification",
        "reddit_status": "blocked" if reddit.get("blocked") else ("json_accessible" if reddit.get("ok") else "json_failed_other"),
        "sources": {"reddit_json": reddit, "pullpush": pullpush, "arctic_shift": arctic},
        "items": items,
        "recommended_next_check": [
            {"action": "browser_verify_live_reddit_url", "url": item["reddit_url"], "reason": "archive hit needs live confirmation"}
            for item in items[:5]
            if item.get("reddit_url")
        ],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Query: {result['query']}")
        print(f"Collected: {result['collected_at']}")
        print(f"Reddit JSON status: {result['reddit_status']}")
        print(f"PullPush: {'ok' if pullpush.get('ok') else 'failed'}; items={len(items)}")
        print(f"Arctic Shift probe: {'ok' if arctic.get('ok') else 'failed/degraded'}")
        print("Caveat: archive hits are not final proof. Browser-check live URLs.")
        for idx, item in enumerate(items, 1):
            print(f"{idx}. [{item.get('kind')}] r/{item.get('subreddit')} {item.get('created_iso') or ''}")
            if item.get("title"):
                print(f"   title: {item['title']}")
            if item.get("text_snippet"):
                print(f"   text: {item['text_snippet']}")
            print(f"   url: {item.get('reddit_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
