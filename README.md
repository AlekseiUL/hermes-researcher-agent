# Hermes Researcher Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Hermes Researcher Agent cover: dramatic researcher poster with the text “researcher” and “из-под земли достану”.](docs/assets/researcher-agent-cover.jpg)

A privacy-safe Hermes Agent profile for public-source research, source scouting, evidence grading, and decision-ready briefs.

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
- **Public-source boundary** — no private data, sessions, cookies, credentials, or login-gated scraping by default.
- **Research skill pack** — includes `research-intelligence` with source ladders, output templates, and safety rules.
- **Browser-aware workflow** — browser verification is recommended when live page state, comments, metrics, visuals, or login walls matter.
- **Public Reddit fallback helper** — handles blocked Reddit JSON as degraded coverage and uses archive hits only as leads that require live verification.
- **Bilingual documentation** — English and Russian instructions in one README.

## Installation

```bash
hermes profile install github.com/AlekseiUL/hermes-researcher-agent --alias
```

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
Question -> Decision frame -> Source ladder -> Evidence collection -> Browser verification -> Evidence gate -> Decision-ready brief
```

## Repository contents

- [`distribution.yaml`](distribution.yaml) — Hermes profile distribution manifest.
- [`SOUL.md`](SOUL.md) — researcher operating prompt.
- [`config.yaml`](config.yaml) — safe starter config and preferred capability set.
- [`skills/research-intelligence/SKILL.md`](skills/research-intelligence/SKILL.md) — installable research workflow skill.
- [`skills/research-intelligence/templates/research-brief.md`](skills/research-intelligence/templates/research-brief.md) — deep research brief template.
- [`skills/research-intelligence/templates/source-ledger.md`](skills/research-intelligence/templates/source-ledger.md) — source ledger template.
- [`tools/public_reddit_fallback_search.py`](tools/public_reddit_fallback_search.py) — public-only Reddit fallback helper.
- [`docs/assets/researcher-agent-cover.jpg`](docs/assets/researcher-agent-cover.jpg) — repository cover / agent poster.
- [`.env.EXAMPLE`](.env.EXAMPLE) — optional environment variable names only; no secrets.
- [`LICENSE`](LICENSE) — MIT license.
- [`NOTICE.md`](NOTICE.md) — canonical source and attribution.
- [`SECURITY.md`](SECURITY.md) — safety and security policy.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules.

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

## Status / roadmap

Current status: **v0.1 public distribution**.

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

Безопасный профиль Hermes Agent для research-задач по открытым источникам: поиск источников, проверка фактов, оценка доказательств и короткие решения, по которым можно действовать.

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
- **Public-source boundary** — по умолчанию нет приватных данных, sessions, cookies, credentials и login-gated scraping.
- **Research skill pack** — внутри `research-intelligence`: source ladders, шаблоны ответов, safety rules.
- **Browser-aware workflow** — browser verification нужен, когда важны live page state, comments, metrics, visuals или login walls.
- **Public Reddit fallback helper** — если Reddit JSON заблокирован, источник помечается как degraded, а archive hits считаются только leads для live-проверки.
- **Документация EN/RU** — английская и русская версии в одном README.

## Установка

```bash
hermes profile install github.com/AlekseiUL/hermes-researcher-agent --alias
```

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
Вопрос -> Decision frame -> Source ladder -> Evidence collection -> Browser verification -> Evidence gate -> Decision-ready brief
```

## Содержимое репозитория

- [`distribution.yaml`](distribution.yaml) — manifest для Hermes profile distribution.
- [`SOUL.md`](SOUL.md) — рабочий prompt researcher-агента.
- [`config.yaml`](config.yaml) — безопасный starter config и preferred capability set.
- [`skills/research-intelligence/SKILL.md`](skills/research-intelligence/SKILL.md) — installable research workflow skill.
- [`skills/research-intelligence/templates/research-brief.md`](skills/research-intelligence/templates/research-brief.md) — шаблон глубокого research brief.
- [`skills/research-intelligence/templates/source-ledger.md`](skills/research-intelligence/templates/source-ledger.md) — шаблон source ledger.
- [`tools/public_reddit_fallback_search.py`](tools/public_reddit_fallback_search.py) — public-only Reddit fallback helper.
- [`docs/assets/researcher-agent-cover.jpg`](docs/assets/researcher-agent-cover.jpg) — обложка / постер агента.
- [`.env.EXAMPLE`](.env.EXAMPLE) — только имена optional env vars, без секретов.
- [`LICENSE`](LICENSE) — MIT license.
- [`NOTICE.md`](NOTICE.md) — canonical source и attribution.
- [`SECURITY.md`](SECURITY.md) — security/safety policy.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — правила contribution.

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

## Статус / roadmap

Текущий статус: **v0.1 public distribution**.

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
