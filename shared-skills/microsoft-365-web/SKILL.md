---
name: microsoft-365-web
description: "Outlook and Teams web access when Graph is blocked."
version: 1.4.0
author: TRIBE admin profiles
license: MIT
metadata:
  hermes:
    tags: [microsoft-365, outlook, calendar, browser, sign-in, ea, admin-assistant]
---

# Microsoft 365 through the browser

Getting and keeping a working Outlook mail/calendar session inside the Hermes
browser, for admin and EA profiles that have no Graph API access. Graph is the
durable answer; this is the path that works today, and it has sharp edges worth
knowing before you configure anything.

## When to Use

- A profile needs to read an inbox and diary and produce drafts, and the Entra
  app registration is blocked, unconsented, or still in a ticket queue.
- `outlook.office.com` in the agent browser lands on
  `login.microsoftonline.com` instead of the inbox.
- Any time someone says "I'm already signed in" and expects the agent to see it.

## Step 1 — establish the actual state before changing anything

```bash
hermes config get browser.headed
hermes config get browser.executable_path
hermes config get browser.user_data_dir
hermes config get browser.inactivity_timeout
ps aux | grep -iE "chrome|edge|chromium" | grep -v grep | awk '{print $2, $11}'
defaults read com.apple.LaunchServices/com.apple.launchservices.secure | grep -iE "safari|edgemac|googlechrome"
```

The last one tells you the macOS default browser, which decides whether the
real-profile route is even available (see Pitfalls). The `ps` output tells you
which browser holds the human's working session — that is the browser they mean
when they say they are signed in, and it is not the agent's browser.

## Step 2 — a dedicated, persistent, visible work profile

```bash
mkdir -p "$HERMES_HOME/cache/browser-use/work-profile"
hermes config set browser.executable_path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
hermes config set browser.user_data_dir "$HERMES_HOME/cache/browser-use/work-profile"
hermes config set browser.headed true
hermes config set browser.inactivity_timeout 900
```

Why each setting earns its place:

- **Real Chrome binary, not the packaged Chromium.** Same engine Microsoft
  expects for a normal browser, and the macOS keychain cookie path stays intact.
- **`user_data_dir`.** Without it every session is a brand-new signed-out
  browser and the sign-in has to be repeated. With it the session survives
  restarts.
- **`headed true`.** The human has to type the password and MFA somewhere they
  can see. Headless gives them no window to type into.
- **`inactivity_timeout 900`.** The 120s default reaps the browser mid-sign-in;
  password plus an authenticator prompt routinely outlives two minutes.

Config is read when the browser launches, so a browser already running keeps
the old settings. Kill the agent's own throwaway Chromium (it is disposable, not
the human's browser) and let the next `browser_exec` call start the configured
one:

```bash
pkill -f "hermes/tools/chromium"
```

Then verify from inside the browser, not from the config file:

```python
print(js("navigator.userAgent"))   # must contain Chrome/15x, must NOT say HeadlessChrome
print(js("location.host"))         # login.microsoftonline.com until sign-in
```

## Step 3 — hand the sign-in over, do not perform it

Navigate to `https://outlook.office.com/mail/` first so the window is sitting on
the Microsoft form, then tell the human exactly which window to use: title
`Sign in to your account`, the one whose only tab is that page. Two Chrome
instances on one desktop look identical, so identify the window by title.

Never type a password, an MFA code, or a recovery detail, and never accept one
in chat. `browser_vault` is the only channel for stored credentials, and on a
fresh profile there is nothing stored yet. Say plainly where the cookies land
and what protects them, since it is their session being copied onto disk.

Then stop talking and wait. The browser stays alive between turns in headed
mode, and the raised inactivity timeout keeps it alive while they fumble for a
phone.

## Step 4 — verify the access you claimed, before saying it works

Once they confirm, do all three and report what you actually saw:

1. Load the inbox and read a couple of subject lines back to them.
2. Load the calendar and read back one real entry.
3. Compose ONE draft, do not send it, and show them the body. Discard it
   afterwards unless the owner asked for that message: a verification draft left
   in their Drafts folder is clutter in a place they read every day.

A page that renders the sign-in form again means the session did not stick —
say so rather than describing access you do not have.

## Reading it once the session works

