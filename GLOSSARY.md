# Take a Look

A private, shared library of links and Internet content (social posts, reels, shopping listings, recipes, articles) that two people send each other, saved so it stays findable and survives the original disappearing.

## Language

### People and intake

**Sender**:
One of the two people allowed to use the Library. Every Drop has exactly one Sender.
_Avoid_: User, member, account

**Channel**:
A route by which Drops arrive in the library, e.g. Messenger, Telegram, or a one-off import of old chat history.
_Avoid_: Source, integration, platform

**Drop**:
A single thing a Sender sends into the library: the raw message with its link(s), attachments and accompanying text, plus who sent it, when, and through which Channel.
_Avoid_: Message, submission, share

**Resend**:
A Drop whose link already belongs to an existing Entry. It attaches to that Entry instead of creating a new one, keeping a record that the item was sent again.
_Avoid_: Duplicate, repost

### The library

**Library**:
The single shared collection of all Entries. Both Senders see and search everything in it, regardless of who sent what or through which conversation.
_Avoid_: Collection, archive, database

**Entry**:
The saved, searchable item built from one or more Drops: the link (if any), its Snapshot, its Category and Tags. A Drop with only an image or only text also becomes an Entry.
_Avoid_: Item, link, bookmark, post

**Snapshot**:
The copy of an Entry's content preserved by the library at save time (text, metadata, images, video), so the Entry stays useful after the original disappears.
_Avoid_: Backup, archive, cache

**Category**:
The single, fixed-list kind of an Entry: Recipe, Product, Social post, Article, Place, or Other.
_Avoid_: Type, kind, folder

**Tag**:
A free-form Polish keyword attached to an Entry to describe it more finely than its Category.
_Avoid_: Label, keyword
