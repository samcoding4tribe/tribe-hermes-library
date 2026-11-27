---
name: session-hygiene
description: "Keep a session cheap: notice growth, advise, hand over."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [tokens, cost, sessions, handover, context]
    related_skills: []
---

# Keeping a session cheap

A session re-sends its whole history on every turn, so cost grows with the square of its
length. One 600-message session costs about six times what six 100-message sessions cost for
the same work. This skill is how the assistant notices that, says so, and moves the work to a
clean session without losing anything.

## When to raise it

Say something in one line — not a lecture — when any of these is true:

- **The task just finished.** The natural boundary. "That's thread 4 done; start the next one in
  a fresh chat and I'll read the checkpoint."
- **A new topic has started** inside a session that already has real history. The old context is
  now baggage.
- **The session has been running across days**, or past roughly a hundred messages.
- **A branch about to be explored is expensive**: reading many documents, fetching many pages,
  scraping, or a long search that will return a lot. Warn before starting, and offer the cheaper
  shape: a subagent, a file, a narrower question.

Do not raise it mid-task, and do not raise it twice in one session.

## What to say

One or two lines, with a number if it is easy:

> This chat is at about 400 messages, so every turn is re-sending a lot of history. Worth
> starting a fresh one for the supplier work — here is the handover.

Offer the handover rather than just the reset. The person should never feel they are losing the
thread.

**Recommend, never open.** The assistant does not create or switch sessions itself — there is no
supported way to open a new chat and put a prompt in it, and doing it through UI automation is
fragile. What it does instead: say the new thread belongs in a new session, and hand over a
document so the next session starts with everything it needs.

## The morning handover

`scripts/daily_handover.py` writes `docs/handover-today.md` from the repo alone — no model, no
tokens: what changed yesterday (grouped by folder), every thread still open with its next
action, and anything the previous handover carried forward. A scheduled job runs it at 07:30 and
publishes it with the library.

So a day starts the same way every time: **open a fresh chat and paste one line** —

> Read docs/handover-today.md, then start on the first thread.

That is the whole of the morning routine. Nothing from yesterday's conversation needs to come
with it, because the checkpoints and the changed-file list already did.

## The handover, which is the actual mechanism

Before ending, write the state where the next session will look:

1. **The thread's checkpoint** in `docs/projects/` — what is done, what is next, what is blocked.
   Three lines changed is enough.
2. **Anything a person may need to read**: a dated note, not a transcript.
3. Then start the new session by reading the projects index and that checkpoint.

`--continue` is for continuing the same task. A new task starts clean.

## How to measure when asked

```bash
hermes insights                 # last 30 days: sessions, messages, tokens, cost, top tools
hermes -p <profile> insights    # the same for another profile
hermes sessions list            # recent sessions with message counts
```

Two numbers explain almost all spend: **which sessions are long**, and **which tools are called
most**. In practice the long-running chat is the whole bill; cron and subagents are noise.

## Cheaper shapes for the same work

- **Subagent for volume.** Research that returns thousands of tokens goes to a subagent; only its
  summary returns.
- **Write big results to a file**, print the count and the path. Never dump a scan into the
  transcript — one bad tool result can outweigh the entire system prompt.
- **Narrow the question before searching.** "Which supplier files mention cancellation terms"
  beats "read the suppliers folder".
- **Split by thread, not by item.** One conversation per piece of work; not one per checkbox.

## What not to do

- Do not warn about cost on every turn. It becomes noise and gets ignored.
- Do not silently drop context to save tokens; say what you are leaving out.
- Do not start a fresh session without a checkpoint. Losing the state costs more than the tokens.

## Reference

Measured numbers for this estate — where tokens actually go, what each layer costs, and the
settings that govern compaction — are in `docs/context-budget.md` in the estate repo:
`compression.threshold`, `target_ratio`, `platform_toolsets`, and the session store's growth.
