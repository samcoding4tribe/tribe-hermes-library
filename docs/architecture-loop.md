# The loop back: worked profiles improving the baseline

Design sketch, 26 November 2026. Nothing here is built. Sections are numbered so
each can be taken on its own later. The thread state and next actions live in
`docs/projects/checkpoint-distillation.md`; this file holds the design only.

Why it exists: Hermes personalises outward by design — a profile is a folder on
one machine and nothing phones home. The estate also copies outward, from template
to person. There is no path in the other direction, and without one every profile
stays as good as the day it was installed while the people using it get better.

---

## 1. The shape in one sentence

Read worked profiles from their backups, keep only what generalises, publish it to
the shared library, and let each profile pull it — so the pipeline writes to the
library and never into a live profile.

---

## 2. The flow

```
  colleague's machine                OneDrive                        this Mac (builder)
  ───────────────────                ────────                        ──────────────────
  profile worked by a person
  ~/.hermes/profiles/<id>/
    SOUL.md  skills/  cron/
    memories/  workspace/  state.db
         │
         │  nightly backup, unchanged (D12)
         ▼
                              Hermes Backups/<machine>/
                                text/  +  db/*.db
                                     │
                                     │  ① HARVEST — include-list only
                                     ▼
                              digest: skills, rules, config,
                              cron; memories ✗ workspace ✗
                              message text ✗ (counts only)
                                     │
                                     │  ② DISTIL — compare across people,
                                     │     weigh with usage counts
                                     ▼
                              proposed baseline change + evidence
                                     │
                                     │  ③ Sam says yes
                                     ▼
  ◀── pull with a diff ──────  Hermes Library/  ◀──  ④ PUBLISH ── repo commit
      (skills by reference)
         │
         │  ⑤ REFRESH — new session, gateway restart
         ▼
  profile runs the improved baseline.
  Its soul, memory and workspace are exactly as they were.
```

Steps ① and ② are the only new code. ③ already exists as a habit, ④ is `sync`
plus a commit, ⑤ is a procedure that needs testing rather than building.

---

## 3. What may cross the line

| Lane | Travels | Shape it travels in |
|---|---|---|
| Skills | Yes — the main harvest | A whole `SKILL.md`, names and companies stripped |
| Soul **rules** | Yes, as a proposal | One rule, quoted, with the failure behind it |
| Soul voice | Never (D34) | — |
| Config | As a recommendation | A diff: timeouts, guardrails, model choice |
| Cron definitions | As an example | Job shape with times and targets blanked |
| Memories | Never (D14, D17) | — |
| `workspace/` notes | Never | — |
| Sessions, `state.db` text | Never | Counts only: sessions, skill runs, cron fires |
| Credentials, `.env` | Never | — |

The include-list rule: the harvester names what it reads. It must not name what it
skips, because Hermes adds personal folders over time and an exclude-list silently
admits the next one.

---

## 4. Push it back without touching anyone's profile

The pipeline's write target is the library and the repo. It never writes into a
profile folder on anyone's machine, this one included. Delivery happens by three
routes, in increasing order of intimacy:

1. **Skills, by reference.** Profiles already read shared skills through
   `skills.external_dirs` (D17); `admin` and `ea` both point at
   `~/tribe-hermes-library/shared-skills`. An improved skill is therefore a file
   edit in one place, with no copying and nothing to overwrite. A person's own
   local `skills/` shadows a shared skill of the same name, so a colleague who
   edited one keeps their version — their change is a fork, not a casualty.
2. **Soul and config, as a diff.** Published to the library like everything else,
   and applied by the person through `pull`, which shows the diff first (D4). D34
   makes this mandatory for souls: no soul is ever replaced wholesale.
3. **Templates, for new installs.** A new colleague starts from the improved
   template. People already running are unaffected, which is the point.

**Known gap.** `external_dirs` is an absolute path into this repo on this Mac, so
it is not portable. Two ways out: point it straight at the synced library folder,
so OneDrive is the delivery mechanism, or have `pull` copy the shared skills into
`~/tribe-hermes-library/shared-skills` on each machine and keep the path stable.
The second keeps the repo as the versioned truth and is the better fit with D3 and
D4. Not decided.

---

## 5. When a local edit and a baseline change collide

Unsolved, and the reason `architecture.md` already flags profile collision as
unwritten work. The pieces that exist: `_manifest.json` holds a hash per published
file, and the repo holds history, so a three-way diff is available — local copy,
last published version, proposed version.

The rule to settle: does a local fork win silently, does it get flagged to the
person as "the baseline has moved under your version", or does it become a harvest
candidate in its own right? The third is probably right, since a fork is evidence
that the baseline was not good enough, but it needs a person's consent to leave
their machine.

---

## 6. Making a running chat use the update

The honest state: what gets re-read when is partly known and partly not, and none
of it has been tested here.

| Thing | Understood | Confidence |
|---|---|---|
| Memories | Injected every turn, so a change lands mid-conversation | Believed, untested |
| Soul | Read at session start; needs a new chat | Believed, untested |
| Skills — edited | Read when the skill is loaded, so an edit may land in a live chat | UNKNOWN |
| Skills — newly added | The skill index is built at session start, so a new skill needs a new chat | Believed, untested |
| Cron | Read by the scheduler, so it needs a gateway restart or the next run | UNKNOWN |
| Model | Fixed when the chat starts | Observed on this machine |

Confirming it is cheap and needs no code: edit one word in a shared skill, ask the
same question in an existing chat and in a new one, and compare the answers. Then
write the procedure that follows from the result — most likely "quit and reopen the
app, or start a new chat, after a pull", which is the whole of step ⑤.

---

## 7. Evidence, and when a change counts

The rule from `agent-profiles.md` is that a procedure becomes a shared skill once it
has been done twice the same way. Harvesting needs the same discipline, or the first
colleague to send something sets the baseline for everyone — the drift D33 exists to
prevent.

Evidence available without reading anyone's conversations: session counts, how often
a skill was loaded, how often a cron fired, from the `state.db` snapshots. That is
aggregate, not content, and it answers "has this been used enough to be worth
copying" without answering "what did they talk about".

Threshold itself: UNKNOWN. Needs Sam. A starting proposal to argue about later —
one instance is a variant, three instances across two roles arriving independently
is a baseline candidate.

---

## 8. Sections still to fill

- §4 the delivery gap: how `external_dirs` reaches a machine that is not this one.
- §5 collision rule and the consent it needs.
- §6 the tested refresh procedure.
- §7 the threshold, and who approves a baseline change besides Sam.
- Not in this file: what a colleague is told at handover about their backup being
  read for this purpose. That belongs in `docs/onboarding.md`, and it has to be
  written before the first colleague receives a profile, not after the harvest works.
