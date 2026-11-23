# Hermes agents

Portable copies of the Hermes profiles used in this organisation, plus the
scripts that move them around. The running copies live in `~/.hermes/profiles/`
on each machine; this repo is the paper trail, and never holds memories or
databases.

## What is here

```
profiles/<name>/     SOUL.md, config.yaml (no secrets), custom skills, cron
templates/role/      the blank starting point for a new assistant
scripts/sync.sh      profile -> repo -> Hermes Library, then commit
scripts/backup.sh    soul, memories, config, cron -> private OneDrive folder
scripts/nightly.sh   runs backup, then sync, once a day
scripts/pull.sh      library edits back onto a machine, diff first
scripts/install-profile.sh   library or repo -> a machine
docs/course.md      seven lessons for a first-time user
docs/agent-profiles.md  what we know and what must be learned before a profile
docs/onboarding.md   set up a new machine, step by step
docs/architecture.md where each copy lives and why
docs/decisions.md    one entry per choice, with the reason
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
- Memories never enter this repo. They go to the private backup only.
- The shared folder is `TRIBE Group Tech/Hermes Library`. The private one is
  `TRIBE GROUP - samuelkn/Hermes`.
- OneDrive holds a published copy for people and machines that do not use
  git. It is one-way: repo to OneDrive, never back.
