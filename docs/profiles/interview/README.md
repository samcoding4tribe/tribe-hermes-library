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

1. Copy the role profile from `templates/role/` and give it the person's name.
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

## What must not travel between profiles

The interview document is shared; the answers are not. Never copy one person's
context file, watchlist, mail rules or memory entry into another person's profile,
and never into this kit. The kit holds the method, the profile holds the person.
