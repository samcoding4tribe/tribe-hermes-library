# Shared skills

Skills in this folder load into every profile that points here, through
`skills.external_dirs`. Write a procedure once and both the personal admin
assistant and the manager's executive assistant follow it.

What belongs here:
- procedures that are about the job, not the person: how to triage an inbox, how
  to prep for a meeting, how to file an expense, how to hold a weekly review
- nothing that names a person, an address, an account or a password. A skill may
  say "ask who signs off"; it may not say who that is.

What does not belong here:
- memory. Each profile keeps its own, and personal facts never cross into a work
  profile.
- anything already shipped with Hermes. Those live in `~/.hermes/skills`.

Each skill is a folder with a `SKILL.md` inside, frontmatter first, description
under 60 characters.

## Current members

| Profile | Reads this folder |
|---|---|
| `admin` | Sam's own work admin |
| `ea` | executive assistant pilot for a manager |
