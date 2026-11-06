# 0007: Classify Entries with Haiku

Spec: [0002 Library core over Messenger](../specs/0002-library-core-over-messenger.md)
Status: ready-for-agent
Blocked by: 0005

## What to build

Every Entry gets a Category (Recipe, Product, Social post, Article, Place, Other), a short Polish title and Polish Tags from Claude Haiku, shown in the confirmation: "✅ Przepis · Sernik baskijski · #deser #bezglutenowe". English content still gets Polish Tags. When the AI is unavailable or out of credit, the Entry is saved and classified later.

## Acceptance criteria

- [ ] Classifier module calls Haiku with structured output; invalid output retried
- [ ] Inputs: Snapshot text/metadata and the Sender's text
- [ ] Confirmation shows Category, title and Tags in Polish
- [ ] AI failure → Entry saved, confirmation says classification will follow; retried with backoff and confirmed when done
- [ ] Seam tests with the fake Classifier, including the unavailable-then-recovered path
