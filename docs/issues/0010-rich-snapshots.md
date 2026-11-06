# 0010: Rich Snapshots

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0005

## What to build

Snapshots preserve more than metadata: Meta's own preview data from the share is used first (per 0003's findings), readable text is extracted from articles, recipe pages yield ingredients and steps, shop pages yield product name and price at the time. Everything feeds search and classification.

## Acceptance criteria

- [ ] Platform preview data from the Drop is stored and preferred for Facebook content
- [ ] Readable main text extracted for articles and generic pages
- [ ] Structured recipe extraction (ingredients, steps) where the page supports it
- [ ] Product name and price captured for shop pages
- [ ] Snapshot text is searchable
- [ ] Seam tests with canned pages for each kind via the fake Fetcher
