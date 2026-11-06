# 0016: co nowego, pomoc and the menu

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0007

## What to build

`co nowego` shows Entries added by either Sender since the asking Sender last used it. `pomoc` explains dropping, searching, `co nowego` and `kosz` in Polish and shows the service version. If 0003 showed the persistent menu works for our EU Page, it offers "🔍 Szukaj", "Co nowego" and "Pomoc".

## Acceptance criteria

- [ ] Per-Sender "last seen" time for `co nowego`, updated on use; shown as a carousel
- [ ] `pomoc` text in Polish including the version
- [ ] Persistent menu configured if supported; otherwise documented as unavailable
- [ ] Seam tests: each Sender sees the other's new Entries once
