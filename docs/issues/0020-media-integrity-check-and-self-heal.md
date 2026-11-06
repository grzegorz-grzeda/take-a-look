# 0020: Media integrity check and self-heal

Spec: [0003 Upkeep](../specs/0003-upkeep.md)
Status: ready-for-agent
Blocked by: 0018, 0013

## What to build

Weekly, every Snapshot media file is checked against its checksum. Missing or corrupted files are re-downloaded from the original when it's still available; otherwise the media is marked lost and search results show "kopia utracona". Files moved within the media store but with matching content are found by checksum and not counted as lost.

## Acceptance criteria

- [ ] Weekly job verifies existence and checksum of every media item
- [ ] Re-fetch via the Fetcher on mismatch/missing; success restores the media
- [ ] Unrecoverable → media marked lost; "kopia utracona" on result cards; "Kopia" explains what's missing
- [ ] Moved-but-intact files located by checksum
- [ ] Lost-media count in `status`
- [ ] Tests: missing file healed, corrupted file unrecoverable, moved file tolerated
