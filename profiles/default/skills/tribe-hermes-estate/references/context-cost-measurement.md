# Measuring what a profile costs

Two bills, measured separately. The fixed prompt is paid on every request; the session total is
paid for history. Do both before proposing a change, and write the numbers into the thread's
checkpoint as you take them.

## The fixed prompt — every request

```bash
hermes prompt-size --json                     # active profile
hermes -p admin prompt-size --json            # another profile
```

Offline, no API call. Returns `system_prompt.chars`, `skills_index.chars`, `memory.chars`,
`user_profile.chars`, and `tools.count` with `tools.json_bytes`, plus a per-skill
`index_line_bytes` breakdown.

- **`tools.json_bytes` is normally the largest block** — one tool schema set outweighs the whole
  skills index several times over, and the system prompt too. Trimming a toolset is therefore
  worth more than curating skills, which is worth more than the soul.
- **`--platform gui` reports 0 tools and a 0 skills index**: it does not model the desktop app's
  prompt. Quote the default `cli` figures only, and never read the `gui` zeros as "the desktop
  loads nothing".
- A skill costs roughly 70–80 bytes of every request even when it is never loaded; compare the
  count of `SKILL.md` files against `insights`' distinct skills loaded to price the dead weight.
- **Lazy loading is already the architecture**, so do not propose it. Skills load as an index
  (3.7 KB for 48 skills) and a body only on `skill_view`; the tool registry ships a subset inline
  (19 schemas) and defers the rest — browser, computer use, cron, sessions, process, todo, TTS,
  the desktop-UI tools — behind `tool_search`/`tool_describe`. Check `grep -n 'mcp_servers'
  config.yaml`: commented out means no MCP tool schema exists at all, so a concern about
  "Microsoft Graph schemas in every prompt" has no target on this machine.
- `prompt-size` takes the profile's config as it stands, so re-run it after a config or soul
  change — it is the cheap before/after for items that would otherwise be argued about.

## The running bill — history

```bash
hermes insights                 # active profile
hermes -p <profile> insights    # another
```

Read the **platform** table, not the headline. `Total tokens` counts cached re-reads of the
whole prompt each turn, so it grows with the square of session length: one marathon `local`
session dominates the total while `cron`, `subagent` and `oneshot` runs are noise. Name the
specific session size when recommending a new session per thread, and compare like with like
(two thread-sized sessions against the marathon), never the 30-day total.

Order of work when the ask is "cut spend": short thread-scoped sessions, then tool-output
discipline, then fewer tools per profile, then fewer skills, then the soul, then compaction.
That is the order the measured sizes put them in — the tool schema dwarfs the skills index,
which dwarfs the soul — not the order they feel like. The measured shape of the problem: one
600-message chat cost 351M tokens where six 100-message chats cost roughly a sixth of that,
and two marathon local sessions were 562M of about 728M across the builder and `admin`, with
cron runs at 2M and subagents at 7M. The store on disk only grows — the builder's `state.db`
was 28 MB over 3,340 messages, `admin`'s 36 MB over 1,881 — and is managed with
`hermes sessions archive` (hide), `prune` (delete) and `optimize` (FTS merge + vacuum).

## The store — split the tables before believing the size

```bash
cd ~/.hermes/profiles/<name>          # or ~/.hermes for the builder
sqlite3 state.db "select name, round(sum(pgsize)/1048576.0,2) mb from dbstat group by name order by mb desc limit 6;"
sqlite3 state.db "select case when key like 'gateway.admission%' then 'gateway.admission' else 'other' end p, count(*), round(sum(length(value))/1048576.0,2) mb from state_meta group by p order by mb desc;"
sqlite3 state.db "select role, count(*), round(sum(length(content))/1024.0,1) kb from messages group by role order by kb desc;"
```

- `state_meta` can be the majority of the database and is almost entirely
  `gateway.admission.result.*` cache rows. `hermes sessions prune` does not touch them, so a
  report that prints only a total sends the reader to trim transcripts to fix a cache table.
  Print the table split in any watch line you write.
- The `messages` group-by is the honest version of "what is this conversation made of": tool
  rows carry most of the bytes, the person's own words a few per cent. That is the argument for
  writing large results to a file with a count printed, and it survives being re-measured.
- Session age lives in `started_at` as a REAL epoch. There is no `created_at` column; a query
  using one fails with `no such column`.

## What the person can look at themselves

The measurement above is for deciding; a person who asks "how full is this chat" should be
pointed at the product, not quoted a figure out of chat.

- **Desktop:** the status bar is the thin row along the bottom edge of the window
  (`data-slot="statusbar"`). It carries a context meter — `[▇▇▇░░] 5%` — and **the meter is off by
  default**: right-click the bar and tick "Context meter". Clicking the meter opens a popover with
  used/max tokens, percent full, a compression count and the split by category (conversation,
  tools, system, memory). Telling someone "the app shows your context" without the right-click
  step sends them looking at a bar that has nothing on it.
- **CLI/TUI:** `/context` draws a 20×5 glyph grid where each cell is about 1% of the window, then
  the same breakdown as text. `/context all` adds every category.
- **Do not patch the app for severity colouring.** The colours in the popover belong to the
  categories, not to how close the session is to compaction, so a green/amber/orange/red gauge is
  a threshold function over `context_percent` in one component — but the desktop runs from a built
  bundle under `apps/desktop`, so the patch is lost on the next `hermes update`. D40 in
  `docs/decisions.md` records the decision and the bands (green <25%, amber 25–35%, orange 35–50%,
  red ≥50%, anchored to `compression.threshold`) if it is ever built upstream.

