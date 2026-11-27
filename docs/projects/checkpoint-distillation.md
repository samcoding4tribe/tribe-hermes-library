# Pooling worked profiles back into the baseline

Parked 26 November 2026. Not started, and not to be started until there are
profiles people have actually worked.

The design lives in `docs/architecture-loop.md`. This page is the state only, so
the two do not drift apart.

## Where it stands

Nothing built. The return path exists physically — `scripts/hermes_files.py backup`
writes each machine to `TRIBE Group Tech/Hermes Backups/<machine>/` nightly — so
nobody has to learn a contribution habit.

The basket is empty. One machine backup, three profiles, zero custom skills: all 33
files under the `skills/` folders are `.locks` and `.hub` metadata. Every skill in
every profile is bundled and inherited from the same baseline, so there is nothing
to compare and nothing to pool.

**27 November 2026 — the two steps are designed; nothing built.** §9 of
`docs/architecture-loop.md` now holds the pre-filter and the model comparison in enough
detail to build or reject: deterministic parse and shingle candidate-finding, one model call
over the whole rule set rather than per pair, quotes verified against the source files in code,
output as `baseline/soul-rules/_proposal.md` awaiting a hand-written yes. It is written
against the real material — 17 rules across the three profiles — and two measured findings
went with it: the summary's exact key under-reports (admin#1 ~ ea#1 scores 0.30 at word
3-grams and pairs nothing), and `cmd_share`'s filenames are keyed on profile id alone, so a
second machine's `admin` would overwrite this one's. That filename change is the one piece of
code that should land before any colleague runs `share`, and it is not written. No decision
recorded: §9 is a proposal, and D34 still governs what may travel.

## What finished looks like

A harvester that reads a machine backup, keeps only what generalises, and proposes a
baseline change with its evidence; and baselines that improve from several people's
practice rather than from one person's taste.

## Remaining work, in order

1. Roll out profiles and let people work them. Nothing above is meaningful before this.
2. Harvest and distil — design §2 and §3.
3. Settle delivery to machines that are not this one — design §4.
4. Settle collisions between a local fork and a baseline change — design §5.
5. Test, then write, the refresh procedure — design §6.
6. Settle the evidence threshold before the first baseline change is published — §7.

## Only Sam can answer

- Is a machine's backup readable for this purpose, and is that said at handover?
  Standing access and per-item opt-in are different trusts.
- The threshold at which repeated practice becomes a baseline change.
- Whether anyone besides Sam approves a baseline change.

The soul question is closed: D34 in `docs/decisions.md` — voice stays local, rules
may travel.

## Rejected on the way here

Per-item opt-in with a contribution skill and an audit receipt for the contributor.
It assumed the material was not already central. It is.

## What the weekly share job proved, 26 November 2026

The first real material from the estate shows the check is too literal. `admin` and `ea` both
carry a "draft, never send" rule as rule 1, and the summary pairs nothing because the wording
differs — "Email, messages, forms" against "Email, Teams messages". Same rule, same intent,
different words.

So distilling is not string matching. It needs a capable model comparing two blocks and saying
"these are the same rule", "this one is a variant for a different role", "this one is new".
That means design work rather than a script:

- a cheap deterministic pre-filter first (normalise, drop near-duplicates, group by shape) so
  the model only sees the pairs worth its attention;
- the model proposes the grouping and the baseline wording, with the source lines quoted;
- a person approves, because the same rule written for a manager and for an admin is a
  decision about what the baseline should say, not a merge conflict.

Token cost is the constraint: comparing every profile against every other grows quadratically,
so the pre-filter is what makes it affordable.
