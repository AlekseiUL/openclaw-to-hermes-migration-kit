# Migration checklist

## Read-only audit

- [ ] Confirm source root.
- [ ] Confirm target profile name.
- [ ] Run `hermes --version`.
- [ ] Run `hermes claw migrate --help`.
- [ ] Run `hermes claw migrate --source <root> --dry-run --preset full` if safe.
- [ ] Run `scripts/openclaw_hermes_audit.py`.
- [ ] Produce `agent-inventory.json`.
- [ ] Produce redacted secrets inventory.
- [ ] Identify Telegram holders without printing tokens.
- [ ] Identify crons/hooks/automations.
- [ ] Identify skills and custom tools.
- [ ] Identify memory/session classes.
- [ ] Run `scripts/database_inventory.py`.
- [ ] Identify SQLite/JSONL/vector DB/external DB connectors.
- [ ] Check SQLite integrity without reading rows.
- [ ] Classify every storage item: archive / import / rebuild / reconnect / quarantine.

## Plan

- [ ] Map OpenClaw agent id to Hermes profile.
- [ ] Map role files to target `SOUL.md`/RoleBrief.
- [ ] Decide skills: copy, rewrite, quarantine, skip.
- [ ] Decide memory: durable, wiki/reference, private continuity, legacy archive.
- [ ] Decide databases/storage: direct archive, knowledge import, index rebuild, external reconnect, or quarantine.
- [ ] Decide crons: migrate, rewrite, disable, skip.
- [ ] Decide provider/auth route.
- [ ] Decide Telegram cutover route.
- [ ] Write rollback plan.

## Apply gate

- [ ] Human approved live changes.
- [ ] Backup path exists.
- [ ] Secrets policy accepted.
- [ ] Old polling holder identified.
- [ ] Downtime window accepted.

## Verification

- [ ] Hermes profile smoke returns exact OK.
- [ ] Skills visible in target profile.
- [ ] Database/storage plan verified; no direct blind DB copy into Hermes internals.
- [ ] Vector/search indexes rebuilt or explicitly archived.
- [ ] Cron jobs listed and safe.
- [ ] Gateway status verified if Telegram in scope.
- [ ] No fresh duplicate polling conflicts.
- [ ] Secret scan clean.
- [ ] Active pointer scan clean or justified.
- [ ] Final report written.