Before proposing to build any gauge, counter or alert, read what the installed app already
ships: `grep -rln 'context_percent' apps/desktop/src` and the panel beside it cost one call and
answer the question that "is this easy to build" is really asking.

## The meter is for the person, not for the agent

Nothing agent-side reads the occupancy figure. `context_used` / `context_max` are produced in
`agent/context_breakdown.py` for the status-bar popover and `/context`, and never enter the
system prompt — `grep -rn 'context_used\|context_max' agent/*.py` returns only that module. So a
soul rule about watching spend is costing zero tokens to follow, and there is nothing to save by
"reusing the meter instead of recalculating it". Wiring the number in costs the other way: a
per-turn line is ~15 tokens on every request of every session, permanently, or the app patch D40
refuses. It is also the wrong trigger — a new session is cheapest at a task boundary, which a
rule can see by reading the conversation, and the host's compaction threshold is the automatic
reaction to real pressure. Say this plainly when asked; the question sounds like an optimisation
and is actually a cost.

## Session ages before proposing housekeeping

```bash
sqlite3 state.db "select sum(case when (<now> - started_at) > 365*86400 then 1 else 0 end) gt1y, sum(case when (<now> - started_at) > 90*86400 and (<now> - started_at) <= 365*86400 then 1 else 0 end) d90_365, count(*) total, min(datetime(started_at,'unixepoch','localtime')) oldest from sessions;"
```

Substitute an epoch for `<now>`. Count what an archive/prune policy would actually touch before
recommending it: on a young estate the answer is zero rows, which makes the policy anticipatory
and the growth you are actually seeing the thing worth reporting.

## Caps that already exist — read the config before proposing one

Both caps an outside suggestion usually names are already implemented. Quote the values, check
whether they have ever fired, and only then talk about changing a number.

- `tool_loop_guardrails` in `config.yaml`: warnings on at 2 exact failures / 3 same-tool failures
  / 2 idempotent no-progress; hard stops at 5 / 8 / 5, **off for interactive sessions** (a person
  is there to interrupt) and on for cron and gateway runs where nobody is. `hard_stop_enabled:
  false` with `non_interactive_hard_stop_enabled: true` is deliberate, not an oversight.
- `agent.max_turns: 500` against the config's own advice of 20–30 for focused work and 50–100 for
  exploration, with `api_max_retries: 3` above the SDK's transport retries.
- Whether a guardrail ever fired: `grep -ic 'loop guard\|non-progress\|hard stop'
  ~/.hermes/logs/agent.log` (and the same file under a profile's `logs/`). Zero is the normal
  answer on this estate and is worth saying — a runaway loop is a thing to plan for, not a thing
  that has happened.
- `max_turns` is the one number that earns a change: the worst builder session made **505 tool
  calls** against a 500 cap and an 87-call average, so a cap near 150 bounds the outlier and
  leaves a normal day untouched. Name that trade rather than agreeing with the premise.

## Did compaction fire, and what a lower threshold is worth

The store cannot answer this. It keeps the full transcript and writes no summary rows, so a
`messages` query proves nothing either way — a count of `system` rows comes back zero whether or
not compaction ran. The log does answer it:

```bash
grep 'context compression started\|context compression done' ~/.hermes/logs/agent.log
```

One pair of lines per event: `messages=` and `tokens=` on the way in, `messages=A->B` and
`rough_tokens=` on the way out, then an `attempt telemetry` JSON with `aux_prompt_tokens` — the
summary call's own bill — and `effective_aux_context`, which is the real window the threshold is
a fraction of. Read that field instead of assuming 128K; on a 1M window a 0.50 threshold fires at
524,288 tokens, which is not what "half the context" sounds like.

**The ratio knobs are nearly inoperative on a 1M window.** A fraction of a million tokens is
hundreds of turns, so lowering `threshold` from 0.50 to 0.35 barely moves when it trips. The
lever for that case is the absolute cap that already exists and ships unset:
`compression.threshold_tokens`, which fires at whichever is lower, ratio or count, and survives
model switches.

Price the change off the session's own messages as well as the log. Anchor a characters-per-token
ratio on the log pair (`tokens=` in against summed `length(content)` for that session at that
timestamp), then walk the session's messages in order to find which tool call each candidate
threshold would have fired at. Measured on the 351M marathon (2,321 messages, 1,004 tool results,
1.555 chars/token), it reads:

| prompt reaches | tool call | of the 1M window |
|---|---|---|
| 100K tokens | 24 | 10% |
| 150K tokens | 63 | 15% |
| 200K tokens | 127 | 20% |
| 367K — `threshold` 0.35 | 286 | 35% |
| 525K — `threshold` 0.50, where it fired | 510 | 50% |

Two things follow. Saying "a lower threshold would have caught it earlier" is only true against
the ratio version: 0.35 lands at call 286 of 1,004, halfway through the spend. An absolute
`threshold_tokens` of 150–200K lands at calls 63–127, before most of the bill, and is the honest
answer to that intuition. And the trade is real and must be said out loud: compacting at 20% of
the window discards context the model could still have used, in exchange for capping what every
later turn re-reads, at the cost of one summary call (tens of thousands of prompt tokens) each
time.

Change one profile first, and not the profile running the comparison: the profile left at the old
value is the control that makes the fortnight comparable.
