# MongoDB Atlas free tier for the Library

The Library's records (Entries, Drops, Snapshot text and metadata) live in MongoDB Atlas (free M0 tier, Frankfurt region) rather than Postgres on the VPS. The VPS has only 2 GB RAM / 1 vCPU, the owner already has an Atlas account, and Atlas Search offers a Lucene Polish analyzer (to be verified) for matching Polish word forms — something Postgres lacks out of the box. Data also survives a VPS loss.

## Consequences

- M0 caps storage at 512 MB, so Snapshot media files never go in the database; they live on the VPS disk (later Google Drive) behind a storage interface, and the database holds only references and checksums.
- M0 has no automated backups: a nightly `mongodump` is copied to Google Drive with `rclone`.
- Every query is a network round trip from the VPS to Frankfurt.
