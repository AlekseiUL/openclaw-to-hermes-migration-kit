# Example: Telegram bot agent

Risk: duplicate polling.

Plan:

1. Identify token env key, no raw value in reports.
2. Identify old holder.
3. Prepare target Hermes profile `.env` but do not start gateway yet.
4. Backup OpenClaw config.
5. Approval gate.
6. Stop/remove old holder.
7. Start Hermes gateway.
8. Wait 60–90 seconds.
9. Check new gateway logs for fresh polling conflicts.
10. Smoke with approved message.

Rollback: stop Hermes gateway, restore OpenClaw binding, restart OpenClaw gateway.
