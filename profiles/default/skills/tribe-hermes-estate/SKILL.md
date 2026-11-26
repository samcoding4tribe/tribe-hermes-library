---
name: tribe-hermes-estate
description: "TRIBE Hermes estate: repo, profiles, rollout, vault notes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [tribe, hermes, profiles, rollout, decisions, oneDrive]
    related_skills: [concurrent-project-checkpoints, hermes-agent]
---

# Working on the TRIBE Hermes estate

Builder work on Sam's work machine: the repo, the profiles, the shared library, the
scheduled jobs and the rollout to colleagues. Not the admin profile's day job.

## When to Use

- Anything touching `~/tribe-hermes-library`, its `docs/`, `scripts/` or `profiles/`.
- Anything touching `~/.hermes` profiles beyond the active one (`admin`, `ea`), the shared
  library folders, or the nightly backup job.
- A question about rollout: who gets a profile, what a baseline is, what stays local.
- Discussion of pooling or distilling worked profiles back into the baseline.

Not for a colleague's day-to-day assistance, and not for Hermes configuration questions
that have nothing to do with the estate (use `hermes-agent`).

## Orient, then work one thread

1. `docs/handover.md` first, then `grep -n '^#' docs/decisions.md` for the index, then
   `docs/projects/README.md` for the numbered threads. Three reads instead of guessing.
2. Say which numbered thread is in play, then work only that one.
3. Read `config.env` before running any script: paths are configuration, not constants.

## Reply style: the rule that gets broken

This section exists because it is broken repeatedly. Treat the limits as mechanical, not
as taste.

- **Ceiling: about eight lines.** A one-line question gets one line. A status report gets a
  short list. If the answer needs a heading, it is a document.
- **No headings, no multi-section essays, no numbered argument in chat.** Draft the doc in
  the repo, then reply with its path and one sentence saying what it settles.
- **A direction is not a build request.** "We could use the backups for this" means agree,
  name the one consequence, ask the one decision it needs — and stop. Sam asks explicitly
  when he wants the system.
- **Park the tangent, do not re-litigate it.** When he says the conversation has drifted or
  the replies are too long: write the parking note, reply in one line, return to the thread
  he named. Do not defend the detail you just produced.
- **Self-check before sending:** would a five-line version still be true and still answer
  the question? If yes, send the five lines. Anything cut goes in the doc, not in a
  PS.
- One question per turn, two at most when they gate genuinely different things.

## Evidence

- Measure before claiming: real paths, real file counts, what a folder actually holds. Repo
  prose goes stale faster than the live tree; verify against OneDrive and `~/.hermes`.
- Where a fact was not observed, write UNKNOWN plus how it could be confirmed. D18 in
  `docs/decisions.md` makes assumed content worse than an empty field.

## Estate facts

- `~/tribe-hermes-library` is the versioned truth. Colleagues reach
  `OneDrive/.../TRIBE Group Tech/{Hermes Library, Hermes WIP, Hermes Backups/<machine>}`.
  The live `~/.hermes` runtime is never published.
- `scripts/hermes_files.py` subcommands: `backup` (text mirror that keeps memories, plus
  `state.db` snapshots), `sync` (to the shared library, memories stripped), `pull`,
  `nightly`.
- The loop back (harvest → distil → publish → pull → refresh) has a design in
  `docs/architecture-loop.md`. Design prose lives there, state lives in
  `docs/projects/checkpoint-distillation.md`; never both in one file. D34: no baseline
  update overwrites a soul — voice stays local, rules may travel as a diff.
- Profiles cloned from one source share a baseline, so diffing them proves nothing about
  what is generally true. Pooling practice only becomes meaningful after people have
  worked their own profiles.
- Order of work when both are on the table: rollout and testing first, distillation of
  worked profiles later. Building the harvester before anyone has worked a profile
  produces a tool validated against nothing.
- Sam's idea vault is `~/Documents/sam-tribe-brain` (Obsidian, git on `main`, Obsidian Git
  commits and pushes). Reading it is allowed; writes happen on request only. Its note
  format, tag rules and the `hermes` tag are in `references/sam-tribe-brain.md`.
- `docs/setup.md` is the estate's front door: install on Windows and macOS, the three
  `config.env` paths per platform, then the first-run sequence. It publishes as the
  library's `README.md` through a name special-case in the scripts. Publishing steps and
  the checks that prove a run landed: `references/library-publishing.md`.
