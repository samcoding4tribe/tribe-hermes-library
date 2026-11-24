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

**Superseded 23 November 2026.** At Sam's request, machine backups moved to
`TRIBE Group Tech/Hermes Backups/<machine>/`, inside the Tech library. The
separation now depends on folder permissions rather than on a separate library.
See D19.

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
`skills.external_dirs`. Their memories stay separate, and no one person's detail
is copied into another person's profile.

**Why.** What should be identical across assistants is the procedure. What should
never be identical is what a person said. Sharing a folder of skills gives the
first without the second, and it keeps the maintenance in one place when a
procedure improves.

---

## D18. Nothing is written into a profile before it is observed

**Decision.** Souls start from a template with placeholders. Skills start from a
workflow watched twice. No skill name, schedule or permission is invented ahead
of the work it serves, and any assumption that does appear is marked as one.

**Why.** Assumed knowledge is harder to remove than absent knowledge, because it
reads like fact in every later session and quietly shapes what the agent does.
A corrected document leaves the original claim behind; an empty field invites the
right answer. The cost of waiting is one conversation. The cost of guessing is a
knowledge base that argues with reality.

---

## D19. Backups sit under Hermes Backups, and access is enforced there

**Decision.** One folder per machine: `TRIBE Group Tech/Hermes Backups/<machine>/`,
holding the text mirror and database snapshots. Never in git, never in the shared
library.

**Why.** Grouping by machine under one heading makes the estate legible: who runs
what, where. The cost is that these folders now live in the library the team can
see, so the privacy of memory depends on permissions instead of on a separate
location. That folder must be limited to the machine's owner and one IT person.
If permissions cannot be limited that way, move backups back out of the library.

---

## D20. Who can read a backup is an access question, not a folder question

**Status.** Open. To settle before the first deployment to someone who is not a
manager.

**Problem.** `Hermes Backups/<machine>/` sits in a library that managers can
already read, and the Tech library is likely the same. Moving the folder does not
change who can read it. Meanwhile the agent needs access to those files to run,
and the person whose profile it is may not need it at all.

**The two levers.**

1. **A service identity.** Hermes runs under an account that can read the backup
   library, and users never get that access. On a Mac this means a separate macOS
   user or a server, because the app inherits whatever the logged-in person can
   read. Thin clients, one runtime.
2. **Encryption.** Backups are written encrypted, so folder visibility stops
   mattering. Keys stay with the machine and the owner. Works with per-machine
   runtimes, and is the only option that survives a folder shared by accident.

**What I would do.** Per-machine runtimes for people who need their own memory,
with backups encrypted at rest. A service identity when several assistants share
one host. Both can be true at once.

**Trigger for a decision.** The first profile deployed to someone without
management permissions.

---

## D21. One implementation in Python, not two

**Decision.** `scripts/hermes_files.py` carries backup, sync, pull and nightly for
every platform. The bash scripts stay in the repo for now and are not developed
further.

**Why.** Most of the estate is Windows, and bash with rsync and sqlite3 does not
exist there. A PowerShell copy would be a second implementation to keep in step,
and two implementations drift until one is wrong in a way nobody notices. Python
ships with Hermes on every platform and carries sqlite in its standard library.

**Cost.** The Mac's scheduled job now runs the same file Windows will run, so a
fault shows up here first rather than on someone else's machine.

---

## D22. The id is the role, the name is the person's

**Decision.** Profiles are named for the role (`assistant-kate`,
`office-manager`) and never renamed for a nickname. What a person sees is a
label: roster title, messaging bot name, and optionally the first line of the
soul. A rename of the id is a migration and is treated as one.

**Why.** Everything downstream keys on the folder name: the library copy, the
backup directory, the scripts, this documentation. A nickname that becomes an id
turns a cosmetic wish into a path change across four systems. Separating the two
lets people personalise what they see while the baseline stays updatable, which
is the whole point of the shared library.

---

## D23. The org chart is edited by the people it describes

**Decision.** Leon, Kelly, Jodie and Vanessa may change `people.json`, and the
three others read it. Changes arrive through the library folder, and Sam pulls
them into the repo, where `render.py` validates the graph before the chart is
regenerated.

**Why.** An org chart maintained by one person goes stale between conversations,
and the cost of that is a new assistant asking its user to describe a company the
business already knows. Editing by the people named on the chart keeps it current,
and a validation step keeps it correct.

**Constraint.** Git has no folder-level permissions, so a manager with write
access to the repo can change anything. The library folder is where edit rights
belong; the repo stays the maintainer's.

---

## D24. A backup is tested or it is a guess

**Decision.** Once a quarter, restore one profile and one database snapshot
onto a clean machine and use it for an hour.

**Why.** Copies fail in ways that only show up on restore: missing directories,
paths that only existed on the original machine, a soul that references a skill
nobody published.

**First run.** Recorded as a to-do: install `ea` from the shared library into a
clean home directory and use it for an hour.

---

## D25. The weekly note is produced at 11am on Monday, after the meeting

**Decision.** The whereabouts note is generated at about 11am each Monday, not
overnight and not before the breakfast meeting. The half hour after the meeting
is the window for small corrections: a location that changed, a person who
joined the roster that morning.

**Why.** The Monday breakfast meeting is where the week is agreed. A note built
before it is stale by the time it is read, and the corrections it needs are
exactly the ones discussed at the table.

**How.** The period folder is generated on the Monday and left for a person to
review and send. Generation is a draft, never a send: the note goes to everyone
in the org, so a human decides the moment it leaves.

**Open.** Whether the generator runs on a schedule or on request is not yet
decided. Scheduling it would only create the folder; sending stays manual.

---

## D26. The weekly note carries the map inline and a link to the site

**Decision.** Each week's map is embedded in the email so it renders in any
client, and the same image is published to the TRIBE GROUP site with a link in
the note for the full size.

**Why.** A link on its own turns a glance into a click, and Outlook blocks remote
images by default, so an image URL alone can arrive as a grey box. An inline copy
is reliable; the published copy is what gets opened on a phone, printed, or put
on a screen in the office.

**Where.** `Shared Documents/TRIBE Group Tech/Whereabouts/<monday>/` on
`tribemanagement.sharepoint.com`, written through the synced library and addressed
directly, so the site copy does not depend on a share link being generated by hand.

**Unverified.** Who can read that folder. The site-level permission list could not
be read from this machine (the API refuses without site-admin rights). Sam believes
everyone has access, because everyone will eventually back up there. Before the
first send, ask one person outside the Tech group to open a link. If it is
restricted, the fallback is a `Whereabouts` folder with its own permissions granted
to everyone except external users.
