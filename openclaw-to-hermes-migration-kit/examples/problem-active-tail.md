# Problem case: old active tail

Bad:

```text
active script sources ~/.openclaw/agents/finance-agent/agent/data/secrets/tribute.env
```

Good:

```text
script reads <target-workspace>/agents/finance-agent/data/secrets/tribute.env
```

Allowed:

```text
legacy-openclaw/ contains old source files as provenance only
```

The scanner must flag active runtime pointers but tolerate explicit legacy/provenance archives when configured.
