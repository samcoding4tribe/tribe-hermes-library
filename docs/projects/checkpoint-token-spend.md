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

### Sam's own figure, and why it agrees

Sam, 27 November, in the session where rule 8 was added: **about 770M tokens over the week
before the change, with the builder used a couple of times since.** That is his figure, not a
measurement from a script, and it covers the week rather than the insights window.

It corroborates the table above rather than repeating it: the three profiles measured 30 days
come to 744,480,299 tokens (461.4M + 283.1M + 21,632), which is 96.7% of his 770M. So nearly all
of the thirty days of spend happened in that one week, and the baseline is representative rather
than chosen.

The residual 25.5M (3.3%) is unattributed. It could be a profile outside these three, sessions
outside each profile's insights window, or counting that includes cached reads differently;
**UNKNOWN** — it would be confirmed from the console or dashboard total across every profile for
the same seven days, which nobody has pulled yet.

**The baseline is already contaminated.** Builder sessions have run since the change, so a
like-for-like before/after cannot be reconstructed: the comparison has to start from the numbers
here and measure forward, and it must say so rather than presenting the two as a clean pair.

### The fixed per-request prompt, measured

`hermes prompt-size --json` (offline, no API call), same day. This is what every single request
carries before a word of history:

| | builder | `admin` | `ea` |
|---|---|---|---|
| System prompt | 22,014 chars | 21,353 | 16,460 |
| — of which skills index | 3,704 | 4,068 | 3,994 |
| Memory | 2,254 | 2,337 | 0 (no `MEMORY.md`) |
| User profile | 1,511 | 1,503 | 232 |
| Tools | 19 tools, **33,628 bytes of schema** | 19 / 33,254 | 19 / 33,254 |

Two things follow, and they set how items 4 and 5 should be ranked:

- **The tool schemas are the largest fixed block, at 1.5× the whole system prompt and 9× the
  skills index.** Trimming a toolset is worth more than curating skills, which is worth more
  than the soul. Items 4 and 5 are not the small end of the list; the soul is.
- **The skills index is about 3.7 KB for 48 skills, roughly 77 bytes a line**, and `insights`
  shows 8 distinct skills loaded in thirty days on the builder (14 loads), 7 on `admin`
  (9 loads). So ~40 installed skills on each profile have not been called in a month and are
  paying rent on every request.

`--platform gui` reports the same tool set as 0 tools and 0 index, so it does not model the
desktop app's prompt; only the `cli` figure above is usable. Do not quote the `gui` one.

## The store is not mostly transcripts (items 6 and 7)

Measured with `dbstat` and a group-by over `state_meta`, 27 November:

| | builder 29 MB | `admin` 36 MB |
|---|---|---|
| `state_meta` total | 12.93 MB | 25.07 MB |
| — of which `gateway.admission.result.*` | **234 entries, 13.36 MB** | **141 entries, 24.87 MB** |
| `messages` | 9.3 MB | 6.14 MB |
| FTS (two tables) | 2.77 MB | 2.23 MB |

So **46% of the builder's database and 69% of `admin`'s is cached gateway admission results**,
not conversation. Two consequences the current policy gets wrong:

- `docs/context-budget.md` says a large database "is usually one long session rather than many
  short ones". Here it is neither: it is one cache table. Pruning sessions would not move the
  number.
- The 100 MB watch line will trip on admission blobs, not on transcripts, so a report that only
  prints database size would send the next person to delete the wrong thing. The maintenance line
  needs the table split in it, not just the total.

Session ages, for item 7: oldest session on any profile is 20 November 2026 and **nothing is
older than 90 days anywhere** (builder 14 sessions, `admin` 8, `ea` 3). An archive-at-90-days,
prune-at-a-year job is anticipatory today and would touch zero rows — the policy still needs
deciding, but it is not urgent, and the growth that is actually happening is the admission cache.

## Item 3: what a lower threshold would have been worth

The log line above is the whole fact base. `effective_aux_context` is 1,048,576, so the two
thresholds fire at:

- 0.50 → 524,288 tokens (where it actually fired: 524,843)
- 0.35 → 367,002 tokens

