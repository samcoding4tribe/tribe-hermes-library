# Checkpoint: events preferred supplier knowledge base

> **27 Nov 2026: hydration is fixed and the contents are known.** The first job — reading the
> 2025 list — is done: 176 name rows, 165 distinct suppliers, 14 category sheets, and a fourth
> supplier record in `ADMIN/Client & Supplier Database/`. What it holds, the proposed 16 fields,
> the owner evidence and the five decisions it needs are in
> `docs/projects/events-suppliers-phase1.md`. Nothing is built; the phase-one proposal is waiting
> on Sam's yes. `checkpoint-onedrive.md` is resolved and no longer blocks this thread.

## Where it stands

The brief is written and researched: `docs/projects/events-suppliers.md`. The phase-one proposal
is written: `docs/projects/events-suppliers-phase1.md`. Nothing has been built and nothing on
OneDrive has been changed.

What exists today, measured on 27 November 2026 with hydration clean (445 files in `SUPPLIERS/`,
0 dataless; 228 in `ADMIN/`, 0 dataless): `SUPPLIERS/` is 38 folders with no single organising
axis, mixing cities, countries, venues, categories and one person's name, plus
`Preferred Suppliers list- 2025.xlsx` (last saved 4 Aug 2026 by Kate Ashton) and a shortcut that
points at a local OneDrive path on Sarah Adams's machine, not a second master. Per-event paperwork
repeats across 43 client folders, 142 supplier folders, 97 supplier agreement files, 368
confidentiality files and 61 contracts folders. Insurance is a filename convention, not a register,
and the only certificates in the Share Drive are TRIBE's own.

Superseded: the earlier note that 3,463 of 3,714 Share Drive files were unreadable and the master
list's contents were unknown. It was true of the measurement taken before hydration.

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

1. ~~Fix hydration, then harvest the real row count and columns from the 2025 list.~~ Done 27
   Nov: 176 name rows, 165 distinct, 14 sheets, columns `NAME, CONTACT, ROLE/TITLE, EMAIL, STATE,
   PHONE, WEBSITE, Notes` plus `Country` and `CHAIN`. See the phase-one proposal.
2. Build the Suppliers list with 16 fields and the four term sets, plus the
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
