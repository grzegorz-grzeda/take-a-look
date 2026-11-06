# 0024: Run the import

Spec: [0004 Messenger history import](../specs/0004-messenger-history-import.md)
Status: ready-for-agent
Blocked by: 0023, 0009, 0016, 0018

## What to build

Without `--dry-run`, imported Drops flow through the same core pipeline as live ones, keeping their original Sender and sent time. Repeated links merge as Resends, including with Entries from live Drops. The import is quiet (no per-Entry replies), runs below live Drops in priority with rate-limited fetching, is resumable and safely re-runnable, and is excluded from `co nowego`. Progress and a final summary appear in `status` and on the next reply.

## Acceptance criteria

- [ ] Imported Drops keyed idempotently (conversation + timestamp + sender + content hash); a re-run changes nothing
- [ ] Original sent time preserved; earliest Drop defines "first sent by/when"
- [ ] Resend merging across history and live Drops
- [ ] No confirmation messages for imported Entries
- [ ] Lower queue priority than live Drops; per-host rate limiting
- [ ] Dead originals still saved with export metadata and marked "oryginał usunięty"
- [ ] `co nowego` ignores Entries whose first Drop is imported
- [ ] Summary (created, Resends, originals gone, failures) in `status` and prepended to the next reply
- [ ] Tests incl. a live Drop and an imported Drop of the same link → one Entry with both
