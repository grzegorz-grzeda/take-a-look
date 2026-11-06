# 0002 Library core over Messenger (v0.1.0)

Status: ready-for-agent

## Problem Statement

My wife and I send each other Facebook posts and reels, shopping listings, recipes and other links on Messenger. Months later we can't find them: Messenger has no useful search, sorting or filtering for shared links, and its link previews are unreliable. Worse, Facebook content is often removed or changed, so even when we find the message, the content behind it is gone and there was never a proper caption to remember it by.

## Solution

A Messenger bot (a Facebook Page, see ADR-0001) that both Senders share things to — usually in the same share as to each other. Every Drop becomes an Entry in one shared Library: the bot preserves a Snapshot of the content (text, metadata, images, video where possible), has Claude Haiku assign a Category and Polish Tags, and confirms in Polish with a one-line summary and buttons to correct it. Either Sender can later search the whole Library in Polish (matching word forms and finding English content too), browse what's new, get the original link or the preserved Snapshot back in the chat, and delete or restore Entries. Released as version 0.1.0.

## User Stories

### Access

1. As a Sender, I want only my spouse and me to be able to use the bot, so that our Library stays private.
2. As the owner, I want messages from anyone not on the allowlist silently ignored, so that strangers get no information about the bot.
3. As the owner, I want each allowlisted Messenger ID mapped to a Sender name, so that the bot can say who dropped what.

### Dropping

4. As a Sender, I want to share a link to the Page from any app's share sheet, so that saving is as easy as sending it to my spouse.
5. As a Sender, I want to share to my spouse and the Page in one share, so that our normal conversation continues while the Library fills up.
6. As a Sender, I want a Facebook post or reel I share to be saved, so that it can be found later.
7. As a Sender, I want a shopping listing I share to be saved with its product name and price at the time, so that I remember what it was and what it cost.
8. As a Sender, I want a recipe page I share to be saved with its ingredients and steps, so that the recipe survives even if the site changes.
9. As a Sender, I want an article or other web page I share to be saved with its readable text, so that I can read it later.
10. As a Sender, I want a screenshot or photo I send to become an Entry, so that things I captured as images are searchable too.
11. As a Sender, I want a text-only message (e.g. "kupić ten mop z Lidla") to become an Entry, so that quick notes are saved too.
12. As a Sender, I want the text I write alongside a link saved with the Entry, so that my own caption survives even when the original has none.
13. As a Sender, I want a message with several links to create one Entry per link, each keeping my text, so that each thing is findable on its own.
14. As a Sender, I want to be told when a link I send is already in the Library — when and by whom it was first sent — so that I notice we already have it.
15. As a Sender, I want a Resend to be recorded on the existing Entry rather than create a duplicate, so that the Library stays clean and I can see something was sent repeatedly.
16. As a Sender, I want the bot to accept my Drop instantly even if processing takes a while, so that sharing never feels slow or fails.

### Preserving

17. As a Sender, I want a Snapshot of the content saved at the time of the Drop, so that the Entry stays useful when the original disappears.
18. As a Sender, I want reel videos downloaded where possible, so that I can still watch them after Facebook removes them.
19. As a Sender, I want images from posts, listings and recipes saved, so that I recognise the Entry visually.
20. As a Sender, I want the Snapshot to use whatever preview data Meta includes in the share, so that Facebook content gets a caption even when it can't be scraped.
21. As a Sender, I want a Drop to be saved even if extraction fails completely, so that I never lose the link itself.
22. As the owner, I want downloaded videos capped at 720p, so that the small VPS disk lasts.

### Classifying

23. As a Sender, I want each Entry to get one Category (Recipe, Product, Social post, Article, Place, Other), so that I can filter by kind.
24. As a Sender, I want each Entry to get a few Polish Tags, so that I can find it by what it's about.
25. As a Sender, I want each Entry to get a short Polish title, so that search results and confirmations are readable even when the original has no caption.
26. As a Sender, I want Entries in English to still get Polish Tags, so that I can search everything in Polish.
27. As a Sender, I want screenshots and photos classified by what's visible in them, so that image Entries are as findable as links.
28. As a Sender, I want Entries saved even when the AI service is unavailable or out of credit, and classified once it comes back, so that nothing is lost.

### Confirming and correcting

