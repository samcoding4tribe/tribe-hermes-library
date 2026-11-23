# Org people map — data, renderer, and the setup-stage idea

A single source of truth for who is in the organisation and how they relate,
plus a renderer that turns it into a chart. Exists so that a deployment agent can
place a new user in the organisation at setup time instead of asking them to
describe it from scratch, and so that every assistant in the org answers "who
does X report to" the same way.

The facts live in `people.json`. The look lives in `org-map.html.tmpl`. Nothing
about an individual's preferences, performance or private notes belongs here —
those stay in that person's own profile.

## Render it

```bash
python3 render.py people.json org-map.html          # writes the chart
python3 render.py people.json /path/to/out.html     # anywhere else
```

Validate-only behaviour: an unknown `reports_to`, an unknown id in a group's
`under`, or a duplicate id fails with exit code 2 and a specific message. Warnings
(name missing, more than one root) print but still render.

To show it in a Hermes desktop chat, put this on its own line:

```
::preview{file="/absolute/path/to/org-map.html"}
```

## What the deployment agent does with it

At profile setup, in this order:

1. **Show the chart.** Ask: "which of these people are you?" The answer gives the
   agent an id, not a free-text title.
2. **Ask the relationship questions, one at a time**, using the chart as the
   answer surface — the user points at a card rather than spelling a name:
   - who do you report to?
   - who reports to you?
   - who approves your expenses, leave, and travel spend?
   - who must be copied on client correspondence?
   - who covers for you when you are away?
3. **Store each answer as an edge with a source**, in that person's
   `workspace/<name>-context.md` and in the profile's memory if it is a fact that
   applies to every session. The chart is the org spine; the person's profile
   holds their own view of it.
4. **Never infer a line the user did not state.** Ownership and delegated
   authority are badges, not rungs. An unnamed team is a dashed card with a
   count, not invented names.

The rendered chart is interactive for exactly this reason. Clicking a card
selects that person and the footer shows their id; a builder can read it in the
page:

```js
window.orgMap.selected()        // "kelly"
window.orgMap.person('kelly')   // the full record
window.orgMap.childrenOf('kate') // [{name: 'Samuel Klett Navarro', ...}]
```

If the widget is embedded in a Hermes desktop chat, a card can carry
`data-hermes-send="I am <id>"` so the click sends the answer as a prompt back to
the agent. Add that only when the agent on the other end is expecting it.

## Data contract

```jsonc
{
  "org": "TRIBE Group",
  "as_at": "2026-11-23",
  "source": "who told you this, and when",       // shown under the title
  "legend": "one line explaining badges and dashed cards",
  "people": [
    {
      "id": "kelly",                             // stable, lowercase, used everywhere
      "name": "Kelly Gelfand",
      "known_as": "Kelly",                       // optional
      "role": "Travel",                          // shown on the card, keep it short
      "function": "Management",                  // grouping, not displayed
      "reports_to": "leon",                      // null for the root, or an id
      "badges": ["Part owner"],                  // authority, never rank
      "notes": "free text: surname unknown, offsite, phone"
    }
  ],
  "groups": [
    { "label": "+ 7 events staff", "detail": "event org, coordinator and management",
      "under": ["ness", "jodie"] }
  ],
  "external": [{ "name": "Sabre — contacts", "detail": "software supplier" }],
  "open_questions": ["who do the event-travel consultants answer to?"]
}
```

- `reports_to` builds the lines: a single id, `null` for the root, or **an array
  of ids** when someone answers to two managers at once. `"unplaced": true` marks
  a person whose reporting line is not known yet; they render in a band beneath
  the tree rather than floating loose or inventing a parent.
- `blocks` place people together beneath one or more managers in numbered tiers,
  without changing anyone's `reports_to`: the block decides where a card is drawn,
  the person's own line stays factual. Use it when the owner wants a team kept in
  one place for legibility rather than repeating who answers to whom, and for a
  rank that sits below the rest of the block (`"tier": 2`).
- `groups` are counted-but-unnamed teams. They render as dashed cards and never
  as lines.
- `open_questions` prints under the chart, so an unanswered relationship is
  visible rather than silently missing.

## Layout rules the renderer already enforces

- Theme variables with hex fallbacks, so the same file is legible inside the
  Hermes frame. Opened standalone it assumes a dark page.
- `box-sizing: border-box` plus a grid row: `min-width` with padding without it
  overflows and silently wraps the last card onto its own line, which reads as a
  different level.
- Verify, do not eyeball: emulate 940px width and compare
  `getBoundingClientRect().top` across a row; equal values mean one row.

## Keeping it current

`people.json` is the file to edit. Then re-run `render.py`. Do not hand-edit the
generated HTML — the next render overwrites it. When someone is added to the org,
add the row, redraw, and ask the one question that places them: who do they
answer to.

## How the tree is drawn

Managers sit in one row under the top of the organisation, each in its own
column, and a manager's team stacks beneath their card sharing a left spine —
the shape people expect from an org chart, rather than rows of boxes.

Connectors are an SVG overlay measured after layout with `getBoundingClientRect`
and redrawn on resize, so the tree survives a narrow window. The paths sit at
`z-index: 0` and the cards at `1`, which means an elbow that crosses another
card is hidden behind it instead of striking through the text.

A team shared by two managers (here the seven events staff under Ness and Jodie)
gets its own row, aligned to the left-most of the two, with a drop from each
manager's card into one horizontal bus. It is the only structure that does not
nest inside a single column, and it is worth the extra code because inventing a
single owner for a shared team would be a worse lie than an unusual line.

Colours, badges and dashed cards behave as elsewhere: badges are authority,
dashed is counted-but-unnamed, and only stated lines are drawn.
