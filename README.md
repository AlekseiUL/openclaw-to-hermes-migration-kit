# OpenClaw to Hermes Migration Kit

A safety-first migration toolkit for moving OpenClaw-style agent setups into [Hermes Agent](https://github.com/NousResearch/hermes-agent) without losing roles, memory, skills, automations, messaging setup, or rollback control.

This is not a “copy the old folder and hope” package. It is a practical operator kit: audit first, redact secrets, map profiles, migrate one agent at a time, verify behavior, and keep rollback available.

## Who this is for

- OpenClaw users who spent time building agents, prompts, skills, crons, and Telegram bots.
- Hermes users who want a controlled migration instead of a risky one-shot import.
- Consultants or operators who need a repeatable migration checklist for client machines.
- Agent builders who care about secrets, duplicate polling, memory boundaries, and post-migration verification.

## What is included

- Read-only audit scripts for OpenClaw agent footprint discovery.
- Storage/database inventory that reports metadata and schema without dumping rows.
- Secret-pattern scanner for generated reports and docs.
- Active-pointer scanner to catch old-root tails after migration.
- Human migration guide, safety gates, and rollback templates.
- A copy-paste agent prompt for Hermes or Codex to drive the migration.
- Hermes-installable skill package under `openclaw-to-hermes-migration-kit/`.

## Quick start from a clone

```bash
git clone https://github.com/AlekseiUL/openclaw-to-hermes-migration-kit.git
cd openclaw-to-hermes-migration-kit

python3 scripts/openclaw_hermes_audit.py \
  --source ~/.openclaw \
  --out ./my-openclaw-audit.json \
  --pretty

python3 scripts/database_inventory.py \
  --source ~/.openclaw \
  --out ./my-openclaw-storage.json

python3 scripts/secret_pattern_scan.py --path ./my-openclaw-audit.json --json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-storage.json --json
```

Expected first result:

- audit files are created;
- raw secret values are not printed;
- database inventory contains metadata/schema only, not table rows;
- secret scan returns zero findings before sharing any report.

## Install as a Hermes skill

Recommended multi-file install:

```bash
hermes skills install AlekseiUL/openclaw-to-hermes-migration-kit/openclaw-to-hermes-migration-kit
```

Single-file fallback:

```bash
hermes skills install https://raw.githubusercontent.com/AlekseiUL/openclaw-to-hermes-migration-kit/main/SKILL.md
```

Then ask Hermes to load or use `openclaw-to-hermes-migration-kit` before planning a migration.

## Safe migration workflow

1. Read [`docs/start-here.md`](docs/start-here.md).
2. Run read-only audit scripts.
3. Scan generated reports for secrets.
4. Map each OpenClaw agent to a target Hermes profile.
5. Re-enter secrets locally; do not paste raw keys into chat.
6. Migrate one agent/profile at a time.
7. Verify model, tools, skills, memory, cron, messaging, and logs.
8. Cut over Telegram only after the old token holder is stopped.
9. Keep rollback artifacts until the new Hermes profile is proven stable.

## Important safety rules

Do not run a live migration blindly.

Blocked without explicit approval:

- editing `.env`, `auth.json`, OpenClaw config, or Hermes `config.yaml`;
- copying raw secrets or OAuth/session files;
- starting a new Telegram gateway with an old bot token;
- stopping a live gateway;
- deleting old agents, sessions, memory, or databases;
- publishing audit reports that were not scanned and redacted.

Default safe mode:

- audit only;
- metadata only for databases;
- secret names only, not values;
- dry-run before apply;
- one profile at a time;
- rollback plan before cutover.

## Repository contents

```text
README.md
SKILL.md
openclaw-to-hermes-migration-kit/   # installable Hermes multi-file skill
  SKILL.md
  references/
  templates/
  examples/
docs/                               # human-readable guides
scripts/                            # clone-friendly helper scripts
templates/                          # copy-modify migration templates
examples/                           # example migration scenarios
SECURITY.md
CONTRIBUTING.md
CHANGELOG.md
LICENSE
```

## Non-goals

- This kit does not promise a magic one-click migration.
- It does not upload secrets anywhere.
- It does not require sending private `.env`, sessions, or audit dumps to an agent chat.
- It does not replace human approval for Telegram, OAuth, subscriptions, or production automations.

## Links / Resources

- YouTube: https://youtube.com/@alekseiulianov
- Telegram channel Sprut AI: https://t.me/Sprut_AI
- Telegram chat: https://t.me/+eH-qNIDmud8zNDZi
- AI Операционка: https://t.me/tribute/app?startapp=sJyg

## License

MIT License. See [LICENSE](LICENSE).

---

# OpenClaw → Hermes Migration Kit

Набор для безопасной миграции OpenClaw-style агентных контуров в [Hermes Agent](https://github.com/NousResearch/hermes-agent): роли, память, skills, automations, Telegram, providers, доступы, rollback и проверка после переноса.

Это не “скопировать старую папку и молиться”. Нормальный путь такой: сначала аудит, потом redaction, потом mapping профилей, потом перенос по одному агенту, потом проверка живого поведения.

## Для кого

- Для пользователей OpenClaw, у которых уже есть агенты, промпты, skills, cron-задачи и Telegram-боты.
- Для пользователей Hermes, которым нужен контролируемый переход, а не опасный one-shot import.
- Для консультантов и операторов, которые переносят агентные системы на клиентских машинах.
- Для тех, кому важны secrets, duplicate polling, границы памяти и нормальная верификация.

## Что внутри

- Read-only audit scripts для инвентаризации OpenClaw-контура.
- Инвентаризация storage/database: metadata/schema без выгрузки строк.
- Secret-pattern scanner для отчётов и документов.
- Active-pointer scanner, чтобы ловить хвосты на старые roots.
- Human migration guide, safety gates и rollback templates.
- Готовый prompt для Hermes/Codex, чтобы вести миграцию по шагам.
- Installable Hermes skill package в `openclaw-to-hermes-migration-kit/`.

## Быстрый старт из clone

```bash
git clone https://github.com/AlekseiUL/openclaw-to-hermes-migration-kit.git
cd openclaw-to-hermes-migration-kit

python3 scripts/openclaw_hermes_audit.py \
  --source ~/.openclaw \
  --out ./my-openclaw-audit.json \
  --pretty

python3 scripts/database_inventory.py \
  --source ~/.openclaw \
  --out ./my-openclaw-storage.json

python3 scripts/secret_pattern_scan.py --path ./my-openclaw-audit.json --json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-storage.json --json
```

Ожидаемо:

- audit-файлы созданы;
- raw secret values не напечатаны;
- database inventory содержит metadata/schema, не строки таблиц;
- secret scan даёт ноль находок перед тем, как отчёт кому-то показывать.

## Установка как Hermes skill

Рекомендуемая multi-file установка:

```bash
hermes skills install AlekseiUL/openclaw-to-hermes-migration-kit/openclaw-to-hermes-migration-kit
```

Single-file fallback:

```bash
hermes skills install https://raw.githubusercontent.com/AlekseiUL/openclaw-to-hermes-migration-kit/main/SKILL.md
```

После этого загружайте `openclaw-to-hermes-migration-kit` перед планированием миграции.

## Безопасный workflow

1. Открыть [`docs/start-here.md`](docs/start-here.md).
2. Запустить read-only audit.
3. Проверить отчёты secret scanner-ом.
4. Сопоставить каждого OpenClaw agent с новым Hermes profile.
5. Ввести secrets локально; не вставлять raw keys в чат.
6. Переносить по одному agent/profile.
7. Проверить model, tools, skills, memory, cron, messaging и logs.
8. Telegram переносить только после остановки старого token holder.
9. Держать rollback artifacts, пока новый Hermes profile не доказал стабильность.

## Жёсткие правила безопасности

Без явного approval нельзя:

- менять `.env`, `auth.json`, OpenClaw config или Hermes `config.yaml`;
- копировать raw secrets или OAuth/session files;
- запускать новый Telegram gateway со старым bot token;
- останавливать live gateway;
- удалять старых agents, sessions, memory или databases;
- публиковать audit reports без scan/redaction.

Safe mode по умолчанию:

- только audit;
- для баз — только metadata;
- показываем названия ключей, не значения;
- dry-run перед apply;
- один profile за раз;
- rollback до cutover.

## Полезные ссылки

- YouTube: https://youtube.com/@alekseiulianov
- Telegram-канал Sprut AI: https://t.me/Sprut_AI
- Чат Telegram-канала Sprut AI: https://t.me/+eH-qNIDmud8zNDZi
- AI Операционка: https://t.me/tribute/app?startapp=sJyg

## Лицензия

MIT License. См. [LICENSE](LICENSE).
