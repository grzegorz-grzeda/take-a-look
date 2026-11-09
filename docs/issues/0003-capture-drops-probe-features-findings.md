# 0003: Capture real Drops, probe Messenger features, write findings

Spec: [0001 Messenger webhook prototype](../specs/0001-messenger-webhook-prototype.md)
Status: ready-for-human
Blocked by: 0002

## What to build

Both Senders use the prototype for real: the wife is invited as an app Tester, then both share a representative set of Drops. The bot gains a few probe commands that try the Messenger features 0002 relies on. The result is a findings note that tells 0002 what Meta actually provides and which features work for an EU Page, plus anonymised payload fixtures for tests.

## Acceptance criteria

- [ ] Walkthrough for the wife to accept the Tester role (developer signup with her normal FB account)
- [ ] Payloads captured for: FB post, FB reel, IG reel, shop listing, recipe page, plain article, screenshot, photo, text-only message, link with the Sender's own text, multi-share to spouse + Page
- [ ] Probes tried and outcome recorded: persistent menu, quick replies, generic-template carousel with buttons, sending a video attachment back
- [ ] Findings note per Drop kind: which fields Meta provides (URL, title, description, image, video) and what is missing
- [ ] Both Senders' Messenger IDs recorded for the allowlist (kept out of the repo)
- [ ] Payload fixtures for the 0002 test harness committed only after full anonymisation: every ID, name, URL, timestamp and text replaced with invented values (Senders "Grzegorz" and "Joanna"); raw logs stay on the VPS and are never committed
- [ ] Spec 0002 updated if findings change any of its decisions

## Comments

- Agent (2026-11-09): delivered the tooling: `probe …` commands in `prototype/webhook.py` (persistent menu, quick replies, generic-template carousel, video upload back), `prototype/summarize.py` (payload shapes without private content), [guide 5](../guides/05-tester-invite.md) (Tester invite, Joanna's part in Polish) and [guide 6](../guides/06-capture-and-probes.md) (Drop checklist, probes, hand-over). Exercised locally against a fake Graph API. Remaining: Senders capture Drops and run probes (guides 5–6), then the agent writes the Answer, synthetic fixtures and any spec 0002 updates.
