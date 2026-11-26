---
name: second-brain
description: "Set up a private notes vault an agent can read and grow."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [notes, obsidian, memory, knowledge-base, personal]
    related_skills: [obsidian]
---

# A second brain an agent can read

A folder of markdown the person owns, in git, that an assistant can read when a question
turns on something that happened before. The point is recall: past meetings, ideas worth
keeping, and why a decision was made — without a growing to-do list and without asking the
person to explain their own history again.

## When to use

- Someone wants their thinking to survive a chat: ideas, meeting records, reasoning.
- An assistant keeps re-deriving things the person already worked out.
- Someone asks how to give an agent "memory of my notes".

Not for: work products that belong in a shared drive, or decisions that belong in a project
repository. See the boundary section.

## The proposition, in one paragraph

Two stores, different jobs. The **work repository** holds the system: decisions, procedures,
scripts, published profiles — anything a colleague or a future maintainer needs. The **vault**
holds the thinking around it: ideas that are not urgent, what was said in a room, the reasons
behind a choice. They are separate repositories with separate audiences, and a note lives in
exactly one of them.

## Shape of a note

- **The filename is the title, written as a sentence.** Not `notes/2026-03-02`, not
  `japan_trip_timing`.
- **No heading that repeats the filename.** Most editors already render it as the title.
- **Open with a lede**: one or two sentences saying what this note is and why it matters,
  then the detail.
- **One idea per note.** If two sections could answer different questions, they are two notes.
- **Sources at the end.** A claim without a source is a memory; say so if it is one.
- **Tags in frontmatter only**, two to five, lowercase and hyphenated. No dates, no status, no
  author — version control already holds those, and hand-kept metadata goes stale.

## Tags and links are not the same thing

Tags answer *what is this about*; links answer *how does this connect*. Do not use one for the
other. A graph built only from tags is a set of category stars; the edges that carry meaning
are the wikilinks between notes. Backlinks are not something a person adds — a link creates
the reverse automatically, so the working rule is simply that every note links out at least
once and is linked from at least once.

## The index note

One entry note, read first every time. It lists the notes worth starting from and defines the
tag vocabulary as a table. **A new tag is added there first, with a one-line meaning**, which
is what stops six spellings of the same idea accumulating. When a tag reaches roughly twenty
notes, it earns a hub note: a page that is mostly links.

## Setting it up

1. Create the vault folder outside any shared or synced team drive, and make it its own git
   repository with a **private** remote.
2. Write the conventions note before the second note exists — naming, tags, links, what does
   not belong. Every later session, human or agent, reads it instead of guessing.
3. Write the index note: where to start, the tag table, and how to navigate by tag.
4. Give the assistant access in its **memory file**, not in its soul or its skills — see the
   boundary below. The rule to write down: read the index first, then follow links or search
   by tag; never read the whole vault to answer a small question.
5. Writes happen on request. Additive notes and corrections are fine; renames, moves and bulk
   rewrites are proposed first.

## The boundary that keeps this clean

Everything in a profile except its memory is published when the profile is shared: souls,
skills and config reach a library other people can read. So:

- **A personal vault is named in the profile's memory**, which never leaves the machine. Never
  in a soul, a skill, or a template.
- **Never copy a decision into the vault as a second version.** The note says what the idea is
  and points at where it is settled; two copies that drift is how the wrong one gets quoted.
- **Private means the repository's visibility**, not the folder's. A private repo with meeting
  records in it is still a repo whose history holds every meeting record forever.
- Contact numbers, credentials and remarks about colleagues do not belong in either store.

## What an agent should do when it works here

- Read the index, follow links, search by tag. Do not sweep the vault.
- Treat notes as claims, not facts; check the history when a date matters.
- When two notes contradict, do not silently pick one: say so in the newer note and flag it.
- Never run git in the vault if an editor plugin already owns the history.
- Never bulk-rename, restructure or delete without an explicit yes.

## Renaming or re-angling a note

The filename is the title, so a rename is a content change that reaches every page pointing at
it. Do it in this order:

1. `mv` the file, keeping the sentence form. Propose it first if the vault's rules say renames
   need a yes; an agent that renames on its own breaks links it cannot see.
2. Grep the vault for the **old title as link text**, not the path, and update every hit. The
   index almost always links it and other notes sometimes do; a wikilink to a filename that no
   longer exists renders as a dead link and nothing warns you.
3. Rewrite the lede to match the new name. A note renamed to a new purpose keeps an opening
   sentence about the old one, and the title then promises something the body does not answer.
4. If the new name is a working artefact — "points to raise at a meeting", "options for the
   board" — put a short numbered summary at the top. A note opened in a room gets read in its
   first ten lines, not in order.

## Pitfalls

- **Anchoring a section insert on a heading deletes the heading.** When patching to add a
  section "before" another, the anchor is the heading line itself: re-emit it at the end of the
  replacement or it disappears and the content under it silently joins the previous section.
  Headings above reference lists are the usual casualty. After any structural patch, read the
  headings back (`grep -n '^## '`) rather than trusting the diff summary.
- **Write what people did, not what it says about them.** A note about a colleague using a tool
  the owner dislikes, or a team keeping a supplier alongside a new one, records an observation
  plus the decision it creates. Dressing it as resistance, shadow purchasing or a discipline
  problem turns a factual record into an accusation the owner has to walk back in the next
  meeting — and the vault keeps the first version forever.

- **Dates in filenames age badly.** A note is edited for months; the date in its name starts
  lying almost immediately, while the body can carry the date where it belongs.
- **Status lines rot.** "Draft", "in progress", "TODO" in frontmatter are stale within a week.
- **An agent that reads the whole vault** costs a fortune in context and answers worse.
- **A vault with no conventions note** becomes a pile of paragraphs nothing can be asked of.
- **One note per thought beats one note per topic** the moment two people need to look things
  up in different orders.
