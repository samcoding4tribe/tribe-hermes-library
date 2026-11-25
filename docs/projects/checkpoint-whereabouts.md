# Checkpoint: the weekly whereabouts note

> **Start here on Monday, or when Dani replies.** The note itself is finished and the
> job is scheduled. What remains is one access test, one real run, and Dani's palette.

## Where it stands

Working, and rehearsed end to end. The Monday 11:00 job builds the week's folder,
captures the map, prints a one-page PDF, publishes it to
`TRIBE Group Tech/Where is my TRIBE/<monday>/`, and reports here. It never sends.

Content comes from two sheets: the leave calendar in the Share Drive for statuses, and
the newest `Workflow_*.xlsx` for destinations, matched through the Onsite column's
initials. `where.json` is only the override, for site visits and shared holidays.

The note: title, map with a base pin that carries a count and trip pins that carry
names, a table with two-line cells for trips, a link to the published copy, and small
print. No legend, no header line, first names only.

Three decisions hold it together: D25 (produce at 11:00 Monday, after the meeting, and
never send automatically), D26 (map and table in the body, plus a link to the site
copy), and the title itself, "Where is my TRIBE?".

The rehearsal on 25 November found four defects, all fixed: the brief pointed at the old
folder name, publishing preferred a stale PDF over a fresh map, the PDF had no room
before the footer spilled, and `MEL` and `PER` in the workflow sheet resolved to
nothing. Only two weeks are kept on the site.

## Definition of done

1. An ordinary employee, not an administrator, opens the published link and sees the
   note.
2. One real Monday run reviewed: right week, right pins, right names.
3. Dani's palette and fonts applied once, in the template.
4. A decision on the Graph send, so the note is real HTML rather than a pasted picture
   if it goes out that way.
5. A one-line command for adding a new starter to the roster and the aliases, so a
   Monday morning addition takes seconds.

## Remaining work, in order

1. The access test, as above. This is the only thing that could embarrass us in front of
   the whole company.
2. Watch the first real run on Monday 30 November, 11:00.
3. Apply Dani's values to `apps/team-map/make_week.py` when they arrive.
4. Decide on the Graph send, and on who sends: Sam, Kate, or the manager on duty.
5. Build the roster command.

## What it needs from you

- Someone outside the tech group to try a link.
- Dani's hex values and fonts.
- A decision on the send path, and on who presses send on a Monday.

## Note on the previously sent draft

The mock-up sent to Dani carried the old header line and the legend, since both changes
came after it left. That is expected, not a fault in the current build.
