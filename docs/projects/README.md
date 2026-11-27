# Five threads, one page each

Every open thread has a checkpoint with the same four parts: where it stands, what
finished looks like, the remaining work in order, and what only Sam can answer. Start at
the checkpoint, not the brief, when picking something up.

| # | Thread | Checkpoint | State | Next action |
|---|---|---|---|---|
| 0 | OneDrive will not hand over files | `checkpoint-onedrive.md` | Resolved 26 Nov: hydrated, one stuck file | Pin policy, then close |
| 1 | Profile set-up interview | `checkpoint-interview.md` | Done except the dry run | Book the dry run |
| 2 | Events supplier knowledge base | `checkpoint-events-suppliers.md` | Brief done, nothing built | Fix hydration, then build the list |
| 3 | Travel consultant support | `checkpoint-travel-support.md` | Brief done, waiting on design | Sam's five topics, then a pilot |
| 4 | Weekly whereabouts note | `checkpoint-whereabouts.md` | Running, scheduled, rehearsed | One access test by an ordinary employee |
| 5 | Pooling worked profiles into the baseline | `checkpoint-distillation.md` | Parked, nothing built | Start after profiles have been worked for a month |
| 6 | Protecting keys across the estate | `checkpoint-credentials.md` | Parked, not started | Only when a trigger in that file is met |
| 7 | Profile maintenance and the soul refresh | `checkpoint-maintenance.md` | Mechanism known (`refresh-prompts`), nothing built | Write the refresh step into the maintenance pass |
| 8 | Is everyone's OneDrive syncing? | `checkpoint-sync-health.md` | Raised, nothing built | Sam's answer on tenant-level sync reports |

Work one at a time, top to bottom. Thread 0 first because it unblocks 2 and 3, then 1
because it is nearly finished and gates every future profile.

**One session per thread.** `session-starters.md` holds a first message for each thread that can
be pasted into a fresh chat, and the three-line routine: read the index and the checkpoint, work
only that thread, update the checkpoint before stopping. A 600-message session costs roughly six
times what six 100-message sessions cost for the same work.

Out of scope here, and owned by the builder workstream: naming rules beyond the label,
telemetry on which skills get used, and pooling improved skills back into the baseline.
The naming rule itself is D22 and D31 in `docs/decisions.md`.

## The briefs behind them

- `events-suppliers.md` — research and recommendation for the supplier knowledge base:
  three competing supplier records, paperwork remade per event, a SharePoint list plus a
  documents library with closed vocabularies and an append-only rates list.
- `travel-support.md` — research and recommendation for the consultant assistant: an
  answer needs three places at once, so five curated topics with owners and a written
  refusal rule come before any platform choice.

Both were produced on 25 November 2026 and both mark document contents UNKNOWN, because
of the hydration fault above. That is honest rather than incomplete: nothing was inferred
from a filename that was never opened.

## A security note worth acting on separately

`TRIBE GROUP - TRIBE Travel/XXX - KELLY to review what to keep/Copy of Passwords (002).xlsx`
is a credential file in a live folder. By decision it stays where it is and no agent may
open it: see `config/exclusions.txt`, D30, and `scripts/scope_check.py` for what currently
matches.
