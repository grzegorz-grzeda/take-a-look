# 0015: Soft delete, kosz and restore

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0008, 0014

## What to build

Either Sender can delete any Entry. Deleted Entries disappear from search and browsing but stay restorable for 30 days: `kosz` lists them with a "Przywróć" button. Search result cards also get a delete option.

## Acceptance criteria

- [ ] Delete sets a deleted time; deleted Entries excluded from search and `co nowego`
- [ ] Delete available from search result cards and from the confirmation
- [ ] `kosz` lists recently deleted Entries (newest first) with "Przywróć"
- [ ] Restore makes the Entry searchable again
- [ ] Seam tests: delete by the other Sender, restore, excluded from search while deleted
