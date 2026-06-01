---
name: research-intelligence
description: Use when a Hermes agent must perform public-source research, source scouting, evidence grading, competitor/tool comparison, community-signal analysis, or decision-ready brief writing without private data or credentials.
version: 1.0.0
author: Aleksei Ulianov / Sprut_AI
license: MIT
metadata:
  hermes:
    tags: [research, public-source, evidence, osint-public, source-scouting, decision-briefs]
    related_skills: []
---

# Research Intelligence

## Overview

This skill turns a Hermes agent into a careful public-source researcher. It is optimized for comparing tools, vendors, repositories, products, papers, market signals, community pain, and public claims.

The operating rule is simple: collect enough evidence for the decision, not enough links to look busy. Facts, weak signals, hypotheses, and interpretation must be kept separate when the answer affects money, risk, implementation, reputation, or public claims.

## When to Use

Use for:

- tool, repository, model, vendor, or product comparison;
- public GitHub/project traction checks;
- official docs/changelog/release research;
- community pain and adoption scouting;
- public OSINT-style due diligence on companies, products, or public claims;
- research briefs for implementation, purchase, positioning, or watch/reject decisions;
- recurring watchlist design, but only when the user explicitly asks for monitoring.

Do not use for:

- private-account scraping;
- bypassing login walls, paywalls, CAPTCHAs, or access controls;
- collecting secrets, credentials, private exports, or personal data;
- legal/medical/financial conclusions without qualified review;
- public posting, registration, payment, joining, following, liking, DMing, or emailing without explicit approval.

## Core Research Loop

1. **Frame the decision.** Name the user decision: adopt, buy, compare, reject, watch, implement, contact, investigate, or hand off.
2. **Build the source ladder.** Pick source classes before searching.
3. **Collect dated facts.** Include timestamps for volatile data like stars, downloads, prices, package versions, and community metrics.
4. **Triangulate important claims.** Corroborate technical/product claims with primary sources when possible.
5. **Classify signal strength.** Use fact / claim / weak signal / hypothesis / interpretation.
6. **Browser-check the shortlist.** Use a real browser for dynamic/social/visual pages when live state matters.
7. **Run the evidence gate.** Fix gaps or label limitations before final answer.
8. **Return the next move.** A good brief ends with a practical action.

## Source Ladder

Use the highest-value source classes first:

1. **Primary sources:** official docs, repositories, changelogs, release notes, pricing pages, standards, papers, product pages, government/regulator pages.
2. **Structured public data:** GitHub API, npm/PyPI metadata, Docker tags, package registries, RSS/Atom, public JSON endpoints, datasets, PDFs, CSVs.
3. **Community ground truth:** Hacker News, Reddit, GitHub issues/discussions, forums, Stack Exchange, public Discord/Telegram mirrors only when accessible without login.
4. **Search pivots:** exact phrases, domain searches, local-language terms, author names, repo names, company IDs, package names, error strings, quoted claims.
5. **Browser verification:** real page state, dates, author identity, comments, visible metrics, UI, login wall, blocked state, screenshots, current context.

## Search Tactics

- Search by use case and symptom, not only product names.
- Use exact phrases from claims, README snippets, error messages, and pricing language.
- Search negative terms: `not working`, `refund`, `scam`, `issue`, `complaint`, `lawsuit`, `broken`, `expensive`, `blocked`.
- Search local-language variants where relevant.
- For GitHub projects, check README, license, releases, issues, recent commits, package registries, and forks before judging traction.
- For popularity claims, caveat stars/downloads as proxies, not proof of usage.

## Evidence Gate

Before finalizing, answer:

- What decision does this research support?
- Which source classes were checked?
- Which sources are primary or high-signal?
- What is fact vs interpretation?
- Is the data fresh enough?
- What is the main caveat?
- What would change the answer?
- What is the next move?

Verdicts:

- `PASS` — enough evidence for the decision.
- `PASS_AFTER_FIX` — usable after small fixes already made.
- `BLOCKED` — required evidence unavailable or coverage too weak.
- `N/A` — not evidence-sensitive.

## Output Templates

For quick answers:

```text
Verdict:
- <one-line decision>

Evidence:
- <source/date/fact>
- <source/date/fact>

Interpretation:
- <what it means>

Caveat:
- <main limitation>

Next move:
- <practical action>
```

For deeper work, use `templates/research-brief.md` and `templates/source-ledger.md`.

## Public OSINT Boundaries

Allowed by default:

- public web pages;
- official APIs and feeds;
- public repositories and package metadata;
- public forums and comments visible without login;
- public PDFs, datasets, registries, and archives;
- browser verification of public pages.

Requires explicit user approval:

- login, signup, email/phone verification, 2FA, joining groups, following accounts;
- paid access, trials, purchases, subscriptions;
- using private cookies, private exports, private channel logs, or account sessions;
- posting, commenting, liking, DMing, contacting people;
- collecting sensitive personal data.

Forbidden:

- bypassing access controls;
- credential harvesting;
- stealth scraping behind authentication;
- doxxing or invasive personal profiling;
- presenting unverified allegations as facts.

## Common Pitfalls

1. **Link dumps.** A list of links is not research. Synthesize into a decision.
2. **Community post as truth.** Treat forums as experience signals until corroborated.
3. **Stars as adoption proof.** Stars are attention, not usage.
4. **No source freshness.** Volatile numbers need a collection date.
5. **Ignoring blocked coverage.** Say `Reddit blocked`, `GitHub API rate-limited`, or `login wall` instead of hiding it.
6. **Over-searching after enough evidence.** Stop when the decision is supported and caveated.
7. **No next move.** Research should end with an action, not just information.
8. **Private data creep.** Do not import local memories, sessions, customer notes, or owner-specific source lists into public research.

## Verification Checklist

- [ ] Decision frame is explicit.
- [ ] Source ladder was chosen before collection.
- [ ] Primary/high-signal sources were checked where possible.
- [ ] Facts, claims, weak signals, hypotheses, and interpretation are separated.
- [ ] Volatile metrics include date/time.
- [ ] Browser verification was used when live state mattered.
- [ ] Coverage limitations are labeled.
- [ ] No private data, credentials, cookies, sessions, or login-gated scraping were used.
- [ ] Final answer includes caveat and next move.
