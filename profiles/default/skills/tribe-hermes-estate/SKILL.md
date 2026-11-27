---
name: tribe-hermes-estate
description: "TRIBE Hermes estate: repo, profiles, rollout."
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

**Route the request before investigating it.** A request that is Sam's own day — inbox, diary,
forms and their responses, expenses, a supplier quote — belongs to the `admin` profile (or `ea`
for the manager's), because it needs that profile's browser logins and its own session store.
Say so in one line, give one paste line for a session in that profile, and stop. Starting the
investigation here burns tokens and hands over a half-answer: a form whose responses live behind
the other profile's Microsoft login cannot be read from this one, and the reply has to admit that
after the work rather than before it. Builder work that merely mentions a form or a meeting stays.

## Orient, then work one thread

0. **Start of a day: `docs/handover-today.md`.** A 07:30 job (`scripts/daily_handover.py`,
   wrapper `~/.hermes/scripts/hermes-handover.sh`) rebuilds it from the repo alone — no model,
   no tokens: what changed yesterday grouped by folder, every open thread with its state and
   next action, and anything the previous handover carried forward. Paste-ready kickoff lines
   per thread are in `docs/projects/session-starters.md`. The morning routine is one line:
   "Read docs/handover-today.md, then start on the first thread." Every open thread needs a
   block there, the nearly-finished one included: a thread with no kickoff line is the one a
   daily routine silently skips, and adding it is a two-minute job.
1. `docs/handover.md` first, then `grep -n '^#' docs/decisions.md` for the index, then
   `docs/projects/README.md` for the numbered threads. Three reads instead of guessing.
2. Say which numbered thread is in play, then work only that one.
3. Read `config.env` before running any script: paths are configuration, not constants.
4. When a decision changes, change every carrier in one pass: `docs/decisions.md`,
   `docs/setup.md`, the kit under `docs/profiles/interview/`, any template that repeats the
   rule, then `sync`. `grep -rn` the old wording across `docs/`, `templates/` and
   `profiles/` before declaring it done — a half-propagated rule is worse than one not yet
   written, because the newest file wins the reader's belief.

## Before you change anything

- **Say what you understood, and act only on that.** When an instruction has two readings —
  which profile, which copy, whose machine — state your reading in one line and wait. A
  stopped turn costs one question; work in a direction he did not ask for costs the whole
  morning and his confidence in every other report.
- **A documentation task is not licence to edit live profiles.** The souls, memory files and
  skills of `admin` and `ea` are behaviour files. Touching them because the surrounding
  conversation mentioned them is exactly the change that gets interrupted.
- **Keep the three estates apart.** The Hermes repo (the system), the shared library
  (colleagues), and Sam's own notes (his) have three audiences. Do not connect two of them
  to be helpful; a pointer added in one direction leaks in that direction.
- **When he interrupts, or asks whether something went wrong:** stop editing, run the state
  check in `references/library-publishing.md`, report the facts in a few lines, then ask. Do
  not defend the reasoning and do not start the next edit.

## Reply style: the rule that gets broken

This section exists because it is broken repeatedly. Treat the limits as mechanical, not
as taste.

- **Ceiling: about eight lines.** A one-line question gets one line. A status report gets a
  short list. If the answer needs a heading, it is a document.
- **No headings, no multi-section essays, no numbered argument in chat.** Draft the doc in
  the repo, then reply with its path and one sentence saying what it settles.
- **Profile ids are your vocabulary, not his.** When he asks what you meant about a window, a
  session or a profile, answer in terms of files and windows — "the edits are in the repo both
  windows read" — then the one decision. An explanation about which profile is running reads as
  evasion when the question was practical, and it earns a "what do you mean?"
- **A direction is not a build request.** "We could use the backups for this" means agree,
  name the one consequence, ask the one decision it needs — and stop. Sam asks explicitly
  when he wants the system.
- **Park the tangent, do not re-litigate it.** When he says the conversation has drifted or
  the replies are too long: write the parking note, reply in one line, return to the thread
  he named. Do not defend the detail you just produced.
- **Self-check before sending:** would a five-line version still be true and still answer
  the question? If yes, send the five lines. Anything cut goes in the doc, not in a
  PS.
- **Ask once, then let the checkpoint hold it.** An unanswered question goes into the
  thread's checkpoint as an open item and comes back when that thread is worked. Repeating
  the same two or three asks at the end of every turn is noise, and it makes a reply that
  was supposed to be one line into a nag.
- One question per turn, two at most when they gate genuinely different things.

## Evidence

- Measure before claiming: real paths, real file counts, what a folder actually holds. Repo
  prose goes stale faster than the live tree; verify against OneDrive and `~/.hermes`.
- Where a fact was not observed, write UNKNOWN plus how it could be confirmed. D18 in
  `docs/decisions.md` makes assumed content worse than an empty field.
- "The previous session managed it" sends you to a profile's `state.db`, not to this chat and
  not to the repo: each profile has its own store, a day-job task usually sat in `admin`, and a
  read-only `LIKE` query over `messages` recovers the route it took. Query, the schema traps and
  the boundary on what may be quoted: `references/past-session-lookup.md`.

## Estate facts

- `~/tribe-hermes-library` is the versioned truth. Colleagues reach
  `OneDrive/.../TRIBE Group Tech/{Hermes Library, Hermes WIP, Hermes Backups/<machine>}`.
  The live `~/.hermes` runtime is never published.
- `scripts/hermes_files.py` subcommands: `backup` (text mirror that keeps memories, plus
  `state.db` snapshots), `sync` (to the shared library, memories stripped), `pull`, `nightly`,
  and `share` — marked soul rules into `baseline/soul-rules/`, weekly via the cron job 'Hermes
  soul share' (Sunday 17:30, wrapper `~/.hermes/scripts/hermes-share.sh`). What travels, how the
  summary compares rules and why identical wording matters, plus the two traps in that folder:
  `references/soul-sharing.md`.
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
- `docs/setup.md` is the estate's front door: install on Windows and macOS, the three
  `config.env` paths per platform, then the first-run sequence. It publishes as the
  library's `README.md` through a name special-case in the scripts. Publishing steps and
  the checks that prove a run landed: `references/library-publishing.md`.
- `templates/builder/` is the first profile on any new machine — labelled Hermes, its soul
  carrying the first-run job: run the setup interview, create the owner's role profile, hand
  the person over (D35). It holds `{{OWNER}}`-style placeholders and must never carry one
  person's details. The live `profiles/default/SOUL.md` is a separate copy and is not
  regenerated from the template.
- One baseline: `admin`. Setup routes on the org role — someone who manages others, or
  whose work is mostly diary, approvals and correspondence, gets the id `ea`; everyone else
  gets `admin` — but the content installed is `profiles/admin` either way. `profiles/ea` in
  the library is one manager's pilot instance, not a baseline, so setup does not install it;
  when managers' use makes `ea` differ in skills or soul attributes, those differences
  become its own published baseline and the id is already correct (D37). `pa` was dropped.
  A new person gets a baseline installed and personalised by the interview, never a blank
  profile invented from `templates/role/`.
- The routes are data, in `config/routing.json`, not prose: each route carries `profile_id`,
  `baseline` and `applies_to`, and promoting one is a single field change plus publishing
  `profiles/<id>/`. Both `docs/setup.md` and the interview kit say "read the file, do not
  retype it" — keep it that way, or a promotion becomes a prose edit in three places.
- Measuring OneDrive's stubbed files, reading the client's own failure counters out of
  `SyncDiagnostics.log`, testing the fetch path without downloading gigabytes, and why a
  hydration count only means anything alongside the state it was taken in:
  `references/onedrive-hydration.md`.
- Surveying the Share Drive's own records (how many rows a master sheet really holds, what a
  folder contains per-event, who last touched a file) is the recipe in
  `knowledge-base-over-documents` plus its `scripts/census_workbook.py`. `read_file` extracts an
  `.xlsx` to text and is the right first look, but it truncates and does no arithmetic, so
  counts come from the script; authorship and ownership come from
  `unzip -p <book>.xlsx docProps/core.xml`; a `.lnk`'s target from `strings`. Every count is
  quoted with its depth and the hydration state it was taken in.
