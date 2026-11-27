---
name: profile-maintenance
description: "Maintain a profile: measure, flag, propose, refresh."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [maintenance, context-budget, memory, soul, sessions, refresh]
    related_skills: [session-hygiene, tribe-hermes-estate]
---

# The maintenance pass

One pass over a profile you did not write, on a machine that is not yours: **measure,
flag, propose** — and only after an explicit yes, **apply and refresh**. The pass never
applies on its own. It has no standing permission to edit a soul, a memory file, a skill
or a database, and a general "tidy it up" is not permission for a specific delete (D32).

This is not the pooling loop. That improves the shared baseline from several people's
practice. This keeps one profile healthy, current and honest about its own size on one
machine.

## When to run it

- **Two weeks after you hand the profile over** — the first review, one question: which
  part is not earning its place.
- **Quarterly**, or when the profile feels slow, forgets a standing rule, or answers as an
  older version of itself.
- **After any change to the static prompt** — a soul edit, a memory consolidation, a skill
  installed or removed. Measuring first is optional; refreshing afterwards is not.

Whether the pass runs on a clock is not decided. Do not schedule it as a job until the
person whose profile it is has said a cadence out loud.

## 1. Measure

Two read-only commands, no model in the loop:

```bash
python3 ~/tribe-hermes-library/scripts/profile_audit.py --profile <id>
python3 ~/tribe-hermes-library/scripts/profile_audit.py --all        # every profile here
python3 ~/tribe-hermes-library/scripts/profile_audit.py --profile <id> --json

hermes -p <id> prompt-size --json    # the fixed prompt: system, skills index, memory, tools
```

On Windows, `python` rather than `python3`. The audit script opens `state.db` with SQLite
`mode=ro` and writes nothing anywhere — it is safe to run on a live profile. `prompt-size`
runs offline and is the only one of the two that weighs **tool schemas**, which are usually
the largest fixed block (33.6 KB against a 3.7 KB skills index, measured 27 November 2026).
Use its default `cli` platform: `--platform gui` reports no tools and no index, so it does not
model the desktop app.

| Line | What it is | Why it matters |
|---|---|---|
| `soul` | bytes in `SOUL.md` | first in the prompt, re-sent every turn |
| `MEMORY.md` / `USER.md` | characters against the caps in that profile's own `config.yaml` | a full memory file refuses writes, and the person loses the next fact |
| `skills` | count of `SKILL.md` files | each adds one line to every prompt |
| `state.db` | disk size, message count | disk only, but it grows with every verbose tool result |
| `external_dirs` | paths from `skills.external_dirs` | an absolute path that does not exist on this machine is an empty skills folder wearing a config |

**Counts, never content.** Do not open another profile's `memories/*.md` to measure it, and
do not quote message text from `state.db`. Aggregate counts are fine; the text is the most
personal material in the estate (D14, D30). If a proposal needs a memory line quoted, the
person quotes it.

## 2. Flag

The script marks what is over a line. Treat each code as "look here", not as a verdict.

| Code | Level | What to do |
|---|---|---|
| `soul_band` | flag | soul over the band: find the paragraph that is really a procedure and propose moving it to a skill |
| `soul_thin` | info | soul under the floor: check the rules are actually present before shortening anything else |
| `memory_pct` / `user_pct` | flag | at 90% of the cap: propose a consolidation, not an appendix |
| `soul_memory_dup` | flag | the same line in the soul and a memory file: keep the memory copy, cut the soul line, or the reverse — say which and why |
| `baseline_dup` | flag | a rule restated outside the soul's marked block, when the profile already carries it inside the block: delete the second copy |
| `soul_self_dup` | flag | one rule twice in one soul, usually after two edits: pick the better wording |
| `state_db` | flag | past the 100 MB watch line: read table sizes before proposing deletion; a large store is usually one long session, not many short ones |
| `state_db_density` | info | few long sessions rather than many: the fix is session habits, not pruning |
| `memory_absent` | info | no memory files yet: the profile has not been used, nothing to consolidate |

Two things the script cannot see and you should:

- **A procedure living in the soul.** "How to triage the inbox" belongs in a skill, however
  important it is. Importance is the reason it should not be repeated every turn.
- **A fact that is really data.** A list of people, sites or accounts belongs in a file read
  by path.

