# Checkpoint: OneDrive will not hand over files

> **Closed, 27 November 2026.** Reading was resolved on 26 November; the pin policy was decided
> on 27 November and is written below. One file is still a stub, and by that policy it stays
> one. Everything here is the record, not work in progress. The estate-wide version of this
> problem, where a colleague's machine looks fine and is not, is thread 8,
> `checkpoint-sync-health.md`.

## Pin policy, decided 27 November 2026

**Pinned — kept on this device.**

| Library | Folders |
|---|---|
| Share Drive | `SUPPLIERS`, `WORKFLOW`, `MASTER TEMPLATES & DOCS`, `PROPOSALS`, `ADMIN` |
| Travel | `TRIBE TRAVEL - DOCS`, `CLIENT INFO`, `Supplier - *` (all seven: AERONOLOGY, AIRLINES, CRUISE, HOTEL, SABRE, TRANSFERS, VIRTUOSO), `DESTINATION INFORMATION` |
| Tech | `Hermes Library`, `Hermes WIP`, `Hermes Backups` |

**Online-only — OneDrive may dehydrate these.**

| Library | Folders |
|---|---|
| Share Drive | `EVENTS CLIENTS`, `DESIGN CLIENTS (Dani)`, `FINANCE` |
| Travel | `XXX - KELLY to review what to keep`, `XXX - LUCI to review what  to keep` (two spaces in the folder name) |

**Why these.** The pinned set is what the agent work reads from: supplier records, workflow and
template material, proposals, admin paperwork, travel documentation and client info, destination
notes, and the three Hermes folders the estate itself depends on. The online-only set is event
and design client archives, finance, and the two review folders — read rarely, read by no agent
routine, and the whole of the weight.

**Reading of two ambiguous names.** `ADMIN` and `WORKFLOW` exist in both libraries and the
decision did not qualify them the way it qualified `TRIBE TRAVEL - DOCS`, so the pinned folders
above are the Share Drive ones. Travel's own `ADMIN` and `WORKFLOW` are unpinned. The entire
Travel library is 7.8 GB, so pinning all of it would cost little if that is preferred.

### State measured 27 November 2026

`st_flags & 0x40000000`, counted per folder:

| Set | Files | Dataless | On disk |
|---|---|---|---|
| Pinned set (all 18 folders) | 2,331 | 0 | fully local |
| EVENTS CLIENTS | 154,877 | 1 | 387.8 GB |
| DESIGN CLIENTS (Dani) | 37,817 | 0 | 232.0 GB |
| FINANCE | 549 | 0 | 0.7 GB |
| XXX - KELLY to review | 2,498 | 0 | 1.0 GB |
| XXX - LUCI to review | 120 | 0 | 0.0 GB |

`TRIBE GROUP - Share Drive` is 195,223 files and 639.2 GB on this disk. The Mac has 191 GB free
of 926 GB. The 26 November figure of "19 GB against 804 GB free" was wrong: it described the
library before the working set came down, not after.

**What this means.** The policy is decided but **not applied**, and applying it moves in the
opposite direction from what this file assumed. Nothing needs downloading: the pinned set is
already fully on disk, so pinning is a keep-it-here rule rather than a fetch order. The
online-only folders are also fully on disk today, which is where ~621 GB of the 639 GB sits;
freeing that space is the only action the policy calls for, and it means OneDrive releasing
local copies, not deleting anything from the cloud. That is Sam's yes to give, and it also
decides whether EVENTS CLIENTS stays readable without a re-fetch — which thread 2 depends on.

Two mechanical notes. Pinning is done in Finder with "Always keep on this device" on each
top-level folder; the client's pin state is not readable from the filesystem, so "hydrated" and
"pinned" are not the same measurement and this file only ever claims the first. And this machine
now holds 647 GB of OneDrive content, so it is worth deciding before the disk, not after.

## The one stuck file, still a stub 27 November 2026

`EVENTS CLIENTS/AFG/AFG Fintelligence/2024_Conference Gold Coast/QT Sponsorship Options.pptx`
— 16,853,540 bytes, `dataless` flag still set, unchanged since the 26 November measurement. It
did not come down with the working set and does not fetch on its own.

Under the pin policy it sits in an online-only folder, so a stub is the correct steady state and
this file is not a blocker for any thread. If something needs it: open it once in PowerPoint, or
set "Always keep on this device" on that single file, which fetches it without changing the
folder policy.

## Resolved, 26 November 2026

Sam downloaded the working set on the machine during the morning. By 16:30 the estate is
hydrated: **199,041 files, one dataless stub left.** A read test across the four folders that
failed that morning:

| Folder | Files read | Failures |
|---|---|---|
| EVENTS CLIENTS | 123,501 | 1 |
| DESIGN CLIENTS (Dani) | 31,618 | 0 |
| FINANCE | 549 | 0 |
| Travel / XXX - KELLY to review | 2,382 | 0 |

The single failure is the PowerPoint named above. Read tests on the pinned folders the same day:
SUPPLIERS 445/445, WORKFLOW 13/13, TRAVEL - DOCS 24/24, CLIENT INFO 812/816 (the four failures
are passport images, which no agent may open anyway).

## What is wrong

Files carry the `dataless` flag: OneDrive keeps them online-only and is meant to fetch one the
moment something opens it. Instead every read failed instantly with `Resource deadlock avoided`,
in about zero seconds. That is the file provider refusing, not a slow download: a file already on
disk reads fine, a stub never does. The client was running, version 26.213.1101, four processes
including the file provider, and its newest log file was dated 12 November — the engine was up
but had stopped logging and was not doing the one job needed. Downloading the working set brought
the files down through a path that did work, and reads have worked since.

## Definition of done — all four met

1. A script reads one file from `SUPPLIERS/` and one from the Travel library: done 26 November.
2. The unreadable count re-measured: one deliberate stub, named above.
3. A pin policy written down: above, decided 27 November.
4. The cause recorded: above, so the next machine loses no morning to it.

## If it recurs

Same symptom (`Resource deadlock avoided` in about zero seconds on a file that should be local)
means the provider again, not the network. Quit OneDrive from the menu bar and relaunch; if
unchanged, sign out and back in; only then reset the app, which re-registers the provider,
re-syncs and can surface conflict copies, and needs an explicit yes. What fixed it on this
machine was forcing the working set down, not any of those three. Measure a folder with
`st_flags & 0x40000000` before and after, and never read "hydrated" as "pinned".
