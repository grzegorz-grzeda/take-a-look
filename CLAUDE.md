# take-a-look

## Versioning

The project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html), starting at `0.1.0`. Keep one source of truth for the version (the Python package metadata once it exists) and tag releases as `vX.Y.Z`.

## Public repository: privacy rules

This repo is public (a showcase). The Library holds two real people's private data, so:

- Never commit secrets: tokens, app secrets, API keys, connection strings. Only an example env file with empty values.
- Never commit real Messenger/Meta IDs (PSIDs, Page/app IDs), real names, real chat content, raw webhook logs, Meta data exports, media, or database dumps.
- Test fixtures are synthetic, or real payloads fully anonymised before they enter the repo: every ID, name, URL, timestamp and text replaced with invented values. In docs and fixtures the Senders are "Grzegorz" and "Joanna".
- Runtime data (payload logs, media, exports, backups) lives on mounted volumes outside the repo and is git-ignored.

## Agent skills

### Issue tracker

Specs live in `docs/specs/NNNN-<slug>.md`, issues in `docs/issues/NNNN-<slug>.md` (four-digit global numbering, each issue links its spec, implemented issues are renamed `done-NNNN-<slug>.md`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
