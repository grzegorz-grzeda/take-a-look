# 0008: Basic search

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0005

## What to build

A Sender sends `? sernik` or `szukaj sernik` and gets matching Entries from the whole shared Library as a carousel of up to 10 cards (image, title, Category, Sender, date) with an "Otwórz" button opening the original and a "Więcej" button for the next 10. Polish word forms match.

## Acceptance criteria

- [ ] `?` / `szukaj` prefix routes to search; everything else stays a Drop
- [ ] Atlas Search index with a Polish analyzer (verify availability; if missing, record it and fall back to keyword variants) over title, Tags, Sender text, Snapshot text
- [ ] Results from both Senders; deleted Entries excluded (once deletion exists)
- [ ] Carousel with "Otwórz" and "Więcej"; friendly Polish message when nothing matches
- [ ] Seam test: Entries dropped by each Sender are found by inflected Polish queries
