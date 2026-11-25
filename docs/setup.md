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
| `scripts/` | `hermes_files.py` — `backup`, `sync`, `pull`, `nightly` — plus the older shell versions. One implementation for macOS and Windows (D21) |
| `config.env.example` | The only file that holds paths. Copied to `config.env` and filled per machine |
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

### Both platforms: the scripts come from the library

`scripts/` is published into this library, so a new machine needs nothing from git. Copy
the whole library folder to `~/tribe-hermes-library` (`%USERPROFILE%\tribe-hermes-library`
on Windows); it arrives with `scripts/`, `config.env.example`, the templates and the
published profiles. Then copy `config.env.example` to `config.env` and fill the three paths
for this machine:

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

## 2. Hand the machine to the agent

The installer leaves a default profile that knows nothing about this estate. Do not
hand-edit it. Open Hermes and paste one line:

> You are the builder on this machine, not the assistant. Read `README.md` in the
> `TRIBE Group Tech/Hermes Library` folder on OneDrive, starting at step 2, and follow it.
> Ask me before anything destructive.

That gives it the three things a stock install cannot know: that it is the builder, where
the truth lives, and that it acts only as far as the procedure goes. From there it should
work one step at a time, with your yes on each:

1. Copy `templates/builder/SOUL.md` over its own soul and fill `{{OWNER}}`, `{{ROLE}}`,
   `{{MACHINE}}` and `{{DATE}}`.
2. Copy `config.env.example` to `config.env` and fill the three paths for this machine.
3. Run the proof query and the backup dry run.
4. Offer the nightly job, and wait for your yes before scheduling it.

The label is Hermes. The folder stays `default`, because the label is presentation and the
id is the role (D22).

If it cannot find the folder, paste the full path instead: the value of
`HERMES_SYNC_ONEDRIVE` in the section above is exactly that path.

Doing it by hand is the fallback, not the plan — `templates/builder/README.md`.

## 3. First run: the baseline profile, personalised by the interview

The builder's one job before it becomes a maintainer is to turn this machine into a working
assistant for its owner, by personalising a baseline rather than inventing a persona.

1. **Choose the baseline.** `admin` for anyone, `ea` for a manager. Those are the two
   baselines; there is no third to choose from. The profile id is the baseline id, never
   the assistant's name and never the person's (D22).
2. **Install it from this library.** `profiles/admin/` or `profiles/ea/` into
   `~/.hermes/profiles/<id>`. Set the model explicitly — a clone inherits a broken one —
   then prove it answers before anything else happens.
3. **Run the interview in that profile**, not about it.
   `docs/profiles/interview/onboarding-interview.md`, blocks 0 to 8, as a conversation held
   inside the assistant. Block 0 asks what the person wants their assistant called, which is
   the one answer that is theirs and not ours (D31).
4. **Wire the access.** Mail and calendar first, through the browser route in the
   `microsoft-365-web` skill. A profile that cannot see the inbox has nothing to do.
5. **Write the four artefacts** the interview produces: the name, `workspace/context.md`,
   the procedures the person actually described in `workspace/procedures.md`, and their
   brief preferences. Nothing is written ahead of the conversation, and nothing is copied in
   from another person's profile.
6. **Hand the person over to their assistant**, and say plainly how to reach it: the
   wrapper command (`<profile-id> chat`), the profile list in the desktop app, or the channel
   it was given. Then run one real task together and read the result back.
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
