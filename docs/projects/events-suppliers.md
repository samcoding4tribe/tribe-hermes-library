# Events preferred supplier knowledge base

25 November 2026. Microsoft prices checked November 2026, USD list. Anything I could not open is marked UNKNOWN.

## 1. What exists today

`TRIBE GROUP - Share Drive/SUPPLIERS/` has 38 folders at one level, mixing cities (`Melbourne`, `Sydney`), countries (`USA`), venues (`Hyatt`), categories (`Caterers`) and a person (`Satwinder`). Six files sit beside them: `Preferred Suppliers list- 2025.xlsx` (79 KB, last saved August 2026), `Hotel Directory.xlsx`, `2022 Hotel Availability.xlsx`, a `.lnk` shortcut to the preferred list, and two event leftovers.

Three records compete:

- The master sheet, named 2025, edited 2026, with a shortcut implying another copy. UNKNOWN where.
- Per-event copies: 43 top-level folders under `EVENTS CLIENTS/`, 32 named `suppliers`, 23 Supplier Agreement files, 50 confidentiality agreements, 38 `contracts` folders. One example: `EVENTS CLIENTS/CBA/2019/03 RSELT Conference March (CBA-1901)/Supplier Agreements/Florist Supplier Agreement.docx`.
- A client list shaped differently: `EVENTS CLIENTS/CBA/CBA Preferred Suppliers.xlsx` has categories in rows, cities as columns, and contacts inside the company cell.

Insurance is a filename convention, not a register: `ADMIN/PL insurance and WorkCover/Certificate of Currency - Public Liability 31 August 2026.pdf`. Travel already uses `TRIBE GROUP - TRIBE Travel/Supplier - VIRTUOSO/`.

Friction: no owner field, dates only in filenames, one supplier in up to four places.

Caveat: 3,463 of 3,714 Share Drive files were online-only placeholders that would not open here (Resource deadlock avoided), including every `SUPPLIERS/` file I saw, so contents were UNKNOWN. **Resolved 27 November 2026:** hydration is clean (445 files in `SUPPLIERS/`, 0 dataless) and the master list has been read — 176 name rows, 165 distinct suppliers, 14 category sheets. What it holds, the proposed fields and the owner evidence are in `docs/projects/events-suppliers-phase1.md`. The paragraph above stands as the finding of 25 November, not as the current state.

## 2. Options

- **SharePoint list (Microsoft Lists)**, same engine. 30 million items per list, lookups, item version history, content approval, views; an afternoon, no developer. Lists mobile apps are retired: phones use Teams or a browser, and offline editing needs OneDrive list sync on Windows or macOS. Included in the existing licence.
- **Document library with content types and managed metadata.** Right for contracts and certificates; closed term sets stop "Melbourne", "melb" and "VIC" becoming three cities. Search reads content, but filtering by expiry needs columns.
- **Power Apps form or canvas.** Better mobile capture; $5 per user per app or $20 per user per month, plus maintenance. Phase three.
- **Loop.** A page canvas for guidance, with no columns, views or expiry dates.
- **Teams tab and SharePoint page.** Views and links, not storage.

## 3. Data model

Three lists and one library on the Tech site.

**Suppliers**: SupplierID, name, legal entity, category, city or region, tier, status, owner, ABN, primary contact, contract status and expiry, public liability expiry and cover, WHS document date, last and next review, notes.

**Rates**, one row per quote: supplier, service, unit, price, currency, GST, minimum spend, valid from, valid to, source document, quoted and approved by. Never edit a price: add a row, close the old one with a valid-to date, and point a current view at today.

**Interactions** and **Reviews**: date, person, channel, summary, next step; review scores for quality, responsiveness, value and compliance.

**Documents**: content types for contract, rate card, insurance certificate, WorkCover, WHS assessment, capability deck, menu, floor plan, photos, each with supplier lookup, type, valid from, expires.

Closed term sets: category (venue, AV, catering, DMC, transport, decor, entertainment, photography, speakers, merchandise, staffing); city or region (folder names plus overseas); tier (Preferred, Approved, Trial, Do not use); status (Active, On hold, Archived).

A fact is a field if you must filter, sort or be reminded; otherwise it is a document.

## 4. Keeping it current

- One named owner per record; a team cannot be accountable for an expiry date.
- Annual review for Preferred, six monthly for Trial; lapsed insurance moves a supplier to On hold by view, not memory.
- One weekly Power Automate flow alerts the owner and a Teams channel 60 and 30 days before expiry.
- Contact history logged after each event; reviews fed by `MASTER TEMPLATES & DOCS/Debrief & Survey`, which already exists.
- Events reference SupplierID rather than copying it; the event folder keeps only its own signed documents.

## 5. Phases

**Phase 1, one week, no developer.** Suppliers list, Documents library, four term sets, about 15 fields, five views, versioning, Teams tab, hand import of the 2025 list (row count UNKNOWN).

**Phase 2, two to four weeks.** Rates list, expiry flow, Reviews, backfill from `SUPPLIERS/` and the event folders, owner named per record.

**Phase 3.** Power Apps form for onsite use, contract generation, Graph read access for the Hermes agent.

Cheapest credible: list plus library, inside the existing licence.
Recommended: the same with the expiry flow in phase 1. The failures worth fixing are stale prices and lapsed insurance, and both are reminder problems, not app problems.

## 6. Open questions

1. Who owns supplier data: Jodie, Vanessa, or an operations coordinator?
2. How many active suppliers are there, and how many are used once?
3. Are suppliers contracted per event or annually?
4. Can supplier rates be visible to all events staff, given client confidentiality?
5. Which plan is held, and is Power Apps or premium Power Automate licensed?
6. Should Travel's `Supplier - X` folders merge in, or stay separate?
7. Who may see contract values: all staff, leads, or finance?
8. What qualifies a supplier as Preferred, and who signs that off?

## What I could not verify

- Contents of `SUPPLIERS/`: none would open. — Resolved 27 Nov: read in full, see `events-suppliers-phase1.md`.
- Whether the 2025 list is the live master, and where the `.lnk` points. — The `.lnk` points at `C:\Users\SarahAdams\…\Share Drive\SUPPLIERS\`, a local OneDrive path, not a second master. Whether the sheet is still live: UNKNOWN.
- Any supplier WHS or insurance certificate. — Checked 27 Nov: none exists. The certificates in `ADMIN/PL insurance and WorkCover/` are TRIBE's own.
- Existing tiers. — Resolved: there are none, in any of the four records.
- Tenant licensing and admin.
