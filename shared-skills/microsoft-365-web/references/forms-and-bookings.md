# Building a survey in Microsoft Forms, and the booking question

Forms is the right tool for a pre-meeting survey. The build is the fragile part: the
import path is fast but does not guarantee question types, and a form that imports as
headings and bullets is a form nobody can answer.

## The one rule that matters

**Verify the instrument is answerable before anyone sees it.** Open the form as a
respondent (Preview) and confirm every closed question renders radio buttons or
checkboxes. `document.body.innerText` on the designer page cannot tell the difference
between an option list and a paragraph that happens to contain the same words, which is
exactly how a text-only import passes a careless check.

## URLs that are current

- `https://forms.cloud.microsoft/` is the app. `forms.office.com` still redirects but shows
  a service error often enough to waste a call.
- `DesignPagev2.aspx?subpage=creationv2` is the template gallery (Feedback, Registration,
  Research, Quiz) and has no blank-form button on it. The home page has **New Form** and
  **Quick import**; use those.
- `pages/portal.aspx`, the old My-forms list, returns 404. Use the home page.

## Quick import: a speed path, not a guarantee

Worth trying because it creates every question in one step. Not worth trusting.

1. **Generate a .docx** with python-docx: the form title as `level=0`, the description as a
   paragraph, each question as `add_heading(text, level=1)`, and its options as
   `add_paragraph(option, style="List Bullet")`. Open questions get a heading and no bullets.
2. **Forms home → Quick import → Upload from this device.** The dialog has one hidden
   `input[type=file]`; set it through CDP rather than clicking:

   ```python
   root = cdp('DOM.getDocument', depth=-1)
   node = cdp('DOM.querySelector', nodeId=root['root']['nodeId'], selector='input[type=file]')
   cdp('DOM.setFileInputFiles', files=["/abs/path/survey.docx"], nodeId=node['nodeId'])
   ```

3. **Choose Form** (not Quiz), and wait for `Your form has been converted successfully`.
   A minute of silence is normal.
4. **Open the result as a respondent and count the controls.** Zero
   `input[type=radio]` or `input[type=checkbox]` on a form whose questions have option
   lists means the import produced text, and the form is unusable. Rebuild by hand; do not
   paper over it by adding questions around the broken ones.

## Building by hand, quickly

Manual construction is fine when it is done with one trick: **paste the whole option list
into the first option box, one option per line**. Forms splits the lines into separate
options. Typing them one at a time is what makes this feel slow, not the clicking.

- Add the question, paste the question text, leave it, then paste the options block.
- Verify inside a fresh question card rather than after several: a field that already
  contains placeholder text appends instead of replacing, which is how "Option 3" becomes
  "Option Both3" and cannot be repaired cleanly. Delete the question and re-add it.
- Settings afterwards: organisation only, record name, one response per person, accept
  responses.

## Hand the build over rather than grinding

After a second failed attempt at the same UI, stop and write a **build sheet**: the title,
the description block, each question with its type and its options in a paste-ready code
block, then the settings to tick and the steps for the link and the response workbook. The
owner can click a five-minute build sheet faster than an agent can lose another twenty
minutes to a designer that reorders fields under it, and a half-built form in their account
is worse than none.

When the owner hands back a form they built themselves, rewrite the build sheet to match
what is actually live — their option lists, their question order, their settings — instead of
the plan you wrote. That sheet is what the next rebuild or the next team copies from, and a
sheet that disagrees with the live form is worse than no sheet.

## Designer pages are separate CDP targets

Clicking a form card, or "Start review", opens a new tab. `js()` keeps evaluating on the
page you navigated to, so the click looks like it did nothing. Recover by listing targets and
navigating to the URL you want:

```python
for t in cdp('Target.getTargets')['targetInfos']:
    if t.get('type') == 'page' and 'DesignPage' in t['url']:
        print(t['url'])
```

**Print the id in full and reuse it in full.** The `id=` parameter is long base64 with a
suffix; clipping it at 150 characters and navigating to the clip returns "This form doesn't
exist" and reads like a deleted form.

