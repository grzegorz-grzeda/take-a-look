# 0011: AI-understood search

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0007, 0008

## What to build

Search understands natural Polish: "przepisy od Joanny z zeszłego miesiąca" filters by Category, Sender and date; Haiku expands the query into Polish and English keywords so a Polish query finds English Entries ("przepis z cukinią" finds "zucchini fritters").

## Acceptance criteria

- [ ] Haiku turns the query into filters (Category, Sender, date range) plus Polish and English keyword sets
- [ ] Filters and keywords combined in the Atlas Search query; ranked by relevance then recency
- [ ] If the AI is unavailable, search falls back to plain keyword search rather than failing
- [ ] Seam tests: Sender filter, Category filter, relative date, cross-language match
