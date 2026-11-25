# Checkpoint: events preferred supplier knowledge base

> **Start here tomorrow.** Read the brief at `docs/projects/events-suppliers.md`, then
> this page. The first job is not building: it is fixing OneDrive hydration, because
> no supplier file can be opened until it is. See `checkpoint-onedrive.md`.

## Where it stands

The brief is written and researched: `docs/projects/events-suppliers.md`. Nothing has
been built and nothing on OneDrive has been changed.

What exists today, from files actually seen: `SUPPLIERS/` is 38 folders with no single
organising axis, mixing cities, countries, venues, categories and one person's name,
plus `Preferred Suppliers list- 2025.xlsx` last saved in August 2026 and a shortcut
implying a second copy. Per-event paperwork repeats across 43 client folders, 32
supplier folders, 23 agreements, 50 confidentiality agreements. Insurance is a filename
convention, not a register.

Blocker: 3,463 of 3,714 files in the Share Drive are online-only placeholders that fail
to open, so the contents of the master list are unknown. The recommendation does not
depend on reading them, but the import does.

## Definition of done

1. One Suppliers list and one Documents library on the Tech site, inside the existing
   licence, with closed term sets for category, region, tier and status.
2. Prices held as an append-only rates list, never overwritten, with a current view
   filtered on today.
3. One named owner per record, a review cadence, and reminders at 60 and 30 days before
   an insurance or contract expiry.
4. The 2025 master sheet retired with a stated date, so two lists stop competing.
5. A weekly change report a person reads, produced from file metadata alone.
6. The kit and the report published to `Hermes Library`, and the brief updated with
   what was actually built.

## Remaining work, in order

1. Fix hydration, then harvest the real row count and columns from the 2025 list.
2. Build the Suppliers list with 12 to 15 fields and the four term sets, plus the
   Documents library with content types.
3. Import the 2025 list, one row per supplier, and mark every row with its source file.
4. Add the rates list and a current view. Backfill only prices that are dated.
5. Add the expiry reminders and name an owner per record.
6. Retire the duplicate lists and say which one died.
7. Add the change report, metadata only, before any write automation.

## What it needs from you

- Who owns supplier data: Jodie, Vanessa, or an operations coordinator.
- What qualifies a supplier as Preferred, and who signs that off.
- Whether rates can be seen by all events staff, or only leads and finance.
- Whether Travel's `Supplier - X` folders merge in, or stay a separate record set.
- Which Microsoft 365 plan is held, and whether Power Apps or premium Power Automate
  is licensed, since the expiry flow depends on it.
