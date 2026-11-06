# 0012: Image and text-only Drops

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0007

## What to build

A screenshot, a photo or a text-only message (e.g. "kupić ten mop z Lidla") becomes an Entry. Images are saved and Haiku reads them (vision) to assign Category, title and Tags, so image Entries are as findable as links.

## Acceptance criteria

- [ ] Image attachments saved to the MediaStore with checksums
- [ ] Classifier accepts images; screenshots of products/recipes get the right Category and Tags
- [ ] Text-only Drops become Entries classified from their text
- [ ] Such Entries appear in search and the carousel (image Entries show their image)
- [ ] Seam tests for screenshot, photo and text-only Drops
