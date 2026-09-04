#!/usr/bin/env python3
"""Bounded, public-only YouTube research helper for Hermes Researcher Agent.

The helper ignores user yt-dlp configuration and never uses cookies, login,
OAuth, API keys, browser profiles, downloads, or account actions.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

VERSION = "0.1.0"
MAX_RESULTS = 20
MAX_TRANSCRIPT_CHARS = 60_000
DEFAULT_TIMEOUT = 60
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
LANGS = re.compile(r"^[A-Za-z0-9.*_,-]{1,80}$")
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
LOCAL_PATH = re.compile(r"(?i)(?:^|\s)(?:/Users/|/home/|~[/\\]|[A-Z]:[\\/])")
PHONE = re.compile(r"(?<!\w)\+?\d(?:[\s().-]*\d){8,}(?!\w)")
TOKEN = re.compile(
    r"(?i)(?:\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[A-Za-z0-9_-]{20,})\b|"
    r"(?:api[_-]?key|secret|password|passwd|token|authorization|cookie|session)\s*[:=]\s*\S+)"
)
ERROR_PATTERNS = [
    ("rate_limited", re.compile(r"(?i)(429|too many requests|rate.?limit)")),
    ("forbidden", re.compile(r"(?i)(403|forbidden)")),
    ("bot_check", re.compile(r"(?i)(confirm you.?re not a bot|sign in to confirm|captcha)")),
    ("age_restricted", re.compile(r"(?i)(age.?restricted|confirm your age)")),
    ("no_subtitles", re.compile(r"(?i)(no subtitles|subtitles.*not available|requested subtitles.*not available)")),
    ("not_found", re.compile(r"(?i)(video unavailable|not available|404|private video|removed)")),
]

Runner = Callable[..., subprocess.CompletedProcess[str]]


def reject_sensitive_query(value: str) -> str:
    value = " ".join(value.strip().split())
    if not value:
        raise ValueError("query must not be empty")
    if len(value) > 300:
        raise ValueError("query is too long; maximum is 300 characters")
    checks = ((EMAIL, "email address"), (LOCAL_PATH, "local path"), (PHONE, "phone-like value"), (TOKEN, "secret/token-like value"))
    for pattern, label in checks:
        if pattern.search(value):
            raise ValueError(f"query rejected: contains a {label}")
    return value


def _https_youtube_url(value: str) -> str:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in YOUTUBE_HOSTS or parsed.username or parsed.password:
        raise ValueError("target must be a public HTTPS YouTube URL")
    return value


def video_url(value: str) -> str:
    value = value.strip()
    if VIDEO_ID.fullmatch(value):
        return f"https://www.youtube.com/watch?v={value}"
    value = _https_youtube_url(value)
    parsed = urlparse(value)
    if parsed.hostname == "youtu.be":
        candidate = parsed.path.strip("/").split("/", 1)[0]
    else:
        candidate = parse_qs(parsed.query).get("v", [""])[0]
        if not candidate and parsed.path.startswith("/shorts/"):
            candidate = parsed.path.split("/", 3)[2]
    if not VIDEO_ID.fullmatch(candidate):
        raise ValueError("target is not a valid YouTube video URL or ID")
    return f"https://www.youtube.com/watch?v={candidate}"


def collection_url(value: str, tab: str | None = None) -> str:
    value = _https_youtube_url(value.strip())
    parsed = urlparse(value)
    if parsed.hostname == "youtu.be":
        raise ValueError("channel/playlist target must use youtube.com")
    if parsed.path == "/playlist":
        playlist_id = parse_qs(parsed.query).get("list", [""])[0]
        if not re.fullmatch(r"[A-Za-z0-9_-]{10,80}", playlist_id):
            raise ValueError("invalid YouTube playlist URL")
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    parts = [part for part in parsed.path.split("/") if part]
    if not parts or not (parts[0].startswith("@") or parts[0] in {"channel", "c", "user"}):
        raise ValueError("target is not a supported public YouTube channel URL")
    if parts[0].startswith("@"):
        if not re.fullmatch(r"@[A-Za-z0-9._-]{3,100}", parts[0]):
            raise ValueError("invalid YouTube channel handle")
        base_parts = parts[:1]
    else:
        if len(parts) < 2:
            raise ValueError("incomplete YouTube channel URL")
        if not re.fullmatch(r"[A-Za-z0-9_-]{3,100}", parts[1]):
            raise ValueError("invalid YouTube channel identifier")
        base_parts = parts[:2]
    suffix = tab or "videos"
    return "https://www.youtube.com/" + "/".join([*base_parts, suffix])


def bounded_limit(value: int) -> int:
    if not 1 <= value <= MAX_RESULTS:
        raise ValueError(f"limit must be between 1 and {MAX_RESULTS}")
    return value


def bounded_timeout(value: int) -> int:
    if not 5 <= value <= 180:
        raise ValueError("timeout must be between 5 and 180 seconds")
    return value


def classify_error(text: str, returncode: int | None = None) -> str:
    if returncode == 124 or re.search(r"(?i)timed?\s*out|timeout", text or ""):
        return "timeout"
    for name, pattern in ERROR_PATTERNS:
        if pattern.search(text or ""):
            return name
    return "error"


def safe_error_note(text: str) -> str:
    state = classify_error(text)
    return f"yt-dlp returned {state}; coverage is degraded"


def _run(args: list[str], timeout: int, runner: Runner = subprocess.run) -> subprocess.CompletedProcess[str]:
    try:
        return runner(args, capture_output=True, text=True, errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, "", "timeout")
    except FileNotFoundError:
        return subprocess.CompletedProcess(args, 127, "", "yt-dlp missing")


def _base_command(binary: str) -> list[str]:
    return [
        binary,
        "--ignore-config",
        "--no-warnings",
        "--skip-download",
        "--socket-timeout", "15",
        "--retries", "1",
        "--extractor-retries", "1",
    ]


def _public_video(item: dict[str, Any]) -> dict[str, Any]:
    subtitles = sorted(set((item.get("subtitles") or {}).keys()) | set((item.get("automatic_captions") or {}).keys()))
    return {
        "video_id": item.get("id"),
        "title": item.get("title"),
        "video_url": item.get("webpage_url") or (f"https://www.youtube.com/watch?v={item.get('id')}" if item.get("id") else None),
        "channel": item.get("channel") or item.get("uploader"),
        "channel_url": item.get("channel_url") or item.get("uploader_url"),
        "published": item.get("upload_date") or item.get("release_date"),
        "duration_seconds": item.get("duration"),
        "views": item.get("view_count"),
        "likes": item.get("like_count"),
        "comments": item.get("comment_count"),
        "live_status": item.get("live_status"),
        "availability": item.get("availability"),
        "subtitle_language_count": len(subtitles),
        "subtitle_languages_sample": subtitles[:20],
    }


def _parse_payload(proc: subprocess.CompletedProcess[str]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if proc.returncode != 0:
        state = classify_error(proc.stderr or proc.stdout, proc.returncode)
        return None, {"status": state, "note": safe_error_note(proc.stderr or proc.stdout)}
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError:
        return None, {"status": "parse_error", "note": "yt-dlp returned invalid JSON; coverage is degraded"}


def search(query: str, limit: int, timeout: int = DEFAULT_TIMEOUT, runner: Runner = subprocess.run, binary: str = "yt-dlp") -> dict[str, Any]:
    query = reject_sensitive_query(query)
    limit = bounded_limit(limit)
    timeout = bounded_timeout(timeout)
    command = [*_base_command(binary), "--dump-single-json", "--playlist-end", str(limit), f"ytsearch{limit}:{query}"]
    payload, error = _parse_payload(_run(command, timeout, runner))
    if error:
        return {"schema_version": "youtube-research/v1", "mode": "search", "status": error["status"], "query": query, "entries": [], "coverage": error["note"]}
    entries = [_public_video(item) for item in (payload or {}).get("entries") or []][:limit]
    return {
        "schema_version": "youtube-research/v1",
        "mode": "search",
        "status": "ok" if entries else "insufficient_evidence",
        "query": query,
        "provider_entries": len((payload or {}).get("entries") or []),
        "retained_entries": len(entries),
        "entries": entries,
        "coverage": "public yt-dlp search; no cookies, login, or account state",
    }


def inspect_video(target: str, timeout: int = DEFAULT_TIMEOUT, runner: Runner = subprocess.run, binary: str = "yt-dlp") -> dict[str, Any]:
    url = video_url(target)
    timeout = bounded_timeout(timeout)
    command = [*_base_command(binary), "--no-playlist", "--dump-single-json", url]
    payload, error = _parse_payload(_run(command, timeout, runner))
    if error:
        return {"schema_version": "youtube-research/v1", "mode": "video", "status": error["status"], "target": url, "coverage": error["note"]}
    return {"schema_version": "youtube-research/v1", "mode": "video", "status": "ok", "video": _public_video(payload or {}), "coverage": "public metadata; creator-side analytics are unavailable"}


def inspect_collection(target: str, limit: int, tab: str | None = None, timeout: int = DEFAULT_TIMEOUT, runner: Runner = subprocess.run, binary: str = "yt-dlp") -> dict[str, Any]:
    limit = bounded_limit(limit)
    timeout = bounded_timeout(timeout)
    url = collection_url(target, tab)
    command = [*_base_command(binary), "--flat-playlist", "--playlist-end", str(limit), "--dump-single-json", url]
    payload, error = _parse_payload(_run(command, timeout, runner))
    if error:
        return {"schema_version": "youtube-research/v1", "mode": "collection", "status": error["status"], "target": url, "entries": [], "coverage": error["note"]}
    entries = [_public_video(item) for item in (payload or {}).get("entries") or []][:limit]
    observed_views = [item["views"] for item in entries if isinstance(item.get("views"), (int, float))]
    baseline = {
        "sample_size_with_views": len(observed_views),
        "median_lifetime_views": statistics.median(observed_views) if observed_views else None,
        "caveat": "lifetime-view baseline is not age-normalized; inspect publication dates before comparing performance",
    }
    return {
        "schema_version": "youtube-research/v1",
        "mode": "collection",
        "status": "ok" if entries else "insufficient_evidence",
        "target": url,
        "retained_entries": len(entries),
        "entries": entries,
        "baseline": baseline,
        "coverage": "flat public listing; inspect shortlisted videos separately for current metrics",
    }


def _vtt_text(raw: str) -> str:
    lines: list[str] = []
    previous = ""
    for source in raw.splitlines():
        line = source.strip()
        if not line or line == "WEBVTT" or "-->" in line or line.isdigit() or line.startswith(("NOTE", "Kind:", "Language:")):
            continue
        line = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
        if line and line != previous:
            lines.append(line)
            previous = line
    return "\n".join(lines)[:MAX_TRANSCRIPT_CHARS]


def transcript(target: str, languages: str, timeout: int = 90, runner: Runner = subprocess.run, binary: str = "yt-dlp") -> dict[str, Any]:
    url = video_url(target)
    timeout = bounded_timeout(timeout)
    if not LANGS.fullmatch(languages):
        raise ValueError("languages must be a comma-separated yt-dlp language selector")
    with tempfile.TemporaryDirectory(prefix="youtube-research-subs-") as temp:
        template = str(Path(temp) / "%(id)s.%(language)s.%(ext)s")
        command = [
            *_base_command(binary),
            "--no-playlist",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", languages,
            "--sub-format", "vtt",
            "-o", template,
            url,
        ]
        proc = _run(command, timeout, runner)
        files = sorted(Path(temp).glob("*.vtt"))
        if not files:
            state = classify_error(proc.stderr or proc.stdout, proc.returncode)
            if proc.returncode == 0:
                state = "no_subtitles"
            return {"schema_version": "youtube-research/v1", "mode": "transcript", "status": state, "target": url, "text": "", "coverage": "no public subtitle file was retained"}
        text = _vtt_text(files[0].read_text(encoding="utf-8", errors="replace"))
        return {
            "schema_version": "youtube-research/v1",
            "mode": "transcript",
            "status": "ok" if text else "no_subtitles",
            "target": url,
            "language_file": files[0].name.split(".")[-2] if "." in files[0].name else "unknown",
            "truncated": len(text) >= MAX_TRANSCRIPT_CHARS,
            "text": text,
            "coverage": "public subtitle/automatic-caption track; may contain transcription errors",
        }


def comments(target: str, limit: int, sort: str = "top", timeout: int = 60, runner: Runner = subprocess.run, binary: str = "yt-dlp") -> dict[str, Any]:
    url = video_url(target)
    if not 1 <= limit <= 50:
        raise ValueError("comment limit must be between 1 and 50")
    timeout = bounded_timeout(timeout)
    if sort not in {"top", "new"}:
        raise ValueError("comment sort must be top or new")
    with tempfile.TemporaryDirectory(prefix="youtube-research-comments-") as temp:
        template = str(Path(temp) / "%(id)s.%(ext)s")
        extractor_args = f"youtube:comment_sort={sort};max_comments={limit},{limit},0,0"
        command = [
            *_base_command(binary),
            "--no-playlist",
            "--write-info-json",
            "--write-comments",
            "--extractor-args", extractor_args,
            "-o", template,
            url,
        ]
        proc = _run(command, timeout, runner)
        files = sorted(Path(temp).glob("*.info.json"))
        if not files:
            state = classify_error(proc.stderr or proc.stdout, proc.returncode)
            if proc.returncode == 0:
                state = "comments_unavailable"
            return {"schema_version": "youtube-research/v1", "mode": "comments", "status": state, "target": url, "comments": [], "coverage": "no bounded public comment sample was retained"}
        try:
            payload = json.loads(files[0].read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            return {"schema_version": "youtube-research/v1", "mode": "comments", "status": "parse_error", "target": url, "comments": [], "coverage": "comment info JSON was invalid"}
        rows = []
        for item in (payload.get("comments") or [])[:limit]:
            rows.append({
                "text": str(item.get("text") or "")[:1000],
                "likes": item.get("like_count") or 0,
                "published": item.get("timestamp") or item.get("time_text"),
                "is_reply": bool(item.get("parent") and item.get("parent") != "root"),
            })
        return {
            "schema_version": "youtube-research/v1",
            "mode": "comments",
            "status": "ok" if rows else "comments_unavailable",
            "target": url,
            "sort": sort,
            "retained_comments": len(rows),
            "comments": rows,
            "coverage": "bounded public sample; author names, IDs, and profile URLs are intentionally omitted",
        }


def doctor(binary: str = "yt-dlp", runner: Runner = subprocess.run) -> dict[str, Any]:
    resolved = shutil.which(binary)
    checks: list[dict[str, str]] = []
    if resolved:
        proc = _run([resolved, "--ignore-config", "--version"], 20, runner)
        checks.append({"name": "yt-dlp", "status": "pass" if proc.returncode == 0 else "warn", "note": (proc.stdout.strip().splitlines() or ["version unavailable"])[0]})
    else:
        checks.append({"name": "yt-dlp", "status": "warn", "note": "missing; install yt-dlp for the lightweight lane"})
    companion = shutil.which("youtube-intel")
    if companion:
        proc = _run([companion, "--version"], 20, runner)
        checks.append({"name": "youtube-intelligence-stack", "status": "pass" if proc.returncode == 0 else "warn", "note": (proc.stdout.strip().splitlines() or ["version unavailable"])[0]})
    else:
        checks.append({"name": "youtube-intelligence-stack", "status": "optional", "note": "missing; install the companion CLI only for deep persistent runs"})
    return {"schema_version": "youtube-research-doctor/v1", "ok": any(c["name"] == "yt-dlp" and c["status"] == "pass" for c in checks), "checks": checks}


def render(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"status: {payload.get('status', 'ok' if payload.get('ok') else 'degraded')}")
    print(f"mode: {payload.get('mode', 'doctor')}")
    if "retained_entries" in payload:
        print(f"retained entries: {payload['retained_entries']}")
    if payload.get("coverage"):
        print(f"coverage: {payload['coverage']}")
    if payload.get("entries"):
        for item in payload["entries"]:
            print(f"- {item.get('title') or item.get('video_id')} — {item.get('video_url')}")
    elif payload.get("video"):
        item = payload["video"]
        print(f"- {item.get('title')} — {item.get('video_url')}")
    elif payload.get("text"):
        print(payload["text"])
    elif payload.get("checks"):
        for item in payload["checks"]:
            print(f"- {item['status']}: {item['name']} — {item['note']}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Bounded public-only YouTube research helper.")
    root.add_argument("--version", action="version", version=f"youtube-research {VERSION}")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("doctor", "search", "video", "channel", "playlist", "transcript", "comments"):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
        if name == "search":
            p.add_argument("query")
            p.add_argument("--limit", type=int, default=5)
            p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
        elif name == "video":
            p.add_argument("target")
            p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
        elif name == "channel":
            p.add_argument("target")
            p.add_argument("--tab", choices=["videos", "shorts", "live"], default="videos")
            p.add_argument("--limit", type=int, default=10)
            p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
        elif name == "playlist":
            p.add_argument("target")
            p.add_argument("--limit", type=int, default=10)
            p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
        elif name == "transcript":
            p.add_argument("target")
            p.add_argument("--languages", default="en.*,en,ru.*,ru")
            p.add_argument("--timeout", type=int, default=90)
        elif name == "comments":
            p.add_argument("target")
            p.add_argument("--limit", type=int, default=10)
            p.add_argument("--sort", choices=["top", "new"], default="top")
            p.add_argument("--timeout", type=int, default=60)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "doctor":
            payload = doctor()
        elif args.command == "search":
            payload = search(args.query, args.limit, args.timeout)
        elif args.command == "video":
            payload = inspect_video(args.target, args.timeout)
        elif args.command == "channel":
            payload = inspect_collection(args.target, args.limit, args.tab, args.timeout)
        elif args.command == "playlist":
            payload = inspect_collection(args.target, args.limit, None, args.timeout)
        elif args.command == "transcript":
            payload = transcript(args.target, args.languages, args.timeout)
        else:
            payload = comments(args.target, args.limit, args.sort, args.timeout)
    except ValueError as exc:
        print(json.dumps({"ok": False, "status": "rejected", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    render(payload, args.json)
    return 0 if payload.get("status") not in {"error", "parse_error"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
