# 0004 Messenger history import

Status: ready-for-agent

## Problem Statement

Years of links my wife and I already exchanged live only in our personal 1:1 Messenger conversation, where they're practically unfindable. The bot can't read that conversation (ADR-0001), so the Library starts empty while our biggest "way-back" problem is exactly that old history.

## Solution

A one-off (re-runnable) import of the conversation from Meta's "Download your information" export (JSON format), treated as its own Channel. Each shared link in the history becomes a Drop with its original Sender and original sent time, flowing through the same Snapshot-and-classify pipeline as live Drops. Many old Facebook originals will already be gone; those Entries keep the link, the message text and whatever the export itself contains, and are marked accordingly.

## User Stories

1. As the owner, I want step-by-step instructions for requesting the right Meta export (JSON, Messages only, chosen date range), so that I get a usable file without guessing.
2. As the owner, I want to copy the export to the VPS and start the import with one command, so that running it is simple.
3. As the owner, I want a dry run that reports how many links, shared posts and photos it found, and the date range, without saving anything, so that I know what will happen before committing.
4. As the owner, I want to pick which conversation to import when the export contains several, so that only our 1:1 chat is imported.
5. As a Sender, I want each historical message that contains a link or a shared post to become a Drop attributed to whichever of us sent it, so that "od Joanny" filters work on old Entries too.
6. As a Sender, I want each imported Drop to keep its original sent time, so that "z zeszłego roku" searches and ordering are correct.
7. As a Sender, I want the message text that accompanied a link imported with it, so that my old captions are searchable.
8. As a Sender, I want plain chit-chat messages without links not imported, so that the Library isn't flooded with conversation.
9. As the owner, I want photos from the history excluded by default but importable with a switch, so that personal photos don't flood the Library unless we want them.
10. As a Sender, I want the same link sent several times in the history to become one Entry with Resends, so that the import doesn't create duplicates.
11. As a Sender, I want imported links that are already in the Library (from live Drops) attached as Resends to the existing Entry, so that history and live data merge cleanly.
12. As a Sender, I want imported Entries to get Snapshots and Category/Tags like live ones, so that they're just as searchable.
13. As a Sender, I want imported Entries whose original is already gone saved anyway, marked "oryginał usunięty", with whatever title or preview the export contains, so that I can still find them by text and date.
14. As a Sender, I want Polish characters in imported text to be correct, so that search works on old messages (Meta's export mis-encodes non-ASCII text).
15. As the owner, I want the import to be safely re-runnable and resumable after interruption without creating duplicates, so that a crash or a newer export isn't a problem.
16. As the owner, I want the import throttled so that live Drops keep being processed promptly on the 1 vCPU VPS, so that the bot stays usable during a long import.
17. As the owner, I want fetching of old originals rate-limited, so that Facebook and other sites don't block the VPS.
18. As the owner, I want classification of a large backlog to use the cheapest suitable API mode (e.g. batch requests), so that importing thousands of Entries costs little.
19. As a Sender, I want no confirmation message per imported Entry, so that my chat with the bot isn't spammed.
20. As a Sender, I want a summary of the import (Entries created, Resends, originals already gone, failures) shown in `status` and on my next interaction, so that I know it finished.
21. As a Sender, I want imported Entries excluded from `co nowego`, so that catching up on new things isn't buried under years of history.

## Implementation Decisions

- **Import is a Channel.** The importer parses the export into the same normalized Drops as the Messenger adapter (Sender, Channel = history import, original sent time, text, links, attachments, any share metadata in the export) and hands them to the 0002 core. No import-specific Entry logic.
- **Sender mapping.** Export participant names are mapped to configured Senders; unmapped participants abort the import with a clear message.
- **Selection rules.** Import messages with links or share objects; photos only when explicitly enabled; skip text-only messages, reactions, calls, stickers and system messages.
- **Encoding fix.** Meta's JSON export stores UTF-8 text as Latin-1 escapes; text is re-decoded before use.
- **Idempotency.** Each imported Drop is keyed by conversation + message timestamp + sender + content hash; re-running skips known messages. Resend detection reuses 0002's canonical-link matching.
- **Ordering and attribution.** The Entry's first Drop (earliest sent time) defines "first sent by/when"; imports never overwrite live Drops.
- **Throughput.** Imported Drops enter the job queue at a lower priority than live Drops; fetching is rate-limited per host; classification of the backlog uses the Anthropic batch mode where available, falling back to normal requests.
- **Quiet mode.** Imported Drops produce no per-Entry replies; the import's progress and final summary live in the health state read by `status` and prepended to the next reply (as in 0003).
- **`co nowego`** considers only Entries whose first Drop came from a live Channel.
- **Invocation.** Run on the VPS as a service command against an export directory or zip on a mounted volume, with `--dry-run`, `--conversation` and `--include-photos` options.

## Testing Decisions

- **Seam: the import job's entry point**, fed small fixture exports that mimic Meta's real JSON structure (including the mis-encoded Polish text), with the same edge fakes and local Atlas container as 0002.
- Assertions are observable: what search returns (Sender, original date, Tags), Resend counts, what `status` reports, that no confirmations were sent, and that a second run changes nothing.
- One end-to-end test mixes a live Drop (through the 0002 webhook seam) and an import of the same link, asserting a single Entry with both Drops.

## Out of Scope

- Live reading of the personal 1:1 conversation (rejected, ADR-0001).
- Importing other conversations or group chats unless explicitly selected.
- Importing from Telegram or other platforms' exports.
- Recovering removed Facebook content from third-party archives.

## Further Notes

- Expect a large share of old Facebook links to be dead; the export's own share metadata (when present) is the main source of captions for them.
- Depends on 0002 (core, pipeline) and 0003 (health state/`status`, removed-original marking).
- Estimated API cost should be reported by the dry run (number of Entries × approximate per-Entry cost), so the owner can top up credits first.
