"""Throwaway Messenger webhook prototype (spec 0001, issue 0002).

Verifies Meta's subscription handshake, checks every POST's X-Hub-Signature-256,
appends each payload as one JSON line to the payload log and replies to each
incoming message with a fixed Polish acknowledgement.

Standard library only. Replaced by the real service in issue 0004.
"""

import hashlib
import hmac
import json
import logging
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ACK_TEXT = "Dzięki, mam to! 👀 (to jeszcze prototyp: niczego nie zapisuję do Biblioteki)"
MAX_BODY_BYTES = 1_000_000

log = logging.getLogger("webhook")


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"Missing environment variable {name} (see .env.example)")
    return value


APP_SECRET = required_env("META_APP_SECRET").encode()
VERIFY_TOKEN = required_env("META_VERIFY_TOKEN")
# Optional so the webhook can be verified before the Page token exists (guide 4 order).
PAGE_ACCESS_TOKEN = os.environ.get("META_PAGE_ACCESS_TOKEN", "").strip()
GRAPH_API_VERSION = required_env("META_GRAPH_API_VERSION")
PAYLOAD_LOG = os.environ.get("PAYLOAD_LOG", "/data/payloads.jsonl")
SEND_API_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/messages"

log_lock = threading.Lock()


def signature_is_valid(body: bytes, header: str | None) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest().encode()
    return hmac.compare_digest(expected, header.removeprefix("sha256=").encode())


def append_payload(body: bytes) -> None:
    """One JSON line per POST; `raw` is the request body exactly as Meta sent it."""
    line = json.dumps(
        {
            "received_at": datetime.now(timezone.utc).isoformat(),
            "raw": body.decode("utf-8", errors="replace"),
        },
        ensure_ascii=False,
    )
    with log_lock, open(PAYLOAD_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def senders_to_acknowledge(payload: dict) -> list[str]:
    """IDs of people who sent a message (not echoes of the Page's own replies)."""
    senders = []
    for entry in payload.get("entry") or []:
        for event in (entry.get("messaging") or []) if isinstance(entry, dict) else []:
            message = event.get("message") if isinstance(event, dict) else None
            sender_id = (event.get("sender") or {}).get("id") if message else None
            if sender_id and not message.get("is_echo"):
                senders.append(sender_id)
    return senders


def send_ack(recipient_id: str) -> None:
    if not PAGE_ACCESS_TOKEN:
        log.warning("no META_PAGE_ACCESS_TOKEN set: not replying")
        return
    body = json.dumps(
        {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {"text": ACK_TEXT},
        }
    ).encode()
    request = urllib.request.Request(
        SEND_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            log.info("ack sent (HTTP %s)", response.status)
    except urllib.error.HTTPError as e:
        # Graph API error bodies carry the reason (expired token, outside 24 h window, ...)
        log.error("ack failed (HTTP %s): %s", e.code, e.read().decode(errors="replace"))
    except urllib.error.URLError as e:
        log.error("ack failed: %s", e.reason)


class WebhookHandler(BaseHTTPRequestHandler):
    timeout = 10  # seconds per socket read; stops slow or stalled clients holding a thread

    def do_GET(self) -> None:
        url = urllib.parse.urlsplit(self.path)
        if url.path != "/webhook":
            return self.respond(404, "Not found")
        query = urllib.parse.parse_qs(url.query)
        mode = query.get("hub.mode", [""])[0]
        token = query.get("hub.verify_token", [""])[0]
        challenge = query.get("hub.challenge", [""])[0]
        if mode == "subscribe" and hmac.compare_digest(token.encode(), VERIFY_TOKEN.encode()):
            log.info("webhook verified")
            return self.respond(200, challenge)
        log.warning("webhook verification refused")
        return self.respond(403, "Forbidden")

    def do_POST(self) -> None:
        if urllib.parse.urlsplit(self.path).path != "/webhook":
            return self.respond(404, "Not found")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return self.respond(400, "Bad Content-Length")
        if not 0 <= length <= MAX_BODY_BYTES:
            return self.respond(413, "Too large")
        body = self.rfile.read(length)
        if not signature_is_valid(body, self.headers.get("X-Hub-Signature-256")):
            log.warning("rejected POST with bad or missing signature")
            return self.respond(403, "Forbidden")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return self.respond(400, "Bad JSON")
        if not isinstance(payload, dict):
            return self.respond(400, "Expected a JSON object")

        append_payload(body)
        # Answer Meta first (must be within 5 s), reply to the Sender afterwards.
        self.respond(200, "EVENT_RECEIVED")
        senders = senders_to_acknowledge(payload)
        log.info("event logged (object=%s, messages=%d)", payload.get("object"), len(senders))
        for sender_id in senders:
            threading.Thread(target=send_ack, args=(sender_id,), daemon=True).start()

    def respond(self, status: int, text: str) -> None:
        data = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        # Default access log would print query strings, which include the verify token.
        pass


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log.info("Graph API %s, payload log %s", GRAPH_API_VERSION, PAYLOAD_LOG)
    ThreadingHTTPServer(("0.0.0.0", 8000), WebhookHandler).serve_forever()


if __name__ == "__main__":
    main()