- A machine that is not this one needs nothing from git: `Hermes Library` carries `scripts/`, `config.env.example`, the templates and the published profiles. Copy the folder to `~/tribe-hermes-library`, copy `config.env.example` to `config.env`, fill the three paths using the machine's asset name.
- Bootstrap of a fresh install is one pasted line: that it is the builder, to read `README.md` in `TRIBE Group Tech/Hermes Library` and follow it, and to ask before anything destructive. The stock default profile knows nothing about the estate, so that line, not a hand-edited soul, is what makes the install self-directing.
- Every machine writes its own backup into `Hermes Backups/<machine>/` (text plus dated `state.db` snapshots, created on first run) and needs to read back only its own. Per-folder permissions there are the open question; a backup read by every machine means every colleague can read every memory.
- Everything in a profile except `memories/` reaches the shared library: `SOUL.md`, `skills/`,
  `config.yaml`, `cron/`, and every file under `docs/`. So a personal path, a private vault or
  a colleague's detail written into a soul, a skill, a doc or a decision is published to the
  team. Durable personal operating facts belong in the memory file, and the rule that
  protects them must not restate the value it protects — `docs/decisions.md` is published
  too, so quoting the path inside the rule leaks it.
- **Token spend is a session-length problem, not a config problem.** A session re-sends its
  whole history on every turn, so thread-sized sessions beat one marathon chat. Attribute with
  `hermes insights` and `hermes prompt-size --json` (offline; there is no `--list-toolsets` flag
  in this build — the schema byte count is the number). Order of work: sessions, tool-output
  discipline, toolsets, skills, soul, compaction. Figures and commands:
  `references/context-cost-measurement.md`.
