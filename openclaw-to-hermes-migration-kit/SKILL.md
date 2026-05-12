---
name: openclaw-to-hermes-migration-kit
description: Use when planning or executing a safety-first migration from an OpenClaw-style agent setup into Hermes Agent. Audits old agents, maps profiles, protects secrets, handles memory/skills/cron/messaging, and requires verification gates before cutover.
version: 1.0.0
author: AlekseiUL
license: MIT
metadata:
  hermes:
    tags: [openclaw, hermes-agent, migration, agents, skills, memory, telegram, automation, security]
    related_skills: [hermes-agent, systematic-debugging]
---

# OpenClaw to Hermes Migration Kit

## Overview

This skill guides a controlled migration from an OpenClaw-style agent setup into Hermes Agent.

The goal is not to copy everything blindly. The goal is to preserve useful agent behavior while protecting secrets, sessions, Telegram tokens, databases, memory boundaries, and rollback options.

## When to Use

Use this skill when the user wants to:

- migrate OpenClaw agents to Hermes Agent;
- audit old roles, skills, memory, crons, tools, provider config, and messaging setup;
- prepare a subscriber/client migration kit;
- avoid duplicate Telegram polling during cutover;
- move agent knowledge without leaking private `.env`, auth/session files, or raw audit data.

Do not use it for generic Hermes setup only; use the `hermes-agent` skill for that.

## Default Workflow

1. Start with a read-only audit.
2. Generate a storage/database inventory with metadata only.
3. Run secret scans on every generated report before sharing.
4. Build an agent-to-profile mapping.
5. Re-enter secrets locally instead of pasting values into chat.
6. Migrate one profile at a time.
7. Verify model, skills, memory, tools, cron, messaging, and logs.
8. Cut over Telegram only after the old token holder is stopped.
9. Keep rollback artifacts until the new Hermes profile is proven stable.

## Core Commands

From a cloned repository:

```bash
python3 scripts/openclaw_hermes_audit.py --source ~/.openclaw --out ./my-openclaw-audit.json --pretty
python3 scripts/database_inventory.py --source ~/.openclaw --out ./my-openclaw-storage.json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-audit.json --json
python3 scripts/secret_pattern_scan.py --path ./my-openclaw-storage.json --json
```

When installed as a Hermes skill, use it as the decision and safety playbook. For executable helper scripts, clone the public repository and run scripts from the clone so the user can inspect them before execution.

## Safety Rules

Blocked without explicit approval:

- editing `.env`, `auth.json`, OpenClaw config, or Hermes `config.yaml`;
- copying raw secrets or OAuth/session files;
- starting a Hermes gateway with an old Telegram bot token;
- stopping a live gateway;
- deleting old agents, sessions, memory, databases, or archives;
- publishing unscanned migration reports.

Default secrets policy:

- detect key names and source files;
- do not print values;
- show where each key should be entered locally;
- keep automatic secret migration as advanced mode only.

## Supporting References

In the multi-file package, read:

- `references/start-here.md`
- `references/copy-this-to-hermes-or-codex.md`
- `references/keys-and-access-policy.md`
- `references/human-migration-guide.md`
- `references/migration-playbook.md`
- `references/migration-checklist.md`
- `references/database-and-memory-migration.md`
- `references/reliability-and-safety-gates.md`

## Verification Checklist

- [ ] Source OpenClaw root was audited read-only.
- [ ] Generated reports passed secret scan.
- [ ] Database inventory contains metadata/schema only, not rows.
- [ ] Old and new profile boundaries are explicit.
- [ ] No raw secrets were pasted into chat or committed.
- [ ] Telegram token holder was identified before cutover.
- [ ] Hermes profile was verified with a live smoke task.
- [ ] Rollback plan exists and was not deleted early.
