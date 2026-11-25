# The people map

A cited map of who the principal works with, kept as a table in the context file
and rendered as a widget so the owner can correct it at a glance. It is the
reference every later task leans on — who to chase, who approves, who is away.

## Build it

1. Take the relationships **from what the owner tells you**, one statement at a
   time. They arrive in ones and twos over several turns; expect to rebuild.
2. Tag each edge with its source in the table (`as told by <name>` once at the
   top is enough; per-row sources only for entries that came from evidence).
3. Put everything from mail and calendar into the table with the artefact that
   proved it — a signature block for a phone number, an invite for an attendee.
4. Render it. Then treat the render as the question: "say which of these lines is
   wrong and I will redraw it."

## Drawing rules

- **Only draw what you were told.** An unconfirmed relationship is a card in a
  band, not a line. One confirmed edge is worth more than a tidy chart.
- **Peers share one band row**, labelled `Same level, beneath <person>`. Do not
  stack them under each other to imply seniority you were never given.
- **A single report goes inside the card** as `↳ Name — role`; a team is a
  labelled branch row (`Under <name>`) beneath the peer row. Inline arrows stop
  working the moment one peer has three people under them — the card grows while
  its neighbours sit empty, which reads as uneven seniority.
- **Groups shared by two managers** get their own row titled with both names, not
  one row per manager, or the same team appears twice and invites a correction
  that is really about the duplicating.
- **Separate the drawing decision from the fact.** `blocks: [{id, title, parents}]`
  plus `block` and `tier` on a person draws them together beneath one or more
  managers in numbered rows, while each person's `reports_to` keeps the line the
  owner actually stated. Use it when the owner says "put them with the others to
  make it easier": the chart stays legible and a future session cannot read the
  grouping as a second reporting line. A person whose manager is not known gets
  `unplaced: true` and renders in a `Not yet placed` band, never a guessed parent.
- **Authority is a badge, not a rung.** Part owner, executive power, delegated
  sign-off: text on the card. Making the box taller or wider asserts a rank the
  owner did not describe.
- **Leave gaps visible.** No surname until given, `+ N unnamed` for a team counted
  but not named. An empty slot invites the next correction; an invented name
  destroys the file's credibility.
- **Two artifacts, one edit.** The table and the widget change together, in the
  same reply, or the next session works from a stale map. If the map has a data
  file, the data file is the third: edit it, re-render, and never hand-edit the
  generated HTML.

## Pitfalls

- **Escape each string once.** A band title built as `esc(name)` and then passed
  through a helper that escapes again renders `&quot;` and `&amp;` on screen. Keep
  escaping at the point of interpolation only.
- **Exclude block and shared-row members from the children lookup.** A person
  drawn in a shared block still has a `reports_to`, so a naive
  `childrenOf(id)` renders them twice: once in that manager's column and once in
  the block. Filter `!p.block` in `childrenOf` and keep one rendering path per
  person; verify by collecting every card's id and asserting no duplicates.

## Rendering the widget

- Use the frame's theme vars with hex fallbacks — `var(--foreground, #e9e9ea)`,
  `var(--border, #3a3a40)`, `var(--card, #1b1b1f)`, `var(--accent, #ff7a1a)`.
- **Fallbacks alone do not make a standalone page readable**, because the owner
  will open the file in a browser: light text on a white page. Detect the missing
  theme and set a dark page instead of forcing every colour by hand —
  `if (!getComputedStyle(document.documentElement).getPropertyValue('--foreground').trim())`
  then set the five vars plus a dark `background` and `colorScheme` on the root.
- **Set `box-sizing: border-box` on flex cards.** `min-width` plus padding and
  border without it overflows the row and silently wraps the last card onto its
  own line, which reads as a different level.
- **A peer row inside a flex column collapses to min-content.** With
  `.tree { display:flex; flex-direction:column; align-items:flex-start }` the
  row's width comes from the widest card, so six peers break into a two-column
  grid of three rows and read as three levels of rank. Put `width: 100%` on the
  flex column and on the band that holds the row, then re-verify the tops.
