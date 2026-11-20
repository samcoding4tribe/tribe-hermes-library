# Hermes agents

Portable copies of the Hermes profiles used in this organisation, plus the
scripts that move them around. The running copies live in `~/.hermes/profiles/`
on each machine; this repo is the paper trail.

## What is here

```
profiles/<name>/     SOUL.md, config.yaml (no secrets), memories/, custom skills, cron
templates/role/      the blank starting point for a new assistant
scripts/sync.sh      profile -> repo -> OneDrive, then commit
scripts/install-profile.sh   OneDrive or repo -> a machine
docs/rollout.md      the working plan, edited in chat
```

## Everyday use

```bash
./scripts/sync.sh --dry-run     # what changed
./scripts/sync.sh               # copy, commit, publish to OneDrive
./scripts/sync.sh ea            # one profile only
./scripts/pull.sh ea            # see edits made in OneDrive
./scripts/pull.sh ea --apply    # take them into the local profile
./scripts/install-profile.sh ea # put it on another machine
```

Two knowledge bases, and why: [docs/architecture.md](docs/architecture.md).
The choices behind it, one per entry: [docs/decisions.md](docs/decisions.md).

## Rules

- Credentials never enter this repo. `sync.sh` strips key lines from
  `config.yaml`, and `.env` plus `auth.json` are ignored by git.
- Skills that ship with Hermes are not copied. Only the ones written here.
- The live profile stays in `~/.hermes/profiles/`. Never run one from a
  synced folder; SQLite and cloud sync do not mix.
- OneDrive holds a published copy for people and machines that do not use
  git. It is one-way: repo to OneDrive, never back.