```python
# inbox rows — the list is virtualised, so this is the rendered window only
rows = js("""[...document.querySelectorAll('div[role="option"]')]
  .map(e => e.innerText.replace(/\\s+/g,' ').trim())""")
# the calendar states its own completeness
js("document.body.innerText.match(/Loaded \\d+ events[^\\n]*/)[0]")
```

- Cross-check the rendered rows against the folder's unread badge before saying
you have read the inbox. Write "the seven threads that rendered" rather than
"your inbox" — the list page is not the mailbox.
- **A reply's text is not in the slice of page text after the subject line.** Threaded messages
  collapse their quoted history, so reading `innerText` around the subject returns the signature
  and the previous message while the new content sits unrendered. Click the message, or the
  Expand / Show more control, and re-read before concluding the sender wrote nothing — or, worse,
  summarising the wrong person's words back to the principal.
- For one meeting, click its block on the calendar grid and read the details
pane; the invite body and the attendee list are not in the subject line you
clicked, and the attendees are usually the point.
- The calendar header (`Loaded N events in N selected calendars`) is the cheapest
  proof that a quiet week is genuinely quiet — **but only when no filter is applied.** Read the
  toolbar for `Filter applied` first: with a filter on, the header counts the filtered view, and
  you will report "0 events" for a day that has meetings in it. Check the filter before quoting
  the count, and say which view you read whenever a day looks empty — "nothing on" and "nothing
  visible in the view I happened to have open" are different claims, and only the first is worth
  telling the principal.

### Scanning the diary for a date window

Day cells do not expose their event text in a node you can read reliably, and the
"Loaded N events" header is missing from some views. What does work is the event
elements' own accessible names, which pair a full date with a time:

```python
js("""[...document.querySelectorAll('[aria-label]')]
  .map(e => e.getAttribute('aria-label') || '')
  .filter(l => /December \\d{1,2}, 2026/.test(l) && /\\d{1,2}:\\d{2}/.test(l))""")
```

Swap the month for the window you need and run it in month view: one line per
event, each carrying its date. It covers the days the view has rendered, which is
what a slot check needs. Report two things from it beyond clashes: an empty day,
and any pair of events starting at the same minute.

A same-minute pair is a prompt to look, not a clash to report. Before calling it
one, open both and compare organiser, subject and location: organisations
routinely book a meeting room at the same time as a Teams meeting so the team
joins from one room instead of separate desks, which renders as two entries and
is one meeting. The reverse failure matters more than the false alarm — telling
the principal they are double-booked when they are not erodes the one thing the
brief sells, which is judgement. Say what you saw and what would confirm it:
"these two start at the same minute; if the room entry is the Teams call, ignore
it, otherwise Tuesday has a problem."

## Creating an invitation

Read the resolved date and time back before going any further; the click is not
the setting.

Sequence that has held end to end — follow it in this order rather than
improvising clicks:

1. **New event** from the calendar. The composer opens on today, at the next half
   hour, with a Teams toggle already on.
2. Title line, then the attendee line: `insertText` the address and dispatch
   Enter, then confirm a chip with the person's name and availability appeared.
3. Click the date line to open the picker, then click the small **calendar icon at
   the right of the start date field**. A month grid opens: check its header,
   click the day cell, and read the date back out of the page text before
   touching anything else.
4. Click the **Start time** field, Backspace a dozen times to clear it, then
   `insertText` `11:00 AM`; repeat for End time. The header line must read e.g.
   `Mon 30/11/2026 11:00 AM - 11:30 AM`.
5. Close the picker by clicking **blank space in the left margin of the dialog**,
   never the middle of the compose.
6. Click the body area, confirm the cursor is in the body, then insert the whole
   message in one call.
7. Read four things off the screen before Send — title, attendee chip, exact date
   and times, body text where it belongs — then send and verify it landed.

Pitfalls that cost real time here, each one observed:

- **Month grids render the neighbouring month's leading and trailing days in the
  same rows.** Clicking at the position of a month's final day can land on the
  2nd of the next one. After any date selection, read `\\d{1,2}/\\d{1,2}/\\d{4}`
  out of the page text and correct it before touching the times.
