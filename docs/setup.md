# Start here: setting up Hermes on a new machine

The shared reference for the assistants Hermes runs at TRIBE Group, and the front door
for setting one up. Readable by the team. Written from one machine at a time.

Start here if you are setting Hermes up on a new computer. If you are looking for how a
decision was made, go to `docs/decisions.md`. If you are picking up unfinished work, go to
`docs/projects/README.md`.

## What is here

| Folder | Contents |
|---|---|
| `templates/builder/` | The soul for the Hermes profile itself, with placeholders. Used once, on a new machine, before any assistant exists |
| `templates/role/` | Blank starting point for a role assistant: soul with placeholders, config, instructions |
| `profiles/<id>/` | Published copy of each assistant: soul, config without credentials, custom skills |
| `shared-skills/` | Procedures the assistants share, loaded by reference so one edit serves all |
| `docs/` | Architecture, decisions, the rollout plan, the setup interview, the open threads |
| `apps/` | Small tools that read the shared data, such as the team map |
| `_manifest.json` | A hash per file. If a local copy differs, this shows it in one line |

## What is deliberately absent

Memories, working notes and session databases. They hold what a particular person said
and did, so they stay in that machine's private backup under
`TRIBE Group Tech/Hermes Backups/<machine>`, never here. Credentials are absent too:
every machine holds its own `.env`.

---

## 1. Set up Hermes on a new machine

You need: the machine, an account with install rights, OneDrive signed in, and either an
API key for the model provider or a Nous Portal login. Note the machine's asset name — it
becomes the backup folder name.

### Windows

In PowerShell:

```
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

Add `-IncludeDesktop` to build the desktop app and create shortcuts. Hermes data lives in
`%LOCALAPPDATA%\hermes`. Then run `hermes setup`, and `hermes setup --portal` if you are
using Portal, which covers the model and most tool keys in one login.

### macOS

```
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Hermes data lives in `~/.hermes`. Then run `hermes setup`.

### Both platforms: point the scripts at this machine

Clone or copy the repo to `~/tribe-hermes-library` (`%USERPROFILE%\tribe-hermes-library`
on Windows), then edit the three paths at the top of `config.env`:

```
# macOS
HERMES_SYNC_REPO="$HOME/tribe-hermes-library"
HERMES_SYNC_ONEDRIVE="$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/TRIBE GROUP - TRIBE Group Tech/Hermes Library"
HERMES_BACKUP_ONEDRIVE="$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/TRIBE GROUP - TRIBE Group Tech/Hermes Backups/<machine asset name>"

# Windows
HERMES_SYNC_REPO="%USERPROFILE%\\tribe-hermes-library"
HERMES_SYNC_ONEDRIVE="%USERPROFILE%\\OneDrive - TribeTravelandEvents\\TRIBE GROUP - TRIBE Group Tech\\Hermes Library"
HERMES_BACKUP_ONEDRIVE="%USERPROFILE%\\OneDrive - TribeTravelandEvents\\TRIBE GROUP - TRIBE Group Tech\\Hermes Backups\\<machine asset name>"
```

Nothing else in the repo holds a path (D21, one implementation).

### Prove it runs before you go further

```
hermes chat -q "One line: who are you and what is your first rule?"
python3 scripts/hermes_files.py backup --dry-run
```

Windows has no `python3` alias by default, so use `python scripts\hermes_files.py`.

### Schedule the nightly job

`python3 scripts/hermes_files.py nightly` backs up, commits, pushes and publishes. In
Hermes, schedule it at 17:00 as a `no_agent` job pointing at a two-line wrapper in
`~/.hermes/scripts/`. On macOS it must be the Hermes scheduler, not launchd, because
launchd cannot write into a OneDrive folder (D12). On Windows, Task Scheduler also works
if the gateway is not always running.

---

## 2. The first profile is Hermes

Before any assistant exists, the machine needs the profile that builds them. On this
estate that profile is called **Hermes** and it is the default profile the installer
creates.

1. Replace the default profile's soul with `templates/builder/SOUL.md`.
2. Fill its placeholders: owner name, role, machine asset name, date.
3. Set the label to Hermes. The folder stays `default`; the label is what people see
   (D22).
4. Start it and confirm in one line that it knows its job.

Full steps: `templates/builder/README.md`.

## 3. First run: Hermes builds the assistant

The Hermes profile has one job before it becomes a maintainer: turn this machine into a
working assistant for its owner. It does that by running the setup interview, not by
inventing a persona.

1. **Interview.** `docs/profiles/interview/onboarding-interview.md`, blocks 0 to 8, as a
   conversation. Block 0 asks what the person wants their assistant called, because that
   is the one answer that is theirs and not ours (D31).
2. **Create the profile.** A role-based id such as `admin`, `ea` or `assistant-coordinator`
   — never the assistant's name and never the person's (D22). Soul from `templates/role/`,
   with the placeholders filled from the interview answers and nothing else.
3. **Set the model explicitly.** A clone inherits the source model, including a broken
   one. Set it, then prove it answers before handing it over.
4. **Wire the access.** Mail and calendar first, through the browser route in the
   `microsoft-365-web` skill. A profile that cannot see the inbox has nothing to do.
5. **Write the four artefacts** the interview produces: the name, `workspace/context.md`,
   the procedures the person actually described in `workspace/procedures.md`, and their
   brief preferences. Nothing is written ahead of the conversation.
6. **Hand the person over to their assistant**, and say plainly how to reach it: the
   wrapper command (`<profile-id> chat`), the profile list in the desktop app, or the
   channel it was given. Then run one real task together and read the result back.
7. **Book the review** two weeks out: one question, which part is not earning its place.

Hermes stays as the maintainer profile on that machine, and stays out of the assistant's
job. Both live on the same computer with separate memories, backups and skills.

## 4. Keeping machines in step

```
python3 scripts/hermes_files.py pull <profile-id>    # show the diff
python3 scripts/hermes_files.py pull <profile-id> --apply
python3 scripts/hermes_files.py sync                # publish, commit, push
```

Publish one way, pull with a diff (D4). Souls and skills travel both ways; memories never
travel (D14). One writer at a time in this library: two editors in one file produce a
"conflicted copy" nobody reads.

## 5. The other procedures

| When | Read |
|---|---|
| Setting up a profile, start here | `docs/profiles/interview/README.md` |
| Running the set-up conversation | `docs/profiles/interview/onboarding-interview.md` |
| The second conversation, after a real brief | `docs/profiles/interview/brief-interview.md` |
| How much can load into every turn | `docs/profiles/interview/context-budget.md` |
| The boundary between building and doing | `docs/profiles/interview/FOR-THE-BUILDER-PROFILE.md` |
| Who is who, and how the chart is drawn | `docs/org-map.md` |
| A profile's own working notes | `docs/profile-notes.md` |
| Why it is built this way | `docs/architecture.md`, `docs/decisions.md` |
| Picking up unfinished work | `docs/projects/README.md` |

## What is not proven yet

Stated plainly so nobody assumes otherwise. As at 26 November 2026: the Windows flow has
never been run end to end; no profile has been restored from this library onto a clean
machine; and Teams has never been set up as a channel. Each is a to-do in `docs/TODO.md`,
not a feature.

## The rule that keeps this simple

One writer at a time. This folder is a published copy, not a live agent. The agent runs
from a local profile on its own machine.
