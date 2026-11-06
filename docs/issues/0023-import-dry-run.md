# 0023: Import dry run

Spec: [0004 Messenger history import](../specs/0004-messenger-history-import.md)
Status: ready-for-agent
Blocked by: 0004

## What to build

The owner requests Meta's "Download your information" export (JSON, Messages only), copies it to the VPS and runs the import with `--dry-run`. The importer parses the export as a Channel into normalized Drops, fixes Meta's mis-encoded Polish text, maps participant names to Senders, lets the owner pick the conversation, and reports counts (links, shared posts, photos), the date range and an estimated API cost — saving nothing.

## Acceptance criteria

- [ ] Walkthrough for requesting the right export
- [ ] Import command with `--dry-run`, `--conversation`, `--include-photos`, reading a directory or zip on a mounted volume
- [ ] Latin-1-escaped UTF-8 text re-decoded correctly
- [ ] Unmapped participants abort with a clear message
- [ ] Selection rules: links and shares in; text-only, reactions, calls, stickers, system messages out; photos only with the switch
- [ ] Report: counts, date range, estimated Entries and API cost
- [ ] Tests with small, fully synthetic fixture exports mimicking Meta's real structure (never derived from a real export); nothing persisted on dry run
