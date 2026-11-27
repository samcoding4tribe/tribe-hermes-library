#!/usr/bin/env python3
"""Word-shingle similarity between the rules in baseline/soul-rules/.

Reads only the weekly `share` job's own output: one `*.md` per profile, rules as
numbered lines. Nothing else is opened, nothing is written unless --json is given,
and no model is called — this is the free half of the distillation design in
`docs/architecture-loop.md` §9.

Use it to answer "are these two rules the same rule?" with numbers instead of an
opinion, and to see whether a proposed threshold still catches every plausible
pair before you spend a token on a model.

    python3 rule_pair_probe.py                 # table + threshold sweep
    python3 rule_pair_probe.py --th 0.10       # sweep a specific candidacy floor
    python3 rule_pair_probe.py --json /tmp/p.json
"""
import argparse
import itertools
import json
import re
from pathlib import Path

MARK = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+")
SLOT = re.compile(r"\[(?:person|email|number)\]")
CODE = re.compile(r"`[^`]*`")
WORD = re.compile(r"[^a-z0-9]+")

STOP = set(
    """a an the and or but if of to in on at for from by with is are be been being was were
    this that these those it its as so than then there what which when who whom you your
    yours we our they their he she his her not no do does did done has have had can could
    would should may might must will shall about before after over under more most less least
    very only just also into out up down per each any all some such same other own both
    either neither one two""".split()
)

# ~20 leading imperatives, enough to block the rule shapes this estate writes. Data, not
# logic: extend the tuple, do not add cleverness to the matcher.
VERBS = (
    "draft", "cite", "keep", "say", "protect", "never", "read", "stay", "send", "ask",
    "write", "delete", "check", "use", "name", "prefer", "stop", "report", "watch",
    "destroy", "approve",
)
NEGATORS = {"not", "never", "no"}


def parse_rules(text: str):
    """Split a share output file into rules: marker starts one, blank line ends it."""
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    out, current = [], None
    for line in body.splitlines():
        if MARK.match(line):
            if current:
                out.append(current)
            current = MARK.sub("", line).strip()
        elif not line.strip():
            if current:
                out.append(current)
                current = None
        elif current is not None:
            current += " " + line.strip()
    if current:
        out.append(current)
    return out


def normalise(rule: str) -> str:
    s = rule.lower()
    s = SLOT.sub(" slot ", s)
    s = CODE.sub(" path ", s)
    s = WORD.sub(" ", s)
    return " ".join(t for t in s.split() if t not in STOP)


def shingles(tokens, k):
    if len(tokens) < k:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[i:i + k]) for i in range(len(tokens) - k + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def verb_family(tokens):
    for token in tokens[:4]:
        for verb in VERBS:
            if token.startswith(verb[:5]):
                return verb
    return tokens[0] if tokens else "?"


def polarity(tokens):
    return "N" if NEGATORS & set(tokens[:12]) else "P"


def load(directory: Path):
    """Rules keyed by '<profile>#<n>'. Skips _-prefixed files: _summary.md is not a profile."""
    items = []
    for path in sorted(directory.glob("*.md")):
        if path.stem.startswith("_"):
            continue
        for n, rule in enumerate(parse_rules(path.read_text(encoding="utf-8")), 1):
            items.append((f"{path.stem}#{n}", rule))
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", default="~/tribe-hermes-library/baseline/soul-rules")
    ap.add_argument("--k", type=int, default=3, help="shingle size used for the candidacy score")
    ap.add_argument("--th", type=float, default=0.10, help="candidacy floor, set for recall")
    ap.add_argument("--json", help="write the pair table here")
    args = ap.parse_args()

    directory = Path(args.dir).expanduser()
    items = load(directory)
    if not items:
        raise SystemExit(f"no rules found under {directory}")

    by_profile = {}
    for key, _ in items:
        by_profile.setdefault(key.split("#")[0], 0)
        by_profile[key.split("#")[0]] += 1
    print("rules per profile: " + ", ".join(f"{p}={n}" for p, n in sorted(by_profile.items())))
    print(f"total rules {len(items)}, chars {sum(len(r) for _, r in items)}")

    toks = {key: normalise(rule).split() for key, rule in items}
    rows = []
    for (ka, _), (kb, _) in itertools.combinations(items, 2):
        if ka.split("#")[0] == kb.split("#")[0]:
            continue
        scores = {k: round(jaccard(shingles(toks[ka], k), shingles(toks[kb], k)), 3)
                  for k in (2, 3, 4, 5)}
        rows.append({
            "a": ka, "b": kb, **{f"j{k}": v for k, v in scores.items()},
            "key": f"{verb_family(toks[ka])}/{verb_family(toks[kb])}"
                   f"|{polarity(toks[ka])}{polarity(toks[kb])}",
            "tokens": f"{len(toks[ka])}/{len(toks[kb])}",
        })

    rows.sort(key=lambda r: -r[f"j{args.k}"])
    print(f"\ncross-profile pairs: {len(rows)}")
    print(f"\n-- top 12 by j{args.k} --")
    for r in rows[:12]:
        print(f"{r['a']:>14} ~ {r['b']:<14} j2={r['j2']:<5} j3={r['j3']:<5} j4={r['j4']:<5} "
              f"j5={r['j5']:<5} key={r['key']:<20} tokens={r['tokens']}")

    keep = [r for r in rows if r[f"j{args.k}"] >= args.th]
    print(f"\n-- above th={args.th} ({len(keep)} of {len(rows)}) --")
    for r in keep:
        print(f"  {r['a']} ~ {r['b']}")

    print("\n-- best partner per rule --")
    for key, _ in items:
        partners = [r for r in rows if key in (r["a"], r["b"])]
        if not partners:
            print(f"{key}: no cross-profile partner (singleton)")
            continue
        best = max(partners, key=lambda r: r[f"j{args.k}"])
        other = best["b"] if best["a"] == key else best["a"]
        flag = "" if best[f"j{args.k}"] >= args.th else "  <- below floor, singleton"
        print(f"{key}: {other} j{args.k}={best[f'j{args.k}']}{flag}")

    print("\nClose scores are candidates, not verdicts. The verdict is the model step, "
          "and the baseline wording is a person's decision; see docs/architecture-loop.md §9.")

    if args.json:
        Path(args.json).expanduser().write_text(json.dumps(rows, indent=1), encoding="utf-8")
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
