# Keeping a profile's context small

What actually costs tokens when a profile runs, what only costs disk, and the rules
that keep the second from becoming the first. Numbers below are measured on the
admin profile on 25 November 2026 and will drift, so re-measure rather than quote.

## What loads on every turn

| Thing | Size measured | Loads |
|---|---|---|
| `SOUL.md` | 1.5 KB | every turn, first in the prompt |
| `USER.md` (facts about the person) | 1.36 KB, cap 1,375 chars | every turn, frozen at session start |
| `MEMORY.md` (what the agent learned) | 2.07 KB, cap 2,200 chars | every turn, frozen at session start |
| Skills index | 44 skills, one name and description each | every turn |
| `AGENTS.md` / `.hermes.md` | varies | session start, from the working directory |

Everything else is on demand: a skill's body loads only when `skill_view` is called,
a workspace file only when something reads it, a document only when it is opened.

## What costs disk instead

The database held 14 MB in total at the time of measurement, of which 3 MB was
message history and 0.6 MB its search index. A skill folder with scripts and
templates is disk only. A 9 KB interview document is disk only. Neither of them
appears in a conversation unless read.

The disk grows from transcripts, not from documents: every browser call, every file
read, every long tool output is stored as part of the session. That is the number to
watch when a profile feels slow, and it is why large results get written to a file
with a summary printed, rather than printed in full.

## Where each kind of information belongs

| If it is… | It goes in | Because |
|---|---|---|
| Who the person is, how they want to be spoken to | `USER.md` via memory | loaded every turn, so every word costs |
| A durable fact the agent must never re-derive (paths, quirks, conventions) | `MEMORY.md` via memory | same, and it is a scarce budget |
| How to do a recurring job (triage, brief, download, interview) | a skill | loads only when the job comes up |
| One organisation's data (people, sites, systems) | a data file read by path | never loaded unless used |
| A project's rules for one repository | `AGENTS.md` | scoped to the project, not the person |
| The person's own working record | `workspace/<name>-*.md` | theirs, not the org's |

The failure mode is putting a procedure into `SOUL.md` because it is important. It
is important, which is why it should not be repeated on every turn forever.

## Rules that keep it small

- **Consolidate, never append.** Memory is capped; when it is full the tool refuses
  the write. Rewrite the overlapping entries into one rather than adding a sixth
  version of the same fact.
- **One fact per sentence, no narration.** "Gmail is read through the browser, not
  Graph" is a memory entry. The story of why is a skill or a document.
- **Procedures are skills, not paragraphs.** If it has steps, it belongs where it
  loads on demand.
- **Data is read by path.** A 26-person org map belongs in JSON, not in a prompt.
- **Delegate volume.** Research that would return thousands of tokens goes to a
  subagent, and only its summary comes back.
- **Write big results to disk.** Batch downloads, scrapes and extractions append to a
  file in the workspace; the chat gets the count and the path.
- **Audit quarterly, or when a profile feels heavy.** Count the skills, check both
  memory files against their caps, and look at the database size.

## Measuring a profile

```bash
cd ~/.hermes/profiles/<name>
sqlite3 state.db "select name, round(sum(pgsize)/1048576.0,2) mb from dbstat group by name order by mb desc limit 6;"
wc -c memories/*.md
find skills -name SKILL.md | wc -l
```

The two numbers that matter are the memory files against 2,200 and 1,375 characters,
and the skill count, since each skill adds a line to every prompt.

## The conversation to have with the builder

Agenda for a session with the profile that deploys the others, thirty minutes:

1. **Show the measurement**, run on one profile, so the caps are concrete rather than
   abstract.
2. **Agree the split.** Which skills are shared in `shared-skills/`, which stay with a
   person, and what may never leave a profile: memories, sessions, transcripts.
3. **Decide what a new profile starts with.** A role template, the shared skills, and
   an empty memory. Nothing else travels.
4. **Agree the review cadence.** The two-week check after set-up, and a quarterly
   context audit for every deployed profile.
5. **Agree who owns consolidation.** In practice the agent proposes and the person
   approves, because the agent can see the budget and the person knows which fact
   still matters.

The point of all of it: a profile that carries too much stops being accurate, and one
that carries too little asks the same questions every week. The target is small,
durable, and mostly pointers to files that only load when needed.
