# Reliability and safety gates

## Цель

Чтобы у человека ничего не поломалось при переходе с OpenClaw на Hermes.

## Нулевое правило

До явного approval миграционный агент работает только в режиме:

```text
read-only audit + dry-run + report
```

## Gate 1. Source preservation

Перед любым изменением:

- [ ] source root найден;
- [ ] OpenClaw version/status сохранён;
- [ ] список агентов сохранён;
- [ ] `.env` значения не печатались;
- [ ] backup plan готов;
- [ ] rollback plan готов.

## Gate 2. Secrets safety

- [ ] отчёт показывает только key names;
- [ ] raw secret values не попали в Markdown/JSON/report;
- [ ] advanced secret migration выключена;
- [ ] Telegram token не используется, пока старый holder не остановлен;
- [ ] OAuth/session files не копируются вслепую.

## Gate 3. Database safety

- [ ] `database_inventory.py` запущен;
- [ ] DB классифицированы: config/state, sessions, memory/vector, tool/app, flat files;
- [ ] SQLite quick_check сделан для SQLite;
- [ ] vector indexes marked as rebuild, not blind copy;
- [ ] raw sessions archived, not auto-indexed;
- [ ] external DB credentials not printed;
- [ ] source DB не удаляется.

## Gate 4. Profile isolation

- [ ] каждый OpenClaw agent получает отдельный Hermes profile;
- [ ] active files не ссылаются на старый OpenClaw root;
- [ ] legacy files лежат в `legacy-openclaw/` или `archive/`;
- [ ] skills переписаны под Hermes;
- [ ] profile smoke проходит.

## Gate 5. Telegram cutover

- [ ] старый holder найден;
- [ ] downtime/rollback объяснён;
- [ ] старый holder остановлен до запуска Hermes gateway;
- [ ] после запуска Hermes нет fresh polling conflict 60-90 секунд;
- [ ] тестовое сообщение отправлено только после approval.

## Gate 6. Cron and automation

- [ ] jobs классифицированы read-only/write/external-send;
- [ ] чистые проверки имеют `[SILENT]` режим;
- [ ] внешние отправки выключены до approval;
- [ ] one-shot dry run пройден;
- [ ] timezone проверен.

## Gate 7. Final smoke

Минимум:

```bash
hermes --profile <profile> chat -Q -q 'Reply exactly: OK'
hermes --profile <profile> skills list
hermes --profile <profile> cron list
hermes --profile <profile> gateway status
python3 scripts/secret_pattern_scan.py --path <target-folder>
python3 scripts/active_pointer_scan.py --path <target-folder> --json
```

## Fail closed

Если любой gate не пройден:

- не продолжать apply;
- не “чинить на ходу”;
- написать `BLOCKED` и причину;
- дать безопасный следующий шаг.
