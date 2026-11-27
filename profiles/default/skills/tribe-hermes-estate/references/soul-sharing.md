# The soul share: how rules travel between profiles

`scripts/hermes_files.py share` pulls the marked rules out of every soul on this machine into
`baseline/soul-rules/`. It runs weekly through the cron job 'Hermes soul share' (Sunday 17:30,
wrapper `~/.hermes/scripts/hermes-share.sh`). The other subcommands for reference: `backup`
(text mirror that keeps memories, plus `state.db` snapshots), `sync` (to the shared library,
memories stripped), `pull`, `nightly`.

## What travels

A soul contributes only what sits between `<!-- shared:start -->` and `<!-- shared:end -->`, and
a soul without markers is reported as unmarked. The markers are HTML comments, so adding them
changes no behaviour and needs no `refresh-prompts`. All three souls on this machine are marked,
with the block drawn around the numbered rules only — the paragraphs below them (working notes,
how a profile shares skills) are profile-specific and must not travel.

## How rules are compared, and why "identical" is not "the same"

The summary pairs rules on the whole line, lowercased, markers stripped, gated at >25 chars. It
answers "identical" when the question is "the same rule": a rule phrased for a manager against
the same rule phrased for an admin ("Email, messages, forms" against "Email, Teams messages")
pairs nothing, while a genuinely unrelated pair scores near zero. So write a shared rule in
identical words in every soul — including the live ones — or the summary reports it three times
as unpaired.

Measure before arguing about it: `scripts/rule_pair_probe.py` prints word 2–5-gram shingle
scores per cross-profile pair, a blocking key and the best partner per rule. Stdlib only, no
tokens. Run it before proposing a matcher or asking a model — it turns an opinion about wording
into numbers you can quote. The pre-filter and model comparison that follow are designed in §9 of
`docs/architecture-loop.md` (proposal, nothing built).

## Two facts that bite any consumer of that folder

- Glob `*.md` in it and you parse `_summary.md` as a profile called `_summary`. Skip
  `_`-prefixed files.
- `cmd_share` names files `<profile>.md`, so the second machine to run the job overwrites the
  first machine's `admin.md`. Machine-key that filename before any colleague runs `share`, or the
  builder's evidence silently shrinks.
