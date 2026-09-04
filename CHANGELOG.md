# Changelog

All notable public-distribution changes are documented here.

## 0.4.0 — 2026-09-04

- Added the public `youtube-research-pack` skill with search, video, channel, playlist, transcript, bounded-comment, and deep-radar workflows.
- Added `tools/youtube_research.py` for bounded YouTube search, video metadata, channel tabs, playlists, temporary subtitle extraction, and identity-minimized comment sampling.
- Added sensitive-query rejection, YouTube URL allowlisting, hard result/timeout limits, degraded-access classification, minimized public output, and eleven offline regression cases.
- Added bounded comment sampling with author names, IDs, profile URLs, and comment IDs omitted from output.
- Integrated the separately maintained public `youtube-intelligence-stack` as an optional deep companion rather than copying private watchlists or runtime state.
- Added comment-personal-data minimization, non-causality rules, channel-baseline cautions, browser verification, external corroboration, and a YouTube research brief template.
- Forced both the YouTube helper and source-reach doctor to ignore inherited `yt-dlp` configuration.
- Added a CI guard that checks current capability coverage in both English and Russian README sections.

## 0.3.1 — 2026-09-04

- Made provider authentication opt-in in the GitHub helper and blocked private-repository metadata.
- Added bounded public-query checks before Reddit/archive requests.
- Strengthened the privacy audit with reachable Git-history scanning, common secret formats, binary printable metadata, forbidden runtime paths, and value-suppressed findings.
- Removed misleading optional-key prompts from profile installation.
- Stopped source diagnostics from printing local executable paths.
- Added privacy regression tests and full-history checkout in CI.
- Synchronized the public agent prompt with research modes, source-lineage grouping, counterexample checks, confidence, and evidence-gate verdicts.

## 0.3.0 — 2026-09-02

- Added six bounded research modes with explicit depth and stop rules.
- Added source-lineage grouping so copied announcements do not count as independent evidence.
- Added a counterexample gate for decision-relevant claims.
- Added the `research-run/v1` JSON example and a strict standard-library validator.
- Added regression tests for lineage inflation, inaccessible/discovery-only evidence, missing counterexamples, embedded credentials, internal URLs, and sensitive URL query fields.
- Updated the research brief, source ledger, README, distribution metadata, and repository CI.


## 0.2.3 — 2026-06-08

- Added public-source reach diagnostics and safe fallback guidance.
- Added GitHub traction and Reddit fallback helpers.
- Added document-ingestion guidance and public example reports.