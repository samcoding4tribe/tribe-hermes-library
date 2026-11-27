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
5. ~~A one-line command for adding a new starter~~ Done: `apps/team-map/add_person.py`,
   dry run by default, refuses a duplicate id, an unknown manager or a calendar name
   already mapped. Needs a real person to prove it end to end.

## Remaining work, in order

1. The access test — script and pass criteria in "The access test" below, written 27
   November. This is the only thing that could embarrass us in front of the whole
   company.
2. Watch the first real run on Monday 30 November, 11:00.
3. Apply Dani's values to `apps/team-map/make_week.py` when they arrive.
4. Decide on the Graph send, and on who sends: Sam, Kate, or the manager on duty.
5. ~~Build the roster command~~ Done, see definition of done item 5.

## The access test

**What it proves.** D26 published into `TRIBE Group Tech`, a Tech-group library, on the
belief that everyone in the org can read it. Nobody outside the Tech group has opened a
link. Two faults hide behind one test and the tester's own words are what tells them
apart: the folder is restricted, or the address is wrong — `publish.py` builds the URL by
hand from `WEB_ROOT` and no one has confirmed it resolves. An anonymous fetch cannot settle
it: SharePoint answers `403` for any path, valid or not (measured 27 November). So the
report has to come from a signed-in person, and the screen they describe is the evidence.

The file to use is the rehearsal copy already published for the week of Monday 30
November. It will be overwritten by the real run and carries the current styling, not
Dani's palette yet.

**Ask them this** — paste, changing only the tester's name:

> Hi — could you try one thing for me? Open this link in your browser while you are signed
> in to your TRIBE account:
> https://tribemanagement.sharepoint.com/Shared%20Documents/TRIBE%20Group%20Tech/Where%20is%20my%20TRIBE/2026-11-30/Where%20is%20my%20TRIBE%20-%202026-11-30.pdf
> It should open a one-page PDF called "Where is my TRIBE?", for the week of Monday 30
> November: a map of the team at the top, a table of who is where underneath.
> Just tell me what you see. If it says you need permission, or asks you to request
> access, that is useful too — send me a screenshot of the words on the screen, not just
> "it didn't work". The colours are not final, so don't judge the look.

**Working looks like** all four:

1. No sign-in loop, no "request access" — the PDF opens (in the browser or as a download).
2. One page, titled "Where is my TRIBE?", no header line above it and no legend.
3. Map at the top with one pin carrying a count and trip pins carrying names; the table
   below matches the map.
4. It is the week of Monday 30 November, not the week before.

**Failing, by the screen they describe:**

| They see | What it means | What to do |
|---|---|---|
| "You need permission" / Request access button | The folder is restricted to the Tech group | D26's fallback: publish to a `Whereabouts` folder with Everyone-except-external granted, re-run, re-test with the same person |
| "File not found" / "Sorry, something went wrong" | The address is wrong, not the permission | Correct `WEB_ROOT`/`FOLDER` in `apps/team-map/publish.py` against the real library path, re-publish 2026-11-30, re-test |
| The PDF, but the wrong week or missing pins | A publishing fault, not access | Note it for the 30 November run; do not count the test as passed |
| Fails for one person, works for another | Their membership or licence, not the file | Check that person's account before changing the folder |

**Record the result here** as: who tested, the date, the screen they described, and the
verdict. Tested: **UNKNOWN** — to be done before the first send on Monday 30 November.

## What it needs from you

- The tester: anyone outside the Tech group who reads email, and their answer recorded
  against the criteria above.
- Dani's hex values and fonts.
- A decision on the send path, and on who presses send on a Monday.

## Note on the previously sent draft

The mock-up sent to Dani carried the old header line and the legend, since both changes
came after it left. That is expected, not a fault in the current build.
