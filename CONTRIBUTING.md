# Contributing

Contributions are welcome if they preserve the safety-first contract.

Before opening a PR:

1. Keep examples synthetic.
2. Do not add real `.env`, auth files, Telegram session files, database dumps, or client reports.
3. Run:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/secret_pattern_scan.py --path . --json
```

4. Update docs if behavior changes.
5. Prefer dry-run/read-only defaults for every new script.
