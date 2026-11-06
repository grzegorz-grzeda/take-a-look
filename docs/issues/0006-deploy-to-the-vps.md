# 0006: Deploy to the VPS

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0005

## What to build

The service from 0005 runs in production on `look.g2labs.pl`, replacing the prototype, so both Senders start using the real bot while the rest is built.

## Acceptance criteria

- [ ] Compose service image built on the VPS, connected to MongoDB Atlas (Frankfurt, free tier)
- [ ] All secrets and the allowlist supplied via environment; an example env file documents them without values
- [ ] Deploy script: pull, rebuild, restart
- [ ] Structured logs for each Drop, processing step and failure, readable via Compose
- [ ] Atlas Search indexes applied on deploy
- [ ] Both Senders save a real link and get the confirmation
