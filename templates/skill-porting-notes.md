# Skill porting notes

Skill: `<name>`

## Source

- Source path:
- Source contour:
- Runtime dependencies:
- Old hardcoded roots:

## Target

- Target profile:
- Target skill path:
- Shared or profile-local:

## Required rewrites

- [ ] Frontmatter valid for Hermes.
- [ ] OpenClaw commands removed or translated.
- [ ] Old roots replaced with target-owned roots.
- [ ] Secrets/examples redacted.
- [ ] References copied physically.
- [ ] No symlinks into source contour.

## Verification

```bash
hermes --profile <profile> skills list | grep <name>
```
