# The Sam Tribe Brain vault

`~/Documents/sam-tribe-brain` — Sam's second brain for TRIBE work: durable ideas and
decisions, not a scratch pad, not the repo. Working material belongs in the repo; a note
here is for what should still make sense in a year.

## Rules of the house

- **Read freely; write on request.** Sam has allowed reads; a note is written when he asks
  for one, not because a session produced something interesting.
- **Obsidian Git owns history.** It auto-commits and pushes on `main`. Never run git in the
  vault, never switch its branch, never stage/commit/push from a shell.
- **Filename is the title**, written as a sentence: `Only the rules travel from a soul, not
  the voice.md`. No H1 repeating it.
- **One idea per note.** If two sections would answer different questions, that is two
  notes.
- **Open with a lede** of one or two sentences, then detail. End with `## Sources` naming
  who said it, when and where; a claim with no source is a memory, so say so.
- **Frontmatter carries only 2–5 lowercase hyphenated tags.** No dates, no status, no
  author.
- **A new tag is declared in `index.md` first**, with a one-line definition in the tag
  table, then applied. A tag missing from that table is a typo.
- **Every note is linked from `index.md` and links out at least once.** An orphan is
  invisible.

## Tag vocabulary worth knowing

Domain: `dsh`, `hermes`, `safety`, `permissions`, `setup`, `events`, `travel`.
Type: `index`, `meta`, `conventions`, `decision-record`, `idea`, `reference`.

`hermes` was added for the Hermes agent estate — profiles, baselines, rollout. Use it on any
note touching the agent setup. `dsh` is the *older deepseek-harness* workspace and is not
interchangeable: a note about DSH rules is not a Hermes note.

## Pitfall: the vault's own AGENTS.md describes another workspace

The vault carries an `AGENTS.md` written for the DSH harness — `.notes-staging/`,
`publish-notes.sh`, `sync-agents.sh`, a staging-then-one-approval batch flow. Those scripts
live in that workspace, not here, and they are not the route for a Hermes session. Write
notes with `write_file` against the resolved absolute vault path, then update `index.md`, and
leave git to Obsidian.

Do not follow the tier/branch procedure in that file for ordinary additive notes; it exists
to stop an agent reorganising the vault, and nothing here warrants it.

## The write, in order

1. `search_files` the vault for an existing note on the idea; extend it rather than add a
   second copy.
2. `write_file` the note at the resolved path — no shell variables, the path has no spaces
   but sibling paths in OneDrive do.
3. `patch` `index.md` to add the link under Start here, and the tag row if it is new.
4. Reply with the note titles and the tags used, two or three lines.
