# Hermes Researcher Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Hermes Researcher Agent cover: dramatic researcher poster with the text “researcher” and “из-под земли достану”.](docs/assets/researcher-agent-cover.jpg)

A privacy-safe Hermes Agent profile for public-source research, document ingestion, source scouting, evidence grading, and decision-ready briefs.

**Tagline:** Public-source research with an evidence gate — no private data, no secret sauce leaks.

This repository packages a clean researcher profile for [Hermes Agent](https://hermes-agent.nousresearch.com/docs/). It is built for people who need an AI research operator that can search broadly, verify carefully, separate fact from interpretation, and return a practical recommendation instead of a raw link dump.

This is **not** an export of a private internal agent. It is a sanitized public distribution: reusable methodology, safe default boundaries, research skills, templates, and helper scripts — without private memories, sessions, credentials, cron jobs, or owner-specific sources.

---

## What this is

This repository packages a Hermes profile distribution for:

- public-source research and source scouting;
- tool, vendor, repository, model, product, and paper comparison;
- GitHub/project traction checks;
- official docs, changelog, release, pricing, RSS/Atom, and public API research;
- community-pain and adoption-signal analysis;
- evidence-gated decision briefs.

It is not a private OSINT kit, credentials bundle, login-wall scraper, or scheduled monitoring service out of the box. It is a safe starter researcher that uses the tools available in the installer's own Hermes setup.

## Who it is for

- Builders who need fast but evidence-aware research.
- Operators comparing tools, vendors, repositories, or public claims.
- Teams that want a reusable research profile across machines.
- Hermes users who want a researcher agent without importing someone else's private memory or cron jobs.

## Key features

- **Hermes profile distribution** — install the whole profile from GitHub with one command.
- **Evidence gate** — every serious answer checks source quality, freshness, caveats, and next move.
- **Research mode router** — chooses quick fact, deep research, repo/tool, community-pain, live/visual, or monitoring-design depth before collection.
- **Source-lineage checks** — mirrors and articles repeating one announcement count as one evidence lineage, not independent proof.
- **Counterexample gate** — decision-relevant claims must seek contrary evidence or record the coverage gap.
- **Reproducible research runs** — a public-safe `research-run/v1` artifact can be validated before a brief is trusted.
- **Public-source boundary** — no private data, sessions, cookies, credentials, or login-gated scraping by default.
- **Research skill pack** — includes `research-intelligence` with source ladders, output templates, and safety rules.
- **Document ingestion** — includes a sanitized `markitdown-document-ingestion` skill for turning public PDFs, DOCX, PPTX, XLSX, HTML, CSV/JSON/XML, EPUB, and inspected trusted document bundles into Markdown before the evidence gate.
- **Browser-aware workflow** — browser verification is recommended when live page state, comments, metrics, visuals, or login walls matter.
- **Safe source-reach doctor** — checks Jina Reader, GitHub public API, Reddit public/Jina fallback, and optional `yt-dlp` metadata/subtitle reach without cookies or login.
- **YouTube Research Pack** — bounded public search, video metadata, channel `videos`/`shorts`/`live` tabs, playlists, temporary transcript extraction, privacy-minimized comment samples, browser-verification rules, and an optional deep radar companion.
- **Public Reddit fallback helper** — handles blocked Reddit JSON as degraded coverage and uses archive hits only as leads that require live verification.
- **GitHub traction helper** — collects public repo metadata, releases, latest commit, topics, license, stars/forks/watchers, and caveats metrics as proxies rather than usage proof.
- **Degraded-access reporting** — blocked, rate-limited, login-gated, or subtitle-missing sources are labeled as coverage gaps instead of hidden.
- **Example outputs** — includes real example briefs and generated GitHub traction checks under `examples/`.
- **Bilingual documentation** — English and Russian instructions in one README.

## Source coverage at a glance

The profile separates bundled collectors from capabilities supplied by the
installer's Hermes toolsets. This keeps the product claim accurate: GitHub,
Reddit fallback, evidence validation, source diagnostics, and bounded YouTube
collection have repository helpers; broader web, browser, and visual research
uses the corresponding Hermes tools when they are configured.

- **Web and primary sources:** official sites, docs, pricing, changelogs,
  releases, standards, regulators, papers, public datasets, RSS/Atom, public
  APIs, and JSON endpoints.
- **Software ecosystem:** public GitHub repositories, issues/discussions,
  package registries such as npm and PyPI, Docker tags, model repositories,
  licenses, releases, install paths, tests, and maintenance signals.
- **YouTube:** search, video metadata, channel tabs, playlists, subtitles,
  bounded comments, live browser checks, and optional persistent radar runs.
- **Community evidence:** public Reddit plus fallbacks, Hacker News, GitHub
  discussions, Stack Exchange, forums, public comments, and public social
  pages or mirrors reachable without login.
- **Documents:** public PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, EPUB, and
  inspected trusted bundles converted to Markdown analysis copies when useful.
- **Live and visual evidence:** dynamic pages, dashboards, charts, screenshots,
  thumbnails, visible metrics, UI state, and login-wall or blocked-state proof.
- **Monitoring design:** watch scope, source classes, deduplication, freshness,
  thresholds, storage boundaries, and stop rules. Scheduling remains disabled
  until the user explicitly creates it.

## Installation

```bash
hermes profile install github.com/AlekseiUL/hermes-researcher-agent
hermes profile show hermes-researcher-agent
hermes -p hermes-researcher-agent setup
hermes -p hermes-researcher-agent chat
```

The distribution installs without API keys. Provider and optional search/browser credentials stay in your own local Hermes profile; do not paste them into chat or commit `.env`.

For local testing from a clone:

```bash
hermes profile install /path/to/hermes-researcher-agent --name researcher-test --alias
hermes -p researcher-test chat
```

Then configure your own model provider and optional tools:

```bash
hermes -p researcher-test setup
hermes -p researcher-test tools
```

## Recommended Hermes toolsets

The profile is designed to be useful with these Hermes toolsets when available:

- `web` — web search and extraction;
- `browser` — live page verification, social pages, UI state, blocked/login-wall checks;
- `terminal` — public APIs, RSS/Atom, JSON, reproducible collection scripts;
- `file` — save ledgers and source packs;
- `code_execution` — quick structured parsing and scoring;
- `vision` — screenshots, charts, posters, visual pages;
- `skills` — load reusable research procedures;
- `memory` — remember stable user preferences only;
- `cronjob` — only when the user explicitly creates recurring monitoring.

## Quick start

1. Install the profile.
2. Configure your own model provider and toolsets.
3. Ask a research question with a clear decision frame.
4. Let the agent collect public evidence and label limitations.
5. Use the returned brief: verdict, evidence, interpretation, caveat, next move.

For document-heavy research, convert the source into a Markdown analysis copy first, then cite the original as source-of-truth:

```bash
markitdown ./sources/report.pdf -o ./research-artifacts/report.md
```

Example prompt:

```text
Compare these three AI coding agents for a small team. Use primary docs first, then community pain signals. Return a shortlist and caveats.
```

Another example:

```text
Find whether this GitHub repo has real adoption or only stars. Check docs, releases, issues, package/download proxies, and community mentions.
```

## Example workflow

```text
Question -> Decision frame -> Mode -> Source ladder -> Evidence collection -> Lineage grouping -> Counterexample search -> Browser verification -> Evidence gate -> Decision-ready brief
```

## Example outputs

Real examples included in this repo:

- [`examples/research-brief-researcher-agent-readiness.md`](examples/research-brief-researcher-agent-readiness.md) — decision brief on whether this repository is ready to promote.
- [`examples/github-traction-hermes-researcher-agent.md`](examples/github-traction-hermes-researcher-agent.md) — generated GitHub traction check for this repository.
- [`examples/github-traction-nousresearch-hermes-agent.md`](examples/github-traction-nousresearch-hermes-agent.md) — generated GitHub traction check for the upstream Hermes Agent repository.

Run the GitHub helper yourself. It is unauthenticated by default and refuses private repositories. If public API rate limits require authentication, opt in explicitly with `--token-env GITHUB_TOKEN`; the helper still rejects private visibility and never prints token values.

```bash
python3 tools/github_traction_check.py AlekseiUL/hermes-researcher-agent
python3 tools/github_traction_check.py NousResearch/hermes-agent --json
python3 tools/github_traction_check.py NousResearch/hermes-agent --token-env GITHUB_TOKEN --json
```

Validate the included reproducible research run. It reports both page count and independent lineage count, so copied announcements cannot inflate the evidence:

```bash
python3 tools/evidence_lineage_check.py examples/research-run-source-lineage.json --json
```

Use the Reddit fallback only for public, non-sensitive queries. The query is transmitted to Reddit and public archive endpoints; before network access, the CLI rejects email addresses, local paths, phone-like values, and common token shapes:

```bash
python3 tools/public_reddit_fallback_search.py "Hermes Agent research" --limit 5 --json
```

Run the safe source-reach doctor before serious research. It is read-only: no cookies, no login, no social actions, no MCP registration.

```bash
python3 tools/source_reach_doctor.py
python3 tools/source_reach_doctor.py --json
python3 tools/source_reach_doctor.py --skip-youtube
```

Typical interpretation:

- `PASS` — public-source reach is healthy.
- `WARN` / `PASS_AFTER_FIX` — research can continue, but the report should label the degraded layer. Missing MarkItDown is a warning for document-heavy work, not a blocker for ordinary web research.
- `DEFER` — a social/login/MCP path exists or is missing, but it is approval-gated, not a default setup task.
- `BLOCKED` — required safe evidence paths are unavailable; the result is not ready to support the decision.

### YouTube research

The bundled lightweight helper ignores inherited `yt-dlp` configuration, so a
user-level config cannot silently add cookies or account state:

```bash
python3 tools/youtube_research.py doctor --json
python3 tools/youtube_research.py search "AI agents" --limit 5 --json
python3 tools/youtube_research.py video "dQw4w9WgXcQ" --json
python3 tools/youtube_research.py channel "https://www.youtube.com/@NousResearch" --tab videos --limit 10 --json
python3 tools/youtube_research.py playlist "https://www.youtube.com/playlist?list=PL590L5WQmH8fJ54F369BLDSqIwcs-TCfs" --limit 10 --json
python3 tools/youtube_research.py transcript "dQw4w9WgXcQ" --languages "en.*,en,ru.*,ru" --json
python3 tools/youtube_research.py comments "9GpWELm3_XI" --limit 10 --sort top --json
```

For persistent topic/channel watchlists, comments, metric snapshots, and
Markdown reports, install the separately maintained public companion. It is
optional and is never installed automatically:

```bash
uv tool install --python 3.10 "git+https://github.com/AlekseiUL/youtube-intelligence-stack.git@v0.4.3"
youtube-intel doctor
youtube-intel init ~/youtube-intel-demo --template general
youtube-intel full ~/youtube-intel-demo --safe --query "AI agents" --limit-per-query 3 --skip-watchlist-channels
```

YouTube and `yt-dlp` may return partial coverage because of rate limits, region,
removed videos, bot checks, age gates, missing subtitles, or unavailable
comments. The pack reports these states instead of suggesting a bypass.

## Repository contents

- [`distribution.yaml`](distribution.yaml) — Hermes profile distribution manifest.
- [`SOUL.md`](SOUL.md) — researcher operating prompt.
- [`config.yaml`](config.yaml) — safe starter config and preferred capability set.
- [`skills/research-intelligence/SKILL.md`](skills/research-intelligence/SKILL.md) — installable research workflow skill.
- [`skills/markitdown-document-ingestion/SKILL.md`](skills/markitdown-document-ingestion/SKILL.md) — optional document-to-Markdown intake workflow for public research files.
- [`skills/research-intelligence/templates/research-brief.md`](skills/research-intelligence/templates/research-brief.md) — deep research brief template.
- [`skills/research-intelligence/templates/source-ledger.md`](skills/research-intelligence/templates/source-ledger.md) — source ledger template.
- [`tools/source_reach_doctor.py`](tools/source_reach_doctor.py) — safe public-source reach diagnostics: Jina, GitHub public API, Reddit fallback, optional MarkItDown detection, optional YouTube subtitle smoke, and approval-gated social/MCP detection.
- [`tools/public_reddit_fallback_search.py`](tools/public_reddit_fallback_search.py) — public-only Reddit fallback helper.
- [`tools/github_traction_check.py`](tools/github_traction_check.py) — public GitHub metadata traction check helper.
- [`tools/evidence_lineage_check.py`](tools/evidence_lineage_check.py) — validates reproducible runs, independent source lineages, counterexamples, access state, and decision-relevant evidence.
- [`tools/youtube_research.py`](tools/youtube_research.py) — bounded public YouTube search, video/channel/playlist inspection, temporary transcript extraction, and identity-minimized comment sampling.
- [`skills/youtube-research-pack/SKILL.md`](skills/youtube-research-pack/SKILL.md) — evidence-aware YouTube workflows and privacy boundaries.
- [`skills/youtube-research-pack/templates/youtube-research-brief.md`](skills/youtube-research-pack/templates/youtube-research-brief.md) — reusable YouTube research brief.
- [`skills/research-intelligence/references/research-modes.md`](skills/research-intelligence/references/research-modes.md) — depth router and stop rules for six public-safe research modes.
- [`examples/research-run-source-lineage.json`](examples/research-run-source-lineage.json) — runnable example where three pages collapse into one announcement lineage.
- [`examples/`](examples/) — real example briefs and helper outputs.
- [`docs/assets/researcher-agent-cover.jpg`](docs/assets/researcher-agent-cover.jpg) — repository cover / agent poster.
- [`.env.EXAMPLE`](.env.EXAMPLE) — optional environment variable names only; no secrets.
- [`LICENSE`](LICENSE) — MIT license.
- [`NOTICE.md`](NOTICE.md) — canonical source and attribution.
- [`SECURITY.md`](SECURITY.md) — safety and security policy.
- [`SECURITY-SCANNER-NOTES.md`](SECURITY-SCANNER-NOTES.md) — reviewed scanner findings and the privacy-minimized operation-audit contract.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules.
- [`CHANGELOG.md`](CHANGELOG.md) — versioned release notes.

## Safety, privacy, and non-goals

This repository intentionally does **not** include:

- API keys or `.env` values;
- OAuth tokens or `auth.json`;
- memories;
- sessions;
- logs;
- workspaces;
- private source lists;
- scheduled cron jobs;
- owner-specific research outputs.

The researcher profile is public-source by default. It should stop and ask before any action that requires login, signup, payment, joining a group, posting, DMing, following, private exports, or account sessions.

For auditable YouTube subprocess execution without recording queries, targets, command arguments, or collected content, add `--audit`; structured `operation-audit/v1` events are written to `stderr`. See [`SECURITY-SCANNER-NOTES.md`](SECURITY-SCANNER-NOTES.md).

## Status / roadmap

Current public source-tree version: **v0.4.0**.

v0.4.0 adds a public YouTube Research Pack with a bundled bounded helper and an optional deep companion. v0.3.1 hardened privacy and installation; v0.3.0 added six research modes, source-lineage deduplication, counterexamples, and reproducible evidence validation. The distribution does not add account access, enabled monitoring, private source lists, or autonomous external actions.

Possible next improvements:

- add more safe research templates;
- add examples for GitHub traction checks, vendor due diligence, and paper/tool comparison;
- add optional disabled cron examples for users who want their own monitoring;
- add more public-source helper scripts after security review.

## Contributing

Contributions are welcome if they improve practical usefulness, safety, clarity, or examples.

Rules:

- no secrets, credentials, cookies, sessions, logs, or private data;
- no owner-specific research output;
- no enabled cron jobs by default;
- no scripts that bypass access controls or scrape behind login;
- claims must be source-backed and caveated.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md).

