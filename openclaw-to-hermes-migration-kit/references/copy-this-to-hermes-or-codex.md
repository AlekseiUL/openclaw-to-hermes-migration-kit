# Задача для Hermes/Codex: перенести OpenClaw агента в Hermes безопасно

Ты должен помочь мне перенести уже настроенный OpenClaw агент в Hermes Agent.

Главная цель: сохранить рабочую настройку агента - роль, промпты, skills, память, sessions archive, tools, cron, Telegram и provider/key requirements - без утечки секретов и без поломки старого контура.

## Жёсткие правила

1. Сначала только audit/dry-run. Никаких изменений.
2. Не печатай значения API keys, Telegram tokens, OAuth/session tokens, cookies, passwords.
3. Не запускай Hermes gateway с Telegram token, пока не найден и не остановлен старый OpenClaw holder.
4. Не удаляй OpenClaw files, sessions, memory или config без отдельного approval.
5. Не используй `hermes claw migrate --yes` или apply-mode как unattended путь.
6. `hermes claw migrate --dry-run` можно использовать только как discovery/preview.
7. Если нужны ключи, выдай список key names и инструкцию, куда человеку ввести их локально. Не проси прислать ключи в чат.

## Что сделать

### 1. Проверить окружение

Выполни:

```bash
hermes --version
hermes claw migrate --help
hermes profile list
```

### 2. Провести read-only audit OpenClaw

Если kit рядом, используй:

```bash
python3 scripts/openclaw_hermes_audit.py --source ~/.openclaw --out ./openclaw-audit.json --pretty
python3 scripts/database_inventory.py --source ~/.openclaw --out ./openclaw-storage.json
python3 scripts/secret_pattern_scan.py --path ./openclaw-audit.json
python3 scripts/secret_pattern_scan.py --path ./openclaw-storage.json
```

Если kit нет, сам сделай read-only inventory без печати секретов.

### 3. Сформировать migration plan

Для каждого агента укажи:

- OpenClaw agent id;
- visible name, если есть;
- target Hermes profile;
- role/prompt files;
- skills;
- memory files;
- database/storage files: SQLite, JSONL, vector DB, flat files, external DB connectors;
- database action for each item: archive / import / rebuild / reconnect / quarantine;
- sessions count/archive plan;
- tools/scripts;
- cron/jobs;
- provider/key requirements;
- Telegram status;
- risks;
- approval needed.

### 4. Сформировать keys plan

Вывести только так:

```text
Нужен ключ: OPENROUTER_API_KEY
Где найден: ~/.openclaw/.env
Куда добавить: Hermes profile <profile>
Способ: вручную через Hermes auth/config или profile .env
Значение: не показываю
```

### 5. Предложить apply-план, но не выполнять

Apply-план должен включать:

- backup;
- создание Hermes profile;
- копирование role/skills/data by value;
- перенос databases только по классификации: config/state не активировать, sessions архивировать/суммаризировать, vector indexes перестраивать, external DB переподключать;
- перенос sessions только как legacy archive;
- ручной ввод ключей;
- cron migration после approval;
- Telegram cutover после approval;
- smoke tests;
- rollback.

### 6. Остановиться на approval gate

В конце спроси человека:

```text
Можно переходить к apply для агента <agent>? Это изменит: <список>. Риски: <список>. Rollback: <коротко>.
```

Без approval не продолжать.

## Формат ответа

Коротко и структурно:

```text
Audit done.
Agents found: N
Recommended first migration: <agent>
Keys needed: <names only>
Telegram risk: yes/no
Next safe action: <one command or one approval question>
```
