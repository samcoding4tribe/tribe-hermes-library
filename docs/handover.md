# Handover: start here

Written 24 November 2026 for whoever picks this up, human or agent. It says what
exists, where it lives, what was decided and why, and what hurt along the way.

Read this first, then `decisions.md`, then `TODO.md`.

## What this is

A Hermes agent setup for TRIBE Group: profiles that run locally on each machine,
backed up nightly to OneDrive, with everything reusable published to a shared
library and a private GitHub repo. Built on one Mac, intended for an estate that
is mostly Windows.

## Where things live

| Thing | Path |
|---|---|
| Working agent (me) | `~/.hermes`, profile `default` |
| Second profile | `~/.hermes/profiles/admin`, Sam's work admin |
| Third profile | `~/.hermes/profiles/ea`, a manager's assistant (pilot) |
| Repo | `~/tribe-hermes-library`, private remote `tribe-hermes-library` |
| Shared skills | `~/tribe-hermes-library/shared-skills` — seven skills, all procedures that are about the job rather than the person (D17) |
| Org map | `templates/org/people.json`, 26 people, documented in `docs/org-map.md` |
| Per-profile notes | `~/.hermes/profiles/<name>/workspace/`, private, in `docs/profile-notes.md` |
| Shared library | `OneDrive / TRIBE Group Tech / Hermes Library` |
| Machine backups | `OneDrive / TRIBE Group Tech / Hermes Backups / <machine>` |
| Nightly job | Hermes cron `Hermes backup`, 17:00, runs `scripts/hermes_files.py nightly` |

## What works today

- The nightly job backs up three profiles, snapshots their databases, commits,
  pushes and publishes the library. Verified on this machine, including a
  scheduler run at 17:00 on 23 November.
- `scripts/hermes_files.py` is the single implementation: `backup`, `sync`,
  `pull`, `nightly`, on macOS, Windows and Linux.
- Reading and drafting email works through the Outlook web session in the preview
  pane, with no Graph access and no password handling.

## What has not been proven

- Anything on Windows. The Python scripts have only run on this Mac.
- A restore. `install-profile.sh` exists; it has never been used to rebuild a
  profile from the library.
- Teams as a channel. It needs an app registration in the tenant.

## How to run it

```bash
cd ~/tribe-hermes-library
python3 scripts/hermes_files.py backup --dry-run
python3 scripts/hermes_files.py sync
python3 scripts/hermes_files.py pull ea --apply
python3 scripts/hermes_files.py nightly
```

The `.sh` versions still work on the Mac and are no longer developed (D21).

## Decisions worth knowing before you change anything

| | In one line |
|---|---|
| D1 | The running profile stays local. Never run one from a synced folder |
| D4 | Publish one way, pull with a diff. No silent two-way sync |
| D5 | Credentials never leave the machine |
| D10 | Machine backups sit under `Hermes Backups/<machine>`, never in git |
| D14 | Memories are never committed |
| D16 | Every sync pushes; a remote that lags is not a backup |
| D18 | Nothing goes into a profile before it is observed |
| D20 | Who can read a backup is an access question. Still open |
| D22 | The id is the role, the label is the person's. Never rename a folder for a nickname |

## What cost time, so you do not pay twice

- **launchd cannot write to OneDrive.** macOS blocks a launchd job from the
  CloudStorage container with `Operation not permitted`. Run the backup from the
  Hermes scheduler instead (D12).
- **`\n` in a typed email collapses.** Typing a body with newlines into Outlook's
  editor produces one paragraph. Use carriage returns, which produce real
  paragraphs. Verified by reading the saved draft back.
- **A model the provider does not serve fails with 400.** The default profile can
  carry a model its key cannot reach, and the message names the allowed models.
  Check `hermes -p <profile> config get model` before blaming the key.
- **OneDrive folder names differ by platform.** `OneDrive-TribeTravelandEvents` on
  the Mac, `OneDrive - TribeTravelandEvents` on Windows. One `config.env` covers
  both through fallbacks.
- **Folders look private and are not.** Anything in a shared library is readable
  by everyone with access, whatever Hermes is configured to do.

## What changed on 26 November 2026

- **`docs/setup.md` is now the front door** and publishes as the library's `README.md`:
  install on Windows and macOS, `config.env` per platform, then a one-line bootstrap that puts
  the builder profile on the machine and tells it to read the procedure.
- **`templates/builder/`** holds the builder soul with placeholders, so a machine that is not
  this one can be set up by someone who is not Sam (D35).
- **`config/routing.json`** decides which profile id a person gets and which baseline it comes
  from: a manager gets `ea`, everyone else `admin`, and both install `admin` because that is
  the only baseline (D37).
- **`hermes_files.py share`** copies the marked block of each soul into `baseline/soul-rules/`,
  weekly, names scrubbed (D36). `admin` and `ea` still need their two markers.
- **`scripts/`, `config/` and `baseline/` publish with the library**, so a new machine needs
  nothing from git.
- **Decisions D34 to D38** cover the soul boundary, the front door, the marked block, there
  being one baseline, and keeping a personal knowledge base out of published files.
- **Eight threads are numbered in `docs/projects/README.md`**, three of them raised today:
  maintenance and the soul refresh, sync health across the estate, and protecting keys.
- **Thread 0 closed for reading**: the OneDrive fault cleared once the working set was
  downloaded. One PowerPoint remains a stub; the pin policy is still Sam's to decide.

## What to do next

0. Use the org map at setup: show the chart, take the person's id, ask the five
   relationship questions. It is the one piece of shared knowledge that is ready.
1. Run the flow once on a Windows machine.
2. Restore test: install `ea` from the library into a clean home and use it.
3. Settle the access model in D20 before a non-manager gets a profile.
4. Write the collision procedure: how a published profile merges onto a machine
   that already has one.

## The habit that matters

Do not write knowledge into a profile because it seems likely. Watch the work
twice, then write it down. A wrong document is harder to remove than an empty one.
