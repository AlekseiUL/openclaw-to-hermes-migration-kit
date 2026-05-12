## Summary

## Verification

```bash
python3 -m py_compile scripts/*.py
python3 scripts/secret_pattern_scan.py --path . --json
```

## Safety

- [ ] No real secrets or private data
- [ ] No unsafe live migration default
- [ ] Docs updated
