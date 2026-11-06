# 0018: Upkeep scheduler, status, warnings and disk watch

Spec: [0003 Upkeep](../specs/0003-upkeep.md)
Status: ready-for-agent
Blocked by: 0006, 0016

## What to build

The service schedules its own upkeep jobs on the durable job mechanism, at low priority so Drops keep flowing on the 1 vCPU VPS. Each job's last run and outcome is recorded as health state. A Sender's `status` command shows version, media disk usage, last successful backup, and counts of lost media and removed originals. Problems (failed backup, disk above threshold) are prepended to the Sender's next bot reply. The first job is an hourly disk watch.

## Acceptance criteria

- [ ] In-service scheduler with configurable cadences; jobs runnable on demand
- [ ] Upkeep jobs throttled below live Drop processing
- [ ] Health state stored in the database; every run logged with its outcome
- [ ] `status` command in Polish
- [ ] Warning prepended to the next reply when a job failed or disk usage exceeds the threshold
- [ ] Hourly disk watch on the media volume
- [ ] Tests: job entry point invoked directly; effects asserted via `status` and the next reply through the webhook seam