- **The date field is a control, not a text box.** Three ways it bites: focus,
  select-all and `insertText` are often ignored; the picker popup takes focus
  back; and typing appends to the masked value instead of replacing it, leaving
  rubble like `:5/11/202630/11/2026` while the field still submits the original
  date. Click the day cell in the picker, and if you must type, Backspace the
  value to empty first, then verify what the field actually holds.
- **Opening the composer from the grid is not dependable.** A click on a day-view
  slot can select the slot and open nothing, so do not build the event out of the
  grid. If two attempts at a coordinate have not held, change route — grid cell,
  then hand-over — rather than trying a fifth coordinate.
- **Two attempts at the date, then hand over.** The date control fails in several
  distinct ways — typed dates ignored, select-all-then-type appending rubble, the
  month grid rendering translucent over the time suggestions so clicks fall through
  to the rows beneath, arrow keys doing nothing because the field never took focus.
  Attendees, room and times will set fine throughout, which makes it tempting to keep
  going. Stop at two: hand the owner a four-field block per invitation — title, start
  and end, attendee address, room, Teams yes or no — and say plainly that the composer
  would not take the date. They create three invites in two minutes; a dozen automation
  attempts produce nothing sendable and spend their morning.
- **Set the date before the times.** Once a time is in the fields, the picker renders the
  time-suggestion list underneath the month grid and the day cells stop taking clicks: the
  overlay swallows them and the popup closes with the old date intact. Choose the day on a clean
  picker first, then fill start and end, then close from the margin.
- **With the picker open, a click lands in whichever field sits under the cursor.**
  Text inserted after such a click went into a scheduling poll's end-date field
  and silently converted the draft into a poll with three options. Close the
  picker from the margin, and if the composer ever shows "Create a poll to find
  the best meeting time", discard the draft and rebuild it as an **Event** rather
  than sending a poll to a colleague.
- **Verify the invitation after sending, not the composer closing.** The event must
  be back on the grid at the right time, and its detail pane must read
  `You're the organizer, <name> didn't respond`. That is the difference between a
  sent invitation and a closed window.
- **Never dispatch an invitation whose date, time and recipient you have not read
  back on screen.** Hand the owner the exact set instead: title, start and end,
  attendee address, paste-ready body. An invite with the wrong time reaches a
  colleague and has to be withdrawn; a short hand-over costs them thirty seconds.
- **Invitations are forwardable by default**, so an owner who wants a colleague to
  add people only needs a line in the body saying so; changing attendees directly
  stays with the organiser.

## Getting attachments and files onto disk

An attachment card offers Preview, Edit in browser, Save to OneDrive and Copy. There
is no plain Download, and the Office viewer opens as a separate browser target that
page JavaScript cannot reach.

1. **Save to OneDrive** from the attachment's chevron menu. The toolbar then shows
the button as done and the file lands in `Documents/Attachments`.
2. **Pull a real copy through SharePoint's download endpoint**, in the same browser
session, so the cookies do the authorising:

   ```
   https://<tenant>-my.sharepoint.com/personal/<first>_<domain>_<tld>/_layouts/15/download.aspx?SourceUrl=%2Fpersonal%2F<first>_<domain>_<tld>%2FDocuments%2FAttachments%2F<file>
   ```

   Read the tenant, user and folder segments off the OneDrive web address bar rather
   than constructing them: from `My files`, a single click selects a row and a
   `dblclick` event on the row's name element opens the folder.
3. **Confirm it arrived**: `ls -lt ~/Downloads | head` and `file <name>`, not the
   absence of an error message.

Then parse the file locally with openpyxl or pandas. A spreadsheet is workable data;
its rendered viewer is not.

## Composing a draft in the web editor

The compose pane is a small editor with its own rules: fill To, Cc, Subject and Body in that
order, one `insertText` per field, and verify a recipient chip rather than a raw address string.
`references/compose-and-send.md` carries the field-by-field sequence and the body-rewriting rules;
read it before composing rather than improvising clicks.

**Documents and attachments have a working path:** `references/compose-and-send.md` carries the
field-by-field sequence, the `setFileInputFiles` attachment method, the headless-Chrome PDF recipe
for material the owner wants to read later, and the rules for sending to an external personal
address — including the "Attachment reminder" modal, whose Send is a second click. Two rules to
keep in view without opening it: the attachment chip must be on screen before Send, and a document
asked for "to read later" ships as a PDF, not as markdown pasted into the body.

