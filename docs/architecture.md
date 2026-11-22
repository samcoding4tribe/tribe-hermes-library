# How it fits together

Three places, three jobs. An agent runs locally, its memory is backed up
privately, and what makes it an agent is published so another machine can start
from it.

```
  your computer                     OneDrive                          remote
  ─────────────                     ────────                          ──────
  ~/.hermes/profiles/ea/  ──daily──▶  samuelkn/Hermes (private)
    soul, skills, config                text/  soul, memories, skills, config
    memories, state.db        ──────▶  db/    session snapshots
    .env (never moves)

  ~/tribe-hermes-library         ──sync───▶  TRIBE Group Tech/Hermes Library  ──push──▶ private repo
    templates, docs, scripts            templates/, profiles/, docs/            tribe-hermes-library
```

## 1. The running agent, local

`~/.hermes` and `~/.hermes/profiles/<name>/`

The agent reads this at the start of every session and writes to it while it
works. A soul, a memory file, skills, config, credentials, and the SQLite
session store. It has to work with no network at all.

`state.db`, `sessions/`, `.env` and `auth.json` never leave this machine. Not to
OneDrive, not to git. Credentials are re-entered after a restore until a vault is
chosen, which is D11.

## 2. The private backup, OneDrive, per person

`OneDrive/TRIBE GROUP - samuelkn/Hermes Backup/`

Daily at 17:00, `scripts/nightly.sh` writes:

| Path | Contents |
|---|---|
| `text/default/`, `text/profiles/<name>/` | Soul, memories, config with credentials stripped, custom skills, cron |
| `db/<date>-<profile>.db` | Consistent SQLite snapshot, ten kept |

This is what restores a machine. It holds memory, so it stays private and per
person, not shared with the team.

## 3. The shared library, OneDrive, per organisation

`OneDrive/TRIBE Group - TRIBE Group Tech/Hermes Library/`

| Path | Contents |
|---|---|
| `templates/role/` | The blank starting point for a new assistant |
| `profiles/<name>/` | Soul, config without credentials, custom skills. No memories |
| `docs/` | Architecture, decisions, the rollout plan |
| `README.md`, `TODO.md` | What this is, and what is outstanding |
| `_manifest.json` | Hash per file, so drift shows up in one line |

Published one way, from a machine. The maintainer or an agent can edit it there,
and that edit comes onto a machine through `pull.sh`, which shows the diff
first. Nothing writes back silently.

## 4. The repo

`~/tribe-hermes-library`, with a private remote once the key is on GitHub.

Versioned copy of the library, plus the scripts. No memories, no databases. It is
what makes a change reviewable, two assistants comparable, and eventually
checkable on push.

## Getting an agent onto a new machine

1. `install-profile.sh <name>` copies a published profile out of the library.
2. Add that machine's credentials to `.env`.
3. The daily job starts backing it up that evening.

A shared server is the same deal, except its profile is started by the gateway
rather than by hand, and its backup goes to the same private folder.

Colliding a profile onto a machine is not solved yet: today it is
`install-profile.sh` plus credentials. Merging a published profile with a local
one that has drifted needs a procedure, which is written down as the next piece
of work.

## What is deliberately not here yet

One git repo per computer. Today history lives in one repo and machine state
lives in OneDrive. Per-machine repos earn their place when several machines run
assistants and each needs its own access boundary or its own checks. Until then
they are admin without a payoff. Recorded as D15.
