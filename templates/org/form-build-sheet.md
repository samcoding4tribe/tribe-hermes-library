# Form build sheet — as built

The live form, 25 November 2026. This records what was actually built rather than the earlier
plan, so a rebuild or a copy for another team starts from the real thing.

Title: **How your week works, and what to automate**

Description:
```
I'm mapping how the business actually runs before building anything, so this is about your
week rather than tools in the abstract. Six questions, about three minutes. Only used to work
out what would genuinely help your role.
```

Settings: organisation only, record name on, one response per person, accepting responses.

---

## Q1 — Which of these do you use at all?

Choice, required, multiple answers allowed.

```
Comm channels other than Teams - Slack
Travel apps - Sabre, Tramada
Booking or reservations system
EventsAir
GPT based AI - Claude, Gemini, Copilot or ChatGPT
Adobe apps
Agent based AI - like Hermes
Coding apps - Cursor, Claude Code or the like
Xero
Accounting apps other than Excell or Sheets
Other
```

Grouping by category rather than naming every product was the right call: Microsoft 365 is a
given for everyone and does not need asking, and a category survives a tool being swapped.

## Q2 — Select 3 you could not work without?

Choice, required, multiple answers with **at most 3** selected. Same eleven options as Q1.

## Q3 — Which two or three of these slow you down most?

Choice, required, multiple answers with **at most 4** selected.

```
Too many systems to check
Re-typing the same information
Chasing clients or suppliers
Not finding the right document or email
Building reports
Scheduling
Email volume
No single source of truth
Handovers between people
Something else
```

## Q4 — Which two or three tasks would you most like to never do again?

Text, required. Free text on purpose: the named tasks are the demand signal, and options would
narrow them.

## Q5 — What do you love about the job that you would not want to lose to automation?

Text, required. This is the question that stops something people value being automated away.

## Q6 — Pick preferred time for our chat, pick two in case there are clashes, sorry I did not have access to the Bookings app.

Choice, required, multiple answers with **at most 2** selected.

```
Tue 1 Dec, 11:00-11:20
Tue 1 Dec, 16:00-16:20
Wed 2 Dec, 14:00-14:20
Thu 3 Dec, 11:30-11:50
Thu 3 Dec, 15:00-15:20
Fri 4 Dec, 11:00-11:20
Fri 4 Dec, 14:30-14:50
Tue 8 Dec, 11:00-11:20
Tue 8 Dec, 15:00-15:20
Thu 10 Dec, 11:30-11:50
Thu 10 Dec, 15:00-15:20
Fri 11 Dec, 11:00-11:20
Tue 15 Dec, 14:00-14:20
Wed 16 Dec, 11:30-11:50
Thu 17 Dec, 15:00-15:20
None of these work - I will suggest two times
```

Asking for two picks rather than one is better than a booking tool here: it gives one preferred
and one fallback per person, which resolves most collisions without another round of email.

**Diary check, 25 November:** five events sat in the period. Sabre AI and Automation (Tue 1 Dec,
2:00-3:30) and Tribe Travel Automation and AI (Tue 1 Dec, 2:00-3:00) are the *same meeting* —
Iva books a room as a separate entry so the team can join the Teams call from the office, so
that is not a double booking. Also in the period: Tribe x Hyatt Centric visit (Wed 2 Dec, 11:30-12:00), the welcome lunch with Kelly and Leon
(Tue 8 Dec, 12:30-1:30), and the AI project review (Wed 9 Dec, 2:30-3:30). Re-check before
sending if anything lands in the meantime.

---

## Two corrections to earlier assumptions

- **Forms does cap selections.** The question menu offers "at most N options", so the limit is
  enforced rather than implied by wording. Q2 and Q3 use it; Q6 uses it at two.
- **Do not import questions from a Word document.** Headings and bullets arrived as text
  paragraphs rather than choice controls, producing a form that looked right in the editor and
  could not be answered. Build the choice questions by hand, pasting all options into the first
  option box at once so Forms splits them.

## After the form is live

- Collect responses → Copy link for the email.
- Responses → Open in Excel creates the workbook; move it into **TRIBE Group - TRIBE Group Tech**
  before responses arrive, and delete the test row from your own preview submission.
- When answers land, reconcile the two time picks against the diary, then send the invites.

## What the answers are for

Two questions carry the building decisions. Q2 says what must not break in a role, and Q4 says
where the time goes. A role scoring high on both pays back first; a role where nothing is
critical is a training problem, not an automation one. Q5 is the brake on all of it.
