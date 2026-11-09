# 3. Compose project and Caddy

Goal: `https://look.g2labs.pl/health` answers `ok` from anywhere, over a certificate Caddy obtained and renews by itself.

Needs guides [1](01-dns-ovh.md) (DNS resolves) and [2](02-vps-docker-and-firewall.md) (Docker, ports 80/443 open in ufw).

## What's in the repo

- [`compose.yaml`](../../compose.yaml): Compose project `take-a-look` with one service, `caddy` (official `caddy:2` image). It publishes only 80, 443/tcp and 443/udp. Certificates live in the `caddy_data` volume so they survive restarts and upgrades.
- [`caddy/Caddyfile`](../../caddy/Caddyfile): one site, `{$DOMAIN}`. `/health` returns `ok`, `/webhook` goes to the prototype service ([guide 4](04-meta-app-and-webhook.md)), everything else is `404`.
- [`.env.example`](../../.env.example): settings, without values. This guide needs only `DOMAIN`; the `webhook` service starts and exits with `Missing environment variable` until guide 4 fills in the `META_*` values, which doesn't affect Caddy or `/health`.

Caddy handles HTTPS automatically: on first start it requests a certificate for `DOMAIN` from Let's Encrypt (falling back to ZeroSSL) via the HTTP-01 / TLS-ALPN challenge, redirects HTTP to HTTPS, and renews the certificate before it expires. No certbot, no cron.

## 3.1 Optional: try it on your laptop first

```bash
git clone https://github.com/grzegorz-grzeda/take-a-look.git && cd take-a-look
echo 'DOMAIN=localhost' > .env
docker compose up -d
curl -k https://localhost/health        # ok
docker compose down -v
```

With `localhost`, Caddy uses its own local CA (hence `-k`). Needs ports 80/443 free on the laptop.

## 3.2 Deploy on the VPS

On the VPS:

```bash
sudo mkdir -p /opt/take-a-look && sudo chown "$USER": /opt/take-a-look
git clone https://github.com/grzegorz-grzeda/take-a-look.git /opt/take-a-look
cd /opt/take-a-look

cp .env.example .env
chmod 600 .env
sed -i 's/^DOMAIN=.*/DOMAIN=look.g2labs.pl/' .env

docker compose up -d
docker compose logs -f caddy
```

In the logs, within about a minute, look for:

```
"msg":"certificate obtained successfully","identifier":"look.g2labs.pl"
```

Then `Ctrl+C` (Caddy keeps running). `restart: unless-stopped` brings it back after a reboot.

## 3.3 Check from outside

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

All commands from `/opt/take-a-look`.

| Task | Command |
|------|---------|
| Status | `docker compose ps` |
| Logs | `docker compose logs --tail 100 -f caddy` |
| Update to latest `main` | `git pull && docker compose up -d --build`, plus the Caddyfile reload below if it changed |
| Apply a Caddyfile change without downtime | `docker compose exec -w /etc/caddy caddy caddy reload` |
| Check a Caddyfile change before applying | `docker compose exec -w /etc/caddy caddy caddy validate` |
| Upgrade Caddy image | `docker compose pull && docker compose up -d` |
| Restart | `docker compose restart caddy` |
| Stop (keeps certificates) | `docker compose down` |

`caddy/` is mounted as a whole directory, so a `git pull` that changes the Caddyfile is visible inside the container; it takes effect on `reload`.

**Never run `docker compose down -v` on the VPS** unless you mean to: `-v` deletes the `caddy_data` volume with the certificates, and re-issuing them counts against Let's Encrypt rate limits.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `set DOMAIN in .env` error on any `docker compose` command | `.env` missing or `DOMAIN` empty | Redo the `cp`/`sed` lines in 3.2 |
| `bind: address already in use` on 80/443 | Another web server on the host | `sudo ss -tlnp 'sport = :80'`, then stop it (guide 2.4) |
| Logs show `challenge failed` / `timeout during connect` | DNS not pointing here yet, or 80/443 blocked | `dig +short look.g2labs.pl` from outside; `sudo ufw status`; provider firewall |
| Challenge fails over IPv6 only | AAAA record exists but IPv6 doesn't work | Remove the AAAA record (guide 1.2 step 4) or fix IPv6 |
| `CAA record ... prevents issuance` | CAA record without `letsencrypt.org` | Add CAA entries `0 issue "letsencrypt.org"` and `0 issue "sectigo.com"` (ZeroSSL fallback), or remove CAA |
| `too many failed authorizations` / rate limited | Repeated failed attempts | Fix the cause, then wait (Let's Encrypt: 5 failures per hostname per hour). Caddy retries on its own and may fall back to ZeroSSL |
| Browser certificate warning | Request hit something other than this Caddy, or Caddy is still on its first attempt | Check `dig`, wait a minute, read the logs |
| `/health` works on the VPS but not from outside | Testing via localhost, or upstream firewall | Always test from the laptop; check the provider's network firewall |
