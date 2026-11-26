# Profile maintenance, run by the builder on someone else's machine

Parked 26 November 2026. Two things in one thread because they share a trigger: the periodic
maintenance pass, and what happens to a chat that is already open when a soul changes.

## The job

A skill for the builder profile on a delegated machine — the Hermes that sets up somebody
else's assistant and then maintains it. Its pass, on a schedule:

1. Measure: soul size against the target band, both memory files against their caps, skill
   count.
2. Flag: soul over the band, memory above ninety per cent, a line present in both soul and
   memory, a rule that duplicates a shipped one.
3. Propose a diff. Never apply it. The person says yes.
4. Repeat the pass after a soul change so the profile knows it is running a new self.

Targets and where each kind of information belongs: `docs/context-budget.md`. The reasoning
behind proposing rather than applying: `A weekly prompt budget check for each profile` in
Sam's vault.

## The refresh problem

A session builds its system prompt once, from `SOUL.md` and the memory files, and replays it
verbatim so the provider's prefix cache stays warm. That is why a soul change does not reach
a chat that is already open.

**There is a supported way to force it, though.** `hermes sessions refresh-prompts` records a
refresh epoch in the profile's `state.db`. At the start of that session's next turn Hermes
compares the epoch against the one stamped when the prompt was built and, when the prompt is
older, rebuilds it once through the normal builder: history, session id and the `tools[]` pin
are kept, `on_session_start` does not fire, and the new bytes are persisted so later turns
replay them verbatim. The cost is one prefix-cache break per refreshed session — real money,
but a single event rather than a permanent penalty.

So the refresh is a backend command, not necessarily a new chat. The handover-note idea below
becomes an option for when a person wants the old context carried across, rather than the only
mechanism.

The automated answer, if we build one, is a handover rather than a copy: before the restart,
write the live context into the profile's `workspace/` as a short note — what this
conversation is about, what was decided, what is pending — then start a new chat pointed at
that note. History is preserved as a note a person can read, not as a transcript replayed
into a new prompt.

## UNKNOWN, to test before designing anything

- Whether `refresh-prompts` reaches sessions held open by the gateway and the desktop app, or
  only sessions that start a turn afterwards. The code says "next turn", which implies both,
  but it has not been run here.
- What a skill change does to a running chat: a loaded skill may pick up an edit; the index
  that lists it does not. Test both.
- Whether a memory write needs the same treatment, given memory is injected at session start
  too.

## Not to be confused with

The pooling loop in `docs/architecture-loop.md`. That improves the baseline from several
people's practice. This keeps one profile healthy and current on one machine.

## What it needs from Sam

- Whether the maintenance pass runs weekly, monthly, or on demand.
- Whether the delegated builder may edit a soul, or only propose the diff.
- A decision on the restart: the refresh is now known to be `hermes sessions refresh-prompts`
  plus one turn, so this is only about whether a handover note is also wanted.

## Next action

Write the refresh step into the maintenance pass: after a soul or memory change, run
`hermes sessions refresh-prompts` for that profile and say so, because otherwise the change
sits invisible until somebody starts a new chat and wonders why the assistant is unchanged.
