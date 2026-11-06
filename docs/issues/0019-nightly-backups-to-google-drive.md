# 0019: Nightly backups to Google Drive

Spec: [0003 Upkeep](../specs/0003-upkeep.md)
Status: ready-for-agent
Blocked by: 0018

## What to build

Every night the Library's database is dumped and copied, together with new and changed media, to a Google Drive folder via `rclone`. Old dumps are rotated. A restore script and runbook make the backup actually usable. The owner sets up the `rclone` Google Drive remote, guided by a walkthrough.

## Acceptance criteria

- [ ] Walkthrough for configuring an `rclone` Google Drive remote on the VPS (credentials not committed)
- [ ] Nightly `mongodump` of Atlas + incremental media sync to Drive
- [ ] Rotation (e.g. 7 daily, 4 weekly dumps), configurable
- [ ] Restore script and runbook
- [ ] Failed backup recorded in health state and surfaced as a warning
- [ ] Test against a local filesystem `rclone` remote including a dump → restore round trip
