# 0013: Media preserved and returned with Kopia

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0008, 0010

## What to build

Reel videos (capped at 720p) and content images are downloaded into the MediaStore with checksums when an Entry is saved. Each search result gets a "Kopia" button that sends the Snapshot — video, images, text — back into the chat, so content can be seen after the original disappears.

## Acceptance criteria

- [ ] MediaStore interface (put/get/exists, checksum) with a VPS-volume implementation
- [ ] Video download for reels via the Fetcher, capped at 720p; images downloaded for posts, listings, recipes
- [ ] Database stores only media references and checksums
- [ ] "Kopia" sends the stored media and text back; over-limit files get a Polish explanation
- [ ] Seam tests: reel Drop → media stored → "Kopia" postback sends it back; oversized file path
