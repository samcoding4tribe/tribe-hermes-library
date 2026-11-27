# Token spend, and what to change

Opened 27 November 2026, after 700M tokens in four days. This is the thread for making the
estate cheap to run: measuring where the tokens go, changing the defaults, and keeping the
practice in place.

## The measurement that started it

`hermes insights`, last 30 days, on this machine:

| Profile | Sessions | Messages | Input | Output | Total |
|---|---|---|---|---|---|
| builder (`default`) | 7 | 2,179 | 1.98M | 1.01M | **445M** |
| `admin` | 8 | 839 | 1.62M | 0.76M | **283M** |

Almost all of the total is cached prompt re-read, which is why the dollar estimate is small —
$2.23 and $1.54 for the fortnight — while the token count is enormous. Two chats carry it: one
local session at 351M on the builder and one at 210M on admin. Cron runs are 2M; subagents 7M.

Inside this builder session, 645 messages: tool results 543 KB, assistant 68 KB, user 12 KB. The
person's words are 2% of the conversation.

## What is already done

- `docs/context-budget.md` carries the numbers and the ranked levers: new chat per task, tool
  output discipline, delegation, fewer toolsets, fewer skills, smaller soul, earlier compaction.
- `shared-skills/session-hygiene/` is the advice: when to raise it, what to say, how to measure,
  and that the assistant recommends a new session rather than opening one.
- Rule 8 in both soul templates: watch what the conversation costs, warn before an expensive
  step, offer the fresh chat with the handover written first.
- `scripts/daily_handover.py` and the 07:30 job: the morning handover, generated from the repo
  with no model in the loop.
- `docs/projects/session-starters.md`: a paste-ready first message per thread.

## What is not done

1. **Rule 8 is not in the three live souls** (`default`, `admin`, `ea`) — only in the templates.
   So the habit does not fire here yet. Needs three approval prompts plus
   `hermes sessions refresh-prompts` for each profile.
2. **No per-session baseline after the change.** The comparison that matters: run threads 2 and 5
   in separate sessions and compare their `hermes insights` numbers with the marathons above.
3. **Compaction settings untouched.** `threshold: 0.50`, `target_ratio: 0.20`. Lowering to 0.35
   and 0.15 compacts sooner; untested here, and worth testing on one profile before all three.
4. **Toolsets not trimmed.** `platform_toolsets` gives every profile the full set. A role profile
   that never browses should not carry the browser toolset.
5. **48 skills installed on the builder.** Each adds a line to every prompt. Curating to what is
   actually used is a decision, not a cleanup.
6. **`state.db` growth** has a watch line (100 MB) in `docs/context-budget.md` but no job that
   reports it; it belongs in the maintenance pass (thread 7).
7. **Session-store housekeeping** — archive past 90 days, prune past a year — is written as a
   suggestion, not decided, and no job runs it.

## What finished looks like

Two sessions of comparable work, before and after, with the token numbers written down; rule 8
live in all three profiles; and a monthly line in the maintenance pass that reports sessions,
database size and the top three tools by call count.

## Only Sam can answer

- Whether to lower the compaction threshold on all profiles or test on one first.
- Which toolsets each role profile actually needs.
- Which skills the builder can live without.

## Session starter

```
Load the tribe-hermes-estate skill. Read ~/tribe-hermes-library/docs/projects/checkpoint-token-spend.md,
then docs/context-budget.md. Work the "what is not done" list in order. Measure before you change
anything, and record the numbers in the checkpoint as you go.
```
