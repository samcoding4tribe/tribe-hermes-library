# Two knowledge bases

Hermes on a machine reads from its own home directory. Everything that has to
work offline, and everything that changes while the agent runs, lives there.
The shared library in OneDrive is a separate thing: templates to start from, and
readable copies of what each agent is, for people and for recovery.

They are deliberately not the same folder.

## 1. Local, per machine, always available

`~/.hermes` and `~/.hermes/profiles/<name>/`

| What | Why it is local |
|---|---|
| `SOUL.md` | Read at the start of every session; a network hiccup must not change who the agent is |
| `memories/` | USER.md and MEMORY.md, read at every start, written during work |
| `skills/` | Loaded on demand during work |
| `config.yaml` | Model, approvals, platforms |
| `.env`, `auth.json` | Credentials. Never leave the machine |
| `state.db`, `sessions/` | SQLite written constantly. Sync tools corrupt it |
| `cron/` | Schedules the gateway runs |

This is the running copy. Nothing else is allowed to be the running copy.

## 2. Shared library, OneDrive

`OneDrive .../Hermes/`

| What | Why it is shared |
|---|---|
| `templates/role/` | The blank starting point for a new assistant |
| `profiles/<name>/` | Published copies of souls, memories and custom skills, for reading, recovery and setup |
| `docs/` | Architecture, decisions, the rollout plan |
| `_manifest.json` | Hash and timestamp per file, so drift is visible |

The library is one-way out of a machine by default. A person or another agent
can edit a soul there, and that edit comes back through a pull that shows the
diff before applying it. Nothing writes back silently.

## 3. Repo, local git, remote when it exists

`~/hermes-agents`

Versioned mirror of the library, plus the scripts that move files around. A
local repo gives history and a second copy. A remote gives an off-site backup
and, later, a place to run checks on push.

## Flow

```
local profile  --sync-->  repo (commit)  --publish-->  OneDrive library
      ^                                                      |
      |______________________ pull, diff first ______________|
```

New device: OneDrive is normally already there through the org account, so
`install-profile.sh <name>` is the whole setup. Devices set up by someone
comfortable with git can use the repo with one flag.

## The line that does not move

`state.db`, `sessions/`, `.env` and `auth.json` are never copied anywhere, in
either direction. If a backup needs credentials to work, the credentials are
added on that machine, from the vault, by the person who owns it.
