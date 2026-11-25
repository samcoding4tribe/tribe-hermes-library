#!/usr/bin/env python3
"""Renumber downloaded assets to <n>.<date>-<who>.<ext>, preserving delivery order.

    python3 asset-rename.py ~/Downloads/job-name            # dry run
    python3 asset-rename.py ~/Downloads/job-name --apply

Reads the names asset-download.py writes (2026-11-19_2258_anastasia-kotanidis_a6380e37.jpg)
and produces 1.2026-11-19-anastasia-kotanidis.jpg, numbered in chronological order
so the sequence survives a copy anywhere. Two uploads by one person in one minute
share a date-name; the number keeps the filename unique and keeps the order.

rename-map.csv in the folder records new name, old name, date, time and contact, so
the rename is reversible and every file traces back to its source row.
"""

import argparse
import csv
import pathlib
import re
import sys

PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})_(?P<time>\d{4})_(?P<who>[^_]+)_(?P<hash>[a-f0-9]+)\.(?P<ext>jpe?g|png|webp|gif|pdf)$",
    re.IGNORECASE,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--apply", action="store_true", help="rename for real; default is a dry run")
    ap.add_argument("--start", type=int, default=1)
    args = ap.parse_args()

    folder = pathlib.Path(args.folder).expanduser()
    if not folder.is_dir():
        raise SystemExit(f"not a folder: {folder}")

    parsed, unmatched = [], []
    for p in folder.iterdir():
        if not p.is_file() or p.name.startswith("."):
            continue
        m = PATTERN.match(p.name)
        if m:
            parsed.append((m.group("date"), m.group("time"), m.group("who"), p))
        elif p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".pdf"}:
            unmatched.append(p)

    if not parsed:
        raise SystemExit("nothing to rename: no files match the download naming pattern")
    parsed.sort(key=lambda r: (r[0], r[1], r[3].name))

    plan, rows = [], []
    for i, (date, time, who, src) in enumerate(parsed, start=args.start):
        target = folder / f"{i}.{date}-{who}{src.suffix.lower()}"
        plan.append((src, target))
        rows.append({"new": target.name, "old": src.name, "date": date, "time": time, "contact": who})

    print(f"{len(plan)} files, numbered {args.start}..{args.start + len(plan) - 1}")
    for src, target in plan[:5]:
        print(f"  {src.name}  ->  {target.name}")
    if len(plan) > 5:
        print("  ...")
    if unmatched:
        print(f"{len(unmatched)} file(s) left alone (not in the download pattern): "
              + ", ".join(p.name for p in unmatched[:5]))

    map_path = folder / "rename-map.csv"
    with map_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["new", "old", "date", "time", "contact"])
        w.writeheader()
        w.writerows(rows)
    print(f"map written: {map_path.name}")

    if not args.apply:
        print("dry run — pass --apply to rename")
        return 0

    staged = []
    for src, target in plan:
        tmp = src.with_name(src.name + ".renaming")
        src.rename(tmp)
        staged.append((tmp, target))
    for tmp, target in staged:
        tmp.rename(target)
    print(f"renamed {len(plan)} files in {folder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
