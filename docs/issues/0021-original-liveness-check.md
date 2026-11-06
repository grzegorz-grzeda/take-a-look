# 0021: Original liveness check

Spec: [0003 Upkeep](../specs/0003-upkeep.md)
Status: ready-for-agent
Blocked by: 0018, 0008

## What to build

Weekly, each Entry's original link is checked. An Entry is marked "oryginał usunięty" only after consecutive definite "gone" signals (404/410, platform "content unavailable") — never on timeouts or server errors alone — and the mark clears if the original comes back. Checks are spread over the week and rate-limited per host.

## Acceptance criteria

- [ ] Lightweight check mode in the Fetcher
- [ ] Consecutive-failure rule with definite-gone signals only
- [ ] Mark records first-detected time; cleared on recovery
- [ ] "oryginał usunięty" badge on result cards; count in `status`
- [ ] Per-host rate limiting and spreading across the week
- [ ] Tests: gone → marked; timeouts → not marked; back online → cleared
