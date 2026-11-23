# For the builder profile — what this folder is and why it exists

Written by the admin profile that runs Sam's own day (the profile at
`~/.hermes/profiles/admin/`), 23 November 2026. You are the profile that builds
agent profiles for the rest of TRIBE. This note exists so you inherit the
reasoning rather than reverse-engineering it, and so neither of us drifts into
the other's job.

## Why these files exist

Two problems were on the table. The first is that every new assistant profile
otherwise starts from nothing: it asks its user to describe a reporting line that
the business already knows, and it cannot tell whether "GM" means the general
manager or one of two managing directors. The second is that Sam needs to collect
data about which applications each role depends on, and answers that cannot be
attributed to a role are not much use for deciding which profiles to build.

One data file answers both. `people.json` is the shared spine, and the
questionnaire's respondent list comes from it so nobody types 26 names twice.

## What is here, and the reasoning behind it

**`people.json` is the only source of truth.** Everything else is generated. A
chart drawn by hand goes stale the first time somebody leaves, and then two agents
answer "who does X report to" differently. `render.py` validates before writing —
an unknown `reports_to`, an unknown id in a group, or a duplicate id exits with
code 2 and names the offender — because a builder has to be able to trust a file a
human edited.

**The chart is a tree of nested columns, not rows of boxes.** Managers sit in one
row, each is a column, and their own team stacks beneath their card on a left
spine. That is the shape people recognise as an org chart. The connectors are an
SVG overlay measured after layout, so they survive a narrower window, and they sit
behind the cards so an elbow crossing another card is hidden rather than striking
through the text.

**A block is a drawing decision; `reports_to` is the fact.** The events team is
drawn together under Ness and Jodie because Sam asked for one block rather than a
scatter, and Jamie and Jovelle sit a tier lower inside it. Their own
`reports_to` still says Ness. When you read the data, trust `reports_to`; when you
explain the picture to a user, the block is what they will point at.

**Badges carry authority and location, never rank.** Kelly is a part owner with
executive authority and sits on the same level as the other managers. Leon heads
both businesses but is drawn in the events space by Sam's instruction. Both facts
live as text on the card, because making a box taller asserts a hierarchy nobody
stated.

**The roster came from a photo directory, not an org chart.** Page 4 of the
induction manual lists names and titles in two panels and draws no lines at all.
If you are ever handed a similar page, extract names and titles from it and expect
to get the relationships from the owner. Laura has left and is excluded; Jamie,
Jovelle and ERJ are offshore in the Philippines; Jan is a consultant and not
in-house, so he sits with external contacts.

## What still has to come from a human

Whether the Vanessa on page 4 is Ness; which two people are the internal
event-travel consultants; whether Belinda or Dani have teams; and surnames for
Leon, Belinda, Dani and much of the events team. These are recorded in
`open_questions` inside the data file, and they are the reason the chart is not
finished. Do not resolve them by inference, and do not clear the list to make the
chart look tidy.

## How to use it at set-up

Read `people.json`, show `org-map.html`, and ask the new user which card is
theirs. Take the id. Then ask the relationship questions against the chart rather
than in prose, because pointing at a card is faster and less ambiguous than
typing a title. Every answer belongs in that person's own context file with its
source; the shared folder holds the spine, the person's profile holds their view.

## The boundary between our two jobs

Sam asked for these two jobs to stay apart. The admin profile keeps a person's own
day: inbox, diary, drafts, follow-ups. It does not deploy or maintain other
profiles, and it should not be asked to. You own deployment, and the people you
deploy for are not technical, so nothing you hand them should require a repository,
a build, or a command to remember. They get their own record and their own
assistant, not this folder.

Two rules follow from that. Facts about one person stay in that person's profile
and never get copied into another — not their inbox habits, not their manager's
comments, nothing. And the shared spine is data, not a checkout: copy
`people.json` forward, do not link a colleague's profile to a git remote.

## Updating this

Edit `people.json`, run `python3 render.py people.json org-map.html`, and the
chart follows. This folder is a snapshot of
`~/tribe-hermes-library/templates/org/`; the library copy is the versioned one.
If you change anything here, tell Sam, so the change goes back into the library
and the history stays in one place instead of two.

## The questionnaire

`questionnaire.xlsx` is a draft, not a deliverable. Sam's view, and he is right,
is that nine minutes is too long and that the collection belongs in a Microsoft
form — Forms or a SharePoint list — writing into a table that can be pivoted. The
target is around three minutes: six questions with two grids over the app list.
The analytics intent is worth keeping when it gets rebuilt: answers in long format,
one row per respondent per question, so importance can be cut against repetitive
hours by role. A role where an app is critical and the manual work is heavy pays
back first. Leave the rebuild to the admin profile unless Sam says otherwise.
