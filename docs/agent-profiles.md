# Agent profiles for TRIBE Group

Revised 23 November 2026. The first draft treated each job as its own assistant,
which was wrong. People do several jobs, and the events team does mostly the
same ones as each other.

The business, in one line: TRIBE Events sells conferences and incentive programs,
TRIBE Travel sells leisure travel as a Virtuoso agency, and both sell care and
detail rather than volume.

## The shape that fits

Two kinds of assistant, one per person:

**Manager assistant.** Diary, inbox, briefings, follow-ups, the things that
protect a manager's attention. Fewer tasks, higher stakes, more sending rights.

**Team assistant.** For event managers, coordinators and travel advisors. Budget
work, bookings, flight checks, run sheets, venue research, theme ideas, and
keeping account managers in the loop. Many tasks, repetitive, internal.

Both read the same shared skills. What differs is authority: a coordinator's
assistant drafts and checks, a manager's assistant can send after approval.

## Skills for the team assistant

| Skill | What it does | Where it reads |
|---|---|---|
| `budget-check` | Reconciles a budget sheet against quotes and bookings, flags variances | event folder, `FINANCE/` |
| `flight-watch` | Cross-checks itineraries against bookings, flags mismatches and schedule changes | booking confirmations, `TRAVEL/` |
| `run-sheet` | Builds the run sheet from the event folder: times, suppliers, staff, contacts | `EVENTS CLIENTS/<event>/` |
| `account-manager-brief` | Turns the state of an event into three lines an account manager can forward | event folder, mailbox |
| `supplier-chase` | Drafts confirmation chases and tracks what is outstanding | `SUPPLIERS/` |
| `venue-research` | Compiles options with capacity, location, cost ranges and past use | `SUPPLIERS/`, past proposals |
| `theme-ideas` | Proposes directions with references and precedent from past events | past events, `MARKETING/` |

## Skills for the manager assistant

| Skill | What it does |
|---|---|
| `inbox-triage` | Sorts, summarises, drafts replies for approval |
| `meeting-prep` | One page per meeting: who, what for, what was promised last time |
| `daily-brief` | What is due, what needs a decision, what can wait |
| `follow-up-watch` | What was promised and has not happened |

Shared by both: `weekly-review`, `draft-then-ask`.

## Responsibility levels

The same skill behaves differently depending on who owns the profile. This is
configuration, not a second tool.

| Level | Who | Can | Cannot |
|---|---|---|---|
| Draft | coordinators | read internal folders, draft documents and email, propose budgets | send, book, approve a payment |
| Approve | event managers | send approved communication, confirm a booking after a human yes | move money, sign a contract |
| Oversee | managers | everything above, plus briefs and delegation | act outside their own mailbox |

Approval mode is `manual` on role profiles, so a command asks before it runs.

## What that means in practice

- One profile per person, one machine each. Memory stays personal.
- Skills live in `shared-skills/`, improved once and inherited by everyone.
- Two coordinators with identical skills still keep separate memories.
- A manager's assistant is the same engine with a different soul, a different
  skill list and a stricter gate.
- Budgets, run sheets and the supplier register stay in the drive. The assistant
  reads them; it does not become a second copy.

## Counts

| Team | People | Archetype |
|---|---|---|
| Managers | few | manager assistant |
| Event managers and coordinators | most of the events team | team assistant |
| Travel advisors | a handful | team assistant, travel skills |
| Finance and admin | one or two | team assistant, finance skills |

Start with one event manager and one coordinator, because they do the same work
and their feedback will be about the same skills.

## Order I would build

1. `run-sheet`, `flight-watch`, `budget-check`. They recur every event and fail
   expensively when done by hand.
2. `account-manager-brief`, because the gap between coordinators and account
   managers is where information gets lost.
3. Manager skills, once the pattern holds on the events side.
4. `venue-research` and `theme-ideas` last, since judgment there is the hardest
   to encode and the easiest to get wrong.

## Still unknown

- How many managers, coordinators and advisors actually need one
- Whether coordinators own a budget or only track one against someone else's
- Whether the finance system has an API or only exports
- Who signs off on a booking, and whether that varies by event size
