"""Throwaway Messenger webhook prototype (spec 0001, issue 0002).

Verifies Meta's subscription handshake, checks every POST's X-Hub-Signature-256,
appends each payload as one JSON line to the payload log and replies to each
incoming message with a fixed Polish acknowledgement. A few "probe ..." text
commands (issue 0003) try the Messenger features spec 0002 relies on.

Standard library only. Replaced by the real service in issue 0004.
"""

import hashlib
import hmac
import json
import logging
import mimetypes
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ACK_TEXT = "Dzięki, mam to! 👀 (to jeszcze prototyp: niczego nie zapisuję do Biblioteki)"
MAX_BODY_BYTES = 1_000_000
MAX_UPLOAD_BYTES = 25 * 1024 * 1024

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
# Overridable only so the prototype can be exercised against a local fake Graph API.
GRAPH_URL = os.environ.get("GRAPH_BASE_URL", "https://graph.facebook.com") + f"/{GRAPH_API_VERSION}"
DOMAIN = os.environ.get("DOMAIN", "look.g2labs.pl")

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


def message_events(payload: dict) -> list[dict]:
    """Incoming messages and postbacks from people (not echoes of the Page's own replies)."""
    events = []
    for entry in payload.get("entry") or []:
        for event in (entry.get("messaging") or []) if isinstance(entry, dict) else []:
            if not isinstance(event, dict) or not (event.get("sender") or {}).get("id"):
                continue
            message, postback = event.get("message"), event.get("postback")
            if isinstance(message, dict) and not message.get("is_echo"):
                events.append(event)
            elif isinstance(postback, dict):
                events.append(event)
    return events


# --- Graph API ---------------------------------------------------------------


def graph_post(path: str, data: bytes, content_type: str, what: str, method: str = "POST") -> bool:
    if not PAGE_ACCESS_TOKEN:
        log.warning("no META_PAGE_ACCESS_TOKEN set: not sending %s", what)
        return False
    request = urllib.request.Request(
        f"{GRAPH_URL}/{path}",
        data=data,
        headers={"Content-Type": content_type, "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}"},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            log.info("%s sent (HTTP %s)", what, response.status)
            return True
    except urllib.error.HTTPError as e:
        # Graph API error bodies carry the reason (expired token, outside 24 h window, ...)
        log.error("%s failed (HTTP %s): %s", what, e.code, e.read().decode(errors="replace"))
    except (urllib.error.URLError, TimeoutError) as e:
        log.error("%s failed: %s", what, getattr(e, "reason", e))
    return False


def graph_post_json(path: str, body: dict, what: str) -> bool:
    return graph_post(path, json.dumps(body).encode(), "application/json", what)


def send_message(recipient_id: str, message: dict, what: str = "reply") -> bool:
    return graph_post_json(
        "me/messages",
        {"recipient": {"id": recipient_id}, "messaging_type": "RESPONSE", "message": message},
        what,
    )


def send_text(recipient_id: str, text: str, what: str = "reply") -> bool:
    return send_message(recipient_id, {"text": text}, what)


def upload_attachment(recipient_id: str, kind: str, data: bytes, mime: str, what: str) -> bool:
    filename = "probe" + (mimetypes.guess_extension(mime) or ".mp4")
    """Send a file from this server as an attachment (multipart upload, max 25 MB)."""
    boundary = uuid.uuid4().hex
    fields = {
        "recipient": json.dumps({"id": recipient_id}),
        "messaging_type": "RESPONSE",
        "message": json.dumps({"attachment": {"type": kind, "payload": {"is_reusable": False}}}),
    }
    parts = [
        f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, v in fields.items()
    ]
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="filedata"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n".encode()
        + data
        + f"\r\n--{boundary}--\r\n".encode()
    )
    return graph_post("me/messages", b"".join(parts), f"multipart/form-data; boundary={boundary}", what)


# --- Probes (issue 0003): try the Messenger features spec 0002 relies on ------

PROBE_HELP = (
    "Komendy testowe:\n"
    "• probe menu – ustawia stałe menu (☰ przy polu wiadomości)\n"
    "• probe quick – szybkie odpowiedzi (przyciski pod wiadomością)\n"
    "• probe carousel – karuzela kart z przyciskami\n"
    "• probe video – odsyła ostatnie wideo, które mi wysłałeś/aś\n"
    "• probe menu off – usuwa stałe menu"
)

# Last video attachment URL per Sender, so "probe video" can download it and upload it back:
# the same round trip the Library will do with Snapshot media.
last_video_url: dict[str, str] = {}


