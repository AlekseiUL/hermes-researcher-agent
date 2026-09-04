#!/usr/bin/env python3
"""Safe public-source reach doctor for Hermes Researcher Agent.

Read-only diagnostics only:
- no cookies;
- no login;
- no browser profile/session reads;
- no MCP registration;
- no package installation;
- no social account actions.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

TIMEOUT = 25
USER_AGENT = "hermes-researcher-source-reach-doctor/0.1 (public-only; no cookies)"
YOUTUBE_SMOKE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@dataclass
class Check:
    name: str
    status: str
    note: str


def redact(text: str) -> str:
    text = text or ""
    return re.sub(
        r"(?i)(api[_-]?key|secret|password|passwd|token|authorization|cookie|session)\s*[:=]\s*(?:bearer\s+)?\S+",
        r"\1=[REDACTED]",
        text,
    )


def run(args: list[str], timeout: int = TIMEOUT) -> tuple[int, str]:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, errors="replace", timeout=timeout)
        return proc.returncode, redact(((proc.stdout or "") + (proc.stderr or "")).strip())
    except FileNotFoundError:
        return 127, "missing"
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except Exception as exc:  # noqa: BLE001 - doctor must report degradation, not crash
        return 1, f"error: {type(exc).__name__}: {exc}"


def fetch(url: str, timeout: int = 20, max_bytes: int = 6000) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/html,text/plain,*/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read(max_bytes).decode("utf-8", errors="replace")
            return int(getattr(response, "status", 200) or 200), redact(body)
    except urllib.error.HTTPError as exc:
        body = exc.read(max_bytes).decode("utf-8", errors="replace") if exc.fp else ""
        return int(exc.code), redact(body)
    except urllib.error.URLError as exc:
        return 0, f"urlerror: {exc.reason!r}"
    except Exception as exc:  # noqa: BLE001
        return 0, f"error: {type(exc).__name__}: {exc}"


def command(name: str) -> Optional[str]:
    return shutil.which(name)


def check_hermes_tools(checks: list[Check], runner: Callable[[list[str], int], tuple[int, str]] = run) -> None:
    if not command("hermes"):
        checks.append(Check("Hermes CLI", "WARN", "hermes command not found in PATH; install/configure Hermes before using the profile"))
        return
    code, out = runner(["hermes", "tools", "list"], TIMEOUT)
    if code == 0:
        needed = ["web", "browser", "terminal", "file", "code_execution"]
        found = [name for name in needed if name in out]
        missing = [name for name in needed if name not in out]
        if missing:
            checks.append(Check("Hermes core tools", "WARN", f"tool list reachable; not all recommended tools visible: missing {', '.join(missing)}"))
        else:
            checks.append(Check("Hermes core tools", "PASS", f"recommended tools visible: {', '.join(found)}"))
    else:
        checks.append(Check("Hermes core tools", "WARN", f"could not list tools: {out[:160]}"))


def check_jina(checks: list[Check], fetcher: Callable[[str, int, int], tuple[int, str]] = fetch) -> None:
    status, text = fetcher("https://r.jina.ai/http://example.com", 20, 6000)
    if status == 200 and "Example Domain" in text:
        checks.append(Check("Jina Reader", "PASS", "reader endpoint works for a public page"))
    elif status:
        checks.append(Check("Jina Reader", "WARN", f"HTTP {status}; reachable but unexpected response"))
    else:
        checks.append(Check("Jina Reader", "WARN", text[:180]))


def check_github_public_api(checks: list[Check], fetcher: Callable[[str, int, int], tuple[int, str]] = fetch) -> None:
    status, text = fetcher("https://api.github.com/repos/octocat/Hello-World", 20, 6000)
    if status == 200:
        try:
            data = json.loads(text)
            checks.append(Check("GitHub public API", "PASS", f"unauthenticated repo endpoint works: {data.get('full_name', 'octocat/Hello-World')}"))
        except Exception:
            checks.append(Check("GitHub public API", "WARN", "HTTP 200 but response was not valid JSON"))
    elif status in {403, 429}:
        checks.append(Check("GitHub public API", "WARN", f"HTTP {status}; likely unauthenticated rate limit; use browser/web or optional token if approved"))
    elif status:
        checks.append(Check("GitHub public API", "WARN", f"HTTP {status}; public API degraded"))
    else:
        checks.append(Check("GitHub public API", "WARN", text[:180]))


def check_markitdown(
    checks: list[Check],
    runner: Callable[[list[str], int], tuple[int, str]] = run,
    finder: Callable[[str], Optional[str]] = command,
) -> None:
    """Detect optional local document-to-Markdown ingestion support without installing anything."""
    cli = finder("markitdown")
    if cli:
        code, out = runner([cli, "--version"], TIMEOUT)
        if code == 0:
            version = out.splitlines()[0] if out else "version unknown"
            checks.append(Check("MarkItDown document ingestion", "PASS", f"CLI available: {version}"))
        else:
            checks.append(Check("MarkItDown document ingestion", "WARN", f"CLI found but version check failed: {out[:160]}"))
        return

    code, out = runner(["python3", "-c", "import markitdown; print('python module available')"], TIMEOUT)
    if code == 0:
        checks.append(Check("MarkItDown document ingestion", "PASS", "Python module available; CLI not found in PATH"))
    else:
        checks.append(Check("MarkItDown document ingestion", "WARN", "not installed; local PDF/DOCX/PPTX-to-Markdown ingestion is unavailable"))


def check_ytdlp(
    checks: list[Check],
    runner: Callable[[list[str], int], tuple[int, str]] = run,
    finder: Callable[[str], Optional[str]] = command,
) -> None:
    binary = finder("yt-dlp")
    if not binary:
        checks.append(Check("yt-dlp", "WARN", "not installed; YouTube metadata/transcript reach will be limited"))
        return

    base = [binary, "--ignore-config"]
    code, out = runner([*base, "--version"], TIMEOUT)
    version = out.splitlines()[0] if out else "unknown"
    code2, out2 = runner([*base, "--no-warnings", "--dump-single-json", "--skip-download", YOUTUBE_SMOKE_URL], 70)
    if code2 == 0:
        try:
            data = json.loads(out2)
            checks.append(Check("yt-dlp metadata", "PASS", f"{version}; YouTube metadata smoke: {data.get('id')}"))
        except Exception:
            checks.append(Check("yt-dlp metadata", "WARN", f"{version}; metadata smoke returned non-json"))
    else:
        checks.append(Check("yt-dlp metadata", "WARN", f"{version}; metadata smoke degraded: {out2[:160]}"))

    with tempfile.TemporaryDirectory(prefix="hermes-researcher-youtube-subs-") as tmp:
        code3, out3 = runner([
            *base,
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", "en",
            "--sub-format", "vtt/best",
            "-o", str(Path(tmp) / "%(id)s.%(ext)s"),
            YOUTUBE_SMOKE_URL,
        ], 90)
        files = [path for path in Path(tmp).glob("*") if path.is_file() and path.stat().st_size > 0]
        if code3 == 0 and files:
            checks.append(Check("YouTube transcript smoke", "PASS", f"subtitle file saved under temporary directory: {files[0].name}"))
        elif files:
            checks.append(Check("YouTube transcript smoke", "WARN", f"subtitle file saved, but yt-dlp exited {code3}: {files[0].name}"))
        else:
            checks.append(Check("YouTube transcript smoke", "WARN", f"no subtitle file saved; subtitles may be unavailable/degraded: {out3[:160]}"))


def check_reddit_public_fallback(checks: list[Check], fetcher: Callable[[str, int, int], tuple[int, str]] = fetch) -> None:
    status, text = fetcher("https://www.reddit.com/r/LocalLLaMA/hot.json?limit=1", 20, 6000)
    if status == 200 and ("LocalLLaMA" in text or '"children"' in text):
        checks.append(Check("Reddit public fallback", "PASS", "public Reddit JSON reachable without login/cookies"))
        return

    first_note = f"reddit JSON HTTP {status}" if status else text[:80]
    jina_status, jina_text = fetcher("https://r.jina.ai/http://old.reddit.com/r/LocalLLaMA/", 20, 6000)
    if jina_status == 200 and ("LocalLLaMA" in jina_text or "Reddit" in jina_text):
        checks.append(Check("Reddit public fallback", "PASS", f"Jina/old.reddit fallback works after {first_note}"))
    elif status in {403, 429} or jina_status in {403, 429}:
        checks.append(Check("Reddit public fallback", "WARN", f"blocked/rate-limited ({first_note}; Jina HTTP {jina_status}); use browser/search/manual verification"))
    else:
        checks.append(Check("Reddit public fallback", "WARN", f"public fallback degraded ({first_note}; Jina HTTP {jina_status})"))


def check_deferred_tools(
    checks: list[Check],
    names: Iterable[str] = ("bird", "twitter", "rdt", "xhs", "bili", "mcporter"),
    finder: Callable[[str], Optional[str]] = command,
) -> None:
    notes = {
        "bird": "X/Twitter tool may include read/write commands and cookie/session use",
        "twitter": "X/Twitter tooling usually requires account/session access",
        "rdt": "Reddit CLI/auth paths often require login/cookies",
        "xhs": "XiaoHongShu tooling is login/cookie-sensitive and may have write risk",
        "bili": "Bilibili tooling may require cookies/proxy depending on region/content",
        "mcporter": "MCP routing/registration changes local agent configuration",
    }
    for name in names:
        path = finder(name)
        if path:
            checks.append(
                Check(
                    name,
                    "DEFER",
                    f"present in PATH; {notes.get(name, 'approval-gated tool')}; not executed",
                )
            )
        else:
            checks.append(Check(name, "DEFER", f"missing; {notes.get(name, 'approval-gated tool')}; install/use only after explicit approval"))


def collect_checks(skip_live: bool = False, skip_youtube: bool = False) -> list[Check]:
    checks: list[Check] = []
    check_hermes_tools(checks)
    if not skip_live:
        check_jina(checks)
        check_github_public_api(checks)
        check_reddit_public_fallback(checks)
    else:
        checks.append(Check("live web checks", "DEFER", "skipped by --skip-live"))
    check_markitdown(checks)
    if not skip_youtube:
        check_ytdlp(checks)
    else:
        checks.append(Check("YouTube yt-dlp checks", "DEFER", "skipped by --skip-youtube"))
    check_deferred_tools(checks)
    return checks


def verdict(checks: list[Check]) -> tuple[str, int]:
    if any(check.status == "FAIL" for check in checks):
        return "BLOCKED: one or more safe public-source paths failed.", 2
    if any(check.status == "WARN" for check in checks):
        return "PASS_AFTER_FIX: core public-source reach is usable; warnings are scoped/degraded paths.", 0
    return "PASS: public-source reach checks are healthy.", 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run safe public-source reach diagnostics.")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--skip-live", action="store_true", help="skip live web checks")
    parser.add_argument("--skip-youtube", action="store_true", help="skip yt-dlp YouTube metadata/subtitle checks")
    args = parser.parse_args()

    checks = collect_checks(skip_live=args.skip_live, skip_youtube=args.skip_youtube)
    text, code = verdict(checks)
    if args.json:
        print(json.dumps({"ok": code == 0, "verdict": text, "checks": [asdict(check) for check in checks]}, ensure_ascii=False, indent=2))
    else:
        print("Hermes Researcher Source Reach Doctor — safe/read-only")
        print("=" * 58)
        for check in checks:
            print(f"{check.status:5}  {check.name}: {check.note}")
        print("\nVerdict:")
        print(text)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