Where each kind of information belongs is the table in `docs/context-budget.md`. Read it
rather than recalling it; the mapping is the part people get wrong.

## 3. Propose

A proposal is a diff and one sentence of cost, in the chat, not a document:

> Your soul is 3.5 KB. This paragraph — the four steps for preparing a supplier quote — is a
> procedure, so it belongs in a skill where it loads only when quoting. Moving it takes about
> 700 bytes off every turn. Here is the skill and the trimmed soul. Yes?

- **One change per proposal.** A batch hides the one item the person disagrees with.
- **Show the deletion, not just the addition.** Bad proposals add a rule and leave the old one.
- **Name the cost in bytes and in behaviour.** "One cache miss per open chat" is a cost too.
- **Say where the displaced material goes**, or it reappears as a memory entry next month.
- **Then stop.** No edit before the yes, and no second attempt in the same breath.

## 4. Apply, then refresh

On an explicit yes, one file at a time, with a targeted edit rather than a rewrite. Editing
`SOUL.md` raises an approval prompt: a prompt that times out is **not** consent — re-issue
the edit and ask the person to approve it in the dialog. Never reach the same change through
a shell redirect. Two profiles' souls go through the gate one at a time, so a half-approved
batch cannot leave one marked and one not.

Then force the new self into the chats that are already open:

```bash
hermes sessions refresh-prompts                         # the profile this session is in
hermes -p <profile-id> sessions refresh-prompts         # another profile on this machine
hermes -p <profile-id> sessions refresh-prompts --session <session-id>
hermes -p <profile-id> sessions refresh-prompts --json  # {"epoch": 2, "session_id": null, "sessions": 13}
```

**What it does.** Stamps a refresh epoch in that profile's `state.db`. At the start of each
session's next turn Hermes compares the epoch with the one stamped when the prompt was
built, and when the prompt is older rebuilds it once through the normal builder: history,
session id and the `tools[]` pin are kept, `on_session_start` does not fire, and the new
bytes are persisted so later turns replay them verbatim. It covers soul edits, skill edits
and context files, and it works while the gateway is running and across restarts.

**What it costs.** One prefix-cache miss per refreshed session — real money, once, not a
standing penalty.

**What it is not.** A dry run. With no selector it stamps every session in the profile
immediately (measured 27 November 2026: 13 sessions on the builder). Use `--session` when
only one chat should change, and read `sessions` out of `--json` to know how many you just
touched.

Then say so, in one line, to the person:
"Changed; your open chats pick it up on their next message, one cache miss each."

### Verified, and not

- Verified 27 November 2026: the command and its flags, `-p` targeting another profile, the
  `--json` shape, and that a bare call stamps every session at once.
- **Not verified:** whether a session held open in the desktop app or by the gateway picks
  the rebuild up before its next turn (the code says next turn, it has not been run here);
  what a skill edit does to a chat that has already loaded that skill — the body may reload,
  the index line will not; and whether a memory write needs the same refresh. It should —
  memory is injected at session start too — so treat a memory consolidation as needing the
  refresh, and test it the first time it matters.
- **If the person says the assistant has not changed:** ask them to send one more message,
  then check the soul they are running against. Do not edit again on the assumption that the
  first edit failed.

## 5. Record the pass

Write one short note per pass at `~/.hermes/profiles/<id>/workspace/maintenance-<YYYY-MM-DD>.md`:
date, what was flagged, what was applied, what was deferred and why. `workspace/` is copied
into this machine's backup and stripped from the published library (`hermes_files.py`
removes `workspace/` and `memories/` on the publish path), so it stays on the machine.

Do not write the pass into the repo's `docs/` on somebody else's machine: `docs/` publishes
to the shared library, and one person's maintenance history would land in front of the team.

## What the pass never does

- Never applies a change without a yes, and never treats silence as one.
- Never deletes sessions. `prune`, `archive` and `optimize` are separate acts with their own
  description and their own yes; a big database is a finding, not an instruction.
- Never consolidates memory by dropping a fact the person still uses. Show the two entries
  that overlap and ask which still matters.
- Never copies a memory, a working note or a transcript between profiles (D14, D17).
- Never publishes from a colleague's machine to make the library look current.

## Done looks like

Counts printed, every flag either applied with a yes or recorded as deferred, the refresh run
and stated out loud, and the note written. A pass that ends with nothing applied is a
successful pass if that is what the person chose.