### Where those points fall in the marathon

The 351M session (`local-fb5a…`, 20–26 November, 2,321 messages, 1,004 tool results) is the test
case. Reading its messages in order, with 1.555 characters per token anchored on the log's own
figures (524,843 tokens at 816,014 characters):

| Prompt reaches | Tool call | Fraction of the 1M window |
|---|---|---|
| 100K tokens | 24 | 10% |
| 150K tokens | 63 | 15% |
| 200K tokens | 127 | 20% |
| 367K tokens — a 0.35 ratio | 286 | 35% |
| 525K tokens — the 0.50 ratio, where it fired | 510 | 50% |

So the compaction threshold did flag the conversation — at tool call 510 of 1,004, halfway through
the session's life and long after most of the spend. **Lowering the ratio to 0.35 only moves it to
tool call 286**: a fraction of a 1M window is a very large number of turns before it trips.

### The knob that matches the instinct

`config.yaml` already has an absolute cap, off by default: `threshold_tokens`, which fires at the
whichever is lower — the ratio or the token count. Set to 200,000 it would have compacted this
session at tool call 127, and at 150,000 at tool call 63. That is the setting that catches a long
session on any model, because it does not scale with a window that grew to a million tokens.

The trade is explicit: compacting at 20% of the window throws away context the model could still
have used, in exchange for capping what every later turn re-reads. It also costs one summary call
per compaction (~52K prompt tokens). On a 1M-window model the ratio settings are close to
inoperative; the absolute cap is the lever.

Growth is not uniform and cached reads are priced low, which is why the dollar estimate was $2.30
for the fortnight. Against the token count the thread is about, the shift is large.

One profile should change first, and it should not be the one running the comparison. Test on
`admin` and leave the builder at 0.50 as the control; the two profiles then produce comparable
sessions in the same fortnight.

## What is already done

- `docs/context-budget.md` carries the numbers and the ranked levers: new chat per task, tool
  output discipline, delegation, fewer toolsets, fewer skills, smaller soul, earlier compaction.
- `shared-skills/session-hygiene/` is the advice: when to raise it, what to say, how to measure,
  and that the assistant recommends a new session rather than opening one.
- Rule 8 in both soul templates: watch what the conversation costs, warn before an expensive
  step, offer the fresh chat with the handover written first.
- **Rule 8 now live in all three souls**, 27 November, same wording, prompts refreshed. The share
  summary pairs rules by exact wording, so one text across three souls means the Sunday job will
  pair it rather than list it three times as unpaired.
- `scripts/daily_handover.py` and the 07:30 job: the morning handover, generated from the repo
  with no model in the loop.
- `docs/projects/session-starters.md`: a paste-ready first message per thread.
- **The gauge already exists and is off by default.** Status bar along the bottom edge of the
  window; right-click it and tick "Context meter" for `[▇▇▇░░] 5%`, click the meter for the
  popover (used/max, percent full, compressions, split by category). D40: no traffic-light patch
  to the app — rule 8 carries the warning, and the bands are recorded in the decision if it is
  ever built.

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

### Status, 27 November

| # | Measured | State |
|---|---|---|
| 1 | Rule 8 absent from all three live souls, confirmed by `grep` | **Done 27 Nov**: added to all three, identical wording, `refresh-prompts` run on 14 + 8 + 2 sessions. Each system prompt grew exactly 337 chars (22,014→22,351 · 21,353→21,690 · 16,460→16,797). Lands as rule 8 on the builder, rule 6 on `admin` and `ea`, which have five rules each. |
| 2 | Baseline above | Waiting on item 3, then two fresh sessions running threads 2 and 5 |
| 3 | 0.50 / 0.20 on all three; window 1M; **compaction fired once in the whole estate** — builder session `local-fb5a…`, 24 Nov 12:52, at 1,199 messages and ~524,843 tokens (tool call 510 of 1,004), compressed to 129 messages / ~65,991 tokens, aux call 52,511 prompt tokens. `threshold_tokens` (absolute cap) exists and is unset | Sam's call: ratio 0.35 / 0.15, or an absolute `threshold_tokens` of 150–200K, which trips far earlier on a 1M window. Arrows below. |
| 4 | 19 tools / 33.6 KB schema on every profile; `ea` carries the full `hermes-*` set on seven platforms | Sam's call: which toolsets each role needs |
| 5 | 48 skills on the builder, 8 used in 30 days; 45 on `admin`, 7 used | Sam's call: which the builder can live without |
| 6 | `state_meta` is 46% (builder) and 69% (`admin`) of the database, almost all gateway admission cache | Hand to thread 7 with the table split in the report |
| 7 | Nothing older than 90 days on any profile | Policy undecided; not urgent, see the store section |

