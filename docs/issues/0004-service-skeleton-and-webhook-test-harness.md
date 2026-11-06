# 0004: Service skeleton and webhook test harness

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0003

## What to build

The real service's foundation, replacing the prototype code: a Python package at version 0.1.0 with a Channel-agnostic core and a Messenger adapter, plus the test harness every later ticket uses. A signed webhook payload from an allowlisted Sender is accepted and handed to the core; anything else is rejected or silently ignored.

## Acceptance criteria

- [ ] Python package with SemVer version 0.1.0 as the single source of truth
- [ ] Messenger adapter: verification handshake, signature check, fast 200 response, allowlist mapping Messenger IDs to Sender names; unknown senders get no reply
- [ ] Adapter produces normalized Drops / user actions for the core (shape informed by 0003's findings)
- [ ] Test harness: local Atlas container (`mongodb-atlas-local`), recording fake Meta Send API, fake Fetcher, fake Classifier, temporary-directory MediaStore
- [ ] First seam tests (signed payload in → recorded outgoing calls) using 0003's fixtures, including a non-allowlisted sender
- [ ] Tests run with one command locally