29. As a Sender, I want a one-line Polish confirmation after my Drop is processed (Category · title · Tags), so that I know the bot understood it.
30. As a Sender, I want a quick-reply button to change the Category, offering the six Categories, so that I can fix a wrong guess in one tap.
31. As a Sender, I want a quick-reply button to delete the Entry I just dropped, so that I can undo a mistaken share.
32. As a Sender, I want to add Tags by replying `#tag` right after a confirmation, so that I can add my own keywords.
33. As a Sender, I want to be told if processing failed and the Entry was saved with only the link and my text, so that I know what to expect when I find it later.

### Searching

34. As a Sender, I want to start a message with `?` or `szukaj` to search, so that searches are never mistaken for Drops.
35. As a Sender, I want to search in natural Polish ("przepis z cukinią", "ten odkurzacz od Joanny"), so that I don't have to learn a query syntax.
36. As a Sender, I want search to match Polish word forms (cukinia/cukinią/cukinii), so that I find things regardless of grammar.
37. As a Sender, I want a Polish search to find English Entries too, so that the language of the original doesn't matter.
38. As a Sender, I want search to understand Category, Sender and time hints ("przepisy od Joanny z zeszłego miesiąca"), so that I can narrow results naturally.
39. As a Sender, I want search to cover titles, Tags, my own Drop text and the Snapshot text, so that anything I remember about an Entry helps find it.
40. As a Sender, I want results as a swipeable carousel of up to 10 cards with image, title, Category, Sender and date, so that I can recognise the right one at a glance.
41. As a Sender, I want an "Otwórz" button on each result that opens the original link, so that I can go back to the source.
42. As a Sender, I want a "Kopia" button that sends the Snapshot (video, images, text) back into the chat, so that I can see the content even after the original is gone.
43. As a Sender, I want a "Więcej" button for the next 10 results, so that I can dig deeper.
44. As a Sender, I want a friendly Polish message when nothing matches, so that I know the search ran.
45. As a Sender, I want a persistent "🔍 Szukaj" menu button if Messenger allows it for our Page, so that searching is discoverable.

### Browsing

46. As a Sender, I want `co nowego` to show the Entries added since I last asked — by either of us — so that I can catch up on what my spouse saved.
47. As a Sender, I want my spouse's Drops visible to me in search and `co nowego`, so that the Library is truly shared.

### Deleting and restoring

48. As a Sender, I want to delete any Entry, including ones my spouse dropped, so that either of us can tidy the shared Library.
49. As a Sender, I want a deleted Entry hidden but restorable for 30 days, so that a mistaken delete isn't permanent.
50. As a Sender, I want a `kosz` command listing recently deleted Entries with a "Przywróć" button, so that I can restore one.

### Language and help

51. As a Sender, I want every bot message in Polish, so that it feels natural to both of us.
52. As a Sender, I want a `pomoc` command explaining dropping, searching, `co nowego` and `kosz`, so that my wife can learn the bot without asking me.

### Operating

53. As the owner, I want the whole service started with Docker Compose behind Caddy on `look.g2labs.pl`, so that deployment is one command.
54. As the owner, I want a deploy script that pulls and rebuilds, so that updating the bot is trivial.
55. As the owner, I want all secrets (Meta app secret, Page token, verify token, Anthropic key, Atlas connection string, allowlist) supplied by environment, so that nothing secret is committed.
56. As the owner, I want the service version to follow SemVer and be visible (e.g. in `pomoc` and logs), so that I know what's deployed.
57. As the owner, I want structured logs of every Drop, processing step and failure, so that I can debug problems on the VPS.

## Implementation Decisions

