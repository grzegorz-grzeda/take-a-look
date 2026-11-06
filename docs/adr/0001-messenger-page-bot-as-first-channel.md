# Messenger Page bot as the first Channel

The two Senders already exchange links on Messenger, so the first Channel is a Messenger bot (a Facebook Page backed by a Meta app in Development mode, with both Senders holding app roles), rather than the technically simpler Telegram bot. Keeping the habit unchanged matters more than build effort, and Meta may include its own preview data (title, image, video) for shared Facebook posts and reels in the webhook payload, which would partly solve the "Facebook content can't be scraped" problem. A throwaway webhook prototype verifies that before extraction is designed.

## Consequences

- The bot cannot join a Senders' group chat or read their 1:1 chat; a Sender multi-shares to the other Sender plus the Page. The bot does not notify one Sender about the other's Drops, because Messenger's 24-hour window makes such messages unreliable.
- Unofficial bridges that log in as a Sender's personal account (e.g. `mautrix-meta`) to read the 1:1 chat live were rejected: they violate Meta's terms and risk the personal account. Old 1:1 history comes in only through a one-off import of Meta's data export.
- A public HTTPS webhook is required from day one, so the VPS needs a subdomain and TLS before anything works.
- Meta policy, Graph API version expiry (~2 years) and EU messaging restrictions are ongoing risks; the core is Channel-agnostic so Telegram can be added or swapped in.
