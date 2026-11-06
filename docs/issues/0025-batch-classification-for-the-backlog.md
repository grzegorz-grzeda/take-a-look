# 0025: Batch classification for the backlog

Spec: [0004 Messenger history import](../specs/0004-messenger-history-import.md)
Status: ready-for-agent
Blocked by: 0024

## What to build

Large imports classify their backlog through the Anthropic batch mode instead of one request per Entry, cutting cost, with fallback to normal requests when batching isn't available.

## Acceptance criteria

- [ ] Imported Entries awaiting classification are submitted in batches
- [ ] Batch results applied to Entries; failures retried individually
- [ ] Fallback to per-Entry classification
- [ ] Dry-run cost estimate reflects batch pricing
- [ ] Tests with a fake batch Classifier: success, partial failure, fallback
