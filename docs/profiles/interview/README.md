# Handoff — EA profile kit

What a deploying assistant needs to stand up an admin profile for a new person at
TRIBE, without re-deriving the design or moving facts between profiles by hand.

## Files

| File | What it is |
|---|---|
| `onboarding-interview.md` | The set-up conversation. Fixed-versus-chosen split, eight blocks of questions with the reason for each, and the four artefacts the interview must produce. |
| `FOR-THE-BUILDER-PROFILE.md` | The note written to the deploying agent about the org map package and the boundary between admin work and deployment work. |
| `brief-interview.md` | The second conversation, run after the first brief has been read: what earned its place, what surprised them, timing, frequency, bluntness, and where each answer is stored. |
| `context-budget.md` | What loads on every turn versus what only costs disk, where each kind of information belongs, and the agenda for the context conversation with the builder. |

## The order of operations for a new profile

1. Route on the org role, then install. A person who manages others, or whose work is mostly
   diary, approvals and correspondence, gets the id `ea`; everyone else gets `admin`. The
   content comes from `profiles/admin` in both cases — one baseline exists today, and
   `profiles/ea` is a single manager's pilot instance rather than a second baseline. Keep the
   id role-based: `admin`, `ea`, or a role name for a second assistant, never the assistant's
   name and never the person's (D22). The name is a label, asked in Block 0 and changing
   nothing downstream (D31). `templates/role/` is only for a role neither fits.
2. Read `onboarding-interview.md` and run it as a conversation, not a form. Blocks
   zero to eight, twenty to thirty minutes, two short sessions if the answers get
   thin.
3. Mail and calendar access first, before any preference question. In this
   organisation that means the browser route in the `microsoft-365-web` skill; if
   read access fails, fix that before asking what they want in a brief.
4. Install these skills into the new profile from the shared library:
   `executive-admin-support`, `morning-brief`, `watchlist-digest`,
   `microsoft-365-web`, and `link-batch-download` if they receive asset lists.
5. Write the review into the calendar: two weeks, one question, which part is not
   earning its place.

## The four artefacts the interview produces, and where each one goes

| Artefact | Written to | Produced in |
|---|---|---|
| The assistant's name | The profile's label: roster title, bot name, and optionally the first line of `SOUL.md`. Never the folder id | Block 0 |
| `workspace/context.md` | Inside the profile. Private: copied into the machine's backup, excluded from the repo and the library | Blocks 1 to 5 |
| `workspace/procedures.md` | Inside the profile, same handling. Only the steps the person actually described, never a full task list | Wherever a task was described in detail |
| Brief preferences | `workspace/context.md`, under a heading of its own, after a real brief has been read | `brief-interview.md` |

Nothing else is written at setup. A skill is not one of the four: skills come after a
procedure has been done twice and held.

## What must not travel between profiles

The interview document is shared; the answers are not. Never copy one person's
context file, watchlist, mail rules or memory entry into another person's profile,
and never into this kit. The kit holds the method, the profile holds the person.
