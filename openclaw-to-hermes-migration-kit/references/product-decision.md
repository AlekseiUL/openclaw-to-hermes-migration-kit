# Product decision

## Recommended MVP

Ship as a **Hermes skill pack + AGENT.md prompt + dry-run scripts**.

Why:

- Most of the migration is reasoning + safety gates, not just code.
- Hermes already has profiles, skills, memory, cron, gateway, MCP, Kanban and built-in `hermes claw migrate`.
- A plugin is premature until we see repeated migrations and stable edge cases.
- GitHub repo is useful for distribution later, but the first internal version should stay local and Operator-owned.


## Subscriber-facing product shape

Для подписчиков основной продукт должен выглядеть не как “repo для инженера”, а как простой набор:

1. `START_HERE_FOR_SUBSCRIBERS.md` - начать здесь.
2. `COPY_THIS_TO_HERMES_OR_CODEX.md` - один prompt, который можно дать агенту.
3. `KEYS_AND_ACCESS_POLICY.md` - что делать с ключами и подписками.
4. `HUMAN_MIGRATION_GUIDE.md` - пошаговая инструкция руками.
5. `scripts/openclaw_hermes_audit.py` - первый безопасный audit.

Позиционирование: “миграционный помощник”, а не “волшебная кнопка”. Волшебная кнопка опасна из-за Telegram polling, secrets и cron side effects.

## Product layers

1. **Instruction layer**: `OPENCLAW_TO_HERMES_MIGRATION_AGENT.md`.
2. **Operator method**: `MIGRATION_PLAYBOOK.md`.
3. **Dry-run scripts**: audit, secret scan, active pointer scan, skeleton preview.
4. **Templates**: inventory, mapping, rollback, final report.
5. **Kanban route**: generated specialist tasks.

## Next packaging step

Create Hermes skill:

```text
openclaw-to-hermes-migration/SKILL.md
references/MIGRATION_PLAYBOOK.md
scripts/openclaw_hermes_audit.py
scripts/secret_pattern_scan.py
scripts/active_pointer_scan.py
scripts/generate_profile_skeleton.py
```

Then publish as GitHub skill/repo only after 2–3 real migrations pass.

## Not chosen yet: full Hermes plugin

A plugin makes sense later if we want commands like:

```bash
hermes openclaw audit
hermes openclaw plan --agent support-agent
hermes openclaw apply --plan plan.json
```

Not now. Too easy to hide dangerous cutover behind a friendly command.
