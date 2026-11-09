# 6. Capture real Drops and try the probes

Goal: the payload log holds one example of every kind of Drop we care about, and each Messenger feature spec 0002 relies on has been tried. From that, the findings note for issue [0003](../issues/0003-capture-drops-probe-features-findings.md) is written.

Needs guides [4](04-meta-app-and-webhook.md) and [5](05-tester-invite.md). Takes about 20 minutes per person.

## 6.1 Send these Drops

Send each one to **Zerknij** in Messenger, the way you'd normally share it. Use real things you'd want to save; the log stays on the VPS. Between you, cover every row. Doing a row on both phones (Android/iPhone) is a bonus.

| # | Drop | How to send it | Who |
|---|------|----------------|-----|
| 1 | Facebook post | In the Facebook app: post → **Share** → **Send in Messenger** → Zerknij | both |
| 2 | Facebook reel | Facebook app: reel → **Share** (arrow) → Zerknij | both |
| 3 | Instagram reel | Instagram app: reel → **Share** (paper plane) → **Messenger** / **Share to…** → Zerknij | both |
| 4 | Shop listing | A product page (Allegro, IKEA, any shop) → browser **Share** → Messenger → Zerknij | one |
| 5 | Recipe page | A recipe site (e.g. Kwestia Smaku) → Share → Messenger → Zerknij | one |
| 6 | Plain article | A news or blog article → Share → Messenger → Zerknij | one |
| 7 | Screenshot | Take a screenshot → send it to Zerknij as an image | one |
| 8 | Photo | A photo from the camera roll | one |
| 9 | Text only | A message with no link, e.g. `kupić baterie AA` | one |
| 10 | Link + own text | Paste a link and write something with it, e.g. `https://… to na sobotę?` | both |
| 11 | Multi-share | Facebook app: Share → Send in Messenger → tick **both** your spouse and Zerknij → Send | both |
| 12 | Video | A short video from the camera roll (needed for the video probe) | one |

Every Drop should get the acknowledgement. If one doesn't, note which row: that is itself a finding.

Sharing apps often don't list a Page in their share sheet. If Zerknij isn't offered for a row, note that (it's a finding, and the reason row 11 exists), then fall back to **Copy link** and paste it into the Zerknij chat.

Go through the rows in order and note roughly when you sent each one: the summary in 6.3 is numbered and timed, which makes matching easy.

## 6.2 Try the probes

Type these to Zerknij, one at a time (lowercase or not, doesn't matter). Write down what you see on **both phones** if you can, e.g. in a shared note.

| Command | What should happen | What to note |
|---------|--------------------|--------------|
| `probe` | List of probe commands | — |
| `probe menu` | "Menu ustawione". Close and reopen the chat: a ☰ menu next to the message box with **Co nowego**, **Pomoc**, **Strona** | Is the menu visible at all (EU restrictions)? Tap **Pomoc**: does the bot answer "Kliknięto przycisk…"? |
| `probe quick` | Message with three buttons: Przepis / Produkt / Inne | Do the buttons show? Tap one: does the bot answer "Wybrano szybką odpowiedź…"? |
| `probe carousel` | Three swipeable cards with picture (from picsum.photos: a missing picture alone isn't a template failure), **Otwórz** and **Kopia** buttons | Do cards and pictures show? Does **Otwórz** open a page? Does **Kopia** get "Kliknięto przycisk…"? |
| `probe video` | Right after row 12 (Meta's video links expire, and a server restart forgets them): the bot sends your video back | Does the video arrive and play? |
| `probe menu off` | "Menu usunięte" | Menu gone after reopening the chat |

If something fails, the reason is in the server log, which is the most useful part of the finding:

```bash
docker compose logs --tail 30 webhook | grep -E 'failed|ERROR'
```

## 6.3 Hand the results over

On the VPS:

```bash
docker compose exec webhook python summarize.py > ~/drops-summary.txt
```

`summarize.py` prints the **shape** of every payload: which fields Meta sent, with text replaced by its length, URLs reduced to their host, IDs dropped and Senders numbered. It contains no message text or IDs; what it keeps is the time each payload arrived and the hosts of links (e.g. `allegro.pl`). That's fine to paste into the chat with the agent, but glance through it first. (`--text` adds the first 80 characters of each message: for your eyes only, don't paste that.)

Copy it to your laptop (outside the repo) and paste it together with:

- for each `#N` in the summary, which row of 6.1 it is (e.g. `#14 = row 3, Instagram reel, Joanna, iPhone`),
- your probe notes from 6.2,
- any error lines from the server log (they contain no private data, but check).

```bash
scp vps.g2labs.pl:drops-summary.txt ~/drops-summary.txt
```

## 6.4 What the agent does with it

- Writes the findings note as the `## Answer` of issue 0003: per Drop kind, which of URL, title, description, image and video Meta provides, and which probes work for an EU Page.
- Builds synthetic test fixtures from the payload shapes (invented IDs, names "Grzegorz" and "Joanna", invented URLs and text). Nothing from the real log enters the repo.
- Updates spec 0002 if a finding changes one of its decisions.

✅ Done when every row of 6.1 is in the summary and every probe has an outcome noted.
