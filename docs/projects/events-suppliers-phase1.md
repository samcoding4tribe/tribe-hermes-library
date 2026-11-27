# Phase one: the events Suppliers list

27 November 2026. Proposed, not built. Read with `events-suppliers.md` (the recommendation) and
`checkpoint-events-suppliers.md` (where the work stands). Every number below was measured on this
machine on 27 November 2026 against `OneDrive-TribeTravelandEvents/TRIBE GROUP - Share Drive`,
with hydration clean: `SUPPLIERS/` holds 445 files, 0 of them dataless placeholders, and `ADMIN/`
228 files, 0 dataless. That is the state the brief could not reach.

## 1. What the list actually holds

The brief counted three competing records from filenames. With the files open there are four, and
they are not the same shape:

| Record | Where | Size measured | Has a category field? |
|---|---|---|---|
| Preferred Suppliers list 2025 | `SUPPLIERS/Preferred Suppliers list- 2025.xlsx` | 15 sheets: a CONTENTS page plus 14 category sheets, 176 name rows, 165 distinct supplier names | No. Category is the sheet name. |
| Supplier Christmas cards | `ADMIN/Client & Supplier Database/Client_Supplier_database_Christmas2020.xlsx`, sheet `SUPPLIER CHRISTMAS CARDS` | 239 contact rows, 177 distinct companies | Yes, free text, 24 values |
| Hotel Directory | `SUPPLIERS/Hotel Directory.xlsx` | 12 city sheets, 129 rows, no header row | City is the sheet name |
| 2022 Hotel Availability | `SUPPLIERS/2022 Hotel Availability.xlsx` | 5 rows of hotel stop-sells | n/a |

Per-event paperwork is heavier than the brief recorded: `EVENTS CLIENTS/` holds 43 client folders,
142 folders matching `*supplier*`, 97 files named `*Supplier Agreement*`, 368 `*confidential*`
files and 61 `contracts` folders.

Three findings that change the design:

1. **There is no second master.** `Preferred Suppliers list- 2025 - Shortcut.lnk` resolves to
   `C:\Users\SarahAdams\Tribe Management\TRIBE GROUP - Documents\Share Drive\SUPPLIERS\Preferred
   Suppliers list- 2025.xlsx` — a path inside a synced OneDrive folder, not a SharePoint copy. So
   the record that "implies another copy" is the same file. The duplicate to retire is the
   Christmas-card sheet and the two hotel files, not a phantom master.
2. **The Christmas-card sheet is the only record with a category field and postal addresses.** It
   is also 90 rows of internal TRIBE Travel contacts wearing a supplier category, and carries
   `Exibition Supplier` next to `Exhibition Supplier` and one row whose category is `0`. Useful as
   a cross-check on category vocabulary; not a source of truth.
3. **The preferred list has no tier, no owner, no ABN, no expiry and no date.** Its columns are
   `NAME, CONTACT, EMAIL, STATE, PHONE, WEBSITE, Notes`, with `ROLE` on the Venues, Tourism Bureau
   and Other sheets and `TITLE` on Hotels, `CHAIN` on Hotels and `Country` on DMC. "Preferred" is
   carried by membership of a file called Preferred, and by free text in Notes on two rows
   (`Preferred supplier. 10% discount…`, `Preferred supplier- negotiatig rebate/discount`).

Two data-quality facts a field list has to absorb: 10 supplier names appear on more than one
category sheet (`Vagary Creative` as stylist and florist, `The Big Group` as caterer and venue,
`Simply Seated` as stylist and furniture hire), so category cannot be one closed value per row; and
the `STATE` column holds 26 distinct values for what is really five states plus overseas —
`VIC, NSW & QLD`, `VIC,NSW,QLD`, `VIC,NSW`, `SYD`, `FNQ`, `HBA`, `TAS-HBA`, `State wide`, `AU`,
`ALL`, `All`, `Queenstown`, `Bali`, `SthEast Asia&Pacific`.

The CONTENTS sheet lists 13 categories; the workbook has 14 sheets. `Tourism Bureau` is missing
from CONTENTS and `Entertainmet` is misspelled there. Neither the sheet list nor the CONTENTS page
can be trusted as the category vocabulary on its own.

## 2. The fields

Sixteen columns. Five of them are deliberately empty on import because no source file holds the
fact — they are the reason the list exists, not a gap in the import.

**Carried from the workbook (11):**

| Field | Source | Filled in 176 imported rows |
|---|---|---|
| Supplier name | `NAME` | 176 |
| Category | sheet name, multi-value | 176 |
| Region | `STATE`, mapped to a term set | ~170 |
| Primary contact | `CONTACT` | 129 |
| Contact role | `ROLE` / `TITLE` | 37 |
| Email | `EMAIL` | 155 |
| Phone | `PHONE` | 138 |
| Website | `WEBSITE` | 77 |
| Country | `Country` (DMC rows), `STATE` for overseas | 17 |
| Hotel chain | `CHAIN` (Hotels sheet) | 14 |
| Notes | `Notes`, verbatim | 26 |

**Empty on import (5), each with the reason:**

