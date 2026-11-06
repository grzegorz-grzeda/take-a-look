# 0003 Upkeep

Status: ready-for-agent

## Problem Statement

The Library exists so that Entries outlive their originals. That only holds if the preserved Snapshots themselves stay intact and the Library survives the VPS. Media files can go missing or get corrupted (especially once we start moving them around on Google Drive), Facebook removes originals without telling anyone, the free Atlas tier has no backups (ADR-0002), the VPS disk is small, and deleted Entries must eventually really disappear. Without routine upkeep, the Library silently decays.

## Solution

Scheduled background jobs inside the service: a weekly check that every Snapshot's media still exists and matches its checksum (re-downloading or marking it lost), a weekly check of whether each Entry's original is still online (marking "oryginał usunięty"), a nightly backup of the database and new media to Google Drive via `rclone`, a daily purge of Entries deleted more than 30 days ago, and a disk-usage watch. Results show up in search results (badges) and in a `status` command for the Senders.

## User Stories

1. As a Sender, I want the Library to notice when a Snapshot's media file is missing or corrupted, so that I'm not surprised when "Kopia" fails.
2. As a Sender, I want a missing or corrupted media file re-downloaded from the original automatically when the original is still online, so that the Snapshot heals itself.
3. As a Sender, I want media that can't be recovered marked as lost ("kopia utracona"), so that results tell me honestly what's left.
4. As the owner, I want the media check to tolerate files I moved within the media store as long as their content matches the checksum, so that reorganising doesn't count as loss.
5. As a Sender, I want each Entry's original link checked periodically, so that the Library knows when the source has disappeared.
6. As a Sender, I want Entries whose original is gone marked "oryginał usunięty" in search results, so that I know the Snapshot is now the only copy.
7. As a Sender, I want an Entry whose original comes back online to lose that mark, so that the status stays accurate.
8. As a Sender, I want temporary network errors not to mark an original as removed, so that I don't see false alarms.
9. As the owner, I want a nightly backup of the database copied to a Google Drive folder, so that the Library survives losing Atlas data.
10. As the owner, I want new and changed media files copied to Google Drive nightly, so that Snapshots survive losing the VPS.
11. As the owner, I want old database backups rotated (e.g. keep 7 daily, 4 weekly), so that Drive doesn't fill up.
12. As the owner, I want a documented, tested restore procedure, so that a backup is actually usable when I need it.
13. As a Sender, I want Entries deleted more than 30 days ago permanently removed, including their media, so that deletion is real in the end.
14. As the owner, I want media shared by several Entries kept until no Entry references it, so that purging one Entry doesn't break another.
15. As the owner, I want the media volume's usage watched against a threshold, so that I learn about a filling disk before it breaks saving.
16. As a Sender, I want a `status` command showing version, disk usage, last successful backup, and counts of lost media and removed originals, so that I can check the Library's health from Messenger.
17. As a Sender, I want a warning prepended to my next bot reply when a backup failed or the disk is nearly full, so that problems reach me despite Messenger's 24-hour messaging rule.
18. As the owner, I want every upkeep run logged with its outcome, so that I can audit what happened.
19. As the owner, I want each upkeep job runnable on demand, so that I can trigger it after a fix or during testing.
20. As the owner, I want upkeep jobs to run without making the bot unresponsive on a 1 vCPU VPS, so that Drops keep flowing during checks.

## Implementation Decisions

- **Scheduler inside the service.** Jobs are scheduled by the service itself (no host cron), use the same durable job mechanism as Drop processing (0002), and run at low priority/throttled so they never starve Drop processing.
- **Jobs and cadence:** media integrity — weekly; original liveness — weekly; database + media backup — nightly; purge of deleted Entries — daily; disk watch — hourly. All cadences configurable.
- **Media integrity** uses the checksums the MediaStore records (0002): missing or mismatching file → try re-fetching via the Fetcher from the original → otherwise mark media lost. Lookup by checksum tolerates moved files.
- **Original liveness** uses the Fetcher in a lightweight check mode; an original is marked removed only after consecutive failures across runs with a definitive "gone" signal (404/410, platform "content unavailable"), never on timeouts or 5xx alone. Recovery clears the mark.
- **Backups** run `mongodump` against Atlas and `rclone` to a Google Drive remote configured on the VPS; database dumps rotate by count; media sync is incremental. Credentials via environment/mounted config, never committed. A restore script and runbook are part of this work.
- **Purge** permanently deletes Entries past 30 days in the deleted state, their Drops, and media no longer referenced by any Entry.
- **Health state** (last run/outcome of each job, disk usage, counts) is stored in the database and read by `status` and by the reply path that prepends warnings.
- **Entry state additions:** media lost marker per media item; original-removed marker with first-detected time. Search result cards show "oryginał usunięty" / "kopia utracona".

## Testing Decisions

- **Seam: each upkeep job's entry point**, invoked directly in tests (the "run now" path), with the same edge fakes as 0002 (Fetcher, MediaStore as temporary directory, Meta Send API) and the real local Atlas container. Assertions are on observable outcomes: what search/`status` report afterwards, which files exist, what the next reply contains.
- Backups are tested against a local `rclone` remote (filesystem backend) instead of Google Drive, including a dump → restore round trip.
- Liveness tests cover: gone → marked; flaky/timeouts → not marked; back online → cleared.
- User-facing effects (badges, `status`, prepended warnings) are asserted through the 0002 webhook seam.

## Out of Scope

- Moving primary media storage to Google Drive (Drive is only the backup destination here).
- Proactive alerts outside a Sender's 24-hour window (no message tags apply).
- Monitoring of the VPS itself (CPU, uptime) beyond media disk usage.

## Further Notes

- Liveness checks against Facebook may be rate-limited or blocked; keep request volume low and spread checks over the week.
- Depends on 0002 (Entries, MediaStore checksums, job mechanism, Fetcher).
