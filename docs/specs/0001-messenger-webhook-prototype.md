# 0001 Messenger webhook prototype

Status: ready-for-agent

## Problem Statement

We have decided to build the Library behind a Messenger Page bot (ADR-0001), largely betting that Meta's webhook payload carries useful preview data (title, description, image, video) for shared Facebook posts and reels — data we otherwise cannot scrape. We do not know what Meta actually sends for each kind of Drop, whether a Messenger Page in Development mode works for both Senders, or which Messenger features (persistent menu, quick replies, generic template, attachment upload) are available to an EU Page. Designing extraction without this knowledge means guessing.

## Solution

A throwaway prototype: the real Meta app, Facebook Page and public HTTPS webhook on `look.g2labs.pl`, with a minimal Python service that verifies and logs every incoming webhook payload verbatim, replies to each message with a short acknowledgement, and lets us probe the Messenger features we plan to use. Both Senders share a representative set of real Drops into it. The outcome is a findings note that the Library core spec (0002) builds on. The prototype code is discarded afterwards; the infrastructure (Meta app, Page, DNS, Caddy, VPS Docker setup) is kept.

## User Stories

1. As the owner, I want a step-by-step guide to create the Meta developer app, add the Messenger product and link a new Facebook Page, so that I can set up a platform I have never used before.
2. As the owner, I want a step-by-step guide to point `look.g2labs.pl` at my VPS in OVH DNS, so that Meta can reach the webhook.
3. As the owner, I want Caddy in Docker to serve the webhook over HTTPS with automatic certificates, so that I don't have to manage TLS by hand.
4. As the owner, I want the webhook to pass Meta's subscription verification handshake, so that Meta accepts it.
5. As the owner, I want every incoming payload's signature checked against the app secret, so that only Meta can post to the webhook even during the prototype.
6. As the owner, I want every incoming payload written verbatim to a log, so that we can study exactly what Meta sends.
7. As the owner, I want my wife invited as an app Tester, so that she can message the Page while the app stays in Development mode.
8. As my wife, I want to accept the Tester invite with clear instructions, so that I can join without knowing anything about Meta's developer tools.
9. As a Sender, I want to share a Facebook post to the Page from the Facebook app, so that we see what Meta sends for posts.
10. As a Sender, I want to share a Facebook reel to the Page, so that we see what Meta sends for reels.
11. As a Sender, I want to share an Instagram reel, a shop listing, a recipe page and a plain article link, so that we see the payload for each kind of Drop.
12. As a Sender, I want to send a screenshot, a photo and a text-only message, so that we see attachment and text payloads.
13. As a Sender, I want to multi-share one item to my spouse and the Page at once, so that we confirm the workaround from ADR-0001 works in practice.
14. As a Sender, I want each message acknowledged by the bot, so that we confirm replies within the 24-hour window work.
15. As the owner, I want the bot to try a persistent menu, quick replies, a generic-template carousel and sending a video attachment back, so that we know which features are available to an EU Page.
16. As the owner, I want a written findings note summarising, per Drop kind, which fields Meta provides and what is missing, so that extraction in 0002 is designed on facts.
17. As the owner, I want the Messenger IDs of both Senders recorded from the logs, so that the allowlist in 0002 can be configured.

## Implementation Decisions

- Python service, run with Docker Compose on the VPS, behind Caddy on `look.g2labs.pl`. The Compose project and Caddy setup are meant to be kept and grown in 0002; only the webhook code is throwaway.
- Webhook endpoint handles: GET verification (hub mode / verify token / challenge) and POST events with `X-Hub-Signature-256` HMAC verification using the app secret.
- Payloads are appended as JSON lines to a log on a mounted volume; nothing else is stored.
- Secrets (app secret, Page access token, verify token) come from environment variables, never committed.
- Reply via the Graph API Send API with a fixed Polish acknowledgement; a few hard-coded probe commands exercise the persistent menu, quick replies, generic template and video attachment upload.
- Setup steps that only a human can do (Meta app, Page, Tester invite, DNS, VPS access) are delivered as a guided walkthrough (e.g. the `wizard` skill), not automated.
- Findings are recorded as an Answer on the prototype issue and summarised into 0002 if they change any decision there.

## Testing Decisions

- No automated tests: this is a throwaway spike whose output is knowledge, not code. Verification is manual — real shares from both Senders show up in the log and get acknowledged.

## Out of Scope

- Storing anything beyond raw logs: no Library, Entries, classification or search.
- Extraction, scraping or media download.
- Telegram, web UI, history import.
- Making the app Live or submitting it for App Review.

## Further Notes

- Graph API versions expire roughly every two years; note the version used.
- If Meta's payload turns out to carry rich FB captions/media, 0002's Snapshot extraction for Facebook can lean on it; if not, 0002 relies on best-effort scraping plus the Sender's own text, as already planned.
