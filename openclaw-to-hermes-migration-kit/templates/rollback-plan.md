# Rollback plan

Migration:
Agent:
Target profile:
Date:
Operator:

## Backups

- Hermes target profile backup:
- OpenClaw config backup:
- Env backup policy:
- Workspace backup:

## Rollback steps

1. Stop new Hermes gateway/profile:
   ```bash
   hermes --profile <profile> gateway stop
   ```
2. Restore old OpenClaw binding/config from backup.
3. Restore old token env key if it was moved/commented.
4. Restart old OpenClaw gateway.
5. Verify bot identity and no duplicate polling.
6. Archive or remove partial Hermes profile only after verification.

## Verification

- [ ] Old bot answers.
- [ ] No polling conflict.
- [ ] Hermes partial profile stopped.
- [ ] Report written.
