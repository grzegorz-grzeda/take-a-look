# Issue tracker: Local Markdown

Specs and issues for this repo live as markdown files under `docs/`, committed with the code.

## Conventions

### Specs

- Every spec is one file in `docs/specs/`, named `NNNN-<slug>.md`: a four-digit, zero-padded number, then a kebab-case slug (e.g. `docs/specs/0001-messenger-webhook-prototype.md`).
- Numbers are global and sequential across all specs: scan `docs/specs/` for the highest number and add one. Never reuse or renumber.

### Issues

- Every issue is one file in `docs/issues/`, named `NNNN-<slug>.md`, with the same four-digit numbering scheme as specs (e.g. `docs/issues/0007-save-link-drop.md`). Never a single combined tickets file.
- Issue numbers are global and sequential across all issues, independent of spec numbers: scan `docs/issues/` (including `done-` files) for the highest number and add one. Never reuse or renumber.
- Every issue created from a spec references it on a line near the top: `Spec: [0001 Messenger webhook prototype](../specs/0001-messenger-webhook-prototype.md)`.
- Triage state is recorded as a `Status:` line near the top (see `triage-labels.md` for the role strings).
- Comments and conversation history append to the bottom of the file under a `## Comments` heading.
- **When an issue is implemented**, set `Status: done` and rename the file with a `done-` prefix, keeping its number and slug: `git mv docs/issues/0007-save-link-drop.md docs/issues/done-0007-save-link-drop.md`. Update links that point at it.

### Referring to specs and issues

Refer to them by number (`spec 0001`, `issue 0007`). To find a file by number, match `NNNN-*.md` and `done-NNNN-*.md`.

## When a skill says "publish to the issue tracker"

A spec goes to `docs/specs/NNNN-<slug>.md`; implementation tickets go to `docs/issues/NNNN-<slug>.md`, each referencing its spec.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path, or look it up by number as above.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a spec file with one **child** issue per ticket.

- **Map**: `docs/specs/NNNN-<effort>-map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `docs/issues/NNNN-<slug>.md`, numbered like any issue, with a `Spec:` line linking the map and the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NNNN, NNNN` line near the top. A ticket is unblocked when every issue it lists is `resolved` or `done`.
- **Frontier**: scan `docs/issues/` for the map's children that are open, unblocked, and unclaimed; lowest number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, rename with the `done-` prefix, then append a context pointer (gist + link) to the map's Decisions-so-far.
