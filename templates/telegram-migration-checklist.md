# Telegram migration checklist

- [ ] Token env key identified, value not printed.
- [ ] Old polling holder identified.
- [ ] Bot username checked via approved safe `getMe`.
- [ ] Group/privacy policy documented.
- [ ] `allowed_users`, `allowed_chats`, `allowed_threads`, `require_mention` decided.
- [ ] Old holder stopped only after approval.
- [ ] New Hermes gateway started only after approval.
- [ ] Wait 60–90 seconds after start.
- [ ] No fresh `polling conflict` in gateway error log.
- [ ] Smoke message approved and executed.
- [ ] Rollback path tested or documented.
