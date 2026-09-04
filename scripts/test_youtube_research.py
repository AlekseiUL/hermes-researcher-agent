#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "youtube_research.py"
spec = importlib.util.spec_from_file_location("youtube_research", MODULE_PATH)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Recorder:
    def __init__(self, stdout: str = "{}", stderr: str = "", returncode: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.calls: list[list[str]] = []

    def __call__(self, args, **kwargs):
        self.calls.append(list(args))
        return subprocess.CompletedProcess(args, self.returncode, self.stdout, self.stderr)


def must_reject(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError(f"expected rejection for {args!r}")


def test_sensitive_queries() -> None:
    for query in (
        "contact person@example.org about research",
        "read " + "/" + "Users" + "/demo/private/report.txt",
        "call +1 202 555 0187",
        "token=not-a-safe-production-value-1234567890",
        "sk-" + "abcdefghijklmnopqrstuvwxyz123456",
    ):
        must_reject(mod.reject_sensitive_query, query)
    assert mod.reject_sensitive_query("local AI agents benchmark") == "local AI agents benchmark"


def test_url_validation_and_channel_tabs() -> None:
    assert mod.video_url("dQw4w9WgXcQ").endswith("v=dQw4w9WgXcQ")
    assert mod.video_url("https://youtu.be/dQw4w9WgXcQ").endswith("v=dQw4w9WgXcQ")
    assert mod.collection_url("https://www.youtube.com/@example/featured", "videos") == "https://www.youtube.com/@example/videos"
    assert mod.collection_url("https://youtube.com/channel/UC1234567890/videos", "shorts") == "https://www.youtube.com/channel/UC1234567890/shorts"
    assert mod.collection_url("https://youtube.com/playlist?list=PL1234567890") == "https://www.youtube.com/playlist?list=PL1234567890"
    must_reject(mod.collection_url, "https://youtube.com/channel/../videos")
    must_reject(mod.collection_url, "https://youtube.com/@x/videos")
    for target in ("http://youtube.com/watch?v=dQw4w9WgXcQ", "https://evil.example/watch?v=dQw4w9WgXcQ", "file:///tmp/video"):
        must_reject(mod.video_url, target)


def test_bounds() -> None:
    assert mod.bounded_limit(1) == 1
    assert mod.bounded_limit(20) == 20
    must_reject(mod.bounded_limit, 0)
    must_reject(mod.bounded_limit, 21)
    assert mod.bounded_timeout(5) == 5
    assert mod.bounded_timeout(180) == 180
    must_reject(mod.bounded_timeout, 4)
    must_reject(mod.bounded_timeout, 181)


def test_search_command_and_output() -> None:
    fixture = {
        "entries": [
            {
                "id": "dQw4w9WgXcQ",
                "title": "Fixture video",
                "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "channel": "Fixture channel",
                "view_count": 42,
                "subtitles": {"en": []},
            }
        ]
    }
    runner = Recorder(json.dumps(fixture))
    result = mod.search("AI agents", 3, runner=runner, binary="yt-dlp-fixture")
    assert result["status"] == "ok"
    assert result["retained_entries"] == 1
    command = runner.calls[0]
    assert command[0] == "yt-dlp-fixture"
    assert "--ignore-config" in command
    assert "--skip-download" in command
    assert "--playlist-end" in command
    assert "ytsearch3:AI agents" in command
    forbidden = {"--cookies", "--cookies-from-browser", "--username", "--password"}
    assert not forbidden.intersection(command)


def test_video_minimizes_output() -> None:
    payload = {
        "id": "dQw4w9WgXcQ",
        "title": "Fixture",
        "description": "This should not be exported",
        "channel": "Channel",
        "channel_id": "private-ish-unneeded-id",
        "view_count": 100,
        "automatic_captions": {"en-orig": []},
    }
    runner = Recorder(json.dumps(payload))
    result = mod.inspect_video("dQw4w9WgXcQ", runner=runner)
    serialized = json.dumps(result)
    assert result["status"] == "ok"
    assert "This should not be exported" not in serialized
    assert "private-ish-unneeded-id" not in serialized
    assert result["video"]["subtitle_language_count"] == 1
    assert result["video"]["subtitle_languages_sample"] == ["en-orig"]


def test_collection_is_flat_and_bounded() -> None:
    runner = Recorder(json.dumps({"entries": [{"id": "dQw4w9WgXcQ", "title": "One", "view_count": 10}, {"id": "9GpWELm3_XI", "title": "Two", "view_count": 30}]}))
    result = mod.inspect_collection("https://youtube.com/@fixture", 2, "shorts", runner=runner)
    assert result["target"].endswith("/@fixture/shorts")
    command = runner.calls[0]
    assert "--flat-playlist" in command
    assert command[command.index("--playlist-end") + 1] == "2"
    assert result["baseline"]["sample_size_with_views"] == 2
    assert result["baseline"]["median_lifetime_views"] == 20
    assert "not age-normalized" in result["baseline"]["caveat"]


def test_error_classification_suppresses_raw_stderr() -> None:
    runner = Recorder("", "ERROR 429 token=super-secret-value", 1)
    result = mod.search("AI agents", 1, runner=runner)
    assert result["status"] == "rate_limited"
    assert "super-secret-value" not in json.dumps(result)
    assert mod.classify_error("Sign in to confirm you're not a bot") == "bot_check"
    assert mod.classify_error("requested subtitles are not available") == "no_subtitles"


def test_vtt_cleanup_and_cap() -> None:
    raw = "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nHello &amp; welcome\n00:00:01.000 --> 00:00:02.000\nHello &amp; welcome\nNext <c>line</c>\n"
    assert mod._vtt_text(raw) == "Hello & welcome\nNext line"
    assert len(mod._vtt_text("x\n" * 100_000)) <= mod.MAX_TRANSCRIPT_CHARS


def test_cli_rejection() -> None:
    proc = subprocess.run(
        ["python3", str(MODULE_PATH), "search", "person@example.org", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert '"status": "rejected"' in proc.stderr


def test_transcript_uses_temp_and_no_cookies() -> None:
    class SubtitleRunner(Recorder):
        def __call__(self, args, **kwargs):
            self.calls.append(list(args))
            template = args[args.index("-o") + 1]
            path = Path(template.replace("%(id)s", "dQw4w9WgXcQ").replace("%(language)s", "en").replace("%(ext)s", "vtt"))
            path.write_text("WEBVTT\n\n00:00:00 --> 00:00:01\nFixture transcript\n", encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, "", "")

    runner = SubtitleRunner()
    result = mod.transcript("dQw4w9WgXcQ", "en", runner=runner)
    assert result["status"] == "ok"
    assert result["text"] == "Fixture transcript"
    command = runner.calls[0]
    assert "--ignore-config" in command
    assert "--write-auto-subs" in command
    assert "--cookies" not in command


def test_comments_are_bounded_and_identity_minimized() -> None:
    class CommentRunner(Recorder):
        def __call__(self, args, **kwargs):
            self.calls.append(list(args))
            template = args[args.index("-o") + 1]
            path = Path(template.replace("%(id)s", "dQw4w9WgXcQ").replace("%(ext)s", "info.json"))
            path.write_text(json.dumps({"comments": [{"id": "comment-id", "author": "Person", "author_id": "author-id", "author_url": "https://youtube.com/@person", "text": "Useful point", "like_count": 4, "parent": "root"}]}), encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, "", "")

    runner = CommentRunner()
    result = mod.comments("dQw4w9WgXcQ", 5, runner=runner)
    assert result["status"] == "ok"
    assert result["retained_comments"] == 1
    serialized = json.dumps(result)
    assert "comment-id" not in serialized
    assert "author-id" not in serialized
    assert "@person" not in serialized
    command = runner.calls[0]
    assert "--ignore-config" in command
    assert "--write-comments" in command
    extractor = command[command.index("--extractor-args") + 1]
    assert "max_comments=5,5,0,0" in extractor
    assert "--cookies" not in command
    must_reject(mod.comments, "dQw4w9WgXcQ", 51)


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(json.dumps({"ok": True, "tested": "youtube_research", "cases": len(tests)}))


if __name__ == "__main__":
    main()