- **Never print a card's reports twice.** The root's direct reports are the peer
  row; listing them again as `↳` lines on the root card duplicates a whole level
  and makes the chart look broken. Inline `↳ Name — role` belongs to cards whose
  reports are not drawn as a row beneath them.
- Cards carry name, role, badge, and the `↳` line. Long role text wraps to three
  lines and breaks the row's rhythm; move detail into the table instead.
- **Verify the layout, do not eyeball it.** Emulate the frame width with
  `cdp('Emulation.setDeviceMetricsOverride', width=940, ...)` and check two
  things: `document.documentElement.scrollWidth` has not exceeded the frame (a
  card `min-width` that ignores the column width pushes the last column off the
  edge), and the connector path has one segment per expected edge.

## Drawing it as a tree

Owners ask for a tree, not stacked rows of boxes, once the org has depth. The
shape that works in a chat frame:

- **Nested columns.** One row of managers; each manager is a flex column holding
  their card, with their team stacked beneath it sharing a left spine. Rows of
  boxes read as a list; columns with connectors read as an org chart.
- **Wire with an SVG overlay measured after layout** (`getBoundingClientRect`),
  not with CSS borders: the row a card lands in depends on text wrapping, so any
  line drawn from assumptions breaks at another width. Redraw inside
  `requestAnimationFrame` and on a `ResizeObserver` of the tree.
- **Paths behind cards, cards in front** (`svg { z-index: 0 }`, `.node
  { z-index: 1 }`). An elbow that crosses another card then disappears behind it
  instead of striking through the label.
- **Shared teams get their own row**, aligned to the left-most manager who owns
  them, with a drop from each manager into one bus. Splitting a shared team to
  make the chart tidier invents an owner.
- **Set `min-width: 0` on cards inside a column.** A card carrying
  `min-width: 170px` in a 146px column overflows the frame and silently truncates
  the right-most manager.
- When the people are external, group them under an `External` heading rather
  than mixing them into the levels. Suppliers and partners have no rung.

## Package it for reuse

When other deployment agents have to consume the map — the usual reason is that
setup should ask "which of these people are you" instead of collecting a free
text title — ship data, template and renderer rather than a finished HTML file.

- `people.json` — the source of truth: `id`, `name`, `known_as`, `role`,
  `function`, `reports_to` (id or null), `badges`, `notes`, plus `groups` for
  counted-but-unnamed teams, `external`, and `open_questions`.
- `org-map.html.tmpl` — the chart carrying a `__DATA__` token, rendered
  client-side from the injected JSON.
- `render.py` — stdlib only. Validate before writing: unknown `reports_to`,
  unknown group id or duplicate id exits non-zero naming the offender. Validation
  is what lets a builder trust a file a human edited by hand.
- `README.md` — the setup sequence and the data contract.

Render the owner's own map from the same JSON. A hand-written second copy drifts
the first time the org changes, and then two agents answer "who does X report to"
differently.

Ship three documents, not one: a `HANDOFF.md` with the read-this-file and the
set-up sequence, a `FOR-THE-<ROLE>-PROFILE.md` written to the agent that will
consume the package explaining what was built and why, and the README with the
data contract. The middle one is the one that stops the next agent re-deriving
your reasoning: state the decisions (source of truth, why a tree, why a block is
a drawing decision and `reports_to` is the fact), the open questions that must
come from a human, and the boundary between the two jobs so it does not walk back
into the owner's day. Keep it in the owner's voice and free of build steps, since
the people receiving those profiles are not technical.

Leave the chart clickable for the setup flow: a click sets a selected id that the
page exposes back (`window.orgMap.selected()`, `person(id)`, `childrenOf(id)`), so
the builder asks "who do you report to?" with the chart itself as the answer
surface. In this org the package lives at
`~/tribe-hermes-library/templates/org/`.

## Updating it later

- Rebuild the file and the widget from the model you now hold, rather than
  patching prose around the old mistake. The artifacts are cheap.
- Record open questions in the table's notes column (`surname not yet given`,
  `offsite since <month>`), not as footnotes nobody re-reads.
- When a new position is described, add the row, redraw, and ask the one question
  that would let you place them properly — usually who they answer to.
