# Checkpoint: OneDrive will not hand over files

> **Resolved for reading, 26 November 2026.** One stuck file and the pin policy remain — see
> the resolution section below and the remaining work. The estate-wide version of this problem,
> where a colleague's machine looks fine and isn't, is thread 8, `checkpoint-sync-health.md`.

## Resolved, 26 November 2026

Sam downloaded the working set on the machine during the morning. By 16:30 the estate is
hydrated: **199,041 files, one dataless stub left.** A read test across the four folders that
failed this morning:

| Folder | Files read | Failures |
|---|---|---|
| EVENTS CLIENTS | 123,501 | 1 |
| DESIGN CLIENTS (Dani) | 31,618 | 0 |
| FINANCE | 549 | 0 |
| Travel / XXX - KELLY to review | 2,382 | 0 |

The single failure is
`EVENTS CLIENTS/AFG/AFG Fintelligence/2024_Conference Gold Coast/QT Sponsorship Options.pptx`
— 16.8 MB, still a stub, and not progressing on its own over 30 seconds. It needs a manual
touch: open it once in PowerPoint, or set "Always keep on this device" on the file.

Definition of done, against the four items above: (1) reads work — done; (2) re-measured and
the remaining set is one known file — done; (3) the pin policy is still unwritten, in the
remaining work below; (4) the cause is recorded in this file.

## What is wrong

Files carry the `dataless` flag: OneDrive keeps them online-only and is meant to fetch
one the moment something opens it. Instead every read fails instantly with
`Resource deadlock avoided`, in about zero seconds. That is the file provider refusing,
not a slow download: a file already on disk reads fine, a stub never does.

Measured again on 26 November 2026, whole tree, `st_flags & 0x40000000`:

| Library | Files | Dataless |
|---|---|---|
| Share Drive | 194,848 | 52,698 |
| TRIBE Travel | 4,124 | 1,419 |
| TRIBE Group Tech | 141 | 0 |

Where the weight sits, and where it does not:

| Folder | Files | Dataless |
|---|---|---|
| Share Drive / EVENTS CLIENTS | 154,555 | 48,709 (31%) |
| Share Drive / DESIGN CLIENTS (Dani) | 37,817 | 3,605 (9%) |
| Travel / XXX - KELLY to review what to keep | 2,498 | 1,331 (53%) |
| Share Drive / FINANCE | 549 | 385 (70%) |
| **Share Drive / SUPPLIERS** | **445** | **0** |
| **Share Drive / WORKFLOW** | **13** | **0** |
| **Travel / TRIBE TRAVEL - DOCS** | **24** | **0** |
| **Travel / CLIENT INFO** | **816** | **4** |

Read test, 26 November: SUPPLIERS 445/445 read, WORKFLOW 13/13, TRAVEL - DOCS 24/24,
CLIENT INFO 812/816 (the four failures are passport images, which no agent may open
anyway).

**Why this changed.** On 26 November Sam downloaded the working set to the machine, which is
why the picture below is different rather than contradictory. The 25 November note recorded
3,463 of 3,714 Share Drive files unreadable; that was the state of a tree that had not been
brought down, where most files were stubs and large parts of the tree were not even
enumerated. After the download the same scan sees 194,848 files, and the folders the two
projects need read cleanly. The earlier numbers were a measurement of a different state, not
a mistake.

The client is running, version 26.213.1101, four processes including the file provider.
Its newest log file is dated 12 November, so the engine is up but has stopped logging and
is not doing the one job needed.

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
