# 4. Meta app, Page and a verified webhook

Goal: a Facebook Page (working name **Zerknij**) backed by a Meta app in Development mode. Meta delivers every message sent to the Page to `https://look.g2labs.pl/webhook`. The prototype service checks the signature, appends the payload to a log on the VPS and replies with a short Polish acknowledgement.

Needs guide [3](03-compose-and-caddy.md) (`/health` answers over HTTPS). Issue: [0002](../issues/done-0002-meta-app-page-and-verified-webhook.md).

> Meta changes its dashboard often. If a label below doesn't match, look for the nearest equivalent; the order of steps is what matters. Written against Graph API **v26.0** (Nov 2026).

## What's in the repo

- [`prototype/webhook.py`](../../prototype/webhook.py): throwaway service (standard-library Python), replaced in issue 0004.
  - `GET /webhook`: Meta's verification handshake (`hub.mode`, `hub.verify_token`, `hub.challenge`).
  - `POST /webhook`: rejects anything without a valid `X-Hub-Signature-256` (HMAC-SHA256 of the body with the app secret), appends `{"received_at": ..., "raw": <body exactly as received>}` as one line to `/data/payloads.jsonl`, answers `200` immediately, then replies to each message via the Send API.
  - `probe …` text commands (guide [6](06-capture-and-probes.md)) try the persistent menu, quick replies, a carousel and sending a video back.
- [`prototype/summarize.py`](../../prototype/summarize.py): prints the shape of every logged payload without its private content.
- [`compose.yaml`](../../compose.yaml): service `webhook`, no published ports (only Caddy can reach it), payload log on the `webhook_data` volume.
- [`caddy/Caddyfile`](../../caddy/Caddyfile): `/webhook` is proxied to `webhook:8000`.
- [`.env.example`](../../.env.example): the four `META_*` settings.

## 4.1 Meta developer account

1. Log in to Facebook with your normal account, then open <https://developers.facebook.com>.
2. **Get started** (or **Log in**) → accept the Platform Terms → verify your phone/email when asked → choose a role (anything, e.g. *Developer*).

You now have **My Apps** in the top bar.

## 4.2 The Facebook Page

1. Open <https://www.facebook.com/pages/create>.
2. Name: `Zerknij`. Category: something neutral like *App page* or *Personal blog*. Skip the optional steps (picture, invites).
3. The Page can stay as it is: in Development mode only people with a role on the app can message it, and nobody else gets a reply.

## 4.3 The Meta app

1. **My Apps** → **Create app**.
2. App name: e.g. `Zerknij dev` (names containing "Facebook", "Messenger" or "Meta" are refused). Contact email: yours.
3. Use case: **Engage with customers on Messenger from Meta**.
4. Business portfolio: **I don't want to connect a business portfolio yet**.
5. Confirm, re-enter your Facebook password if asked → **Create app**.

The app starts in **Development** mode. Leave it there: going Live needs App Review, which is out of scope (spec 0001).

## 4.4 Secrets into `.env` on the VPS

You need three values now (the Page token comes in 4.7).

1. **App secret**: app dashboard → **App settings** → **Basic** → **App secret** → **Show** (asks for your password). Copy it.
2. **Verify token**: you invent it. On the VPS:
   ```bash
   openssl rand -hex 32
   ```
3. **Graph API version**: `v26.0`.

On the VPS, edit `/opt/take-a-look/.env` (e.g. `nano .env`) and fill in:

```
META_APP_SECRET=<app secret>
META_VERIFY_TOKEN=<the random string>
META_PAGE_ACCESS_TOKEN=
META_GRAPH_API_VERSION=v26.0
```

Keep the verify token at hand for 4.6. Then deploy:

```bash
cd /opt/take-a-look
git pull
docker compose up -d --build
docker compose exec -w /etc/caddy caddy caddy reload
docker compose logs webhook
```

The log should end with `Graph API v26.0, payload log /data/payloads.jsonl`. A `Missing environment variable` line means a value in `.env` is empty.

Check routing from your laptop (a wrong token must be refused):

```bash
curl -s -o /dev/null -w '%{http_code}\n' 'https://look.g2labs.pl/webhook?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=1'
```

Expect `403`. A `404` or `502` means Caddy wasn't reloaded or the `webhook` container isn't running (`docker compose ps`).

## 4.5 Add the Messenger permission

App dashboard → **Use cases** → **Engage with customers on Messenger from Meta** → **Customize** → **Permissions** (if shown): make sure `pages_messaging` is **Added**. In Development mode it works for people with a role on the app without App Review.

## 4.6 Configure the webhook

Same use case → **Messenger API Settings** (or **Products → Messenger → Settings**) → **1. Configure webhooks**:

