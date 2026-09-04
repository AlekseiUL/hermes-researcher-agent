# Research modes

Choose the smallest mode that can support the user's decision. A mode controls depth and evidence requirements; it is not a role-play label.

## Mode router

### `quick_fact`

Use for one current fact, version, date, price, availability, or source check.

Minimum:

- open the primary source;
- record when it was checked;
- state one caveat if the fact is volatile.

Stop when the fact is verified. Do not manufacture a deep report.

### `deep_research`

Use when the decision is consequential, disputed, broad, or likely to survive the current chat.

Minimum:

- frame the decision and success criteria;
- compare at least two independent source lineages;
- include primary or structured-data evidence;
- seek a counterexample;
- record coverage gaps and confidence;
- save a `research-run/v1` artifact when repeatability matters.

### `repo_tool`

Use for repositories, packages, models, APIs, and developer tools.

Check the real implementation boundary: README, license, recent commits, releases, issues/PRs, package metadata, install path, tests, and independent usage signals. Stars and forks are attention proxies, not adoption proof.

### `community_pain`

Use for recurring user problems, complaints, requests, workarounds, and adoption friction.

Open full threads or comments. Preserve context, look for repetition and counterexamples, and corroborate pain with an observable artifact. One loud post is a weak signal, not a market fact.

### `live_visual`

Use when the answer depends on current UI state, charts, screenshots, dashboards, thumbnails, maps, comments, filters, or a JavaScript-heavy page.

Search/API provides breadth; browser/DOM/vision verifies the shortlisted evidence. Record whether the page was public, degraded, blocked, or login-required. Never use private cookies or authenticated state by default.

### `monitoring_design`

Use only to design a recurring public-source watch. Define query scope, source classes, dedupe key, freshness window, change threshold, no-change output, storage boundary, and stop rule.

This mode does not create or enable cron jobs. Scheduling and external delivery require a separate explicit user action.

## Universal stop rules

Stop or report a gap when:

- the decision is already supported and caveated;
- independent evidence cannot be reached safely;
- important coverage is blocked, login-required, or paid/private;
- the next step would require credentials, account actions, payment, posting, or access-control bypass;
- additional pages repeat the same source lineage without adding independent evidence.

## Default output

```text
Mode:
Decision supported:
Sources and reach:
Facts:
Hypotheses:
Interpretation:
Counterexample:
Recommendation:
Coverage gaps:
Next move:
Confidence:
Evidence gate:
```
