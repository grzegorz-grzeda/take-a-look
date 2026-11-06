# 0005: Save a link Drop end to end

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0004

## What to build

A Sender shares a link and it is saved: the Drop is persisted immediately, a pending Entry is created, a durable background job builds a basic Snapshot (page metadata: title, description, preview image URL, site), and the bot replies in Polish "Zapisane: <tytuł>". If extraction fails, the Entry still keeps the link and the Sender's text.

## Acceptance criteria

- [ ] Drop persisted before the webhook returns; processing happens asynchronously
- [ ] Durable job queue in the database with retry and backoff; jobs survive a restart
- [ ] Basic Snapshot from page metadata via the Fetcher
- [ ] Polish confirmation once processing completes
- [ ] Failed extraction → Entry with link + Sender text and a Polish message saying so
- [ ] Seam test: shared link → confirmation sent → Entry stored with Sender and time
