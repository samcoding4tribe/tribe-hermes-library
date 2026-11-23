# The org map

One source of truth for who is in the organisation and who reports to whom, used
at setup so a new assistant does not ask its user to describe a company the
business already knows.

Verified 24 November 2026: 26 people, one root, the renderer exits clean, the
chart draws 26 cards and no unnamed groups.

## Where it lives

| Path | What |
|---|---|
| `templates/org/people.json` | The data. Everything else derives from it |
| `templates/org/org-map.html` | The rendered chart, regenerated from the data |
| `templates/org/org-map.html.tmpl` | Markup and styles, carrying a `__DATA__` token |
| `templates/org/render.py` | Rebuilds the chart, validating the graph first |
| `templates/org/roster-2026.json` | Extracted from page 4 of the induction manual, including who has left |
| `templates/org/roster-review.html` | Tick list for pruning that roster |
| `templates/org/questionnaire.py` and `.xlsx` | The apps-and-agents questionnaire, rows generated from `people.json` |
| `templates/org/README.md` | The data contract, in the author's own words |

Published to `Hermes Library/templates/org`, so it is readable by the team.

## The fields

| Field | Meaning |
|---|---|
| `id` | Short stable key, used everywhere else. This is what a setup takes |
| `name`, `known_as` | Full name, and what people call them |
| `role` | Job title as the business states it |
| `function` | Broad area: management, events, travel, finance, design, support |
| `reports_to` | An id, or a list of ids, or null for the root |
| `badges` | Authority or location. Never rank |
| `notes` | Why a line is drawn as it is, and what is unresolved |
| `block`, `tier` | Drawing only. Where a card sits, not who it answers to |

## The rules the file enforces

- `reports_to` is the fact. A block is a drawing decision, and the two can
  disagree on purpose.
- An unknown `reports_to`, an unknown id in a group, or a duplicate id exits with
  code 2 and names the offender. A warning prints but still renders for a missing
  name or more than one root.
- No line is drawn that the business did not state. An unnamed team is a dashed
  card with a count, not invented names.
- Badges carry authority and location, never seniority.

## Using it at setup

1. Read `people.json` before asking the user anything.
2. Show the chart, ask which card is theirs, and take the `id` rather than a
   typed job title.
3. Ask the relationship questions against the chart, one at a time: who they
   report to, who reports to them, who approves expenses, leave and travel spend,
   who is copied on client correspondence, who covers when they are away.
4. Each answer becomes an edge with a source, written into that person's own
   context and, if it applies to every session, into their memory.
5. The chart is the shared spine. The person's profile holds their own view.

## What is not stored here

Contact numbers, email addresses, performance, preferences, anything private about
a person. Contacts belong in the directory. Preferences belong in that person's
profile. A chart that anyone can open should hold only what anyone may read.

## Current state

- Root: Leon, from whom every stated line descends
- One drawn block: the events team, grouped under Ness and Jodie
- Three external entries: a consultant, a software supplier, and a partner contact
- Four open questions: whether Vanessa and Ness are one person, which two people
  are the internal event-travel consultants, whether Belinda or Dani have teams,
  and the surnames still missing

## Updating it

```bash
cd templates/org
# edit people.json
python3 render.py people.json org-map.html
cd ~/tribe-hermes-library && python3 scripts/hermes_files.py sync
```

Edit the data, never the generated HTML. If the renderer rejects the file, read
the message: it names the id that broke.
