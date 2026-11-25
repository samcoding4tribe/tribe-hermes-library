---
name: microsoft-365-web
description: "Outlook and Teams web access when Graph is blocked."
version: 1.0.0
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
- For one meeting, click its block on the calendar grid and read the details
pane; the invite body and the attendee list are not in the subject line you
clicked, and the attendees are usually the point.
- The calendar header (`Loaded N events in N selected calendars`) is the cheapest
proof that a quiet week is genuinely quiet rather than not yet loaded. Quote it
when reporting an empty diary.

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
  `input[type="search"]` does not exist. Set the value, then dispatch a `keydown`
  with `key: 'Enter'` to run the search, and read results from the message list.
- **Quote the badge, not a total you did not read.** An unread count is the
  folder's claim; the rows you reviewed are yours. Presenting one as the other is
  how an assistant reports an empty afternoon on a full inbox.
- **Do not schedule inbox or diary briefs before access is verified.** A cron
  that fires into a sign-in page produces noise the human learns to ignore.

## Related

- `executive-admin-support` — what the assistant does with this access once it
  works: context file, people map, day shape, drafting boundary.
- The `hermes-agent` skill's `org-rollout` reference: the Graph/Entra route and
  rolling assistant profiles out to colleagues.
- `email-inbox-triage` for what to do with the mail once the session works.