**Sending work material to an external personal address** is the owner's call, not a boundary to
argue: confirm the recipient is one they named, say what you checked is not in the file (client
names, contact details, another party's pricing), then send. Flag rather than refuse if something
sensitive is in it.

Two attachment failures worth knowing even without the reference:

- **Outlook blocks the send with an "Attachment reminder" dialog** when the body
  mentions an attachment and none is present. It is a modal with **Send** and
  **Don't send**; the send is not complete until the dialog's Send is clicked.

Pitfalls that cost real time here:

- **A DOM Range plus Backspace does not clear the body.** Selecting with
  `selectNodeContents` and pressing Backspace can leave the old text in place, and
  the replacement then lands on top of it. To rewrite: `el.focus()`,
  `document.execCommand('selectAll', false, null)`, dispatch Delete, then check
  `el.innerText.length` is about zero before inserting the new body.
- **Clicking an unrelated row while compose is open opens another draft under you.**
  Before editing, read the subject input and the To chips; otherwise a "rewrite"
  lands in somebody else's message.
- **Update the existing draft rather than composing a second one.** A reply to
  "make it more casual" is an edit of the draft they already have. Two drafts to
  the same person is clutter the principal has to clean up.
- **One insertText call per field.** Typing a paragraph character by character
  through key events is slow enough to hit tool timeouts.

## Building a survey in Forms

Forms is the right tool for a pre-meeting survey. Do not author it by automated import: a
Word document imported through **Quick import** produced headings and bullets as text
paragraphs, which looks correct in the editor and cannot be answered by respondents. Build
the questions by hand, pasting the whole option list into the first option box so Forms splits
it, or hand the owner a paste-ready build sheet and let them click it in — they finish it
faster than a designer that reorders fields under you.

Forms does support caps (**at most N options**), so a "pick two or three" question can be
enforced rather than merely worded. Verify answerability in **Preview** before sharing: zero
radio or checkbox inputs on a question with options means the form is broken.

Before offering time slots, read the principal's calendar for the whole window and re-check
it the day the form goes out; a slot that lands on an existing meeting is a reschedule you
have handed to a colleague. Ask for **two** picks per person, not one, so every respondent
supplies their own fallback and most clashes resolve without another round of email. Check
`bookings.cloud.microsoft/bookwithme` before promising a self-booking link; where the tenant
does not licence Bookings, named slots in the form are the fallback.

A designer page opens as its own CDP target, so a click that "does nothing" means `js()` is
still on the old tab — list targets and navigate to the full URL, with the `id=` printed in
full. Full recipe, including how to read individual responses and reconcile the time picks into
invitations: `references/forms-and-bookings.md`.

## The window belongs to them

This browser is the principal's window as much as the agent's: they read mail and forms in it
while you work. Navigating the tab they are looking at takes the page away from them mid-read,
and they will notice before you finish the next call.

- **Say so before you take the window.** One line: what you are about to do and that the tab
  will move. It costs a sentence and prevents the interruption being read as the agent
  breaking their machine.
- **Account settings are not yours to open.** Not the signature, not rules, not a setting the
  principal has already told you is configured. Reading one is still an intrusion into the
  part of the account that is theirs alone, and asking costs a sentence. If a draft's sign-off
  looks wrong, leave the ending to them or ask — do not go looking for the configuration.
- **Prefer a new tab over reusing theirs**, and leave their reading tab where it was.
- **One profile means one browser.** There is no side channel to build in: a second Chromium
  on the same `user_data_dir` collides, and pointing the config at Edge drops the Microsoft
  sign-in this profile depends on. A genuinely separate build browser is a second profile with
  its own sign-in, which is a decision for the owner, not something to improvise mid-task.

## Drafting rules for these profiles

Outlook web is a send surface one click away, so the drafting boundary has to be
mechanical: drafts only, no send, no reply posted, no calendar invite dispatched
until the human says yes in that conversation. Read-only actions (opening a
message, listing the diary) need no approval; anything that leaves the account
needs an explicit one.

## Pitfalls

- **`browser.use_real_profile` fails closed unless a Chromium browser is the
  macOS default.** With Safari as default it refuses with "your default browser
  is not a supported Chromium browser". Do not flip the human's default browser
  to get around it: the dedicated work profile avoids copying their everyday
  cookies and is reversible with four config lines.
- **"I'm already signed in" does not transfer.** A session in the human's own
  Chrome or Edge profile is invisible to a separate-profile or headless agent
  browser. Only two things carry it over — a manual sign-in in the agent's
  window, or real-profile snapshotting.
- **Conditional Access can still win.** An unmanaged browser may be refused
  outright or forced to re-auth every few days. State that caveat when you set
  the route up, so a surprise lockout is not read as the agent being broken. If
  it bites, Graph is the answer, not more browser tweaking.
- **The window closing between turns is normal, not a lost sign-in.** The agent
  browser is reaped after `browser.inactivity_timeout` idle even when headed, so
  a human who walks away returns to no window. With `user_data_dir` set the
  cookies survive: relaunch with a `browser_exec` call and check `location.host`
  before assuming anyone has to sign in again.
- **You can confirm a sign-in landed without reopening the browser.** Copy
  `Default/Cookies` out of the work profile and query it: rows for
  `outlook.cloud.microsoft` plus an `ESTSAUTHPERSISTENT` expiring months ahead
  mean the session is real. This separates "signed in, window closed" from
  "never got past the form", and the two need different responses.
- **macOS TCC blocks reading `~/Library/Application Support/Google/Chrome/Local State`
  from the terminal.** `Operation not permitted` there is privacy protection, not
  proof Chrome is absent — check `/Applications` before concluding anything.
- **The sign-in page title is a poor navigation target.** Identify the window by
  title for the human, but drive the form by input `name` attributes
  (`loginfmt`, `passwd`) when you come back to check state.
- **A file in the OneDrive terminal path is often a placeholder, not the bytes.**
  Reading `~/Library/CloudStorage/OneDrive-…/<file>` straight after a save gives
  `BadZipFile` or `OSError: [Errno 11] Resource deadlock avoided`, because the File
  Provider has not materialised it, and `brctl download` is iCloud-only and refuses
  a OneDrive path. Fetch a real copy through the SharePoint download endpoint and
  read that.
- **Do not scrape the Office viewer.** It renders in its own target, so `js()`
  against the mail page finds zero `[role="gridcell"]` elements while the sheet is
  plainly on screen. Download the file and read it with openpyxl instead of driving
  a grid the page cannot see.
- **The mail search box is `#topSearchInput`** (type `text`, role `combobox`);
  `input[type="search"]` does not exist. The id is not always present on the
  loaded page, so fall back to the accessible name before concluding the box is
  missing: find the `input` whose `aria-label` or `placeholder` matches
  `/search/i`, tag it with your own id, then `fill_input` that and dispatch a
  `keydown` with `key: 'Enter'`. Read results from the message list.
- **Quote the badge, not a total you did not read.** An unread count is the
  folder's claim; the rows you reviewed are yours. Presenting one as the other is
  how an assistant reports an empty afternoon on a full inbox.
- **A navigation that times out waiting for the daemon is not a broken browser, and
  neither is a page that goes blank mid-sequence.** After a burst of clicks and text
  inserts, `Page.navigate` can return `timed out after 5s waiting for the daemon`, and
  a tab sometimes renders nothing at all with an empty `document.title`; call
  `ensure_real_tab()` in a fresh `browser_exec` call and the session recovers with its
  state intact, including anything that was already saved. Retry once before reporting
  the browser as unusable, and prefer reading state you already have over re-driving the
  UI. Unsaved compose content is the exception: after a blank-out, check Drafts before
  retyping a message you had already written.
- **Do not schedule inbox or diary briefs before access is verified.** A cron
  that fires into a sign-in page produces noise the human learns to ignore.

## Related

- `references/compose-and-send.md` — filling, attaching and rewriting a compose body; the
  headless-Chrome recipe for PDFs the owner will read later; external-address sending.
- `executive-admin-support` — what the assistant does with this access once it
  works: context file, people map, day shape, drafting boundary.
- The `hermes-agent` skill's `org-rollout` reference: the Graph/Entra route and
  rolling assistant profiles out to colleagues.
- `email-inbox-triage` for what to do with the mail once the session works.