- `templates/builder/` is the first profile on any new machine — labelled Hermes, its soul
  carrying the first-run job: run the setup interview, create the owner's role profile, hand
  the person over (D35). It holds `{{OWNER}}`-style placeholders and must never carry one
  person's details. The live `profiles/default/SOUL.md` is a separate copy and is not
  regenerated from the template.
- Two baselines only: `admin` for anyone, `ea` for a manager. `ea` is adapted from manager use; `pa` was dropped and D31 now names only those two. A new person gets a baseline installed and personalised by the interview, not a blank role profile invented from `templates/role/`.
- A machine that is not this one needs nothing from git: `Hermes Library` carries `scripts/`, `config.env.example`, the templates and the published profiles. Copy the folder to `~/tribe-hermes-library`, copy `config.env.example` to `config.env`, fill the three paths using the machine's asset name.
- Bootstrap of a fresh install is one pasted line: that it is the builder, to read `README.md` in `TRIBE Group Tech/Hermes Library` and follow it, and to ask before anything destructive. The stock default profile knows nothing about the estate, so that line, not a hand-edited soul, is what makes the install self-directing.
- Every machine writes its own backup into `Hermes Backups/<machine>/` (text plus dated `state.db` snapshots, created on first run) and needs to read back only its own. Per-folder permissions there are the open question; a backup read by every machine means every colleague can read every memory.
- `docs/projects/README.md` numbers every thread with its checkpoint file. Parked threads
  still get a row and a file, so a direction raised mid-conversation costs one small page
  rather than a re-argument later.
- The vault holds ideas; the repo holds decisions and procedures. Do not copy a decision
  into the vault as a second version — the vault note says what the idea is and points at
  the repo path that settles it.

## Pitfalls

- `custom_skills()` skips bundled skills, so a backed-up `skills/` can look populated while
  holding only `.locks` and `.hub` metadata. Count `SKILL.md` files, never files.
- Backups carry `memories/` and `db/` snapshots: the most personal material in the estate,
  and the shared library deliberately strips what backups keep. Any cross-profile reading
  needs an INCLUDE-list (`SOUL.md`, `skills/`, `config.yaml`, `cron/`) rather than an
  exclude-list, because Hermes gains personal folders over time and an exclude-list admits
  the next one silently. Aggregate counts out of `state.db` are fine; message text is not.
- `skills.external_dirs` in `admin` and `ea` points at an absolute path into this repo
  (`~/tribe-hermes-library/shared-skills`), so it is not portable to another machine. Any
  plan to push updates back has to close that gap first — design §4 in
  `docs/architecture-loop.md`.
- Never `grep -r` from the repo root: `profiles/*/skills/.hub/index-cache/` holds huge
  catalogue blobs (86 MB on one file) and will flood a tool result. Scope searches to
  `docs/`, `scripts/`, `templates/` or a named file.
- `sync` publishes `profiles/`, `templates/`, `shared-skills/`, `apps/`, `scripts/`,
  `docs/` and `config.env.example`, and it wipes and rebuilds the library folder from the
  repo each run. Anything put into the
  library by hand is deleted, so edits belong in the repo. It also commits and pushes.
- Two backup locations are described in the docs (a private per-user folder, and
  `Hermes Backups/<machine>`). Check what the script writes today instead of trusting the
  older note, and correct the note.
- A checkpoint's "remaining work" list goes stale: verify each item against the file before
  editing it. Doing an item that was already done wastes a turn; claiming it was pending
  makes the handover document lie.
- Where a doc states a rule and then gives an example that breaks it, readers follow the
  example. Fix the example, not just the rule (a role id illustrated with a person's name
  is how `assistant-<their name>` survived a naming decision).
- Never explain a repo↔library difference you measured before your own sync ran. Reading the
  library first and the repo second makes an in-flight sync look like a missing script
  feature, and the correction costs the user's trust in every other state you report. Sync,
  then measure both sides.
- Name a document for the person who opens the folder, not for its role in the repo:
  `setup` or `start here`, never `library-readme`. The published filename stays `README.md`
  because that is what the file browser surfaces; the title inside carries the meaning.
- The 17:00 job, `sync` and any manual publish all push to `origin`, so a claim that work is
  "committed locally" is wrong on this estate. Check `git remote -v` before describing the
  repo as local-only.
