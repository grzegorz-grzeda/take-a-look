# 0001: VPS ready behind HTTPS on look.g2labs.pl

Spec: [0001 Messenger webhook prototype](../specs/0001-messenger-webhook-prototype.md)
Status: done
Blocked by: None (can start immediately)

## What to build

`https://look.g2labs.pl` reaches the VPS and serves a health page over a valid certificate, from a Docker Compose project with Caddy in front. This is the infrastructure the prototype and the real service both grow from. The owner performs the DNS and VPS steps, guided by a walkthrough.

## Acceptance criteria

- [x] Walkthrough for adding the DNS record for `look.g2labs.pl` in OVH while `g2labs.pl` stays on Netlify
- [x] Docker and Docker Compose installed on the VPS (walkthrough if missing)
- [x] Compose project with Caddy obtaining a certificate automatically for `look.g2labs.pl`
- [x] A health endpoint answers over HTTPS from outside the VPS
- [x] Only ports 80/443 (and SSH) exposed

## Comments

- Agent: walkthroughs in [docs/guides](../guides/README.md) (DNS, Docker + firewall, Compose + Caddy) and the Compose project (`compose.yaml`, `caddy/Caddyfile`, `.env.example`) are in place and smoke-tested locally (`DOMAIN=localhost`: `/health` 200 `ok`, other paths 404, HTTP→HTTPS 308, `caddy reload` works). Remaining: the owner runs guides 1–3 on OVH and the VPS and ticks the criteria.
- Agent (2026-11-09): verified from outside the VPS: `https://look.g2labs.pl/health` → `HTTP/2 200 ok`, Let's Encrypt certificate, HTTP → HTTPS 308, other paths 404; of ports 22, 80, 443, 3000, 5432, 8000, 8080, 27017 only 22/80/443 open. Done.
