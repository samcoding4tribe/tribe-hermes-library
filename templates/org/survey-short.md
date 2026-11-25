# Pre-meeting survey and booking — build sheet

The short version of the apps-and-agents questionnaire: six questions, about three minutes,
one link, filled in before the one-to-one. Everything here is written to be pasted into
Microsoft Forms as-is.

## Why Forms, not a SharePoint list

A SharePoint list is a database with a form bolted on; a survey is a form with a spreadsheet
behind it. Forms wins here because responses record the signed-in person automatically when
the form is set to "people in my organisation", it exports cleanly to Excel for pivoting, and
the respondent sees one scrollable page rather than a table they can edit. The list can come
later, as the store the responses are copied into.

## Booking

Microsoft Bookings is the right facility, and it is **not available to this account**: loading
`bookings.cloud.microsoft/bookwithme` returns "You do not have access to Bookings with me", so
the licence is missing or the feature is off in the tenant. Three ways forward:

1. **Ask Comwire to enable Bookings.** Best long term, one week or two of lead time.
2. **Collect the slot in the same form** (recommended now).  Offering fixed windows as a
   question gets people booked without a licence, with collisions resolved by hand.
3. **Send individual calendar invites in batches.** No form change, but more mail and more
   replies to chase.

## The form

Internal only, record respondent name, one response per person. Six items, about three
minutes. Paste these in as written.

**1. Which part of the business do you work in?** Single choice
Events / Travel / Both / Support function

**2. How often do you use each of these, and how important is it?** Two grids, same rows
Frequency: Daily / Weekly / Monthly / Rarely / Never. Importance: Critical, I could not work
without it / Useful / Nice to have / Not needed.

Rows, collided from what we already know about the business rather than guessed:

Outlook · Teams · SharePoint or OneDrive · Excel · Word · PowerPoint · Planner or To Do ·
Power Automate · Power BI · EventsAir · Sabre · Adobe InDesign · Claude or ChatGPT ·
Xero or accounting · Booking or reservations system · Other (name it)

**3. What slows you down day to day?** Multi choice, pick any
Too many systems to check · Re-typing the same information · Chasing clients or suppliers ·
Not being able to find the right document or email · Building reports · Scheduling ·
Email volume · No single source of truth · Handovers between people · Something else

**4. Which two or three tasks would you most like to never do again?** Long text.
Short instruction: "Be specific. 'Chase supplier confirmations' is more useful than
'admin'."

**5. What do you love about the job that you would not want to lose to automation?**
Long text. This one matters as much as the last: it tells us where to leave the work alone,
and it is the question people answer most honestly.

**6. Pick a time for our chat.** Single choice of named slots, each labelled with a cap
("Tue 1 Dec, 9:00-9:20"), plus one option: "None of these work - I will suggest two times",
with a short text field beneath it.

## The email

Subject: **Two minutes before we meet**

> Hi {first name},
>
> I'm meeting everyone over the next few weeks to understand how your week actually works,
> so anything I build fixes something real rather than something I assumed.
>
> Before we talk, could you fill this in? It's six questions and takes about two minutes,
> and it means we can spend our time on the interesting parts instead of the inventory.
>
> {form link}
>
> Then pick a time that suits you from the slots at the end of the form, and I'll send an
> invite. If none of them work, send me two windows that do and I'll make one fit.
>
> Thanks,
> Sam

Send order: managers first, since their answers shape the questions asked of their teams.
Ness has already been contacted; the rest of the management group next, then the wider team
in the same week so nobody hears about it third hand.

## What to do with the responses

Export to Excel, reshape into one row per respondent per question, and pivot importance
against repetitive hours by role. A role where something is critical and the manual work is
heavy pays back first; a role where nothing is critical is a training problem rather than an
automation one. The one-to-one is then a conversation about their three named tasks, not a
second interview.