- Compaction fires at `threshold` 0.50 with `target_ratio` 0.20; on a 1M window those fractions
  are nearly inoperative (0.35 would have tripped at turn 286 of a 1,004-call marathon), so the
  lever is the absolute `compression.threshold_tokens`, which ships unset and fires at whichever is
  lower. The store is managed with `hermes sessions archive`, `prune` and `optimize`, and must be
  split by table before its size means anything — `state_meta` can be most of it. Policy:
  `docs/context-budget.md`; queries, the log lines that prove compaction fired, and the turn
  positions each threshold would fire at: `references/context-cost-measurement.md`.
  The habit ships as `shared-skills/session-hygiene` plus the conversation-cost rule in both role
  templates **and all three live souls**, word-identical because `share` pairs by exact wording;
  it is the last rule in the builder's block and a different number elsewhere, so never cite a
  shared rule by number. A soul edit is live only after `hermes sessions refresh-prompts`, and the
  proof is `prompt-size --json` growing by the rule's length, not the write returning success.
- **The cost is visible in the product, and the surface is hidden by default.** The status bar
  along the bottom edge carries a context meter (`[▇▇▇░░] 5%`) that ships switched off —
  right-click the bar, tick "Context meter" — and clicking it opens the used/max, percent-full,
  compression and per-category popover; `/context` is the CLI equivalent. Point a person there
  before quoting a number, and read `apps/desktop/src` before proposing to build a gauge, counter
  or alert that may already ship: the desktop runs from a built bundle, so a local patch dies on
  the next `hermes update` (D40). Meter location, popover contents and the traffic-light bands:
  `references/context-cost-measurement.md`.
