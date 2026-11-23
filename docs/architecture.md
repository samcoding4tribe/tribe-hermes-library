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

`OneDrive/TRIBE Group Tech/Hermes Backups/<machine>/`

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

## 3a. Two assistants, one skill set

`admin` is Sam's own work admin assistant. `ea` is the executive assistant pilot
for a manager. They are separate profiles with separate memories and separate
backups, and they read the same skills from `~/tribe-hermes-library/shared-skills`
through `skills.external_dirs`.

That is the crossover: a procedure written once serves both, while facts stay
where they belong. A skill may say "ask who signs off"; it may not say who that
is. Personal detail never enters a work profile, and a manager's context never
lands in Sam's memory.

## 3b. Names: the id stays, the label is theirs

Two different things carry a name.

**The profile id** is the folder: `assistant-kate`, `office-manager`. Skills,
memory, backups and library copies all key on it, so it stays stable and
role-based.

**The label** is what a person sees: the roster title in Bot Mode, the messaging
bot's own name, and optionally the first line of their soul, "You are Jarvis".

Someone who wants to call their assistant Jarvis changes the label and nothing
else. Baseline updates from the library still reach them, because the id and the
shared skills never moved.

`hermes profile rename` changes the id, which is a migration: paths in the
library, this repo and the backup folder all follow it. Use it when the role
changes, not when the nickname does.

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

## Who can read what

Folder visibility is not a security control. If a person can open the library in
OneDrive, they can read whatever sits inside it, including a backup that holds
memory. Three things follow:

- Permissions decide who can read, so a folder shared with managers is readable
  by managers no matter what Hermes is configured to do.
- The agent inherits the access of the account it runs under. A stricter profile
  setting changes what it is willing to do, not what the operating system lets it
  read.
- Anything written into a shared folder should be assumed readable by everyone
  who can open that folder.

The open question, and the two ways out, are in D20.

## What is deliberately not here yet

One git repo per computer. Today history lives in one repo and machine state
lives in OneDrive. Per-machine repos earn their place when several machines run
assistants and each needs its own access boundary or its own checks. Until then
they are admin without a payoff. Recorded as D15.
