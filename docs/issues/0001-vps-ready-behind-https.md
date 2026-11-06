# 0001: VPS ready behind HTTPS on look.g2labs.pl

Spec: [0001 Messenger webhook prototype](../specs/0001-messenger-webhook-prototype.md)
Status: ready-for-human
Blocked by: None (can start immediately)

## What to build

`https://look.g2labs.pl` reaches the VPS and serves a health page over a valid certificate, from a Docker Compose project with Caddy in front. This is the infrastructure the prototype and the real service both grow from. The owner performs the DNS and VPS steps, guided by a walkthrough.

## Acceptance criteria

- [ ] Walkthrough for adding the DNS record for `look.g2labs.pl` in OVH while `g2labs.pl` stays on Netlify
- [ ] Docker and Docker Compose installed on the VPS (walkthrough if missing)
- [ ] Compose project with Caddy obtaining a certificate automatically for `look.g2labs.pl`
- [ ] A health endpoint answers over HTTPS from outside the VPS
- [ ] Only ports 80/443 (and SSH) exposed
