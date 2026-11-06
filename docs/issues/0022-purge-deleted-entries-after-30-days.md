# 0022: Purge deleted Entries after 30 days

Spec: [0003 Upkeep](../specs/0003-upkeep.md)
Status: ready-for-agent
Blocked by: 0018, 0015

## What to build

Daily, Entries deleted more than 30 days ago are permanently removed together with their Drops and any media no other Entry references.

## Acceptance criteria

- [ ] Daily purge job; retention period configurable (default 30 days)
- [ ] Entries, their Drops and unreferenced media removed
- [ ] Media shared with a surviving Entry kept
- [ ] Purged Entries no longer appear in `kosz`
- [ ] Tests: 31-day-old deletion purged, 29-day-old kept, shared media kept