## Links / Resources

- YouTube: https://youtube.com/@alekseiulianov
- Telegram channel Sprut AI: https://t.me/Sprut_AI
- Telegram chat: https://t.me/+eH-qNIDmud8zNDZi
- AI Операционка: https://t.me/tribute/app?startapp=sJyg
- Hermes Agent docs: https://hermes-agent.nousresearch.com/docs/

## Canonical source

This project is maintained by Aleksei Ulianov / Sprut_AI.
Original repository: https://github.com/AlekseiUL/hermes-researcher-agent

If you found this project mirrored, repackaged, or redistributed elsewhere, check this repository as the source of truth.

## Attribution

Where permitted by the applicable license, if you reuse, fork, modify, package, or publish this work, keep the original copyright and license notice and link back to the canonical repository.

## License

MIT. See [`LICENSE`](LICENSE).

---

# Hermes Researcher Agent — исследовательский агент для Hermes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Обложка Hermes Researcher Agent: драматичный постер исследователя с текстом “researcher” и “из-под земли достану”.](docs/assets/researcher-agent-cover.jpg)

Безопасный профиль Hermes Agent для research-задач по открытым источникам: приём документов в Markdown, поиск источников, проверка фактов, оценка доказательств и короткие решения, по которым можно действовать.

**Формула:** исследователь по открытым источникам с evidence gate — без приватных данных, без секретов и без утечки внутренней кухни.

