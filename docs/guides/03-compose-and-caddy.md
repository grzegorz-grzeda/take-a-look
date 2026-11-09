# 3. Compose project and Caddy

Goal: `https://look.g2labs.pl/health` answers `ok` from anywhere, over a certificate Caddy obtained and renews by itself.

Needs guides [1](01-dns-ovh.md) (DNS resolves) and [2](02-vps-docker-and-firewall.md) (Docker, ports 80/443 open in ufw).

## Where Caddy lives

Caddy is **not** in this repo. One Caddy serves every project on the VPS (take-a-look, nodbeat, …), so it lives in its own Compose project: [**edge**](https://github.com/grzegorz-grzeda/edge), cloned to `/opt/edge`. It owns ports 80/443, terminates TLS, and holds the `look.g2labs.pl` site block (`/health` → `ok`, `/webhook` → `webhook:8000`, rest `404`). Certificates are in its `edge_caddy_data` volume.

This repo only:

- [`compose.yaml`](../../compose.yaml): Compose project `take-a-look`, service `webhook`, joined to the external Docker network `edge`, no published ports.
- [`.env.example`](../../.env.example): settings, without values.

```
Internet ──80/443──▶ edge: Caddy ──(network edge)──▶ take-a-look: webhook:8000
```

Until 2026-11, Caddy was a service in this repo. Moving an existing VPS to edge (keeping the certificate): edge's [migration guide](https://github.com/grzegorz-grzeda/edge/blob/main/docs/guides/01-migrate-from-take-a-look.md).

## 3.1 Deploy on a fresh VPS

edge first (it creates the `edge` network):

```bash
sudo mkdir -p /opt/edge && sudo chown "$USER": /opt/edge
git clone https://github.com/grzegorz-grzeda/edge.git /opt/edge
cd /opt/edge
docker compose up -d
docker compose logs -f caddy
```

Within about a minute, look for:

```
"msg":"certificate obtained successfully","identifier":"look.g2labs.pl"
```

Then `Ctrl+C`. `/health` already works now: Caddy answers it itself.

Then this project:

```bash
sudo mkdir -p /opt/take-a-look && sudo chown "$USER": /opt/take-a-look
git clone https://github.com/grzegorz-grzeda/take-a-look.git /opt/take-a-look
cd /opt/take-a-look

cp .env.example .env
chmod 600 .env
sed -i 's/^DOMAIN=.*/DOMAIN=look.g2labs.pl/' .env

docker compose up -d
```

The `webhook` service starts and exits with `Missing environment variable` until [guide 4](04-meta-app-and-webhook.md) fills in the `META_*` values; that doesn't affect `/health`. `restart: unless-stopped` brings both projects back after a reboot.

## 3.2 Check from outside

From your laptop (not the VPS, so the request really crosses the Internet):

```bash
curl -i https://look.g2labs.pl/health
```

Expect `HTTP/2 200` and body `ok`, with no certificate warning (no `-k`).

```bash
curl -sI http://look.g2labs.pl/health | head -2       # 308 redirect to https://
curl -s -o /dev/null -w '%{http_code}\n' https://look.g2labs.pl/anything   # 404

# Who issued the certificate, and until when
echo | openssl s_client -connect look.g2labs.pl:443 -servername look.g2labs.pl 2>/dev/null \
  | openssl x509 -noout -issuer -enddate
```

Re-run the port check from [2.5](02-vps-docker-and-firewall.md#25-check-from-outside): 22, 80 and 443 open, nothing else.

✅ Issue [0001](../issues/done-0001-vps-ready-behind-https.md) is done when all of the above pass.

## Day-to-day operations

This project, from `/opt/take-a-look`:

| Task | Command |
|------|---------|
| Status | `docker compose ps` |
| Logs | `docker compose logs --tail 100 -f webhook` |
| Update to latest `main` | `git pull && docker compose up -d --build` |
| Stop | `docker compose down` |

Caddy (Caddyfile changes, reload, logs, upgrades): from `/opt/edge`, see the [edge README](https://github.com/grzegorz-grzeda/edge#operations). Routing for `look.g2labs.pl` is changed in the edge repo, not here.

**Never run `docker compose down -v` in `/opt/edge`**: it deletes the certificates, and re-issuing them counts against Let's Encrypt rate limits.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `network edge declared as external, but could not be found` | edge not set up yet | Start edge first (3.1) |
| `/health` ok, `/webhook` `502` | `webhook` down or not on the `edge` network | `docker compose ps`; `docker network inspect edge` must list `take-a-look-webhook-1` |
| `bind: address already in use` on 80/443 (edge) | Another web server on the host | `sudo ss -tlnp 'sport = :80'`, then stop it (guide 2.4) |
| Logs show `challenge failed` / `timeout during connect` | DNS not pointing here yet, or 80/443 blocked | `dig +short look.g2labs.pl` from outside; `sudo ufw status`; provider firewall |
| Challenge fails over IPv6 only | AAAA record exists but IPv6 doesn't work | Remove the AAAA record (guide 1.2 step 4) or fix IPv6 |
| `CAA record ... prevents issuance` | CAA record without `letsencrypt.org` | Add CAA entries `0 issue "letsencrypt.org"` and `0 issue "sectigo.com"` (ZeroSSL fallback), or remove CAA |
| `too many failed authorizations` / rate limited | Repeated failed attempts | Fix the cause, then wait (Let's Encrypt: 5 failures per hostname per hour). Caddy retries on its own and may fall back to ZeroSSL |
| `/health` works on the VPS but not from outside | Testing via localhost, or upstream firewall | Always test from the laptop; check the provider's network firewall |
