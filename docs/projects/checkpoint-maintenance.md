# Profile maintenance, run by the builder on someone else's machine

Parked 26 November 2026; the pass was built 27 November 2026. Two things in one thread because
they share a trigger: the periodic maintenance pass, and what happens to a chat that is
already open when a soul changes.

## The job

A maintenance pass for the builder profile on a delegated machine — the Hermes that sets up
somebody else's assistant and then maintains it. Built as
`templates/builder/skills/profile-maintenance/SKILL.md`, measuring through
`scripts/profile_audit.py`, shipped with the builder template and installed by
`docs/setup.md` step 2. Its pass:

1. Measure: soul size against the target band, both memory files against the caps in that
   profile's own `config.yaml`, skill count, and the size of `state.db` against a watch line.
2. Flag: soul over the band, memory above ninety per cent, a line present in both soul and
   memory, a rule restated outside the soul's marked block, a rule said twice in one soul, a
   database past the watch line.
3. Propose a diff. Never apply it. The person says yes — that is D39.
4. Repeat the pass after an approved change, and run `hermes sessions refresh-prompts` for
   that profile so the session knows it is running a new self. The refresh step is written
   into the skill, which is what this thread was waiting for.

Targets and where each kind of information belongs: `docs/context-budget.md`. The reasoning
behind proposing rather than applying: `A weekly prompt budget check for each profile` in
Sam's vault.

## Built, and what proves it

- `scripts/profile_audit.py` — read-only: files opened for reading, `state.db` opened with
  SQLite `mode=ro`, nothing written. `--profile <id|path>`, `--all`, `--json`. Verified 27
  November 2026 against all three profiles on this machine (builder 3.5 KB soul, 2105/2200
  memory, 48 skills, 30.7 MB db; `admin` 2.3 KB, 2188/2200, 45 skills, 35.6 MB; `ea` 1.13 KB,
  no memory file, 44 skills, 0.54 MB) and against a synthetic profile built to trip the
  duplicate and cap checks — all three fired, and the real profiles produced no false
  duplicate flags.
- The skill: flag → propose → apply on yes → refresh → record. It also states what the pass
  never does (no deletion of sessions, no memory consolidation that drops a fact in use, no
  copying a memory between profiles).
- Proposals are stated in chat as a diff plus one sentence of cost in bytes and in behaviour.

## The refresh problem

A session builds its system prompt once, from `SOUL.md` and the memory files, and replays it
verbatim so the provider's prefix cache stays warm. That is why a soul change does not reach
a chat that is already open.

**The supported way to force it is `hermes sessions refresh-prompts`.** It records a refresh
epoch in the profile's `state.db`; at the start of that session's next turn Hermes compares
the epoch against the one stamped when the prompt was built and, when the prompt is older,
rebuilds it once through the normal builder: history, session id and the `tools[]` pin are
kept, `on_session_start` does not fire, and the new bytes are persisted so later turns replay
them verbatim. The cost is one prefix-cache break per refreshed session.

So the refresh is a backend command, not necessarily a new chat. A handover note remains an
option for when a person wants the old context carried across, rather than the only mechanism.

Measured 27 November 2026: the command takes `-p` to target another profile, `--session` to
scope it to one chat, and `--json` for `{"epoch": N, "session_id": null, "sessions": 13}`. It
is **not a dry run** — a bare call stamped all 13 sessions of the builder profile at once. The
skill carries that as a pitfall and tells the builder to scope with `--session` or to say how
many sessions it touched.

## UNKNOWN, still untested

- Whether `refresh-prompts` reaches sessions held open by the gateway and the desktop app
  before their next turn, or only sessions that start a turn afterwards. The code says "next
  turn", which implies both; it has not been observed here, because observing it needs a chat
  left open across the change.
- What a skill change does to a running chat: a loaded skill may pick up an edit; the index
  that lists it does not. Test both.
- Whether a memory write needs the same treatment. It should — memory is injected at session
  start too — and the skill says to assume it does until measured.

## Not to be confused with

The pooling loop in `docs/architecture-loop.md`. That improves the baseline from several
people's practice. This keeps one profile healthy and current on one machine.

## What it needs from Sam

- **The cadence.** Weekly, monthly, or on demand. Nothing is scheduled until this is answered;
  the skill says so in its own words rather than guessing.
- **Whether the pass is installed on this machine's builder too**, or stays library-only until
  the first delegated machine runs it. Today it exists once, in the repo, and nothing here
  loads it.
- **Whether a handover note is wanted** alongside the refresh, for the case where someone wants
  the old chat's context carried into the new prompt. Unbuilt either way.

## Next action

Install it on the first delegated machine (or here), then run one pass against a real profile
with a chat left open across the refresh, which is what turns the first UNKNOWN above into a
measured fact.