def probe_menu(sender_id: str) -> None:
    ok = graph_post_json(
        "me/messenger_profile",
        {
            "get_started": {"payload": "GET_STARTED"},
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        {"type": "postback", "title": "Co nowego", "payload": "MENU_CO_NOWEGO"},
                        {"type": "postback", "title": "Pomoc", "payload": "MENU_POMOC"},
                        {"type": "web_url", "title": "Strona", "url": f"https://{DOMAIN}/health"},
                    ],
                }
            ],
        },
        "persistent menu",
    )
    send_text(
        sender_id,
        "Menu ustawione. Zamknij i otwórz rozmowę: szukaj ☰ obok pola wiadomości."
        if ok
        else "Nie udało się ustawić menu (szczegóły w logach serwera).",
    )


def probe_menu_off(sender_id: str) -> None:
    body = json.dumps({"fields": ["persistent_menu", "get_started"]}).encode()
    ok = graph_post("me/messenger_profile", body, "application/json", "menu delete", method="DELETE")
    send_text(sender_id, "Menu usunięte." if ok else "Nie udało się usunąć menu (szczegóły w logach serwera).")


def probe_quick(sender_id: str) -> None:
    send_message(
        sender_id,
        {
            "text": "Szybkie odpowiedzi: wybierz jedną.",
            "quick_replies": [
                {"content_type": "text", "title": "Przepis", "payload": "QR_PRZEPIS"},
                {"content_type": "text", "title": "Produkt", "payload": "QR_PRODUKT"},
                {"content_type": "text", "title": "Inne", "payload": "QR_INNE"},
            ],
        },
        "quick replies",
    )


def probe_carousel(sender_id: str) -> None:
    def card(n: int) -> dict:
        return {
            "title": f"Karta {n}",
            "subtitle": "Tak mogłyby wyglądać wyniki wyszukiwania.",
            "image_url": f"https://picsum.photos/seed/zerknij{n}/600/314",
            "default_action": {"type": "web_url", "url": f"https://{DOMAIN}/health"},
            "buttons": [
                {"type": "web_url", "title": "Otwórz", "url": f"https://{DOMAIN}/health"},
                {"type": "postback", "title": "Kopia", "payload": f"CAROUSEL_KOPIA_{n}"},
            ],
        }

    send_message(
        sender_id,
        {
            "attachment": {
                "type": "template",
                "payload": {"template_type": "generic", "elements": [card(n) for n in (1, 2, 3)]},
            }
        },
        "carousel",
    )


def probe_video(sender_id: str) -> None:
    url = last_video_url.get(sender_id)
    if not url or not url.startswith("https://"):
        send_text(sender_id, "Najpierw wyślij mi jakieś wideo (np. nagrane telefonem), potem znów: probe video")
        return
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(MAX_UPLOAD_BYTES + 1)
            mime = response.headers.get_content_type()
    except (urllib.error.URLError, TimeoutError) as e:
        log.error("video download failed: %s", e)
        send_text(sender_id, "Nie udało się pobrać wideo od Mety (szczegóły w logach serwera).")
        return
    if len(data) > MAX_UPLOAD_BYTES:
        send_text(sender_id, "To wideo ma ponad 25 MB, a tyle Messenger przyjmuje maksymalnie. Spróbuj krótszego.")
        return
    log.info("video downloaded (%d bytes, %s), uploading back", len(data), mime)
    if not upload_attachment(sender_id, "video", data, mime, "video upload"):
        send_text(sender_id, "Nie udało się odesłać wideo (szczegóły w logach serwera).")


PROBES = {
    "probe": lambda sender_id: send_text(sender_id, PROBE_HELP),
    "probe menu": probe_menu,
    "probe menu off": probe_menu_off,
    "probe quick": probe_quick,
    "probe carousel": probe_carousel,
    "probe video": probe_video,
}


def handle_event(event: dict) -> None:
    try:
        reply_to_event(event)
    except Exception:
        log.exception("handling event failed")


def reply_to_event(event: dict) -> None:
    sender_id = event["sender"]["id"]
    if postback := event.get("postback"):
        label = postback.get("title") or postback.get("payload")
        send_text(sender_id, f"Kliknięto przycisk: {label} ({postback.get('payload')})", "postback reply")
        return
    message = event["message"]
    for attachment in message.get("attachments") or []:
        if attachment.get("type") == "video" and (attachment.get("payload") or {}).get("url"):
            last_video_url[sender_id] = attachment["payload"]["url"]
    if quick_reply := message.get("quick_reply"):
        send_text(sender_id, f"Wybrano szybką odpowiedź: {quick_reply.get('payload')}", "quick reply answer")
        return
    probe = PROBES.get((message.get("text") or "").strip().lower())
    if probe:
        probe(sender_id)
    else:
        send_text(sender_id, ACK_TEXT, "ack")


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
        events = message_events(payload)
        log.info("event logged (object=%s, messages/postbacks=%d)", payload.get("object"), len(events))
        for event in events:
            threading.Thread(target=handle_event, args=(event,), daemon=True).start()

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
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), WebhookHandler).serve_forever()


if __name__ == "__main__":
    main()