- **Callback URL**: `https://look.g2labs.pl/webhook`
- **Verify token**: the random string from 4.4
- **Verify and save**

Meta immediately calls `GET /webhook`. On the VPS, `docker compose logs webhook` shows `webhook verified`. If the dashboard shows an error instead, see Troubleshooting.

## 4.7 Connect the Page and get its access token

Same page → **2. Generate access tokens**:

1. **Connect** (or **Add Page**) → log in as yourself → select only **Zerknij** → grant the requested permissions → **Done**.
2. Next to Zerknij → **Generate** → tick the acknowledgement → **Copy**. This is the Page access token. Treat it like a password.

Put it into `.env` on the VPS (`META_PAGE_ACCESS_TOKEN=...`) and recreate the service so it picks up the new value:

```bash
docker compose up -d webhook
```

## 4.8 Subscribe the Page to events

Still in **Generate access tokens**, next to Zerknij → **Add subscriptions** (webhook fields; in some dashboard versions this sits under **1. Configure webhooks** instead) → tick:

- `messages`
- `messaging_postbacks`

→ **Confirm**. Without this the webhook is verified but receives nothing.

## 4.9 Test with a real message

1. In Messenger (phone or <https://www.messenger.com>), search for **Zerknij** and send `test`.
2. Within a few seconds the Page replies: *Dzięki, mam to! 👀 (to jeszcze prototyp: niczego nie zapisuję do Biblioteki)*.
3. On the VPS, look at what Meta sent:
   ```bash
   sudo apt-get install -y jq    # once
   docker compose logs --tail 5 webhook
   docker compose exec webhook tail -n 1 /data/payloads.jsonl | jq '.raw | fromjson'
   ```
   `entry[0].messaging[0].sender.id` there is your **PSID**, your Messenger ID for this Page. Store it outside the repo (e.g. a password manager): issue 0003 needs it for the allowlist.

Check that forged requests are rejected, from your laptop:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST -H 'X-Hub-Signature-256: sha256=deadbeef' -d '{}' https://look.g2labs.pl/webhook
curl -s -o /dev/null -w '%{http_code}\n' -X POST -d '{}' https://look.g2labs.pl/webhook
```

Both must print `403`.

## 4.10 Record the Graph API version

[Issue 0002](../issues/done-0002-meta-app-page-and-verified-webhook.md) records Graph API `v26.0` under Comments (released 29 Jul 2026; Meta supports each version for about two years, see the [version list](https://developers.facebook.com/docs/graph-api/changelog/versions) for its expiry date). If you set a different `META_GRAPH_API_VERSION`, update that comment.

✅ Issue 0002 is done when 4.6 verifies, 4.9 gets a reply, the message is in the log and both forged requests return `403`.

## The payload log

- Lives in the `webhook_data` Docker volume on the VPS, **not** in the repo. It holds real Messenger IDs and message text.
- Follow it live: `docker compose exec webhook tail -f /data/payloads.jsonl | jq '.raw | fromjson'`
- To study it on your laptop, copy it **outside** the repo directory:
  ```bash
  ssh vps.g2labs.pl 'cd /opt/take-a-look && docker compose exec -T webhook cat /data/payloads.jsonl' > ~/take-a-look-payloads.jsonl
  ```
- Anything that goes into the repo as a test fixture must be fully anonymised first (CLAUDE.md, issue 0003).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Dashboard: "The callback URL or verify token couldn't be validated" | Token mismatch, container down, or Caddy not reloaded | Compare `.env` with what you typed (no spaces/quotes); `docker compose ps`; redo the `curl` check in 4.4 |
| Logs show `webhook verification refused` | Verify token differs | Fix `.env`, `docker compose up -d webhook`, verify again |
| Webhook verified, but sending a message logs nothing | Page not subscribed to `messages` (4.8), or the sender has no role on the app | Redo 4.8; message from the account that created the app |
| Logs show `rejected POST with bad or missing signature` for real messages | Wrong app secret | Copy the secret again (4.4), `docker compose up -d webhook` |
| Logs show `no META_PAGE_ACCESS_TOKEN set` | Token not in `.env` or service not recreated | 4.7, then `docker compose up -d webhook` |
| `ack failed (HTTP 400)` with `code 190` | Token invalid or expired (e.g. after a password change) | Generate a new one (4.7) |
| `ack failed` with `code 200` or `230`, mentioning `pages_messaging` | Permission missing | 4.5, then regenerate the token (4.7) |
| `ack failed` with `code 10`, `error_subcode 2018278` | Reply outside the 24-hour window | Expected for old messages; the prototype only replies to fresh ones |
