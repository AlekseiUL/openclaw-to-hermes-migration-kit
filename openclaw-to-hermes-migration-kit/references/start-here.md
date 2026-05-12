# OpenClaw → Hermes: старт для человека

Этот набор нужен, если у вас уже настроен OpenClaw: агенты, правила, промпты, skills, Telegram-боты, cron-задачи, ключи, память, локальные файлы - и вы хотите перейти на Hermes без ручной пересборки всего с нуля.

## Самая короткая версия

1. Сначала делаем **аудит** старого OpenClaw. Без ключей, без изменений.
2. Отдельно делаем **аудит баз и памяти**: SQLite, JSONL, sessions, vector DB, external connectors.
3. Получаем список: какие агенты есть, какие skills, память, crons, Telegram, providers, ключи нужны.
4. Hermes/Codex делает **план миграции**.
5. Вы подтверждаете, что можно переносить.
6. Только после этого переносим агента в Hermes profile.
7. Проверяем: агент отвечает, skills видны, cron работает, Telegram не конфликтует, базы/память не перепутаны, секреты не утекли.

## Что не надо делать

Не надо сразу скидывать все ключи агенту в чат.

Нормальный путь такой:

- аудит видит **названия ключей**, но не печатает значения;
- человек получает список: какие ключи нужны Hermes;
- ключи вводятся локально через Hermes setup/auth или в локальный `.env` профиль;
- агент не публикует, не сохраняет и не отправляет ключи наружу.

## Какой файл использовать

Если хотите, чтобы Hermes или Codex сам вёл процесс, дайте ему этот файл:

```text
COPY_THIS_TO_HERMES_OR_CODEX.md
```

Если хотите понять, что делать руками, читайте:

```text
HUMAN_MIGRATION_GUIDE.md
```

Если вопрос только про ключи и подписки:

```text
KEYS_AND_ACCESS_POLICY.md
```

## Безопасный первый запуск

```bash
cd openclaw-to-hermes-migration-kit
python3 scripts/openclaw_hermes_audit.py --source ~/.openclaw --out ./my-openclaw-audit.json --pretty
python3 scripts/database_inventory.py --source ~/.openclaw --out ./my-openclaw-storage.json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-audit.json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-storage.json
```

Ожидаемый результат:

- audit-файл создан;
- storage inventory создан;
- значения ключей не напечатаны;
- secret scan показывает `findings=0`;
- базы классифицированы: archive / import / rebuild / reconnect / quarantine.

## Что получится в конце

Для каждого агента будет понятная карточка:

- старый OpenClaw agent id;
- новый Hermes profile;
- какие prompts/roles перенести;
- какие skills перенести;
- какая память переносится как активная, а какая только архивом;
- какие ключи надо заново ввести;
- какие Telegram/cron настройки включить;
- как проверить;
- как откатиться.

## Главный риск

Telegram-боты. Нельзя оставлять OpenClaw и Hermes одновременно с одним bot token. Получится конфликт polling, бот начнёт молчать или отвечать нестабильно.

Поэтому Telegram переносится только после отдельного подтверждения.
