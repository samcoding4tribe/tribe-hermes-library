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
- §9's two steps are a proposal, not a fill: §9 has the pre-filter and the model
  comparison in enough detail to build or reject, and no decision behind it yet.

---

## 9. Steps ① and ② in detail: the pre-filter and the model comparison

Proposal, 27 November 2026. Written against real material — the weekly `share` job's own
output — and not built. Expands §2.1 (harvest) and §2.2 (distil) for the soul-rule lane only.

### 9.1 What `share` already hands us, measured

`hermes_files.py share` writes `baseline/soul-rules/<profile>.md` for each profile: frontmatter
(`profile`, `machine`, `extracted`), a fixed header, then the marked block's rules as plain
numbered lines, names, emails and numbers already replaced by `[person]`, `[email]`,
`[number]`. A `_summary.md` is regenerated in the same run: whether each profile offers a
marked block, and the rules more than one profile carries.

On this machine, 27 November 2026: `admin.md` 5 rules, `ea.md` 5, `default.md` 7 — 17 rules,
2,774 characters — plus `_summary.md`. All three offered a marked block.

Its pairing key is the whole line lowercased with leading markers stripped, gated at more than
25 characters. Any word anywhere in the line makes it a different key. So the summary answers
"identical", and the question is "the same rule":

| Pair | Word Jaccard k=3 | Verdict the summary gives |
|---|---|---|
| `admin#1` ~ `default#1` | 1.00 | paired — character-identical after normalising |
| `admin#1` ~ `ea#1` | 0.30 | invisible — same rule, written for a manager |
| `admin#2` ~ `default#2` | 0.57 | paired |
| `admin#2` ~ `ea#2` | 0.375 | invisible |
| `admin#5` ~ `ea#5` | 0.118 | invisible |

Two facts the source material forces on any consumer of it:

- **`_summary.md` must be skipped.** A probe that globbed `*.md` read the summary as an 18th
  rule authored by a profile called `_summary`. Skip files whose stem starts with `_`.
- **The filename is keyed on profile id alone.** Two machines both have an `admin`, so both
  write `admin.md` and overwrite each other in git. Nothing bites today because all three
  profiles are on this machine. Fixed in 9.6, before a second machine runs `share`.

### 9.2 The pre-filter: deterministic, no model, no synonym list

Its job is not to be clever. It collapses exact duplicates, hands the model the pairs it must
not miss, and labels what had no partner so nothing is dropped silently.

1. **Parse.** A rule starts at `^\s*(?:\d+[.)]|[-*])\s+`; unmarked non-blank lines continue it;
   a blank line ends it. Skip `_`-prefixed files.
2. **Normalise.** Lowercase; `[person]`/`[email]`/`[number]` → `slot`; backticked text → `path`;
   drop stopwords; keep the rest as tokens. Compare at k = 2, 3, 4 and 5 word-shingles and
   report all four, because k=2 survives paraphrase and k=5 proves a lift.
3. **Blocking key.** `(leading imperative verb family, polarity)`, polarity N when
   `not|never|no` appears in the first 12 tokens. The verb family list (draft, cite, keep, say,
   protect, never, … about twenty) is data, in `config/soul-rules-blockers.json`, not code.
4. **Candidacy.** Any pair at or above 0.10 Jaccard (k=3), or sharing a blocking key, is a
   candidate. The threshold is set for recall, not precision: a missed pair is invisible in
   the output, a false one costs a few tokens.
5. **Ids.** Every rule gets `<machine>__<profile>#<n>`, stable across runs so a proposal can
   quote it after the numbering of a soul changes.
6. **Output.** `baseline/soul-rules/_candidates.json` — rules, candidate pairs with scores,
   singletons — written by the same weekly job, `_`-prefixed so nothing globs it as a profile.

Measured discrimination on today's 17 rules: the six closest cross-profile pairs score 0.118
to 1.0 at k=3, every other cross-profile pair 0.021 or less. That gap is real but it is not a
verdict, and it narrows as profiles multiply. Hence step 5: the pre-filter proposes, the model
decides.

### 9.3 The model step

**One call per bundle, never one call per pair.** Today is 17 rules and one bundle of about
700 tokens. At twenty people carrying six rules each it is ~5,400 tokens — still one call. The
quadratic worry in §2 is a property of pairwise comparison (95 pairs today, ~7,100 at twenty
profiles), not of comparing rules at all.

**Input:** the candidates file as JSON — every rule once with its id and text, the candidate
pairs with scores, the singleton list.

**Ask:** cluster by intent. Per cluster, emit a relation for each member (`same`, `variant`,
`new`), the proposed baseline wording, and a verbatim quote from each member. A role
difference is named as a role difference, not smoothed away: "form" against "Teams message" is
a claim about a manager's workspace, and that is a decision, not a merge.

**Model:** `deepseek-v4-pro`, temperature 0 — this machine's provider serves only
`deepseek-flash` and `deepseek-v4-pro`, so a config naming an Anthropic model fails with HTTP
400. `deepseek-flash` is the cheap re-run for an unchanged bundle, not the clustering model.

**Verification in code, not by trust.** Every quote must be a verbatim substring of the named
rule's text in `baseline/soul-rules/`; every id must be one the pre-filter issued. A cluster
failing either check is dropped and reported, never repaired. Responses are cached by the
SHA-256 of the bundle, so re-running an unchanged week costs nothing.

**Output:** `baseline/soul-rules/_proposal.md` — per cluster the proposed wording, the quoted
sources, the spread across profiles and machines, and whether a baseline soul already carries
it. Generated, never hand-edited. The human yes is a separate dated line at the top, added by
hand or by a later command.

### 9.4 Where the human yes sits

Nothing in 9.2 or 9.3 writes to `profiles/admin/SOUL.md`, `profiles/ea/SOUL.md` or a template.
A cluster marked `same` across three profiles is evidence; what the baseline then says — and
whether the manager variant is a second rule or a clause in the first — is a soul edit under
D34 and D18. `_proposal.md` is that edit's input and its receipt.

### 9.5 Access

For this lane there is no new access at all, and that is deliberate. `share` already reads each
soul, extracts only the marked block and scrubs it; the pre-filter reads `share`'s output in
the repo. So §2.1 ("harvest" from the backups) is about skills. The rule lane's harvester is
`share`, and it runs where the soul already is.

### 9.6 Prerequisites, all of them before this means anything

- **Machine-keyed filenames.** `cmd_share` writes `<profile>.md`; two machines collide on
  `admin.md`. Change to `<machine>__<profile>.md`, and key the summary's pairing map on the
  same id. One small edit to one function, but it must land before a second machine runs the
  job, or the first colleague's share silently shortens the builder's evidence.
- **Backup readability** (§4, D19/D20). Pooling across people needs their share output to
  reach one folder the builder can read. UNKNOWN which route is acceptable to Sam.
- **Threshold and approval** (§7). Still UNKNOWN, still Sam's, and the pre-filter's 0.10 is a
  recall setting, not that threshold.
- **Rule numbering is not yet comparable.** The token-spend rule (8) is live in the templates
  but in none of the three live souls, so today's rule 5 means different things in different
  files. Read ids, never rule numbers, when quoting.
- **Nothing here is worth building before people have worked profiles** — §1 of the
  checkpoint. The pre-filter is cheap to write and would be validated against three souls
  written by one person.
