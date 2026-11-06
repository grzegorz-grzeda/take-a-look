# 1. DNS record for `look.g2labs.pl`

Goal: `look.g2labs.pl` points at the VPS, while `g2labs.pl` and `www.g2labs.pl` keep serving the Netlify site.

Adding one record for the `look` subdomain doesn't touch the apex or `www` records, so the Netlify site isn't affected.

## 1.1 Find out who serves the DNS zone

The domain is registered at OVH, but the zone may be hosted by OVH **or** delegated to Netlify DNS. Check:

```bash
dig +short NS g2labs.pl
```

| Answer looks like | Zone is hosted at | Go to |
|-------------------|-------------------|-------|
| `dnsXX.ovh.net.` / `nsXX.ovh.net.` | OVH | 1.2 |
| `dnsX.pXX.nsone.net.` | Netlify DNS | 1.3 |
| anything else | that provider | add the same `A` record there (1.2 steps 2–4 apply) |

## 1.2 Zone at OVH

1. Log in to the OVH Control Panel → **Web Cloud** → **Domain names** → `g2labs.pl` → **DNS zone** tab.
2. Look through the existing entries first:
   - The Netlify site is usually an apex `A` record (to Netlify's load balancer) plus a `www` `CNAME` to `<site>.netlify.app`. **Leave them alone.**
   - If there is already a `look` entry, or a wildcard `*` entry, note it: an existing `look` record must be edited instead of added; a wildcard is fine (a specific record wins over it).
   - If there are `CAA` entries, they must allow `letsencrypt.org` (and `sectigo.com` for Caddy's ZeroSSL fallback), otherwise Caddy can't get a certificate. No `CAA` entries at all is fine.
3. **Add an entry** → type **A**:
   - Subdomain: `look`
   - Target: `203.0.113.10` (the VPS IPv4)
   - TTL: leave the default, or set `3600`
4. **Only if the VPS has a working public IPv6 address**, also add an **AAAA** entry: subdomain `look`, target `2001:db8::10`. Don't add an AAAA record if you aren't sure IPv6 works on the VPS: Let's Encrypt prefers IPv6, and a broken AAAA record makes certificate issuance fail.
5. Confirm. OVH applies zone changes within a few minutes (the panel may say up to 24 h; usually much less).

## 1.3 Zone at Netlify DNS

1. Netlify → **Domains** → `g2labs.pl` → **DNS settings** → **Add new record**.
2. Type `A`, name `look`, value `203.0.113.10`, TTL default. Save.
3. AAAA: same rule as in 1.2 step 4.
4. Don't change the Netlify-managed records for the apex and `www`.

## 1.4 Check

From your laptop (not the VPS):

```bash
dig +short A look.g2labs.pl
```

Must print the VPS IPv4. If it's empty, wait a few minutes and ask the zone's authoritative nameserver directly to rule out resolver caching:

```bash
dig +short A look.g2labs.pl @$(dig +short NS g2labs.pl | head -1)
```

Also confirm the main site is untouched:

```bash
curl -sI https://g2labs.pl | head -1
```

Should still be `HTTP/2 200` (or the redirect it gave before).

✅ Done when `look.g2labs.pl` resolves to the VPS. Next: [2. VPS: Docker, Compose and firewall](02-vps-docker-and-firewall.md).
