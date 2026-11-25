# Checkpoint: OneDrive will not hand over files

> **Start here before either knowledge project.** This is not a side issue. It blocks
> reading any supply or travel document, so it blocks the import, the content work and
> any grounding. Fixing it is the cheapest thing on the list.

## What is wrong

Files carry the `dataless` flag: OneDrive keeps them online-only and is meant to fetch
one the moment something opens it. Instead every read fails instantly with
`Resource deadlock avoided`. That is the file provider refusing, not a slow download.

Measured on 25 November 2026:

- Share Drive: 3,463 of 3,714 files unreadable.
- Travel library: 1,093 of 1,112 unreadable.
- One spreadsheet tested by hand: `cp` failed, and a Python read failed in 0.0 seconds.

The client is running, version 26.213.1101, three processes including the file provider.
Its last log entry is 12 November, and that log shows a failed update download with a
network error. So the engine is up but not doing the one job needed.

## Definition of done

1. A script reads one file from `SUPPLIERS/` and one from the Travel library without
   error.
2. The unreadable count is re-measured and is zero, or the remaining set is deliberate.
3. A pin policy is written down: which folders stay on the device and which do not.
4. The cause is recorded, so the next machine does not spend a morning on it.

## Remaining work, in order

1. Quit OneDrive from the menu bar and relaunch. Re-test one file.
2. If unchanged, sign out and sign back in. Re-test.
3. If unchanged, reset the app using the reset command inside the bundle. This
   re-registers the provider and re-syncs, takes a while, and needs Sam's explicit yes
   because it re-downloads and can surface conflict copies.
4. Once reads work, pin `SUPPLIERS`, `WORKFLOW` and the travel `DOCS` folders, and leave
   client archives online-only.
5. Re-measure the unreadable count and update both knowledge briefs, which currently
   mark most contents unknown.

## What it needs from you

- Permission to reset the client if the first two steps do not fix it.
- A decision on which folders are pinned locally. Everything is 19 GB against 804 GB
  free, so the answer can be generous, but client archives need not be held.

## Why this matters beyond convenience

Every knowledge base decision so far was made from filenames and structure because
contents could not be opened. The structure is enough to design the lists, but not
enough to import real values, and not enough for an assistant to ground an answer. Until
this is fixed, both projects are designing blind from the neck down.
