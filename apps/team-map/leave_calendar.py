#!/usr/bin/env python3
"""Read the staff leave calendar and emit today's status per person.

    python3 leave_calendar.py --xlsx "/path/Leave Calendar 2026.xlsx"
    python3 leave_calendar.py --xlsx ... --date 2026-11-30 --json out.json

Stdlib only: the workbook is an unzipped set of XML files, so no spreadsheet
library is needed and this runs on Windows and macOS alike.

The sheet holds a month per block: a row naming the month, a row of weekday
letters, a row of day numbers, then one row per person with a code per day.
Codes come from the legend at the top of the sheet.
"""

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

CODE_MEANING = {
    "": "in the office",
    "AL": "annual leave",
    "FM": "family leave",
    "OTH": "other leave",
    "DIL": "leave",
    "X": "not in the office",
    "OS": "onsite",
    "S": "site inspection",
    "PH": "public holiday",
}

MONTHS = {m.upper(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"], start=1)}


def shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall(f"{NS}si"):
        out.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
    return out


def sheet_paths(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rel_map = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sheet in wb.find(f"{NS}sheets"):
        target = rel_map.get(sheet.get(f"{REL_NS}id"), "")
        if target and not target.startswith("/"):
            target = "xl/" + target.lstrip("./")
        out[sheet.get("name")] = target
    return out


def col_index(ref):
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def read_grid(z, path, strings):
    root = ET.fromstring(z.read(path))
    grid = {}
    for row in root.iter(f"{NS}row"):
        r = int(row.get("r"))
        for cell in row.findall(f"{NS}c"):
            ref = cell.get("r")
            t = cell.get("t")
            v = cell.find(f"{NS}v")
            isel = cell.find(f"{NS}is")
            if t == "s" and v is not None:
                value = strings[int(v.text)]
            elif t == "inlineStr" and isel is not None:
                value = "".join(x.text or "" for x in isel.iter(f"{NS}t"))
            elif v is not None:
                value = v.text
            else:
                continue
            grid[(r, col_index(ref))] = value
    return grid


def pick_sheet(names, year):
    for name in names:
        if str(year) == name.strip():
            return name
    for name in names:
        if str(year) in name:
            return name
    return None


def to_serial(value):
    """Excel stores dates as days since 1899-12-30, sometimes as text."""
    try:
        n = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None
    return n if 30000 <= n <= 70000 else None


def parse_day_blocks(grid):
    """Each month is a block: a row of day serials, then a row per person."""
    day_rows = {}
    for (r, c), v in grid.items():
        if c == 1:
            continue
        serial = to_serial(v)
        if serial:
            day_rows.setdefault(r, {})[c] = serial

    blocks, last_row = [], max((r for r, _ in grid), default=0)
    rows = sorted(r for r, days in day_rows.items() if len(days) >= 20)
    for i, day_row in enumerate(rows):
        end_row = rows[i + 1] if i + 1 < len(rows) else last_row + 1
        people = []
        for r in range(day_row + 1, end_row):
            name = grid.get((r, 1))
            if isinstance(name, str) and name.strip() and not to_serial(name):
                people.append((r, name.strip()))
        if people:
            blocks.append({"day_row": day_row, "days": day_rows[day_row], "people": people})
    return blocks


def statuses_for(grid, blocks, when):
    serial = (when - dt.date(1899, 12, 30)).days
    block = next((b for b in blocks if serial in b["days"].values()), None)
    if not block:
        return []
    col = next(c for c, s in block["days"].items() if s == serial)
    out = []
    for row, name in block["people"]:
        raw = grid.get((row, col), "")
        code = str(raw).strip().upper()
        out.append({
            "name": name,
            "code": code,
            "state": CODE_MEANING.get(code, code or "in the office"),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--date", help="YYYY-MM-DD, defaults to today")
    ap.add_argument("--year", type=int)
    ap.add_argument("--json", help="write the result here")
    args = ap.parse_args()

    when = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    year = args.year or when.year

    with zipfile.ZipFile(args.xlsx) as z:
        strings = shared_strings(z)
        paths = sheet_paths(z)
        sheet = pick_sheet(list(paths), year)
        if not sheet:
            sys.exit(f"no sheet for {year} in {', '.join(paths)}")
        grid = read_grid(z, paths[sheet], strings)

    blocks = parse_day_blocks(grid)
    rows = statuses_for(grid, blocks, when)
    summary = {
        "date": when.isoformat(),
        "sheet": sheet,
        "blocks_found": len(blocks),
        "people": rows,
    }
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=1)
        print(f"wrote {args.json}: {len(rows)} people, {when.isoformat()}")
        return
    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    print(f"{when.isoformat()} · sheet {sheet} · {len(rows)} people · {len(blocks)} months")
    for state, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>3}  {state}")
    for r in rows:
        if r["code"]:
            print(f"       {r['name']}: {r['state']}")


if __name__ == "__main__":
    main()
