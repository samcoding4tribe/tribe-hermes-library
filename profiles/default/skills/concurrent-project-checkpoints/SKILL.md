---
name: concurrent-project-checkpoints
description: "Checkpoint several open threads so each can be finished."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [projects, checkpoints, handover, multi-thread, decisions]
    related_skills: [knowledge-base-over-documents, recurring-visual-reports]
---

# Checkpointing Concurrent Projects

## When to Use

- The user is running three or more conversations or projects at once and says so, or
  asks which one to pick up.
- They ask for a checkpoint, a handover, or "somewhere we can take this to the end".
- They come back after a break and the thread list lives only in their head.
- A long build has several independent tracks and only one can be worked at a time.

Not for a single task with steps (use a todo list), and not for a recurring job's
runbook (that belongs in the skill for that job).

## The shape: one index, one page per thread

```
docs/projects/
  README.md                       # the index: thread, state, next action, in order
  <topic>.md                      # the brief: research and recommendation
  checkpoint-<topic>.md           # this page: state, done, work left, needs you
```

The index is a table, because a user asking "how many are there now?" wants a table, not
prose. Columns: number, thread, checkpoint filename, state, next action.

## What every checkpoint carries, in this order

1. **Start here.** One block at the top naming the file to open next and the first
   action. When the user says "tomorrow", that block is the whole handover.
2. **Where it stands.** What exists, with real paths; what has been built and what has
   not; the condition that blocks it if there is one. Facts that were measured, not
   remembered.
3. **Definition of done.** Numbered, checkable, and short. This is what stops a thread
   becoming permanent: if it cannot be numbered, the thread is not understood yet.
4. **Remaining work, in order.** Numbered steps with the dependency order explicit.
5. **What it needs from you.** Only the decisions, permissions and hands that the agent
   cannot supply. Never a list of things the agent could simply do next.

Strike items in place when they get done, with the date. A checkpoint that is not
updated becomes a lie within a week, and the user stops trusting the file.

## Working order

Sort by unblocking, not by interest: a shared blocker becomes its own thread rather than
a footnote in two others, then whatever is nearly finished and gates future work, then
the long builds. Say the order in the index and work top to bottom, one at a time,
because the point of the exercise is that only one thing is in flight.

Name what is out of scope and whose workstream it belongs to. A thread that keeps
re-entering the list from another conversation is the usual cause of "how many are we
doing?".

When the user redirects mid-conversation — "we are getting sidetracked" — the tangent
becomes a parked thread: write the page, add the row with state Parked, say where it is in
one line, and go back to the thread they named. Finishing the tangent anyway, or defending
it at length, is what makes the user stop trusting the list.

## Pitfalls

- A checkpoint that restates the brief is a second brief. Cite it by filename and spend
  the page on state, finish line and blockers.
- A blocker that affects two threads is one thread of its own. Filed inside both, it gets
  re-diagnosed twice and owned by neither.
- Never list as "needs you" anything the agent can do with the tools it has. That list is
  the user's time; filling it with research tasks wastes the one resource they gave you.
- Checkpoints written after a long session are worth more than a summary in the chat,
  because the chat is not where the next session looks. Write the file, then tell the
  user in one line where it is.
- Say plainly which threads are blocked on a decision versus blocked on a machine fault.
  The first needs a conversation, the second needs ten minutes with the client, and
  mixing them makes the whole list feel unfinishable.
- When a checkpoint's next action turns out to be the user's homework (design work, five
  topics, a name), say so and stop. Guessing at it produces a build they then have to
  unpick.