- `docs/projects/README.md` numbers every thread with its checkpoint file. Parked threads
  still get a row and a file, so a direction raised mid-conversation costs one small page
  rather than a re-argument later.
- **The assistant recommends a new session; it never opens one.** There is no supported way to
  create a chat and put a prompt in it — `hermes desktop` has no `--new`, and driving the app's
  button through UI automation is brittle. That button is labelled **"New session"**, not "New
  chat": use the app's word when telling a person what to click. Say the new thread belongs in
  its own session, write the handover, and give one paste line. `hermes chat -q "<kickoff>"` is
  the terminal equivalent when the work is mechanical and does not need the desktop.

## Pitfalls

- **An improvement suggestion arriving from outside is usually already the architecture.** Lazy
  skill and tool loading, loop guardrails and retry caps all exist in this build; the productive
  answer is to open `config.yaml`, `hermes prompt-size --json` and the guardrail's own log line,
  then reply with the values and the one number that is genuinely unset. Agreeing to build what
  ships costs a session and teaches the person the estate did not know itself. The same holds when
  Sam attributes spend to a knob: measure which mechanism trips at which turn before agreeing that
  it would have fired earlier — the plausible lever is often the inert one.
- A question about the soul's own rules is an evidence task, not a recall task. The builder's
  shared block carries **eight** numbered rules, with "watch what the conversation costs" last;
  `admin` and `ea` carry a shorter block, so the same rule lands on a different number. Read the
  live `SOUL.md` and count before saying "there is no rule N" — a false negative about a rule
  that is on screen reads as the estate not knowing its own guardrails. And `session-hygiene` is
  a hub skill under `shared-skills/` in the repo, so this profile's `skills_list` legitimately
  does not list it; absence there is not absence everywhere.
- A duplicate of a `docs/` procedure under `templates/` publishes twice and drifts: the
  interview kit once lived in three places, and the two copies still carried the colleague
  names that had been genericised out of the canonical one, so the leak reached the library.
  One copy per procedure — `templates/role/README.md` now holds mechanics only and points at
  `docs/profiles/interview/`. Check `templates/` for strays before publishing.
- Editing another profile's `memories/MEMORY.md` is a capped write: read
  `memory.memory_char_limit` from that profile's `config.yaml` (2200, with `user_char_limit`
  1375) before appending. At the cap, consolidate two stale entries into one instead of adding
  a third — the file loads on every turn, and trimming stale paths is usually the room you
  need anyway.
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
- The transcript is mostly tool output, so the cheapest saving is rarely a smaller soul.
  Measured on the builder's own session: 543 KB of tool results against 12 KB of the user's
  messages, with soul, memory and the skills index together about 7 KB. Write large results to
  a file and print the count and the path; one recursive `grep` that printed an 86 MB
  catalogue was billed again on every later turn of that session. When the user asks why spend
  is high, measure the split first (`hermes insights`, and the `messages` table by role) rather
  than proposing config they do not need.
- Never `grep -r` from the repo root: `profiles/*/skills/.hub/index-cache/` holds huge
  catalogue blobs (86 MB on one file) and will flood a tool result. Scope searches to
  `docs/`, `scripts/`, `templates/` or a named file.
- `sync` publishes `profiles/`, `templates/`, `shared-skills/`, `apps/`, `scripts/`,
  `baseline/`, `config/`, `docs/` and `config.env.example`, and it wipes and rebuilds the
  library folder from the repo each run. Anything put into the library by hand is deleted, so
  edits belong in the repo. It also commits and pushes.
- A new top-level folder is invisible to the library until its name is added to the `parts`
  tuple in `cmd_sync` — the publish step copies a list, not the tree. Adding the folder and
  running `sync` is two changes, and forgetting the second one looks exactly like "the folder
  never made it to OneDrive".