Этот репозиторий упаковывает чистый researcher-профиль для [Hermes Agent](https://hermes-agent.nousresearch.com/docs/). Он нужен, когда хочется не просто “найти ссылки”, а получить нормальную исследовательскую работу: что проверили, какие источники сильные, где слабые сигналы, где гипотеза, где факт, какой следующий шаг.

Это **не** экспорт приватного внутреннего агента. Это обезличенная публичная сборка: методология, безопасные границы, research skills, шаблоны и вспомогательные скрипты — без приватной памяти, сессий, ключей, cron-задач и личных источников.

## Что это

Репозиторий упаковывает Hermes profile distribution для:

- исследования по открытым источникам;
- сравнения инструментов, вендоров, репозиториев, моделей, продуктов и статей;
- проверки GitHub-проектов на реальную активность, а не только звёзды;
- анализа официальных docs, changelog, releases, pricing, RSS/Atom и публичных API;
- поиска community pain и слабых сигналов adoption;
- коротких decision-ready briefs с evidence gate.

Это не приватный OSINT-набор, не пачка credentials, не scraper за login-wall и не готовый сервис ежедневного мониторинга. Это безопасный стартовый researcher, который использует инструменты, доступные в вашей установке Hermes.

## Для кого

- Для builders, которым нужен быстрый, но доказательный research.
- Для операторов, которые сравнивают инструменты, вендоров, репозитории или публичные claims.
- Для команд, которым нужен один reusable researcher-профиль на разных машинах.
- Для пользователей Hermes, которые хотят researcher agent без чужой приватной памяти и cron-задач.

## Ключевые возможности

- **Hermes profile distribution** — весь профиль ставится из GitHub одной командой.
- **Evidence gate** — серьёзный ответ проверяет качество источников, свежесть, caveats и следующий шаг.
- **Режимы исследования** — до поиска выбирается quick fact, deep research, repo/tool, community pain, live/visual или monitoring design.
- **Проверка происхождения источников** — зеркала и статьи, повторяющие один анонс, считаются одной линией доказательств, а не независимыми подтверждениями.
- **Поиск контрпримеров** — для важного вывода агент ищет данные против него или честно фиксирует пробел.
- **Воспроизводимый `research-run/v1`** — публичный JSON-артефакт можно проверить валидатором до использования вывода.
- **Public-source boundary** — по умолчанию нет приватных данных, sessions, cookies, credentials и login-gated scraping.
- **Research skill pack** — внутри `research-intelligence`: source ladders, шаблоны ответов, safety rules.
- **Document ingestion** — внутри есть чистый `markitdown-document-ingestion` skill: публичные PDF, DOCX, PPTX, XLSX, HTML, CSV/JSON/XML, EPUB и проверенные trusted document bundles можно переводить в Markdown перед evidence gate.
- **Browser-aware workflow** — browser verification нужен, когда важны live page state, comments, metrics, visuals или login walls.
- **Safe source-reach doctor** — проверяет Jina Reader, GitHub public API, Reddit public/Jina fallback и optional `yt-dlp` metadata/subtitles без cookies и login.
- **YouTube Research Pack** — ограниченный public-поиск, metadata ролика, вкладки канала `videos`/`shorts`/`live`, плейлисты, временное извлечение субтитров, обезличенная выборка комментариев, browser verification и optional deep-radar companion.
- **Public Reddit fallback helper** — если Reddit JSON заблокирован, источник помечается как degraded, а archive hits считаются только leads для live-проверки.
- **GitHub traction helper** — собирает public repo metadata, releases, latest commit, topics, license, stars/forks/watchers и честно помечает метрики как proxies, а не proof of usage.
- **Degraded-access reporting** — blocked, rate-limited, login-gated или missing subtitles попадают в coverage gaps, а не прячутся.
- **Example outputs** — реальные example briefs и generated GitHub traction checks лежат в `examples/`.
- **Документация EN/RU** — английская и русская версии в одном README.

## Какие источники поддерживаются

Профиль отделяет встроенные collectors от возможностей, которые предоставляет
локальная установка Hermes. Поэтому описание остаётся точным: для GitHub,
Reddit fallback, проверки evidence, диагностики источников и ограниченного
YouTube-сбора в репозитории есть собственные helpers. Более широкий web,
browser и visual research использует соответствующие Hermes tools, если они
настроены у пользователя.

- **Web и первичные источники:** официальные сайты, docs, pricing, changelog,
  releases, стандарты, регуляторы, papers, публичные датасеты, RSS/Atom,
  публичные API и JSON endpoints.
- **Экосистема разработки:** публичные GitHub-репозитории, issues/discussions,
  npm, PyPI, Docker tags, model repositories, лицензии, релизы, установка,
  тесты и признаки поддержки проекта.
- **YouTube:** поиск, metadata видео, вкладки каналов, плейлисты, субтитры,
  ограниченные комментарии, live browser checks и optional persistent radar.
- **Community evidence:** публичный Reddit и fallbacks, Hacker News, GitHub
  Discussions, Stack Exchange, форумы, открытые комментарии, публичные
  социальные страницы и зеркала, доступные без login.
- **Документы:** публичные PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, EPUB и
  проверенные trusted bundles с преобразованием в Markdown-копии для анализа.
- **Live и visual evidence:** динамические страницы, dashboards, графики,
  screenshots, thumbnails, видимые метрики, UI state и доказательство
  блокировки или login wall.
- **Проектирование мониторинга:** область наблюдения, классы источников,
  дедупликация, свежесть, пороги изменений, хранение и stop rules. Расписание
  остаётся выключенным, пока пользователь явно его не создаст.

## Установка

```bash
hermes profile install github.com/AlekseiUL/hermes-researcher-agent
hermes profile show hermes-researcher-agent
hermes -p hermes-researcher-agent setup
hermes -p hermes-researcher-agent chat
```

Дистрибутив устанавливается без API-ключей. Ключи провайдера и optional search/browser backends остаются только в вашем локальном Hermes-профиле: не вставляйте их в чат и не коммитьте `.env`.

Локальный тест из clone:

```bash
hermes profile install /path/to/hermes-researcher-agent --name researcher-test --alias
hermes -p researcher-test chat
```

Потом настройте свой model provider и нужные tools:

```bash
hermes -p researcher-test setup
hermes -p researcher-test tools
```

## Рекомендуемые Hermes toolsets

Профиль рассчитан на такие Hermes toolsets, если они доступны:

- `web` — поиск и извлечение веб-страниц;
- `browser` — live verification, соцстраницы, UI state, blocked/login-wall checks;
- `terminal` — публичные API, RSS/Atom, JSON, воспроизводимые collection scripts;
- `file` — сохранение ledgers и source packs;
- `code_execution` — быстрый parsing/scoring;
- `vision` — screenshots, charts, posters, visual pages;
- `skills` — reusable research procedures;
- `memory` — только стабильные пользовательские предпочтения;
- `cronjob` — только если пользователь явно создаёт recurring monitoring.

## Быстрый старт

1. Установите профиль.
2. Настройте свой model provider и toolsets.
3. Задайте research-вопрос с понятным решением: выбрать, купить, внедрить, отклонить, наблюдать.
4. Агент собирает открытые evidence и честно маркирует ограничения.
5. На выходе: verdict, evidence, interpretation, caveat, next move.

Если задача завязана на документ, сначала делается Markdown-копия для анализа, а оригинал остаётся source-of-truth:

```bash
markitdown ./sources/report.pdf -o ./research-artifacts/report.md
```

Пример запроса:

```text
Compare these three AI coding agents for a small team. Use primary docs first, then community pain signals. Return a shortlist and caveats.
```

Ещё пример:

```text
Find whether this GitHub repo has real adoption or only stars. Check docs, releases, issues, package/download proxies, and community mentions.
```

## Пример процесса

```text
Вопрос -> Decision frame -> Режим -> Source ladder -> Evidence collection -> Группировка по происхождению -> Поиск контрпримеров -> Browser verification -> Evidence gate -> Decision-ready brief
```

## Примеры output

Реальные примеры внутри repo:

- [`examples/research-brief-researcher-agent-readiness.md`](examples/research-brief-researcher-agent-readiness.md) — decision brief: готов ли этот repo к публичному показу.
- [`examples/github-traction-hermes-researcher-agent.md`](examples/github-traction-hermes-researcher-agent.md) — generated GitHub traction check для этого repo.
- [`examples/github-traction-nousresearch-hermes-agent.md`](examples/github-traction-nousresearch-hermes-agent.md) — generated GitHub traction check для upstream Hermes Agent repo.

Запуск GitHub helper. По умолчанию он работает без авторизации и отказывается читать private-репозитории. Если для public API не хватает rate limit, токен включается явно через `--token-env GITHUB_TOKEN`; private visibility всё равно блокируется, значение токена не печатается.

```bash
python3 tools/github_traction_check.py AlekseiUL/hermes-researcher-agent
python3 tools/github_traction_check.py NousResearch/hermes-agent --json
python3 tools/github_traction_check.py NousResearch/hermes-agent --token-env GITHUB_TOKEN --json
```

Проверка воспроизводимого research-run. В результате отдельно показаны количество страниц и количество независимых линий источников:

```bash
python3 tools/evidence_lineage_check.py examples/research-run-source-lineage.json --json
```

Reddit fallback предназначен только для открытых, нечувствительных запросов. Запрос передаётся Reddit и публичным архивным endpoints; перед обращением к сети CLI блокирует email, локальные пути, похожие на телефон значения и распространённые форматы токенов:

```bash
python3 tools/public_reddit_fallback_search.py "Hermes Agent research" --limit 5 --json
```

Перед серьёзным research можно прогнать safe source-reach doctor. Он read-only: без cookies, login, social actions и MCP registration.

```bash
python3 tools/source_reach_doctor.py
python3 tools/source_reach_doctor.py --json
python3 tools/source_reach_doctor.py --skip-youtube
```

Как читать результат:

- `PASS` — public-source reach здоров.
- `WARN` / `PASS_AFTER_FIX` — работать можно, но degraded layer надо честно отметить в отчёте. Если MarkItDown не установлен, это warning для document-heavy задач, а не блокер обычного web research.
- `DEFER` — social/login/MCP путь существует или отсутствует, но это approval-gated, а не “нужно срочно поставить”.
- `BLOCKED` — обязательные безопасные источники недоступны; результат пока нельзя использовать для решения.

### YouTube research

Встроенный helper принудительно игнорирует пользовательский конфиг `yt-dlp`,
поэтому локальные cookies или account state не могут подключиться незаметно:

```bash
python3 tools/youtube_research.py doctor --json
python3 tools/youtube_research.py search "AI agents" --limit 5 --json
python3 tools/youtube_research.py video "dQw4w9WgXcQ" --json
python3 tools/youtube_research.py channel "https://www.youtube.com/@NousResearch" --tab videos --limit 10 --json
python3 tools/youtube_research.py playlist "https://www.youtube.com/playlist?list=PL590L5WQmH8fJ54F369BLDSqIwcs-TCfs" --limit 10 --json
python3 tools/youtube_research.py transcript "dQw4w9WgXcQ" --languages "en.*,en,ru.*,ru" --json
python3 tools/youtube_research.py comments "9GpWELm3_XI" --limit 10 --sort top --json
```

Для постоянных topic/channel watchlists, comments, snapshots и Markdown reports
есть отдельный публичный companion. Он optional и автоматически не ставится:

```bash
uv tool install --python 3.10 "git+https://github.com/AlekseiUL/youtube-intelligence-stack.git@v0.4.3"
youtube-intel doctor
youtube-intel init ~/youtube-intel-demo --template general
youtube-intel full ~/youtube-intel-demo --safe --query "AI agents" --limit-per-query 3 --skip-watchlist-channels
```

YouTube и `yt-dlp` могут дать partial coverage из-за rate limit, региона,
удалённого видео, bot check, age gate, отсутствующих субтитров или comments.
Pack честно возвращает degraded state и не предлагает обход ограничений.

## Содержимое репозитория

- [`distribution.yaml`](distribution.yaml) — manifest для Hermes profile distribution.
- [`SOUL.md`](SOUL.md) — рабочий prompt researcher-агента.
- [`config.yaml`](config.yaml) — безопасный starter config и preferred capability set.
- [`skills/research-intelligence/SKILL.md`](skills/research-intelligence/SKILL.md) — installable research workflow skill.
- [`skills/markitdown-document-ingestion/SKILL.md`](skills/markitdown-document-ingestion/SKILL.md) — optional workflow для перевода публичных research-файлов в Markdown.
- [`skills/research-intelligence/templates/research-brief.md`](skills/research-intelligence/templates/research-brief.md) — шаблон глубокого research brief.
- [`skills/research-intelligence/templates/source-ledger.md`](skills/research-intelligence/templates/source-ledger.md) — шаблон source ledger.
- [`tools/source_reach_doctor.py`](tools/source_reach_doctor.py) — безопасная диагностика public-source reach: Jina, GitHub public API, Reddit fallback, optional MarkItDown detection, optional YouTube subtitle smoke и detection approval-gated social/MCP tools.
- [`tools/public_reddit_fallback_search.py`](tools/public_reddit_fallback_search.py) — public-only Reddit fallback helper.
- [`tools/github_traction_check.py`](tools/github_traction_check.py) — public GitHub metadata traction check helper.
- [`tools/evidence_lineage_check.py`](tools/evidence_lineage_check.py) — проверяет research-run, независимость источников, контрпримеры, доступность и доказательства важных выводов.
- [`tools/youtube_research.py`](tools/youtube_research.py) — ограниченный public YouTube search, проверка видео/каналов/плейлистов, временное извлечение субтитров и обезличенная выборка комментариев.
- [`skills/youtube-research-pack/SKILL.md`](skills/youtube-research-pack/SKILL.md) — YouTube workflow, evidence gate и privacy boundaries.
- [`skills/youtube-research-pack/templates/youtube-research-brief.md`](skills/youtube-research-pack/templates/youtube-research-brief.md) — шаблон YouTube research brief.
- [`skills/research-intelligence/references/research-modes.md`](skills/research-intelligence/references/research-modes.md) — шесть безопасных режимов исследования и правила остановки.
- [`examples/research-run-source-lineage.json`](examples/research-run-source-lineage.json) — запускаемый пример, где три страницы оказываются одним анонсом.
- [`examples/`](examples/) — реальные example briefs и helper outputs.
- [`docs/assets/researcher-agent-cover.jpg`](docs/assets/researcher-agent-cover.jpg) — обложка / постер агента.
- [`.env.EXAMPLE`](.env.EXAMPLE) — только имена optional env vars, без секретов.
- [`LICENSE`](LICENSE) — MIT license.
- [`NOTICE.md`](NOTICE.md) — canonical source и attribution.
- [`SECURITY.md`](SECURITY.md) — security/safety policy.
- [`SECURITY-SCANNER-NOTES.md`](SECURITY-SCANNER-NOTES.md) — разбор scanner findings и privacy-minimized контракт операционного аудита.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — правила contribution.
- [`CHANGELOG.md`](CHANGELOG.md) — история версий.

## Безопасность, приватность и non-goals

В репозитории намеренно нет:

- API keys или `.env` values;
- OAuth tokens или `auth.json`;
- memories;
- sessions;
- logs;
- workspaces;
- private source lists;
- scheduled cron jobs;
- owner-specific research outputs.

Researcher-профиль по умолчанию работает только с открытыми источниками. Он должен остановиться и спросить подтверждение перед login, signup, payment, joining a group, posting, DM, following, private exports или account sessions.

Для проверяемого запуска YouTube subprocess без записи запросов, целей, аргументов команд и собранного контента добавьте `--audit`; структурированные события `operation-audit/v1` выводятся в `stderr`. Подробности — в [`SECURITY-SCANNER-NOTES.md`](SECURITY-SCANNER-NOTES.md).

## Статус / roadmap

Текущая публичная версия исходного дерева: **v0.4.0**.

В v0.4.0 добавлен публичный YouTube Research Pack со встроенным ограниченным helper и optional deep companion. В v0.3.1 усилены приватность и установка; в v0.3.0 добавлены режимы исследования, группировка источников, контрпримеры и воспроизводимая проверка evidence. Дистрибутив не добавляет доступ к аккаунтам, включённый мониторинг, приватные списки источников или автономные внешние действия.

Возможные следующие улучшения:

- больше безопасных research templates;
- examples для GitHub traction checks, vendor due diligence и paper/tool comparison;
- optional disabled cron examples для пользователей, которые сами хотят мониторинг;
- дополнительные public-source helper scripts после security review.

## Участие в проекте

Contributions welcome, если они улучшают практическую пользу, безопасность, ясность или examples.

Правила:

- никаких secrets, credentials, cookies, sessions, logs или private data;
- никаких owner-specific research outputs;
- никаких включённых cron jobs by default;
- никаких scripts для обхода access controls или scraping behind login;
- claims должны быть source-backed и caveated.

См. [`CONTRIBUTING.md`](CONTRIBUTING.md) и [`SECURITY.md`](SECURITY.md).

## Полезные ссылки / ресурсы

- YouTube: https://youtube.com/@alekseiulianov
- Telegram-канал Sprut AI: https://t.me/Sprut_AI
- Чат Telegram-канала Sprut AI: https://t.me/+eH-qNIDmud8zNDZi
- AI Операционка: https://t.me/tribute/app?startapp=sJyg
- Hermes Agent docs: https://hermes-agent.nousresearch.com/docs/

## Канонический источник

Проект поддерживает Aleksei Ulianov / Sprut_AI.
Оригинальный репозиторий: https://github.com/AlekseiUL/hermes-researcher-agent

Если вы нашли этот проект в зеркале, перепаковке или на сторонней площадке, сверяйтесь с этим репозиторием как с source of truth.

## Attribution

Если лицензия позволяет reuse/fork/modify/package/publish, сохраняйте оригинальный copyright и license notice, а также ссылку на canonical repository.

## Лицензия

MIT. См. [`LICENSE`](LICENSE).
