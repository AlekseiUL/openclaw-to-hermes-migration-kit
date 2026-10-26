# Offline verification boundary

Synthetic inventory/scaffold round-trip covers dry-run, conflict preservation, rollback and redacted credential references; rejects path-like names and conflicting modes.

## Reproduce

`python3 -m unittest discover -s tests -v`

This is a scaffold/inventory kit, not an automatic migration of live configuration or credentials. Rollback uses the synthetic snapshot; no secret values or Hermes profiles are copied.

## Rollback

Review the commit diff and use a new checkout of the pre-change commit for source rollback. Keep user data and live installations untouched. A source rollback is not permission to restore unsafe network exposure or bypass approval.
