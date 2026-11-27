# Starting a session per thread

One conversation per thread. A session re-sends its whole history on every turn, so a
600-message chat costs about six times what six 100-message chats cost for the same work.

Each block below is a first message to paste into a fresh chat. Every one assumes the same
opening: the session loads the estate skill, reads the index, then reads its own checkpoint.
Each session ends by editing that checkpoint — three lines: done, next, blocked.

## The routine, in three lines

```
Morning: open a fresh chat and paste: "Read docs/handover-today.md, then start on the first thread."
Start:   read docs/projects/README.md, then the thread's checkpoint. Work only that thread.
During:  say so if the work moves to a new topic or the session passes a hundred messages.
End:     update the checkpoint. Three lines. Then stop.
```

`docs/handover-today.md` is rebuilt at 07:30 each day from the repo alone — yesterday's changed
files, every open thread with its next action, and anything carried forward.

---

## Thread 0 — close it

```
Load the tribe-hermes-estate skill. Read ~/tribe-hermes-library/docs/projects/checkpoint-onedrive.md.
The pin policy is decided: pinned = SUPPLIERS, WORKFLOW, MASTER TEMPLATES & DOCS, PROPOSALS,
ADMIN, Travel's TRIBE TRAVEL - DOCS, CLIENT INFO, Supplier - *, DESTINATION INFORMATION and the
three Hermes folders; online-only = EVENTS CLIENTS, DESIGN CLIENTS (Dani), FINANCE, XXX - KELLY
and XXX - LUCI review folders. Write that into the checkpoint, note the one stuck PowerPoint,
and close the thread.
```

Produces: the pin policy in the checkpoint, thread 0 marked closed.

## Thread 2 — events supplier knowledge base

```
Load the tribe-hermes-estate skill. Read ~/tribe-hermes-library/docs/projects/README.md, then
checkpoint-events-suppliers.md and events-suppliers.md. Hydration is resolved, so the folders
read cleanly now. Propose phase one: what the list holds, which fields, who owns it, and what
evidence from the real files supports each decision. Do not build until I say yes.
```

Produces: a phase-one plan grounded in the actual supplier folders, with the UNKNOWNs named.

## Thread 3 — travel consultant support

```
Load the tribe-hermes-estate skill. Read docs/projects/travel-support.md and its checkpoint.
It is waiting on Sam's five topics before a pilot scope exists. Ask me for the five topics one
at a time, record them, and sketch the pilot from the answers. Nothing built.
```

Produces: five topics recorded, a pilot scope sketch.

## Thread 4 — whereabouts note

```
Load the tribe-hermes-estate skill. Read docs/projects/checkpoint-whereabouts.md. The note runs
Mondays at 11:00 and is rehearsed. What remains is one access test by an ordinary employee.
Tell me exactly what to ask them to do and what "working" looks like, then record it.
```

Produces: a test script a colleague can follow in five minutes.

## Thread 5 — pooling worked profiles

```
Load the tribe-hermes-estate skill. Read docs/projects/checkpoint-distillation.md, then
docs/architecture-loop.md. Note what the weekly share job already produces in
baseline/soul-rules/ and that exact matching failed to pair admin's and ea's rule 1. Design the
pre-filter and the model-comparison step, and stop at a proposal.
```

Produces: a design for the comparison step, not code.

## Thread 6 — keys across the estate

```
Load the tribe-hermes-estate skill. Read docs/projects/checkpoint-credentials.md. Parked until a
trigger is met. Check whether a trigger has been met yet; if not, say so in one line and stop.
```

Produces: usually nothing. That is the correct answer.

## Thread 7 — profile maintenance and the soul refresh

```
Load the tribe-hermes-estate skill. Read docs/projects/checkpoint-maintenance.md. Build the
maintenance pass as a skill for the delegated builder: measure soul, memory, skill count and
state.db size; flag; propose; never apply. Include the refresh step using
`hermes sessions refresh-prompts`.
```

Produces: the maintenance skill, ready to test on this machine.

## Thread 8 — is everyone's OneDrive syncing

```
Load the tribe-hermes-estate skill. Read docs/projects/checkpoint-sync-health.md. Sam has no
admin role; the tenant view is closed, and the questions for Kate are prepared separately.
Finish the per-machine check as a script: dataless count, sample reads, the two counters from
SyncDiagnostics.log, counts only.
```

Produces: a script the delegated builder can run weekly.

---

## Notes

- Do not paste two threads into one session "to save time". That is the pattern that produced a
  351M-token chat.
- If a thread turns out to need another, start it fresh and leave a line in both checkpoints.
- `hermes chat -q "<the block above>"` runs one of these as a terminal one-shot if you would
  rather not open the desktop for it.