- **Shape.** One Python service (single process with background workers) in Docker Compose, with Caddy in front. Version 0.1.0, SemVer 2.0.0.
- **Channel boundary.** The core is Channel-agnostic: a Channel adapter turns platform input into a normalized Drop (Sender, Channel, received time, text, links, attachments with any platform-provided preview data) or a normalized user action (search, quick-reply/postback, command), and renders the core's channel-neutral replies (text, quick-reply choices, result cards, media). Messenger is the only adapter in this spec; Telegram later adds another.
- **Messenger adapter.** Webhook verification handshake; `X-Hub-Signature-256` check on every POST; allowlist check (unknown senders dropped without reply); acknowledge Meta immediately and process asynchronously; Send API client for text, quick replies, generic-template carousels, postback buttons, persistent menu (only if 0001 shows it works) and attachment upload for Snapshot media.
- **Message routing.** In order: postbacks/quick replies → action; `?`/`szukaj` prefix → search; `#tag…` within a short window after a confirmation → add Tags to that Entry; exact commands `co nowego`, `kosz`, `pomoc` → command; anything else → Drop.
- **Intake.** Each link in a Drop yields one Entry; a Drop with no links yields one Entry from its images/text. Links are canonicalized (resolve share/redirect URLs, strip tracking parameters) to detect Resends; a Resend appends the Drop to the existing Entry and replies with when/by whom it was first sent.
- **Processing pipeline (background, retryable).** Persist Drop + pending Entry first → build Snapshot → classify → mark ready → send confirmation. Each step is a durable job stored in the database, retried with backoff; a permanently failed extraction still leaves a usable Entry (link + Sender text), and classification waits until the AI is reachable again.
- **Snapshot building.** A Fetcher module behind one interface: platform preview data from the Drop first, then page metadata (Open Graph etc.), readable text extraction, structured recipe extraction for recipe sites, product name/price for shop pages, and video download for reels (capped at 720p). Facebook extraction is best-effort and shaped by 0001's findings; no logged-in scraping of personal accounts.
- **MediaStore.** Interface for put/get/exists with content checksums; first implementation is a directory on a VPS volume. The database stores only references and checksums (ADR-0002).
- **Classifier.** Claude Haiku via the Anthropic API returns Category (fixed list of six), a short Polish title, and Polish Tags, from Snapshot text, Sender text and images (vision for screenshots/photos). Structured output; invalid output is retried.
- **Search.** Haiku turns a Polish query into structured filters (Category, Sender, date range) and keyword sets in Polish and English; these run against MongoDB Atlas Search with Polish and English analyzers over title, Tags, Sender text and Snapshot text, excluding deleted Entries. Results sorted by relevance, then recency; paged in tens.
- **Data model (MongoDB Atlas, ADR-0002).** Senders (name, Channel IDs, last `co nowego` time, last-confirmation context); Drops (Sender, Channel, received time, raw text, links, attachments, raw platform payload); Entries (canonical link, Category, title, Tags, Snapshot text/metadata, media references with checksums, Drop references including Resends, processing state, deleted time); jobs.
- **Deletion.** Delete sets a deleted time; deleted Entries are excluded everywhere except `kosz`; restore clears it. Permanent purge after 30 days is done by Upkeep (0003).
- **Configuration.** All secrets and the Sender allowlist via environment; Atlas Search indexes defined in code/config and applied on deploy.
- **Deployment.** A deploy script on the VPS: pull, rebuild, restart with Compose.

## Testing Decisions

- **One seam: the Messenger webhook endpoint.** Tests post signed webhook payloads (built from real payloads captured in 0001) and assert on (a) the outgoing Send API calls recorded by a fake Meta client and (b) the observable Library state via search/commands. They never assert on internal module calls or document shapes.
- **Fakes only at the system edge:** Meta Send API (recording), Classifier (deterministic Category/title/Tags), Fetcher (canned pages and media), MediaStore (temporary directory). The database is a real local Atlas container (`mongodb-atlas-local`) so Atlas Search and the Polish analyzer behave as in production.
- Background processing runs to completion inside the test (drain the job queue) before asserting.
- Good tests read like the user stories: "a Sender shares a recipe link → receives a confirmation with Category Przepis → `? sernik` returns it as the first card".
- No prior art in the repo yet; these tests establish the pattern for later Channels.

## Out of Scope

- Telegram Channel, web UI, Google Drive media storage.
- Upkeep jobs: integrity/liveness checks, backups, purge of deleted Entries, disk alerts (0003).
- Messenger history import (0004).
- Notifying one Sender about the other's Drops (ADR-0001).
- Embedding-based semantic search.
- Logged-in scraping of Facebook or bridges into personal Messenger accounts.

## Further Notes

- Atlas Search's Polish analyzer is assumed (ADR-0002); verify early. If unavailable, fall back to Haiku-expanded keyword variants.
- Meta requires a fast 200 response to webhooks; all work after persisting the Drop must be asynchronous.
- Replies are within the 24-hour window because they always follow a Sender's message; the confirmation may arrive seconds to minutes later.
- Messenger attachment size limits (~25 MB) may prevent sending some videos back via "Kopia"; reply with a Polish explanation in that case.
