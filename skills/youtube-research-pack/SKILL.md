---
name: youtube-research-pack
description: Use when a Hermes researcher must search public YouTube, inspect videos/channels/playlists, collect subtitles, analyze public signals, or run a bounded YouTube intelligence workflow without cookies or private data.
version: 1.0.0
author: Aleksei Ulianov / Sprut_AI
license: MIT
metadata:
  hermes:
    tags: [youtube, research, video, transcripts, channels, public-source, evidence]
    related_skills: [research-intelligence]
---

# YouTube Research Pack

## Purpose

Research public YouTube evidence without turning access failures into invented facts. Use the lightweight repository helper for quick work and the optional `youtube-intelligence-stack` companion for persistent multi-layer runs.

This pack is public-only by default. It never requires cookies, login, OAuth, API keys, browser-profile extraction, private analytics, or account actions.

## Choose the smallest lane

### Quick search

Use for finding a bounded set of public videos:

```bash
python3 tools/youtube_research.py search "<public query>" --limit 5 --json
```

The helper rejects queries containing email addresses, local paths, phone-like values, and common credential shapes before network access.

### Video verification

Use for current public metadata and subtitle availability:

```bash
python3 tools/youtube_research.py video "<public video URL or ID>" --json
```

Treat views, likes, and comments as volatile observations. Record the collection date. Creator-side CTR, retention, traffic source, subscriber conversion, and revenue are unavailable unless the creator supplies them separately.

### Channel or playlist scan

```bash
python3 tools/youtube_research.py channel "https://www.youtube.com/@handle" --tab videos --limit 10 --json
python3 tools/youtube_research.py channel "https://www.youtube.com/@handle" --tab shorts --limit 10 --json
python3 tools/youtube_research.py playlist "<public playlist URL>" --limit 10 --json
```

The channel URL is normalized to an explicit `videos`, `shorts`, or `live` tab. Flat listings are discovery evidence only; inspect shortlisted videos separately for current metrics.

### Transcript

```bash
python3 tools/youtube_research.py transcript "<public video URL or ID>" --languages "en.*,en,ru.*,ru" --json
```

The helper writes subtitle files only inside a temporary directory, converts one public VTT track to bounded text, and removes the temporary directory. Automatic captions may be wrong. Transcript absence means `no_subtitles`, not that the video lacks relevant content.

### Bounded comments

Use comments only when audience response affects the decision:

```bash
python3 tools/youtube_research.py comments "<public video URL or ID>" --limit 10 --sort top --json
```

The helper enforces a maximum of 50 retained comments and passes an explicit
`max_comments` bound to `yt-dlp`. Output intentionally omits author names, IDs,
profile URLs, and comment IDs. Comment text can still contain personal details;
summarize themes and do not publish the raw sample by default.

### Deep persistent radar

Use the separately maintained public companion when the task needs topic/channel watchlists, transcripts, comments, snapshots, dedupe, and Markdown reports:

```bash
uv tool install --python 3.10 "git+https://github.com/AlekseiUL/youtube-intelligence-stack.git@v0.4.3"
youtube-intel doctor
youtube-intel init ~/youtube-intel-demo --template general
youtube-intel full ~/youtube-intel-demo --safe --query "<public query>" --limit-per-query 3 --skip-watchlist-channels
```

If `uv` is unavailable, install the companion in a dedicated virtual environment. Never install it into an unrelated project environment silently.

Generated evidence belongs in the user's local research instance, outside this repository. Do not commit transcripts, comments, snapshots, watchlists, or reports by default.

## Research sequence

1. Frame the decision and choose quick or deep scope.
2. Run `python3 tools/youtube_research.py doctor --json`.
3. Search broadly with bounded queries.
4. Deduplicate by video ID and channel.
5. Inspect shortlisted videos and record collection time.
6. Collect transcripts only where they affect the decision.
7. Collect comments only in a deep run and only where audience response matters.
8. Browser-check the final shortlist for live title, channel identity, playability, date, visible metrics, visual framing, and blocked state.
9. Corroborate risky product, market, legal, medical, financial, or news claims outside YouTube.
10. Compare independent channels, seek counterexamples, and run the evidence gate.
11. Return a decision-ready brief using `templates/youtube-research-brief.md`.

## Comments and personal-data minimization

Public comments can still contain personal identifiers and sensitive content.

- Do not collect comments by default for ordinary video discovery.
- Limit deep collection to the smallest shortlisted video set.
- Summarize recurring themes; do not reproduce author IDs, profile URLs, or unnecessary usernames.
- Quote only when the exact wording is necessary, and keep attribution proportional to the research purpose.
- Do not infer private traits, identity, location, health, politics, or demographics from comments.
- Never join, like, reply, subscribe, contact, or authenticate without explicit approval.

## Analysis rules

Separate:

- **Public facts:** title, URL, channel, publication date, duration, visible metrics.
- **Computed signals:** ranking, age-normalized ratios, repeated themes, cross-channel frequency.
- **Extracted features:** title structure, declared promise, format, transcript themes, visible thumbnail elements.
- **Interpretation:** why the evidence may matter.
- **Hypothesis:** what might explain performance and still needs testing.

Do not claim causality from views, comments, thumbnails, titles, or correlations. Do not compare lifetime views across different video ages without a caveat or age/cohort normalization. Exclude the focal video from its own channel baseline.

Adapt principles, not identity: never copy another creator's face, channel identity, title, thumbnail text, or composition verbatim.

## Coverage states

Use exact states where possible:

- `ok`
- `insufficient_evidence`
- `degraded`
- `timeout`
- `rate_limited`
- `forbidden`
- `bot_check`
- `age_restricted`
- `not_found`
- `no_subtitles`
- `comments_unavailable`
- `login_required`

A blocked transcript or comment layer does not erase valid metadata. Report each layer separately.

## Evidence gate

Before finalizing:

- Were the final URLs opened or browser-checked?
- Are metrics dated and treated as volatile?
- Were duplicate videos and repeated channels collapsed?
- Is transcript/comment coverage stated separately?
- Are public facts separated from interpretation and causal hypotheses?
- Is there evidence from more than one independent channel when the claim is broad?
- Was the strongest counterexample retained?
- Were important non-YouTube claims corroborated externally?
- Are private analytics explicitly marked unavailable?
- Does the recommendation remain no stronger than the evidence?

Verdicts: `PASS`, `PASS_AFTER_FIX`, `BLOCKED`, or `N/A`.

## Boundaries

Stop and ask before login, cookies, OAuth, API keys, paid access, account creation, browser-profile extraction, private exports, joining, liking, commenting, posting, subscribing, messaging, or contacting anyone.

Do not bypass rate limits, bot checks, age gates, regional restrictions, removals, or private-video controls. Record degraded coverage and use another public source class.
