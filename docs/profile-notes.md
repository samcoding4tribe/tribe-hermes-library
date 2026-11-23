# Notes inside a profile

Each assistant keeps its own working papers in its own folder. They are written
when there is something to write, not scaffolded in advance, and they are plain
markdown because the agent reads them and a person can open them.

No second brain, no vault, no tool to install. The folder is the documentation.

## Where they live

```
~/.hermes/profiles/<name>/workspace/
```

`admin` already works this way: `sam-context.md` holds what Sam told it, and the
two HTML files beside it are working artifacts it produced. That is the pattern,
not an exception.

## What belongs there

| File | Written when | Contents |
|---|---|---|
| `context.md` | Setup, then corrected | Who this person is, their remit, who they report to, what they are accountable for. Every line carries its source and a date |
| `procedures.md` | A task has been done twice | The steps as observed, before they are worth turning into a skill |
| `decisions.md` | A choice is made about this assistant | What was chosen for this profile and why, so a later session does not relitigate it |
| working files | As produced | Drafts, charts, spreadsheets, anything the work generated |

Name files lowercase with hyphens, one topic each, and put the date next to any
claim that could change.

## What does not belong there

Contact numbers, passwords, card details, performance notes about colleagues,
anything you would not be comfortable reading aloud. Contacts belong in the
directory, credentials in `.env`, and remarks about people belong nowhere.

## The lifecycle

1. Something is learned. It goes in `context.md`, with a source.
2. A task is done twice the same way. The steps go in `procedures.md`.
3. The procedure is still right the third time. It becomes a skill in
   `shared-skills/`, where every assistant inherits it, and the note shrinks to
   a pointer.
4. A choice is made about this profile alone. It goes in `decisions.md`.

Notes are the working memory. Skills are the finished product. Nothing skips
straight to a skill, because a procedure written from memory of one attempt is
usually wrong in the details that matter.

## Who can read them

Private. `workspace/` is copied into that machine's backup, so it survives a lost
laptop, and it is excluded from the repo and from the shared library. Doctrine
goes to the library; this person's working notes do not.

If a note is genuinely reusable, the answer is a skill, not a publication.
