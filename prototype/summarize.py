"""Print the shape of every logged payload without its private content (issue 0003).

Strings become <str:N>; URLs keep only host, path depth and query parameter names;
IDs and event timestamps become their type; Senders are numbered in order of appearance.
Kept: the time each payload was received (to match #N to what was sent) and link hosts. The output can be pasted
into the findings discussion; the raw log itself never leaves the VPS.

Usage (on the VPS):  docker compose exec webhook python summarize.py [--text]
  --text  also show the first 80 characters of message text (private: don't paste)
"""

import json
import os
import re
import sys
import urllib.parse

URL_RE = re.compile(r"https?://\S+")
KEEP_VALUES = {"type", "template_type", "object", "content_type"}


def url_shape(url: str) -> str:
    """Host, path depth and query parameter names: enough to spot redirect wrappers
    (l.facebook.com) and expiring CDN links (oe=, _nc_sid=) without the private part."""
    try:
        parts = urllib.parse.urlsplit(url)
        host = parts.hostname
    except ValueError:
        return "unparseable"
    depth = len([p for p in parts.path.split("/") if p])
    params = sorted({k for k, _ in urllib.parse.parse_qsl(parts.query)})
    return f"{host} /{depth} segments" + (f" ?{','.join(params)}" if params else "")


def shape(value, key: str = ""):
    if isinstance(value, dict):
        return {k: shape(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [shape(v, key) for v in value]
    if isinstance(value, str):
        if key in KEEP_VALUES:
            return value
        if value.startswith(("http://", "https://")) and " " not in value:
            return f"<url:{url_shape(value)}>"
        hosts = [url_shape(w).split(" ")[0] for w in URL_RE.findall(value)]
        return f"<str:{len(value)}" + (f" with urls:{','.join(hosts)}>" if hosts else ">")
    if isinstance(value, bool) or value is None:
        return value
    return f"<{type(value).__name__}>"


def main() -> None:
    show_text = "--text" in sys.argv
    sender_numbers: dict[str, int] = {}
    with open(os.environ.get("PAYLOAD_LOG", "/data/payloads.jsonl"), encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            try:
                record = json.loads(line)
                payload = json.loads(record["raw"])
                events = [e for entry in payload["entry"] for e in entry["messaging"] if isinstance(e, dict)]
            except (ValueError, KeyError, TypeError) as e:
                print(f"#{n} unreadable record ({type(e).__name__})")
                continue
            for event in events:
                sender_id = (event.get("sender") or {}).get("id", "?")
                message = event.get("message")
                if isinstance(message, dict) and message.get("is_echo"):
                    continue  # the Page's own replies
                who = f"Sender {sender_numbers.setdefault(sender_id, len(sender_numbers) + 1)}"
                kinds = [k for k in event if k not in {"sender", "recipient", "timestamp"}]
                print(f"#{n} {record['received_at'][:19]}  {who}  {', '.join(kinds)}")
                if show_text and isinstance(message, dict) and (text := message.get("text")):
                    print(f"   text: {text[:80]!r}")
                body = {k: event[k] for k in kinds}
                print("   " + json.dumps(shape(body), ensure_ascii=False, indent=2).replace("\n", "\n   "))


if __name__ == "__main__":
    main()
