# 0014: Correct a confirmation

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0007

## What to build

The confirmation after a Drop carries quick replies "Zmień kategorię" (offering the six Categories), "Usuń" and "OK". Replying `#tag …` shortly after a confirmation adds those Tags to that Entry.

## Acceptance criteria

- [ ] Quick replies on every confirmation
- [ ] "Zmień kategorię" → Category choices → Entry updated and acknowledged
- [ ] "Usuń" deletes the Entry (soft, see 0015 for restore) and acknowledges
- [ ] `#tag` messages within the window after a confirmation add Tags to that Entry; outside it they are a normal Drop
- [ ] Seam tests for each correction
