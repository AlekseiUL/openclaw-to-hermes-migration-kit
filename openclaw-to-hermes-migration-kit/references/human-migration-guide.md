# Как перенести OpenClaw в Hermes без пересборки с нуля

## Что решаем

У вас уже есть OpenClaw. Там долго настраивались:

- агенты;
- роли и промпты;
- skills;
- память и сессии;
- Telegram-боты;
- cron-задачи;
- API-ключи;
- локальные инструменты и файлы.

Переходить на Hermes тяжело, потому что страшно потерять всё это. Этот набор делает переход управляемым.

## Простая схема

```text
OpenClaw audit → migration plan → Hermes profiles → keys setup → Telegram/cron cutover → smoke tests → cleanup
```

## Шаг 1. Сделать аудит

```bash
python3 scripts/openclaw_hermes_audit.py --source ~/.openclaw --out ./my-openclaw-audit.json --pretty
```

Что это делает:

- смотрит структуру OpenClaw;
- находит агентов;
- считает sessions;
- находит role/memory/skills/tools файлы;
- находит названия ключей;
- не печатает значения ключей.

Проверка:

```bash
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-audit.json
```

Если `findings=0`, audit безопасен для дальнейшей работы.

## Шаг 2. Выбрать агента

Пример:

```text
OpenClaw agent: researcher
Новый Hermes profile: hermes-researcher
```

Сгенерировать черновик структуры:

```bash
python3 scripts/generate_profile_skeleton.py --agent researcher --profile hermes-researcher --dry-run
```

## Шаг 3. Составить карту переноса

Заполнить:

```text
templates/profile-mapping.yaml
```

Главные решения:

- какие role/prompt файлы становятся `SOUL.md`;
- какие skills переписываются под Hermes;
- какая память идёт в active memory;
- какие sessions остаются архивом;
- какие crons переносить;
- какие ключи надо заново добавить;
- нужен ли Telegram cutover.

## Шаг 4. Ввести ключи в Hermes

Не скидывать ключи агенту в чат.

Используйте `KEYS_AND_ACCESS_POLICY.md`.

Обычно:

- API keys вводятся локально в Hermes auth/config/profile `.env`;
- OpenAI Codex OAuth проходится локально через `hermes auth add openai-codex --type oauth`;
- Telegram token добавляется только перед cutover, когда старый OpenClaw holder остановлен.

## Шаг 5. Перенести skills и role

Не копировать OpenClaw skills вслепую.

Каждый skill проверить:

- нет ли старых путей `~/.openclaw`;
- нет ли старых команд OpenClaw;
- нет ли секретов;
- понятен ли target Hermes profile;
- видит ли Hermes этот skill.

Проверка:

```bash
hermes --profile <profile> skills list
```

## Шаг 6. Перенести cron

Cron не включать автоматически.

Сначала описать:

- что делает job;
- когда запускается;
- есть ли внешние отправки;
- нужен ли `[SILENT]`, если всё нормально;
- какие ключи нужны.

Потом создать Hermes cron вручную или через agent после approval.

## Шаг 7. Telegram cutover

Если агент был Telegram-ботом:

1. Определить старый OpenClaw holder.
2. Backup.
3. Остановить старый holder.
4. Добавить token в Hermes profile.
5. Запустить Hermes gateway.
6. Подождать 60-90 секунд.
7. Проверить, что нет polling conflict.
8. Отправить тестовое сообщение.

## Шаг 8. Проверить

Минимум:

```bash
hermes --profile <profile> chat -Q -q 'Ответь ровно: OK'
hermes --profile <profile> skills list
hermes --profile <profile> cron list
hermes --profile <profile> gateway status
```

И scan:

```bash
python3 scripts/secret_pattern_scan.py --path <target-folder>
python3 scripts/active_pointer_scan.py --path <target-folder> --json
```

## Шаг 9. Не удалять OpenClaw сразу

Сначала дать Hermes-агенту поработать.

OpenClaw держать как backup, но без активного Telegram polling на тот же token.

Удаление старого контура - отдельный этап.
