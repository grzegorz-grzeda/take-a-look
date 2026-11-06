# take-a-look

A 'take a look at this...' bot for gathering links and Internet content (social posts and reels, shopping listings, recipes, articles) for yourself and your significant other — saved into a shared, searchable Library that survives the originals disappearing.

The first Channel is a Messenger bot; Telegram may follow.

## Status

Pre-release. Infrastructure first: the VPS serves a health page on `https://look.g2labs.pl` from a Docker Compose project with Caddy in front ([issue 0001](docs/issues/0001-vps-ready-behind-https.md)). The Messenger webhook prototype comes next.

## Documentation

| Where | What |
|-------|------|
| [GLOSSARY.md](GLOSSARY.md) | Domain language (Sender, Drop, Entry, Library, …) |
| [docs/guides](docs/guides) | Step-by-step setup walkthroughs: DNS, VPS, Docker, Caddy |
| [docs/adr](docs/adr) | Architecture decisions |
| [docs/specs](docs/specs) | Specs |
| [docs/issues](docs/issues) | Work breakdown, one file per issue |

## Repository layout

```
compose.yaml       Compose project run on the VPS
caddy/Caddyfile    HTTPS, health page, (later) proxy to the service
.env.example       Settings with empty values; copy to .env (git-ignored)
docs/              Guides, ADRs, specs, issues
```

## Quick start

On the VPS, after [guides 1–2](docs/guides):

```bash
sudo mkdir -p /opt/take-a-look && sudo chown "$USER": /opt/take-a-look
git clone https://github.com/grzegorz-grzeda/take-a-look.git /opt/take-a-look
cd /opt/take-a-look
cp .env.example .env && chmod 600 .env
sed -i 's/^DOMAIN=.*/DOMAIN=look.g2labs.pl/' .env
docker compose up -d
curl https://look.g2labs.pl/health   # ok
```

Full walkthrough: [docs/guides/03-compose-and-caddy.md](docs/guides/03-compose-and-caddy.md).

## Privacy

This repo is public, but the Library holds private data. No secrets, real IDs, chat content or runtime data are ever committed; see [CLAUDE.md](CLAUDE.md).
