# Publishing the repo to the shared library, and proving it landed

The estate moves in one direction: repo → library. These are the concrete steps and the
checks that make a claim about it true.

## What `python3 scripts/hermes_files.py sync` does, in order

1. Copies each live profile into `repo/profiles/<id>` with `include_memories=False`
   (custom skills only, bundled skills are skipped by design).
2. `git add -A`, then commits with the message `sync: <YYYY-MM-DD HH:MM>` and pushes if
   `origin` exists. **`git add -A` sweeps up every other dirty file in the repo**, so
   unrelated edits land in a commit labelled `sync:` — deliberate, since the nightly job
   depends on it, but it means the commit message says nothing about the docs you changed.
3. Stages `profiles/` (memories stripped), `templates/`, `shared-skills/`, `apps/` and
   `docs/`, then **deletes everything in the library folder and copies the stage in**. A file
   placed in the library by hand is gone on the next run; the recycle bin and git history
   are the recovery path. Explain this to anyone who asks why their note vanished.
4. `docs/setup.md` is copied to the library root as `README.md`, and `docs/` is published
   without the `setup.md` copy so the front door does not appear twice. Both script
   implementations special-case this name: `hermes_files.py` and the legacy `sync.sh`.
5. Writes `_manifest.json` (a sha256 prefix per file) and `TODO.md`.

Ignored in the publish stage: `.DS_Store`, `status-today.json`, `weeks` (whereabouts app
state that names who is on leave), and any `memories/` path.

## Proving it landed

Run these after sync, never before — a difference measured while a sync is still pending is
your own timing, not a script fault.

```bash
LIB="$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/TRIBE GROUP - TRIBE Group Tech/Hermes Library"
cd ~/tribe-hermes-library

for part in templates shared-skills apps docs; do
  echo "-- $part"; diff -rq "$part" "$LIB/$part" | grep -v '\.DS_Store' | head
done

grep -c '^## D' docs/decisions.md "$LIB/docs/decisions.md"   # decision counts must match
head -3 "$LIB/README.md"                                     # the front door title
git remote -v; git log --oneline -1                          # pushed, and to where
python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))['files']))" "$LIB/_manifest.json"
```

`diff -rq` reporting nothing for a part means the two sides are in step. A file that exists
on one side only is worth naming explicitly to the user — that is how `apps/team-map`
run-time state was found being published.

## Closing out: what "finished on your end" means

When Sam asks whether the work is actually done, run these and report the numbers, not the
intention.

```bash
cd ~/tribe-hermes-library
git status --porcelain                     # empty = nothing left uncommitted
git log --oneline -1
grep -rl "<string that must never be published>" --include="*.md" --include="*.json" . \
  | grep -v '\.hub'                        # must print nothing
wc -c ~/.hermes/memories/MEMORY.md ~/.hermes/profiles/*/memories/MEMORY.md
grep -c '"name"' ~/.hermes/cron/jobs.json  # jobs still scheduled
```

- **Run the leak grep last, and against the library too.** The rule that forbids a value is
  itself published, so a sensitive string survives in `docs/decisions.md` after being removed
  everywhere else. Write the rule about the value, never the value.
- **Filter `.hub`.** `profiles/*/skills/.hub/index-cache/` matches almost any word and one of
  those files is 86 MB; an unfiltered hit list is unreadable and hides the real match.
- **Memory caps are per profile** (`memory.memory_char_limit`, 2200 by default). Check each
  file against the config of the profile that owns it, and consolidate stale entries rather
  than adding a sixth version of one fact — the cap refuses the write when it is full.

## Pulling a published change onto a machine

```bash
python3 scripts/hermes_files.py pull <profile-id>            # prints the diff
python3 scripts/hermes_files.py pull <profile-id> --apply    # applies it
```

Souls and skills travel both ways. `config.yaml` publishes sanitised and never pulls, since
the published copy has credentials stripped and applying it would delete settings the
machine needs. Memories travel neither way (D14).

## When the user says "if you need to sync, go for it"

That is standing approval for this direction of publishing. Still say in one line what
changed and what it touched, because a push and a full library rebuild happened. Ask before
running it if someone else may have edited the library since the last run — after the D23
amendment nobody but the maintainer edits there, so the answer is normally yes.
