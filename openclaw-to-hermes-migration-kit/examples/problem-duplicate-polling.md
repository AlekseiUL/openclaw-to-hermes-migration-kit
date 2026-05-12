# Problem case: duplicate Telegram polling

Symptoms:

- gateway logs show `Conflict` or `polling conflict`;
- bot stops replying or flips between runtimes;
- OpenClaw and Hermes both hold the same token.

Fix:

- stop new Hermes gateway first to distinguish self-conflict from old holder;
- call `getUpdates` only if approved and without printing token;
- if conflict remains while Hermes stopped, old holder is still active;
- remove/restart old holder before starting Hermes again.
