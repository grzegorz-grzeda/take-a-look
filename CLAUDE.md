# take-a-look

## Versioning

The project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html), starting at `0.1.0`. Keep one source of truth for the version (the Python package metadata once it exists) and tag releases as `vX.Y.Z`.

## Agent skills

### Issue tracker

Specs live in `docs/specs/NNNN-<slug>.md`, issues in `docs/issues/NNNN-<slug>.md` (four-digit global numbering, each issue links its spec, implemented issues are renamed `done-NNNN-<slug>.md`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