- After editing a live profile's `SOUL.md`, statements here still work because this chat opened
  before the edit — the change reaches a session only when its system prompt is rebuilt. Use
  `hermes sessions refresh-prompts` (stamps a refresh epoch in that profile's `state.db`; the
  prompt rebuilds once on the session's next turn, one prefix-cache break), or start a new chat.
  It is **not a dry run**: a bare call stamps every session in the profile at once (`--json`
  reports `{"epoch": N, "session_id": null, "sessions": 13}`), so use `--session <id>` when only
  one chat should change — and do not run it with `--help`-style curiosity on a profile you are
  not maintaining. `hermes prompt-size --json` (works with `-p`) is the other half: the fixed
  prompt including tool schemas, 33.6 KB against a 3.7 KB skills index on 27 November 2026, so
  trim a toolset before curating skills.
- `SOUL.md` is a protected agent-instruction file: the write raises an approval prompt, and a
  prompt that times out is **not** consent — the gate refuses an immediate retry, so a
  same-turn re-issue only times out again. End the turn, say in one line that the dialog needs
  approving, and re-issue once he is at the screen. Never reach the same change through
  `terminal`, a heredoc or `execute_code`, and do not read a silent turn as a yes. Two profile
  souls go through the gate one at a time — a batch that is half-approved leaves one approved
  and one not, and the reply has to say which.
- Two backup locations are described in the docs (a private per-user folder, and
  `Hermes Backups/<machine>`). Check what the script writes today instead of trusting the
  older note, and correct the note.
- `scripts/rule_pair_probe.py` is the cheap way to answer "are these two rules the same
  rule": word 2–5-gram Jaccard per cross-profile pair, blocking key, best partner per rule.
  Run it before proposing a matcher or asking a model — it costs nothing and turns an opinion
  about wording into numbers you can quote.
- Appending a new section to a `docs/` file: anchor the edit on the `---` break or the next
  section's heading, never on the last lines of the previous section. Those last lines are
  often a wrapped bullet, and replacing them splits the sentence and orphans its tail after
  the section you just added — the diff looks clean and the file reads as two broken halves.
  Re-read the tail after the write.
- A checkpoint's "remaining work" list goes stale: verify each item against the file before
  editing it. Doing an item that was already done wastes a turn; claiming it was pending
  makes the handover document lie. Carry a status cell per item in the same pass — the measured
  fact it now holds, or who it waits on (Sam's decision, an approval, a later session). When
  most of a list is gated on him, measure all of it first, record the numbers, and end the turn
  with the one decision that unblocks the head of the list rather than a summary of the seven.
  The stalest part of a checkpoint is its preamble — the "tomorrow morning, start here" note
  still names items finished days ago — so rewrite the opening paragraph in the same pass, and
  delete any copied thread-state table in favour of one line pointing at
  `docs/projects/README.md`: a second copy of the list drifts against the first within days and
  the generated handover reads only the canonical one.
- The same staleness runs the other way, and costs more. When the thing that blocked a thread
  is fixed — hydration, an access grant, a missing plan answer — the brief and checkpoint
  written under the block keep offering its UNKNOWNs as current state, and the next session
  re-does the investigation. In the same pass that records the new evidence, mark the old
  finding dated-and-superseded with a pointer to where the truth now lives, and rewrite the
  checkpoint's blocker paragraph rather than appending to the list below it.
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
  repo as local-only. And read `git status --short` before any commit: another session's
  in-flight edits sit in the same working tree, so committing "your" docs sweeps theirs in.
  Leave the tree dirty and name the foreign files in the reply, unless he said to commit.
- A generated handover is only useful if it is quiet: filter `.locks/`, `.hub/`, `logs/` and
  generated artefacts out of the changed-file list, or yesterday's cron lock churn buries the
  three edits that matter. And its "still open" list reads the thread table, so **mark a
  finished thread's state cell starting with `Closed`** — any other wording keeps it in the
  morning list, while a filter on the word "done" silently drops rows like "Brief done,
  nothing built".
