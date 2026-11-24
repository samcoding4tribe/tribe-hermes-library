# Team map

A wall display for the Monday breakfast meeting: where everyone is, and who is
away. Built from the leave calendar rather than a second spreadsheet.

## What exists

`leave_calendar.py` reads `Leave Calendar 2026.xlsx` and writes today's status per
person. Stdlib only, no spreadsheet library, so it runs on a Windows machine too.

```bash
python3 leave_calendar.py --xlsx "/path/Leave Calendar 2026.xlsx"
python3 leave_calendar.py --xlsx "..." --date 2026-12-01 --json status-today.json
```

Verified 24 November 2026 against the real workbook: sheet `2026`, twelve monthly
blocks, nineteen people, and today's codes resolved. The workbook carries sheets
for 2023 through 2027, so the year rolls over without renaming anything. The file
name still needs to change to match the tab, or the script needs to be told which
year to read.

Codes, from the legend at the top of the sheet: blank is in the office, `AL`
annual leave, `FM` family leave, `OTH` other leave, `DIL` leave, `X` not in the
office, `OS` onsite, `S` site inspection, `PH` public holiday.

## What the calendar cannot tell us

**Location.** It says who is away, never where. A world map with pins therefore
needs a second input, and that input is a choice:

1. Everyone has a default pin at the Melbourne office, and only people who are
   away or travelling are moved. Smallest thing that works.
2. A `where.json` per person with a city, updated by whoever knows. More accurate,
   more maintenance.
3. Their holiday destination, only where the person has opted in.

**A join key.** The calendar names do not match the org map: "Kristen Manias"
against `kristen`, "Bianca Berger" against `bianca`, and the calendar still lists
Laura, who has left. Nineteen names against twenty-six people. So the app needs
an alias table, or the org map's ids need to be added to the calendar sheet.

## How the Monday note is made

1. `weekly.py` reads the calendar for the coming week and writes `week.json`,
   `week.html`, `week.txt` and `week-data.js`. Only people on the org chart are
   included; anyone else is listed as skipped.
2. `map.html` draws the world map from `week-data.js` and `where.json`. People away
   with no recorded place appear as faces under the map rather than as guesses.
3. Work places come from the workflow sheet, not from typing. `workflow.py` finds
   the newest `Workflow_*.xlsx` in `WORKFLOW/` on the Share Drive (so the yearly
   rename is handled), reads each row's Destination, Date range and the Onsite
   column, and matches those initials to the org chart through `aliases.json`.
   Set `TRIBE_WORKFLOW_DIR` to point somewhere else. A row named `CG & HL` on
   `26 - 27` in November puts Carlita and Holly at that destination on those days.
   Places the sheet spells loosely are resolved to a point: exact name, then any
   stop of a multi-stop trip (`Saigon & Siem Reap`), then a country or state
   (`QLD`, `China`). No match means no pin, and the person shows as unplaced.

4. `where.json` is the override, for travel the sheet does not carry (a site
   visit, a holiday someone has shared). It is checked before the sheet, keyed by
   person id:

   ```json
   {"kim": {"locations": [{"from": "2026-11-30", "to": "2026-12-04",
                           "place": "Gold Coast", "kind": "work"}]},
    "dani": {"locations": [{"from": "2026-12-14", "to": "2026-12-19",
                            "place": "Queenstown", "kind": "holiday",
                            "public": true, "activity": "ski"}]}}
   ```

   `kind: work` shows on onsite and site-visit days. `kind: holiday` shows only
   when `public` is true, so nobody is revealed as away unless they agreed.
   `activity` picks the little marker: ski, snowboard, beach, surf, city, safari,
   wedding, honeymoon, festival, cruise, hike, food, golf, park. Anything else
   falls back to a palm tree. Holiday pins are teal; trip pins are orange.

5. `make_week.py` builds one folder per week, `weeks/<monday>/`, holding
   `data.json`, `data.js`, `map.html`, the captured `map.png` and `email.html`.
   The note that goes out is `weeks/<monday>/email.html`: title, map, week at a
   glance. There is no single shared mock-up; each week is its own folder.

Before sending, add the places: edit `where.json`, or ask the assistant to. Then
re-run steps 1 to 3. Nothing sends itself.

Friday is work from home unless the calendar says otherwise; that is a display
default in the note, not a code in the sheet.

## Not built yet

The map page itself. It wants three things settled first: the location source
above, where headshots live (the induction manual is a photo directory), and
whether faces appear at all. A world map with names is honest; faces need consent.

## Privacy line

Status and location are personal data. Holiday destination is opt-in per person,
shown only if they gave it, at city level, never live. The wall display shows what
someone chose to share, not where their phone is.
