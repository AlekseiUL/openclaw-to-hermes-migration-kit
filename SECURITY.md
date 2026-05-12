# Security Policy

This repository is about agent migration, so security reports are welcome.

Please report issues if you find:

- raw secret values written into audit reports;
- unsafe handling of Telegram bot tokens or OAuth/session files;
- database scripts dumping private rows instead of metadata;
- migration steps that can create duplicate polling or live gateway conflicts;
- documentation that encourages users to paste secrets into chat.

Do not publish real tokens, private audit reports, or client data in public issues. Use redacted reproduction steps and synthetic examples.
