# Decisions

One entry per choice, with the reason. Newest last. If a decision is reversed,
add a new entry that says so rather than editing history.

---

## D1. The running profile stays local

**Decision.** Profiles run from `~/.hermes/profiles/`. Never from a synced folder.

**Why.** `state.db` is SQLite and is written continuously while the gateway runs.
Cloud sync tools read and rewrite those files underneath an open process, which
is how session stores get corrupted. A second reason is availability: an agent
that needs a cloud folder mounted before it can answer is not an agent you can
rely on.

---

## D2. Two knowledge bases, different jobs

**Decision.** Local home for running. OneDrive library for templates, published
copies and documentation.

**Why.** The local home changes constantly and must work offline. The library
changes rarely and has to be reachable by people who will never open a terminal.
Mixing them means every runtime write becomes a sync event.

---

## D3. The repo is a versioned mirror, not the runtime

**Decision.** `~/tribe-hermes-library` holds copies of souls, memories, custom skills,
templates and docs, committed on each sync. The agent never reads from it.

**Why.** History is what lets you see what changed when an assistant starts
behaving differently. A remote adds an off-site copy. Neither needs to be on the
path the agent uses to answer a question.

---

## D4. Publish one way, pull with a diff

**Decision.** `sync.sh` copies local to repo and repo to OneDrive. Changes made
in OneDrive are pulled back by `pull.sh`, which shows the diff and only applies
with an explicit flag. Souls, memories and skills travel both ways; `config.yaml`
is publish-only, because the library copy has credentials stripped.

**Why.** Two-way automatic sync silently overwrites whichever side it read
second. A visible diff costs one command and prevents losing an edit someone
made deliberately.

---

## D5. Secrets never leave the machine

**Decision.** `.env` and `auth.json` are excluded everywhere. `config.yaml` is
copied with credential lines removed, keeping only `${VAR}` references.

**Why.** The OneDrive library is readable by more people than the machine it came
from. A profile that cannot start without its own key is also a profile whose key
can be rotated without touching twenty other files.

---

## D6. Souls are prose, skills are code

**Decision.** Souls, memories and config can be edited in the library. Skills
come through the repo and get a run before they are trusted.

**Why.** A soul is read by a person and judged in a minute. A skill contains
commands and file paths, and a wrong one fails at the worst moment.

---

## D7. One writer at a time

**Decision.** Only one person or agent edits the library at once.

**Why.** OneDrive resolves simultaneous edits by creating a conflicted copy, and
nobody reads those. A manifest with a hash per file makes drift visible in a
single line.

---

## D8. New machines install from OneDrive by default

**Decision.** `install-profile.sh <name>` reads the OneDrive library unless
`--from-repo` is passed.

**Why.** Most people setting up a device already have OneDrive through the org
account and no git identity. The repo stays the maintainer's tool.

---

## D9. Checks on push, once a remote exists

**Decision.** Later: a pipeline that scans for secrets, checks placeholders are
filled, parses every skill, and installs a profile into a clean home.

**Why.** Versioning records mistakes. Checks prevent them from reaching other
machines.

---

## D10. Private backup sits apart from the shared library

**Decision.** Each machine backs up into the owner's own OneDrive folder.
Souls, memories, configs without credentials, custom skills and database
snapshots go there. The shared TRIBE Group Tech library holds templates and
published copies with memories stripped.

**Why.** Memories and session databases contain personal and client detail.
The shared library is readable by the team, so it carries what is safe to read:
how an assistant is built. What a particular executive said stays with that
machine's owner. Tenant admins can read OneDrive either way, which is why
credentials go into an encrypted archive and never as plain files.

---

## D11. Credentials stay out of the backup until the storage question is settled

**Status.** Open. Decided for now: excluded.

**Decision.** `.env` and `auth.json` are not copied by `backup.sh`. They are
re-entered by hand after a restore until a secure store is agreed.

**Why.** In plain form they would sit in a synced folder that tenant admins can
read. The three candidates are a vault Hermes reads from, an age-encrypted
archive with a passphrase held in the password manager, or manual re-entry. That
choice belongs in a session about security, not in a backup script.

**Revisit when.** A bot token or a shared key exists, or the pilot moves beyond
this machine.

---

## D12. Backups run from the Hermes scheduler, not launchd

**Decision.** A `no_agent` Hermes job fires `scripts/nightly.sh` at 17:00 daily.
A launchd agent was tried and removed.

**Why.** macOS protects the OneDrive container: a launchd process gets
"Operation not permitted" on rsync into `CloudStorage`, while the gateway, which
the user already approved, can write there. The job runs without a model, so it
costs nothing and has no reasoning to go wrong. Its stdout is empty on a quiet
day and a failure produces an alert.

---

## D13. The shared folder is called Hermes Library and is published to

**Decision.** `OneDrive/TRIBE Group - TRIBE Group Tech/Hermes Library`. Written
by a machine, read by people, edited only by the maintainer or an agent.

**Why.** "Library" says what it is: a shelf of templates and published copies,
not a live agent and not a backup. The name also keeps it distinct from the
private `Hermes` folder in a person's own OneDrive, which is a backup and looks
nothing like it.

---

## D14. Memories are never committed to git

**Decision.** `sync.sh` leaves `memories/` out of the repo, and removes it if an
older commit put it there.

**Why.** The remote is for skills, souls and configs, which describe how an
assistant works. Memories describe what a person said, and those belong in the
private backup. A remote repository has more readers than a folder does, and
history keeps what it is given.

---

## D15. One repo, not one per computer

**Decision.** No per-machine repositories for now. Machine state lives in the
private OneDrive backup; the single repo holds the baseline plus published
profiles.

**Why.** A repo per machine means a remote, a key and a tidy-up per machine, for
history nobody reads while there is one machine. The moment several machines run
assistants and need separate access or separate checks, that changes: either
revisit per-machine repos, or put a folder per machine inside the existing one.

---

## D16. Every sync pushes

**Decision.** `sync.sh` commits, then pushes to `origin` when a remote exists.
A failed push reports but does not stop the run.

**Why.** A remote that lags behind is not a backup, it is a snapshot of whenever
someone remembered to push. The daily job already calls the same script, so the
remote stays current without a second habit to remember.

---

## D17. Shared skills are the crossover, never shared memory

**Decision.** `admin` and `ea` load skills from one folder through
`skills.external_dirs`. Their memories stay separate, and no personal fact is
copied into a work profile.

**Why.** What should be identical across assistants is the procedure. What should
never be identical is what a person said. Sharing a folder of skills gives the
first without the second, and it keeps the maintenance in one place when a
procedure improves.

---

## D18. A backup is tested or it is a guess

**Decision.** Once a quarter, restore one profile and one database snapshot
onto a clean machine and use it for an hour.

**Why.** Copies fail in ways that only show up on restore: missing directories,
paths that only existed on the original machine, a soul that references a skill
nobody published.

**First run.** Recorded as a to-do: install `ea` from the shared library into a
clean home directory and use it for an hour.