## Two suggestions checked against the running system

Sam raised them on 27 November, from outside the estate. Both are already the design; the numbers
are what matters.

**1. Lazy-load skills and tool schemas.** Already the architecture, and the saving is banked:

- Skills: 48 `SKILL.md` files on the builder, bodies 20–36 KB each; what loads is a 3,704-char
  index (77 bytes a line). A body loads only when `skill_view` is called — `insights` shows 14
  loads in thirty days.
- Tools: 19 schemas inline, 33,628 bytes; the other 20 — browser, computer use, cron, sessions,
  process, todo, TTS and the ten desktop-UI tools — sit behind `tool_search` and load on the call
  that needs them.
- No MCP servers are configured on this machine at all (`mcp_servers` is commented out in
  `config.yaml`), so no Microsoft Graph schema is being injected anywhere. Graph work happens in
  the browser under `microsoft-365-web`.

So there is nothing to implement here. The remaining rent is the index itself, which is item 5.

**2. Loop and retry caps.** Already in `config.yaml`, and measured:

- `tool_loop_guardrails` warns after 2 exact failures / 3 same-tool failures / 2 idempotent
  no-progress results, and hard-stops at 5 / 8 / 5. Hard stops are **off for interactive
  sessions** (a person is there to interrupt) and **on for cron and gateway runs**, where nobody
  is.
- `agent.max_turns: 500`, against the config's own advice of 20–30 for focused work and 50–100
  for open exploration.
- `api_max_retries: 3` at the Hermes level, on top of the OpenAI SDK's own transport retries.

Neither log has ever recorded a guardrail event: `agent.log` on both the builder and `admin`
return zero hits for loop-guard, non-progress or hard stop. No runaway loop has happened here.

The one number worth acting on is `max_turns`. The builder's worst session — the 351M marathon —
made **505 tool calls**, which is at the ceiling and about five times what the config recommends
for exploratory work. Lowering it to ~150 would have bounded that session without touching normal
days (average is 87 tool calls a session). That is a cheap, mechanical cap and it is a different
lever from the soul, the skills and the threshold: it limits one session's length by rule rather
than asking the model to notice. Sam's call, because a legitimate long task would hit it.

## Where this thread stops, 27 November

Parked, not closed. The reason to stop: everything still on the list needs evidence that only
running sessions under rule 8 can produce, or a call from Sam that is not urgent.

**The wait condition.** Come back when there is a fortnight with rule 8 live, or two sessions of
comparable work run in separate sessions. Then re-run `hermes insights` for all three profiles and
subtract the baseline above. What to look at, in order: messages per session (the honest predictor
of spend), the split between `local` and everything else, and whether any single session passes
~200 messages again.

**What is deliberately not waited on.** None of these need the fortnight, and any of them can be
done in a shorter session:

- Item 3, the compaction threshold (0.50 → 0.35 / 0.15). Sam's call; the arithmetic is above.
- Item 4, toolsets — the largest fixed cost at 33.6 KB of schema per request.
- Item 5, skills — 48 installed, 8 used.
- `agent.max_turns: 500` → ~150, the mechanical cap that would have bounded the 351M marathon.
- Items 6 and 7 go to thread 7's maintenance pass, which already measures; the table split is the
  new requirement.

**What must not be claimed when it is picked up.** Rule 8 has never fired yet: no session has
ended with it live and been observed to offer a fresh chat. The first evidence will be a session
that says so. Until then the item is "live in the souls and prompts refreshed", not "working".

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
