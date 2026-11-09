# Guides

Step-by-step walkthroughs for the setup steps only a human can do. Follow them in order; each ends with a check that must pass before moving on.

| # | Guide | Result | Issue |
|---|-------|--------|-------|
| 1 | [DNS record for `look.g2labs.pl`](01-dns-ovh.md) | `look.g2labs.pl` resolves to the VPS; `g2labs.pl` still on Netlify | [0001](../issues/done-0001-vps-ready-behind-https.md) |
| 2 | [VPS: Docker, Compose and firewall](02-vps-docker-and-firewall.md) | Docker running; only SSH, 80 and 443 reachable | [0001](../issues/done-0001-vps-ready-behind-https.md) |
| 3 | [Compose project and Caddy](03-compose-and-caddy.md) | `https://look.g2labs.pl/health` answers `ok` over a valid certificate | [0001](../issues/done-0001-vps-ready-behind-https.md) |
| 4 | [Meta app, Page and webhook](04-meta-app-and-webhook.md) | Messages to the Zerknij Page are logged on the VPS and acknowledged | [0002](../issues/done-0002-meta-app-page-and-verified-webhook.md) |
| 5 | [Joanna joins as an app Tester](05-tester-invite.md) | Joanna can message the Page and gets replies | [0003](../issues/0003-capture-drops-probe-features-findings.md) |
| 6 | [Capture real Drops and try the probes](06-capture-and-probes.md) | Every kind of Drop logged, every probe tried, summary handed over | [0003](../issues/0003-capture-drops-probe-features-findings.md) |

## Placeholders

The repo is public, so the guides never contain real IP addresses, accounts or IDs (the hostname `look.g2labs.pl` is public anyway). Substitute your own:

| Placeholder | Meaning |
|-------------|---------|
| `203.0.113.10` | The VPS public IPv4 address |
| `2001:db8::10` | The VPS public IPv6 address (only if it has one) |
| `deploy` | Your non-root SSH user on the VPS |
| `vps` | SSH host alias / hostname of the VPS |

## Layout of what gets deployed

```
take-a-look/              # repo, cloned to /opt/take-a-look on the VPS
├── compose.yaml          # Compose project "take-a-look"
├── prototype/            # throwaway webhook service (spec 0001)
├── .env.example          # documented settings, no values
└── .env                  # real settings, VPS only, git-ignored
```

```
Internet ──80/443──▶ Caddy (edge project, /opt/edge) ──▶ /health → "ok"
                         │
                         └──▶ /webhook → webhook:8000  (Docker network `edge` only)
                                            └──▶ /data/payloads.jsonl (volume)
```
