# Database migration plan template

## Source

- Source root:
- Agent/profile:
- Inventory file:
- Date:
- Operator:

## Storage inventory summary

```text
Total storage candidates:
SQLite:
JSON/JSONL:
Vector/index dirs:
External DB connectors:
Secret-name-risk files:
Damaged/unreadable files:
```

## Per-storage decisions

### Storage: <path>

- Type:
- Purpose:
- Size:
- Private risk: low / medium / high
- Secret risk: yes / no
- Integrity check:
- Recommended action: archive / import / rebuild / reconnect / quarantine
- Target Hermes location:
- Verification:
- Rollback:

## External databases

Do not paste connection strings here.

```text
Service: PostgreSQL / MySQL / Supabase / Notion / Airtable / Sheets / other
Needed by profile:
Action: reconnect connector, not copy dump
Credential entry: local only
Smoke test:
```

## Memory import policy

- Raw sessions imported into active memory: yes/no
- Summary created: yes/no
- Embeddings rebuilt: yes/no
- Private memory separated by profile: yes/no
- Global memory pollution checked: yes/no

## Approval gates

- [ ] User approved importing private data.
- [ ] User approved Telegram cutover if needed.
- [ ] User approved external DB reconnect if needed.
- [ ] Rollback archive exists.
