# Changelog

All notable public-distribution changes are documented here.

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