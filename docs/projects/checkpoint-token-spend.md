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

## Baseline re-measured, 27 November 2026 11:45 AEDT

Taken before any change, from `hermes insights`, `hermes -p <p> insights`, `du`, `wc -c`,
`find skills -name SKILL.md | wc -l` and `sqlite3 state.db`.

| | builder (`default`) | `admin` | `ea` |
|---|---|---|---|
| Sessions (30d) | 8 | 8 | 3 |
| Messages | 2,259 | 839 | 4 |
| Input / output | 2.04M / 1.05M | 1.62M / 0.76M | 10.9K / 84 |
| **Total tokens** | **461.4M** | **283.1M** | **21,632** |
| Cost estimate | $2.30 | $1.54 | $0.0017 |
| Largest single platform | local: 2 sessions, 1,848 msgs, **362.4M** | local: 1 session, 698 msgs, **210.6M** | oneshot: 21,632 |
| `state.db` | 29 MB | 36 MB | 584 KB |
| Skills (`SKILL.md`) | 48 | 45 | 44 |
| `MEMORY.md` / `USER.md` chars | 2,112 / 2,200 · 1,371 / 1,375 | 2,195 / 2,200 · 1,359 / 1,375 | none · 85 / 1,375 |
| `compression.threshold` / `target_ratio` | 0.50 / 0.20 | 0.50 / 0.20 | 0.50 / 0.20 |

Builder content split by role, whole store, this measurement: tool 1,560 rows / 2,202 KB,
assistant 1,659 / 288 KB, user 246 / 99 KB. So the person's words are **4%** of stored content
and tool results are 85% — the same shape as the single-session measurement above, which had
it at 87%. Builder `state.db` by table: `state_meta` 12.93 MB, `messages` 9.3 MB, FTS 1.72 +
1.05 MB. The database is a third session metadata: that is worth knowing before any prune.

Item 2's comparison has to be run after items 1 and 3 land, in fresh sessions.

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
