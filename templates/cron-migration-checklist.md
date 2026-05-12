# Cron migration checklist

- [ ] Source cron/job file identified.
- [ ] Job purpose summarized.
- [ ] Read-only/write/external side-effect classified.
- [ ] Delivery target identified.
- [ ] Timezone identified.
- [ ] Clean run `[SILENT]` rule added if user-facing delivery exists.
- [ ] Secrets usage checked.
- [ ] Hermes cron command drafted.
- [ ] One-shot dry run done.
- [ ] No auto-publish/client-send without approval.
