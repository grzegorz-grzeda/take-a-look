# 0009: Resends and multi-link Drops

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0005

## What to build

Links are canonicalized (share/redirect URLs resolved, tracking parameters stripped). A link already in the Library becomes a Resend on the existing Entry and the bot replies when and by whom it was first sent. A Drop with several links creates one Entry per link, each keeping the Sender's text.

## Acceptance criteria

- [ ] Canonicalization covers common FB/IG share URLs, redirects and tracking parameters
- [ ] Resend appended to the existing Entry; no new Entry; reply e.g. "Już zapisane 12 mar przez Joannę (Przepis: Sernik baskijski)"
- [ ] Entry records all its Drops, so "sent N times, last on…" is derivable
- [ ] Multi-link Drop → one Entry and one confirmation per link
- [ ] Seam tests for: same link twice by different Senders, tracking-param variants, three links in one message
