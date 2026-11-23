# Possible agent profiles for TRIBE Group

Drafted 23 November 2026, from the public site and from how the shared drive is
organised. Role-based on purpose: names get attached when a person is chosen,
not before.

The business, in one line: TRIBE Events sells conferences and incentive programs,
TRIBE Travel sells leisure travel as a Virtuoso agency, and both sell care and
detail rather than volume.

## What the work actually is

| Function | The recurring labour | Where the evidence is |
|---|---|---|
| Client proposals | Rebuilding the same document shape for every brief, pricing, options | `PROPOSALS/`, `MASTER TEMPLATES & DOCS/` |
| Supplier management | Rates, availability, confirmations, contracts, expiry dates | `SUPPLIERS/` |
| Event delivery | Run sheets, call times, staff briefings, on-the-night problems | `EVENTS CLIENTS/`, run-sheet attachments |
| Travel advisory | Itineraries, preferences, visas, hotel benefits, changes | `TRAVEL/`, Virtuoso membership |
| Design | Decks, collateral, headshots, client brand work | `DESIGN TRIBE/`, `DESIGN CLIENTS (Dani)/` |
| Marketing | Case studies, award entries, social, post-event write-ups | `MARKETING/` |
| Finance and admin | Invoice chasing, supplier bills, expenses, staff records | `FINANCE/`, `ADMIN/` |
| Internal systems | Workflow, tools, IT liaison | `WORKFLOW/`, `SYSTEMS/`, `COMWIRE/` |

## The profiles worth building

### 1. `admin` (exists)

Sam's own work admin. Inbox triage, diary, meeting prep, follow-ups, travel
bookings, expense claims. Drafts only.

### 2. `proposal-writer`

For whoever owns new business in events. Reads a client brief, pulls the matching
structure from `MASTER TEMPLATES & DOCS/`, drafts the narrative sections, and
assembles a budget skeleton with the pricing fields left for a human to confirm.
Reads past proposals in `PROPOSALS/` to keep the voice consistent.

- Skills: `proposal-from-brief`, `pricing-sheet-check`, `case-study-match`
- Cron: Monday, list proposals older than five days with no reply
- Guardrail: never sends to a client, never invents a price, every figure cites
  its source document

### 3. `supplier-desk`

The register that keeps itself. Contacts, rates, contract dates, confirmations
outstanding. Weekly, it reports what expires in the next sixty days and what has
not replied.

- Skills: `supplier-register`, `chase-outstanding`, `contract-expiry`
- Cron: Monday 08:00, expiry and chase list
- Guardrail: drafts the chase email, a person sends it

### 4. `event-runner`

For the week of an event. Turns the event folder into a run sheet with times,
suppliers, staff assignments and a contact tree, then keeps a live problem log
during the day.

- Skills: `run-sheet-from-folder`, `staff-brief`, `problem-log`
- Cron: daily 06:00 during an event week only
- Guardrail: reads the event folder, writes only to its own log

### 5. `travel-advisor`

For the travel side. Builds itinerary drafts from advisor notes and client
preferences, checks passport and visa validity against travel dates, and lists
the Virtuoso or hotel-program benefits that apply.

- Skills: `itinerary-draft`, `travel-document-check`, `preference-profile`
- Cron: weekly, clients travelling in the next thirty days with missing documents
- Guardrail: no bookings, no payments, no supplier holds. Recommendations cite
  the source rate or availability note

### 6. `marketing-desk`

Post-event, turns photos, run sheets and debrief notes into a case study, three
social captions and an award-entry skeleton.

- Skills: `case-study-from-event`, `caption-set`, `award-entry`
- Cron: two weeks after each event closes
- Guardrail: client approval before anything leaves the building, no client
  names without a signed release

### 7. `finance-ops`

Invoice chasing and supplier reconciliation. Reads the finance folder and the
supplier register, drafts reminders, flags a bill without a matching purchase
order.

- Skills: `invoice-chase`, `po-match`, `expense-claim-check`
- Cron: Tuesday and Thursday 09:00
- Guardrail: read-only against accounting, drafts only, never posts a transaction

### 8. `systems-keeper`

Not for a manager. This is the profile that tends the library: checks backups
ran, publishes the library, keeps the docs current, reports drift between
machines. Mostly what `default` does on this machine today, written down so it
survives handover.

## What they share

One folder, `shared-skills/`, loaded by every profile: `inbox-triage`,
`meeting-prep`, `weekly-review`, `draft-then-ask`. Written once, improved once.

## What each one needs before it works

| Need | Profiles | Who provides it |
|---|---|---|
| Browser session to Outlook | admin, proposals, finance | Sam signs in once per machine |
| Teams bot | all client-facing ones | tenant app registration |
| Graph mail and calendar | finance, travel-advisor on a schedule | admin consent, scoped policy |
| Access to the relevant drive folders | all | folder permissions, not the whole drive |
| A named owner | all | Sam, per profile |

## Order I would build them

1. `admin`, already running, because it proves the pattern on real work
2. `proposal-writer`, the largest recurring labour and the clearest win
3. `supplier-desk`, because it compounds: one register improves every proposal
4. `travel-advisor`, once document checking is understood by the advisors
5. The rest when someone asks for them

## What I could not tell from outside

- Who owns new business and proposals today
- Whether events and travel use the same client records
- Whether the finance system has an API or only exports
- How many machines would need a profile first
