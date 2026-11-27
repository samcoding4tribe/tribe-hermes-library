#!/usr/bin/env python3
"""Write today's handover from what the repo already knows. No model, no tokens.

Sources: yesterday's commit for the files that changed, the thread table in
docs/projects/README.md for state and next action, and anything the previous handover
carried forward that has not been closed.

Usage: python3 scripts/daily_handover.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "handover-today.md"


def git(*args) -> str:
    try:
        return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                              check=False).stdout
    except OSError:
        return ""


IGNORE = ("/.locks/", "/.hub/", ".DS_Store", "/logs/", "/cache/")


def yesterday_files(day: date):
    """Files changed by commits dated yesterday, grouped by top folder."""
    stamp = day.isoformat()
    out = git("log", f"--since={stamp} 00:00", f"--until={stamp} 23:59", "--name-only",
              "--pretty=format:")
    groups = {}
    for line in out.splitlines():
        line = line.strip()
        if not line or any(p in line for p in IGNORE):
            continue
        if line.startswith("."):
            continue
        top = line.split("/")[0] if "/" in line else "(root)"
        groups.setdefault(top, set()).add(line)
    return groups


def threads():
    """Rows of the thread table: number, name, checkpoint, state, next action."""
    readme = REPO / "docs" / "projects" / "README.md"
    if not readme.exists():
        return []
    rows = []
    for line in readme.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        rows.append({"n": cells[0], "thread": cells[1], "checkpoint": cells[2].strip("`"),
                     "state": cells[3], "next": cells[4]})
    return rows


def carried_over():
    """The 'Carried over' list from the previous handover, minus anything now closed."""
    if not OUT.exists():
        return []
    text = OUT.read_text(encoding="utf-8")
    m = re.search(r"## Carried over\n(.*?)(?:\n## |\Z)", text, re.S)
    if not m:
        return []
    return [l.strip("- ").strip() for l in m.group(1).splitlines() if l.strip().startswith("-")]


def build(today: date) -> str:
    prev = today - timedelta(days=1)
    files = yesterday_files(prev)
    rows = threads()
    open_rows = [r for r in rows if not r["state"].lower().startswith("closed")]

    lines = [f"# Handover for {today:%A %d %B %Y}", "",
             f"Generated {datetime.now():%H:%M} from the repo. Read this first, then the",
             "checkpoint of whichever thread you are taking.", "",
             "## Start a new session with", "", "```",
             "Read docs/handover-today.md, then start on the first thread below.",
             "```", "",
             f"## What changed on {prev:%d %B}", ""]

    if files:
        for top in sorted(files):
            names = sorted(files[top])
            shown = ", ".join(n.split("/", 1)[-1] for n in names[:6])
            more = f" (+{len(names) - 6} more)" if len(names) > 6 else ""
            lines.append(f"- **{top}/** {shown}{more}")
    else:
        lines.append("- Nothing committed. Either a quiet day or work that was not published.")

    lines += ["", "## Threads still open", ""]
    if open_rows:
        for r in open_rows:
            lines.append(f"- **{r['n']}. {r['thread']}** — {r['state']}. Next: {r['next']} "
                         f"(`{r['checkpoint']}`)")
    else:
        lines.append("- None. Everything in the table is closed.")

    carry = carried_over()
    lines += ["", "## Carried over", ""]
    if carry:
        lines += [f"- {c}" for c in carry]
    else:
        lines.append("- Nothing carried from the previous handover.")

    lines += ["", "## Before you stop", "",
              "Update the checkpoint of the thread you worked: what is done, what is next, what is",
              "blocked. Three lines. The next morning's handover is built from those.", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", help="YYYY-MM-DD, defaults to today")
    args = ap.parse_args()
    today = date.fromisoformat(args.date) if args.date else date.today()
    text = build(today)
    if args.dry_run:
        print(text)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"handover: {OUT.relative_to(REPO)} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