- **Tier.** No column, no list, no convention. Recommended default `Preferred` for every imported
  row, because the file's own name is the only designation that exists — and that default is the
  first decision Sam has to confirm.
- **Owner.** Named per record, per definition of done 3. Nothing to import from.
- **ABN / legal entity.** Absent from all four records.
- **Contract expiry, public liability expiry and cover, WHS document date.** `ADMIN/PL insurance and
  WorkCover/` holds *TRIBE's own* certificates — public liability and professional indemnity to 31
  August 2026, WorkCover to 4 June 2026 — not supplier certificates. No supplier insurance
  certificate was found anywhere in the Share Drive. These columns start empty and are filled by
  asking suppliers, which is a person-hours cost phase one does not include.
- **Last reviewed / next review.** Nothing to derive it from; and the Hotels sheet already
  simulates it by hand in Notes (`Updated by RC- 05/02/25`, `Updated by SA- 16/03/26`), which is
  the requirement expressing itself.

**Provenance (all 176 rows):** source file, source sheet, import date. This is deliberate — the
phase-one promise is that every row can be traced back to the cell it came from, so a wrong import
is visible rather than inherited.

Rate data is not in the list at all. Its only trace is free text in Notes: a 10% discount or
rebate, a $3000 minimum spend, a staff promo code. That belongs in the phase-two rates list and
argues for those three notes being copied there rather than lost.

## 3. Term sets

- **Category** — the 14 sheet names, renamed to the brief's vocabulary: Venue, Hotel, AV, Catering,
  DMC, Transport, Decor & styling, Entertainment, Photography, Speakers, Merchandise, Staffing,
  plus Florist, Furniture & linen hire, Tourism bureau, Other. Multi-value. `Tourism Bureau` added
  from the sheet the CONTENTS page forgot.
- **Region** — not the 26 raw values. Four Australian states plus territories, New Zealand,
  Pacific, Asia, Europe, Americas, Middle East, Africa, Global. The raw strings are mapped during
  import and the original string kept in Notes, so a bad mapping is correctable later.
- **Tier** — Preferred, Approved, Trial, Do not use. Empty until the default above is agreed.
- **Status** — Active, On hold, Archived.

## 4. Who owns it

Evidence in the files, not in the conversation:

- The master list was last saved by **Kate Ashton** on 4 August 2026, and created by Jess Delon in
  October 2022.
- The Hotel Directory was last saved by **Jodie Haylock** on 3 February 2026.
- The Christmas-card database was created by Kate Ashton and last saved by Lisa McKernan in
  December 2020.
- The Hotels sheet carries manual edit attribution in Notes under the initials RC and SA.
- The shortcut that started the "second master" worry points at Sarah Adams's machine.

Recommendation: **Kate Ashton** as accountable owner of the Suppliers list, because she is the
person already maintaining it, with **Jodie Haylock** as the maintainer for hotels. That is a
recommendation from file metadata, not an approval. The per-record owner field stays empty at
import and is assigned in phase two — the list is worthless if it just moves "who maintains this"
from a person's memory into a column nobody fills.

Vanessa appears in the open questions from the brief; nothing in the four records connects her to
supplier data. Either she is the operations-side candidate for a reason outside these files, or she
should drop off the list. UNKNOWN — confirm with Sam.

## 5. Scope of phase one

In: one Suppliers list on the Tech site, 16 columns, four term sets, five views (all active, by
category, by region, missing owner, review due), item versioning, a Teams tab, import of the 176
rows with provenance, and a dated retirement note on the 2025 sheet and on the two hotel files.

Out: rates list, expiry reminders, reviews and interactions, Power Apps, Graph access for the agent,
and any write automation. The brief puts rates and the expiry flow in phase two. The one thing
worth pulling forward is the expiry reminder *mechanism*, because definition of done 5 and 6 both
depend on the tenant's licensing answer and that is cheaper to ask before the list is built.

The weekly change report stays in phase one as read-only: file metadata only, no writes. It is what
keeps the list from quietly dying the way the Christmas-card sheet did.

## 6. What remains UNKNOWN

- Whether any supplier has ever supplied an insurance certificate, and where it would live if it
  did. No file found in `SUPPLIERS/`, `ADMIN/` or `EVENTS CLIENTS/`.
- Whether the 2025 sheet is still the live master or has been superseded since August 2026. Its
  mtime is 4 August 2026 and no newer copy exists in the Share Drive or in `TRIBE GROUP - TRIBE
  Travel/`.
- What "Preferred" is supposed to mean commercially, who signs it off, and whether the 176 rows
  were ever individually approved.
- Whether the Hotel Directory's 129 rows are a subset of the Suppliers list, a separate hotel
  record set, or a superseded one.
- The Microsoft 365 plan and whether premium Power Automate is licensed.
- Who may see rates and contract values.

## 7. Decisions needed before building

1. Confirm `Preferred` as the tier default for all 176 imported rows, or name the subset that is.
2. Confirm Kate Ashton as accountable owner, with Jodie Haylock on hotels.
3. Take the Hotels out of the Suppliers list entirely, or keep one supplier record per hotel.
4. Rates visible to all events staff, or leads and finance only.
5. The licensing answer, which decides whether the expiry flow is a flow or a weekly email.
