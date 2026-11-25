# The brief interview

A second conversation, run after the person has read one real brief. Its job is to
personalise the brief and to store what comes out of it in the right place, so a later
session doesn't have to guess or ask again.

Five to ten minutes. A conversation, not a form. Offer it at the end of the setup or any
time later with: "Tomorrow morning I will send you a brief. Have a look when it lands, and
when you are free we can set it up together to your taste."

## When to run it

- After the first brief has been read: the normal case.
- When they say the brief is too long, too short, or arriving at the wrong time.
- When their role changes, or someone starts reporting to them.
- Quarterly as a check, if the brief has been running unattended.

Never run it before they have seen a real brief. Preferences given in the abstract are
opinions; reactions to a real one are evidence.

## The conversation

### 1. What earned its place

> "Looking at yesterday's, what did you actually read and what did you skip?"

Mark each section read, skipped, or unmentioned. **Cut anything skipped without asking
twice**; a section nobody reads is a section that makes the rest look longer. Sections that
were unmentioned stay, but note them as unproven.

### 2. What surprised them

> "Was there anything in it you wouldn't have thought to ask for?"

This is the point of the trial. Expect the answers to be the waiting-on list, the promises
they personally owe, or the protected block. Whatever they name, keep and lean into it;
whatever they say nothing about, ask directly once: "did the waiting-on section help, or
would you rather not see who owes you things?"

### 3. Timing and delivery

> "When should it land relative to your first meeting, and where do you want it?"

Record a time, a channel (this chat, a draft email to themselves, somewhere else), and a
fallback for the days they start early. If they say "whenever", pick 7:00 on weekdays and
tell them it is easy to move.

### 4. Frequency

> "Every day, weekdays only, or only when you ask?"

Offer a Monday anchor (the week's three priorities) and a Friday close (what moved, what
carries). Do not impose either.

### 5. How blunt the opening should be

> "When something uncomfortable is the main thing, do you want it named in the first line,
> or softened and placed lower?"

Record their words, and add one example sentence they approve, because "blunt" and "direct"
mean different things to different people.

### 6. What to add next

Offer, do not install: the watchlist digest, promises owed, the protected block, numbers
with a week-on-week comparison. Each one costs the person reading time, so they opt in.

## Where each answer is stored

Most of this personalises more than the brief, so it goes in two places: the person's
context file for anything reusable, and the brief settings for the format itself.

| Answer | Stored in | Field |
|---|---|---|
| Sections kept or cut | brief settings | `sections` |
| Item cap and length | brief settings | `max_items`, `target_minutes` |
| Delivery time and channel | brief settings | `deliver_at`, `channel` |
| Frequency | brief settings | `frequency` |
| Bluntness, with an approved example | context file | `Voice, lead line` |
| Watchlist names and materiality | watchlist file | `items` |
| Protected block window | context file | `Rhythm, protected block` |
| Anything they volunteered about people or priorities | context file | the relevant table row |

Write the settings with the date they were agreed. Re-running the interview replaces them
rather than appending a second set, and the context file keeps the sentence in their words
so a later session can tell a preference from a default.

## What the settings file looks like

```json
{
  "agreed": "2026-11-26",
  "sections": ["lead", "diary", "decisions", "waiting_on", "promises", "protected_block"],
  "max_items": 5,
  "target_minutes": 1,
  "deliver_at": "07:00",
  "channel": "chat",
  "frequency": "weekdays",
  "watchlist_in_brief": false,
  "lead_style": "name the uncomfortable thing first, one sentence",
  "notes": "Skims the diary; reads decisions and waiting-on in full."
}
```

## Failure modes

- **Running it before a brief exists.** You will collect preferences they change their mind
  about on sight.
- **Asking "what would you like in your brief?"** They cannot know, which is why the trial
  comes first.
- **Adding sections they did not react to.** Length is the thing that kills a brief, and
  every unrequested section contributes to it.
- **Storing the answers in the chat.** Anything not written to the settings or the context
  file is lost by the next session.
- **Treating the first settings as final.** Revisit at the two-week review and at the
  quarterly check, and expect the item cap to fall as they trust it.
