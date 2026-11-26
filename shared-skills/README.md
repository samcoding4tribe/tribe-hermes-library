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

| Skill | What it is |
|---|---|
| `second-brain` | How to stand up a private notes vault an assistant can read, and the boundary that keeps it out of published profiles |
| `executive-admin-support` | The admin role: what it covers and how it is done |
| `mail-handling` | Reading, triage and drafting in mail |
| `microsoft-365-web` | Reaching Outlook and the rest through the browser |
| `morning-brief` | The shape of a morning brief |
| `watchlist-digest` | The people and threads not to miss |
| `link-batch-download` | Fetching a list of asset links |

| Profile | Reads this folder |
|---|---|
| `admin` | Sam's own work admin |
| `ea` | executive assistant pilot for a manager |
