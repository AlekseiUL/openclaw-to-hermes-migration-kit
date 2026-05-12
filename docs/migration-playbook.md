# OpenClaw → Hermes Migration Playbook

## 0. Product stance

There are two migration layers:

1. **Framework migration** — what `hermes claw migrate` can import from an OpenClaw root.
2. **Operational migration** — the actual hard part: Telegram ownership, auth routes, crons, skills, memory boundaries, active filesystem tails, and verification.

Use the built-in command when it helps. Do not confuse it with a complete production cutover.

## 1. Preflight

Collect:

- source root path;
- target Hermes profile name;
- target workspace path;
- privacy class;
- whether Telegram is in scope;
- whether secrets are in scope;
- whether live cutover is approved.

Run:

```bash
hermes --version
hermes claw migrate --help
hermes profile list
hermes tools list
```

For Operator team work, use board `<kanban-board>` and keep `orchestrator` as dispatcher.

## 2. Source audit

Run the read-only audit:

```bash
python3 scripts/openclaw_hermes_audit.py --source ~/.openclaw --out audit.json
python3 scripts/database_inventory.py --source ~/.openclaw --out storage.json
```

Inspect:

- `openclaw.json` presence;
- `.env` key names only;
- `agents/<id>/agent` files;
- `agents/<id>/sessions` counts;
- skills directories;
- cron/jobs files;
- likely Telegram env keys;
- provider/auth files presence;
- storage candidates: SQLite, JSONL, JSON/CSV/Parquet, vector/index directories, external connector hints.

Do not dump raw sessions into final docs. Summarize.

## 3. Dependency classes

### Profiles and roles

OpenClaw often separates visible character name from internal id. Example from our history: business-agent visible name mapped to `producer` source id. Never assume folder name equals bot identity.

### Memory

Memory splits into:

- durable memory facts;
- wiki/reference documents;
- private continuity files;
- legacy sessions archive.

Do not index raw psychological, finance, token, or client-private sessions by default.

### Databases and storage

Treat storage as a separate migration class, not as generic memory.

Classify every candidate:

- config/state DB: archive and extract settings, do not activate directly in Hermes;
- sessions DB/JSONL: archive and summarize, do not bulk-index by default;
- memory/vector DB: rebuild embeddings/search indexes in Hermes from source documents when possible;
- tool/application DB: reconnect tool/config only if the target profile really needs it;
- external DB: reconnect locally, do not paste connection strings into reports;
- unknown/secret-named storage: quarantine for manual review.

Use:

```bash
python3 scripts/database_inventory.py --source ~/.openclaw --out storage.json
```

Expected output is metadata and schema only. No row contents, messages, documents or secret values.

See `DATABASE_AND_MEMORY_MIGRATION.md` and `templates/database-migration-plan.md`.

### Skills

Skill migration is rewrite, not copy:

- convert frontmatter to Hermes-compatible `name`/`description`;
- remove OpenClaw hardcoded commands;
- replace old roots with target-owned roots;
- quarantine legacy/provenance material;
- verify `hermes --profile <profile> skills list` sees it.

### Tools/scripts

Prefer Hermes built-ins where possible:

- file/search/patch instead of custom FS scripts;
- terminal/process instead of shell wrappers;
- cronjob/Hermes cron instead of OpenClaw cron;
- memory/session_search instead of bespoke memory search;
- MCP/plugin only when a real integration is needed.

### Providers/subscriptions

Separate routes:

- OpenAI API key billing;
- OpenAI Codex OAuth / ChatGPT-subscription-backed route;
- OpenRouter key;
- Anthropic key;
- Groq STT;
- ElevenLabs/TTS;
- custom OpenAI-compatible endpoints.

ChatGPT Plus/Pro/Team is not automatically an OpenAI API key.

### Telegram

Hard rule: one polling holder per bot token.

Cutover order:

1. Identify source token env key without printing value.
2. Identify old holder: OpenClaw gateway, Ductor, old Hermes profile, launchd service.
3. Stop/remove old holder only after backup and approval.
4. Start Hermes gateway.
5. Wait long enough for Telegram polling retries.
6. Confirm no fresh `polling conflict` in new profile logs.

## 4. Target Hermes layout

Generic:

```text
~/.hermes/profiles/<profile>/
  config.yaml
  .env
  SOUL.md
  skills/
  memories/
  logs/

<workspace>/<agent>/
  RoleBrief.md
  data/
  memory/
  references/
  skills/
  sessions/legacy-openclaw/
  reports/
  migration/
```

Example local layout:

```text
~/hermes-migrated-agents/<agent>
~/hermes-migrated-agents/<agent>/docs/README.md
~/.hermes/profiles/<profile>
```

## 5. Built-in Hermes `claw migrate`

Live check on this machine showed:

```text
hermes claw migrate [-h] [--source SOURCE] [--dry-run]
                    [--preset {user-data,full}] [--overwrite]
                    [--migrate-secrets] [--no-backup]
                    [--workspace-target WORKSPACE_TARGET]
                    [--skill-conflict {skip,overwrite,rename}] [--yes]
```

Description: imports settings, memories, skills and API keys from OpenClaw; always previews before making changes. Secrets are intended to require `--migrate-secrets`.

Recommended safe use today:

```bash
hermes claw migrate --source ~/.openclaw --dry-run --preset full
```

Do **not** use unattended real apply yet on this local checkout.

Technical reviewer review found blockers in the implementation/posture:

- Discord/Slack tokens can migrate without `--migrate-secrets`.
- Raw archive files can persist secret-bearing configs.
- Provider secret allowlist is not strict under `--migrate-secrets`.
- Duplicate polling/session protection is warning-only and bypassable with `--yes`.
- Direct script path can write to wrong Hermes profile unless `HERMES_HOME`/target is explicit.
- Dry-run can hide cron-store-only migrations.

So the kit policy is:

1. Use built-in dry-run for discovery.
2. Treat any apply as blocked until the blockers are fixed or wrapped by stricter local safeguards.
3. Prefer manual/profile-by-profile migration for Telegram/secrets/crons.

## 6. Kanban execution model

Suggested graph:

- Research reviewer: external source ledger and unverified claims.
- Technical reviewer: technical dry-run and script safety review.
- Privacy reviewer: secrets/privacy/approval gates.
- Implementation reviewer: build scripts/templates and run tests.
- Operator: final synthesis and owner report.

Generated commands are available via:

```bash
python3 scripts/render_kanban_tasks.py --agent <agent> --profile <profile>
```

## 7. Verification gates

Minimum:

- dry-run audit completes;
- secret scan returns zero high-confidence leaks in generated reports;
- active pointer scan distinguishes forbidden active roots from allowed legacy/provenance mentions;
- database inventory exists and every storage candidate has an action;
- no direct blind copy into Hermes internal DBs;
- vector/search indexes are rebuilt or explicitly archived;
- target profile model smoke passes;
- skills list shows expected migrated skills;
- cron list shows migrated jobs but no unwanted delivery;
- Telegram gateway status is running only after approval;
- duplicate polling stays zero after 60–90 seconds;
- rollback plan exists.

## 8. Rollback

Before apply, backup:

- Hermes target profile;
- Hermes root config if touched;
- OpenClaw config metadata;
- old `.env` metadata or full encrypted/local backup if approved;
- migration plan.

Rollback must state:

- how to stop new Hermes gateway;
- how to restore OpenClaw binding;
- how to restore tokens/config;
- how to verify old bot answers again;
- how to remove partial target profile safely.
