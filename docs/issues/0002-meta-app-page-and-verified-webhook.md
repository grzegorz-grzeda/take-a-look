# 0002: Meta app, Page and a verified webhook that logs payloads

Spec: [0001 Messenger webhook prototype](../specs/0001-messenger-webhook-prototype.md)
Status: ready-for-human
Blocked by: 0001

## What to build

A Meta developer app with the Messenger product, linked to a new Facebook Page (working name "Zerknij"), subscribed to a webhook on `look.g2labs.pl`. A minimal Python service passes Meta's verification handshake, checks the signature of every POST, appends each payload verbatim to a log on a volume, and replies to each message with a fixed Polish acknowledgement. The owner performs the Meta-side steps, guided by a walkthrough.

## Acceptance criteria

- [ ] Walkthrough: developer account, app creation, Messenger product, Page creation and linking, Page access token, webhook subscription to message and postback events
- [ ] GET verification handshake succeeds in the Meta dashboard
- [ ] POSTs with a bad or missing `X-Hub-Signature-256` are rejected
- [ ] A message from the owner to the Page appears verbatim in the payload log
- [ ] The owner receives the Polish acknowledgement reply
- [ ] Secrets come from environment variables; none committed
- [ ] Graph API version in use is noted

## Comments

- Agent (2026-11-09): prototype service (`prototype/`), Compose/Caddy wiring and [guide 4](../guides/04-meta-app-and-webhook.md) are in place and smoke-tested locally (handshake, 403 on bad/missing signature, payload logged, Send API reached). Graph API version in use: **v26.0**. Remaining: the owner runs guide 4 and ticks the criteria.