## Settings to set before sharing

- **Who can fill**: "Only people in <tenant> can respond", with **Record name** ticked, so
  every answer carries its respondent without asking.
- **One response per person**: tick it. Untick only for a form that is meant to be filled
  repeatedly.
- **Start and end date**: leave off unless the deadline is real; the covering email carries
  the date better than the form does.

## Review by a manager before it goes to the org

Send a form to one trusted reviewer first, and choose deliberately between two links:

- **Share → Share to collaborate** makes them a co-owner: they can open the questions in the
  editor and see every response. That is the right default when the reviewer owns the
  people being surveyed, but say so — co-ownership means they can read what individuals say
  about their own workloads, and they can edit the form underneath you.
- **The fill link plus the question list** gives review without rights. Use it when the
  reviewer only needs to judge wording.

Also give them the fill link and ask for **one dummy submission**, then delete that row: the
editor view does not show what a respondent actually sees.

Ask for three specific things or you will get "looks good": whether any option is missing,
whether the proposed times suit the business, and whether the length is right. Attach a time
("thoughts by tomorrow lunchtime and it goes out that afternoon"), because a review with no
deadline sits until it is chased.

## Questions that survive the tool

Forms has no true matrix grid, but it does cap multi-selects: the question's settings offer
**at most N options**, shown to the respondent as "Please select at most 3 options". Use it
rather than trusting the wording to carry a limit, and mention the cap in the question text
too so people know before they start clicking.

- Asking "rate frequency and importance for twelve apps" as two grids is not possible;
  model it as two multi-select questions over the same option list — "which do you use at
  all" and "which could you not work without". Faster to fill, and it exports one column per
  app, which is what a pivot wants.
- Group options by **category** rather than naming every product ("Travel apps - Sabre,
  Tramada", "GPT based AI - Claude, Gemini, Copilot"). A category survives a tool being
  swapped, and a category the whole business already has (Microsoft 365) does not need asking.
- A free-text "what would you never do again" question is worth more than an invented list of
  tasks: the named tasks are the demand signal, and options narrow them to what you already
  thought of. Pair it with "what do you love that you would not want automated", which is the
  brake on the whole exercise.

## The share link

The link is rendered in a way page JavaScript cannot read, and `navigator.clipboard.readText()`
is refused without a user gesture. The embed panel is the way in: open **Collect responses →
Embed** and read the iframe `src` from the element text, which contains the full
`ResponsePage.aspx?id=…` URL. Failing that, ask the human to press **Copy link**. Do not
claim to have the link.

## Booking before you promise a scheduler

`https://bookings.cloud.microsoft/bookwithme/` answers "You do not have access to Bookings
with me" when the tenant does not licence it. Check that page before telling anyone a
self-booking link is coming, and have the fallback ready: a single-choice question of named
slots, each labelled with its length and a cap, plus one option "None of these work - I will
suggest two times". Picking is easier for respondents than describing availability, and the
agent can reconcile the picks against the principal's diary afterwards and prepare the
invites for approval.

Put slots where they do not cost the respondent their working rhythm: from late morning or
in the afternoon, not 9am, when the people filling it in are trying to get their own day
started.

**Read the principal's diary across the whole slot window before the list is published**, and
re-check it on the day the form goes out. Offering slots and then discovering two of them sit
on existing meetings turns colleagues into rescheduling work, and the owner will ask for the
calendar check if you skip it. Then ask for **two picks per respondent** rather than one: their
own second choice resolves most collisions, where a single pick leaves you emailing people
back. Reconcile the picks against the diary afterwards and prepare the invites for approval.

Spreading slots over several weeks is fine, but say so in the choice wording and keep the
count near a dozen; a list of twenty-five times is a second questionnaire.

## Put the responses where the analytics will look

Forms writes responses to a workbook through Responses then Open in Excel, and that workbook
lands in the OneDrive root. If the owner wants it in a named folder, move it afterwards and
verify the form still writes to it; state the folder in the hand-off rather than assuming the
default was acceptable.
