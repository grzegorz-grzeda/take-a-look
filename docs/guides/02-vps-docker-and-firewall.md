# 2. VPS: Docker, Compose and firewall

Goal: Docker Engine and the Compose plugin run on the VPS, and from the Internet only SSH (22), HTTP (80) and HTTPS (443) are reachable.

Assumes Ubuntu or Debian, and that you SSH in as a non-root user with `sudo` (`deploy` below). Run everything **on the VPS** unless a step says "from your laptop".

## 2.1 Check what's already there

```bash
. /etc/os-release && echo "$PRETTY_NAME"
docker --version
docker compose version
```

- Both `docker` commands print a version → Docker is installed; skip to 2.3.
- `docker compose` fails but `docker-compose` works → old standalone Compose v1. Install the plugin in 2.2 (the guides use `docker compose`, with a space).
- `docker` not found → 2.2.

## 2.2 Install Docker Engine and the Compose plugin

From Docker's official apt repository (the distro's `docker.io` package is older and has no Compose plugin):

```bash
# Remove distro packages that conflict (harmless if absent)
for p in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove -y $p; done

# Docker's signing key and repository
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
. /etc/os-release
sudo curl -fsSL "https://download.docker.com/linux/$ID/gpg" -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/$ID ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start now and on boot
sudo systemctl enable --now docker
```

Let your user run Docker without `sudo` (log out and back in afterwards):

```bash
sudo usermod -aG docker "$USER"
```

> Being in the `docker` group is effectively root on the VPS. Fine for a single-owner box; don't add other users.

Check (after logging back in):

```bash
docker run --rm hello-world
docker compose version
```

## 2.3 Optional: swap on a 2 GB VPS

Image builds (later issues) can briefly exceed 2 GB RAM. A 2 GB swap file prevents the OOM killer from stopping them:

```bash
swapon --show                       # empty output = no swap yet
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 2.4 Firewall: allow only SSH, 80 and 443

Use `ufw`. **Allow SSH before enabling it**, or you lock yourself out.

```bash
sudo apt-get install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH        # or: sudo ufw allow 22/tcp (use your port if sshd isn't on 22)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp        # HTTP/3
sudo ufw enable
sudo ufw status verbose
```

### Docker bypasses ufw

Ports published by Docker (`ports:` in `compose.yaml`) are opened by Docker's own iptables rules **before** ufw sees the traffic. A `ufw deny` does not block them. So the rule in this repo is:

- Only Caddy publishes ports, and only `80/tcp`, `443/tcp` and `443/udp`.
- Every other service (the app, later) uses the internal Compose network, never `ports:`. If one needs to be reached from the VPS itself for debugging, bind to localhost: `"127.0.0.1:8000:8000"`.

If your VPS provider also offers a network/edge firewall in its panel, you can mirror the same three ports there as a second layer.

### Anything else listening?

```bash
sudo ss -tulpn | grep -vE '127\.0\.0\.[0-9]+|\[::1\]'
```

This hides loopback-only listeners (e.g. systemd-resolved on `127.0.0.53`). Only `sshd` (and, after guide 3, `docker-proxy` on 80/443) should remain, plus possibly a DHCP client on UDP 68. Stop or uninstall anything else you don't need (e.g. a preinstalled web server: `sudo systemctl disable --now apache2 nginx`; it would also block Caddy from taking ports 80/443).

## 2.5 Check from outside

From your laptop:

```bash
nc -zv -w 3 203.0.113.10 22     # succeeded
nc -zv -w 3 203.0.113.10 80     # refused until guide 3, then succeeded
nc -zv -w 3 203.0.113.10 443    # refused until guide 3, then succeeded
nc -zv -w 3 203.0.113.10 8080   # timed out (filtered): any other port
```

For a fuller view, `nmap -Pn 203.0.113.10` should list only 22 (and 80/443 after guide 3) as open.

✅ Done when `docker compose version` works for your user and only SSH is reachable. Next: [3. Compose project and Caddy](03-compose-and-caddy.md).
