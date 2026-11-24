"""Event destinations, read from the workflow sheet.

The workflow sheet is the record of what is on and where, with an Onsite column
naming who travels. That makes it the better source for work locations than
typing places by hand: when an event moves, the note follows the sheet.

The sheet is renamed from year to year (Workflow_2026 V3.xlsx today), so the file
is found by pattern rather than by name, and the year is taken from whichever
file is found.

    python3 workflow.py            # show what it parsed
"""

import datetime as dt
import glob
import json
import os
import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
T = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

DEFAULT_DIR = pathlib.Path(
    os.path.expanduser("~/Library/CloudStorage/OneDrive-TribeTravelandEvents/"
                       "TRIBE GROUP - Share Drive/WORKFLOW"))

MONTHS = {m.upper(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}


def find_sheet(folder=None):
    """Newest workflow workbook, whatever it is called this year."""
    folder = pathlib.Path(folder or os.environ.get("TRIBE_WORKFLOW_DIR") or DEFAULT_DIR)
    hits = sorted(glob.glob(str(folder / "Workflow_*.xlsx")), key=os.path.getmtime)
    hits = [h for h in hits if not pathlib.Path(h).name.startswith("~$")]
    if not hits:
        return None
    return pathlib.Path(hits[-1])


def _strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    return ["".join(t.text or "" for t in si.iter(T + "t"))
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]


def _rows(path):
    z = zipfile.ZipFile(path)
    shared = _strings(z)
    out = []
    root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    for row in root.iter(T + "row"):
        cells = {}
        for c in row.findall("m:c", NS):
            col = re.match(r"([A-Z]+)", c.get("r")).group(1)
            kind, v, inline = c.get("t"), c.find("m:v", NS), c.find("m:is", NS)
            if kind == "s" and v is not None:
                val = shared[int(v.text)]
            elif inline is not None:
                val = "".join(x.text or "" for x in inline.iter(T + "t"))
            else:
                val = v.text if v is not None else ""
            if val not in ("", None):
                cells[col] = val.strip()
        if cells:
            out.append(cells)
    return out


def _year_from(path):
    m = re.search(r"(20\d\d)", pathlib.Path(path).name)
    return int(m.group(1)) if m else dt.date.today().year


def _dates(text, month, year):
    """'10 - 13', '18-19', '22 - 24', '10' -> (start, end)."""
    nums = re.findall(r"\d{1,2}", text or "")
    if not nums:
        return None
    start = int(nums[0])
    end = int(nums[1]) if len(nums) > 1 else start
    try:
        a = dt.date(year, month, start)
        b = dt.date(year, month, end)
    except ValueError:
        return None
    if b < a:                                    # range running into the next month
        month2 = month % 12 + 1
        y2 = year + (1 if month == 12 else 0)
        try:
            b = dt.date(y2, month2, end)
        except ValueError:
            return None
    return a, b


def _initials(text):
    """'KM & TC', 'JK, ZA, TC, MK & SA', 'CG & KA or Mia?' -> {'KM','TC',...}."""
    out = set()
    for token in re.split(r"[&,/]|\band\b|\bor\b", text or "", flags=re.I):
        token = token.strip().upper()
        m = re.fullmatch(r"([A-Z]{2,3})", token)
        if m:
            out.add(m.group(1))
    return out


def initials_of():
    """first + last initial per org id.

    The org chart carries first names only for most people, so full names come
    from the calendar aliases, which map a calendar name to an org id.
    """
    out = {}
    people = HERE.parents[1] / "templates/org/people.json"
    if people.exists():
        for person in json.loads(people.read_text()).get("people", []):
            parts = [p for p in person.get("name", "").split() if p]
            if len(parts) >= 2:
                out[person["id"]] = (parts[0][0] + parts[-1][0]).upper()
    aliases = HERE / "aliases.json"
    if aliases.exists():
        for full, pid in json.loads(aliases.read_text()).get("map", {}).items():
            parts = [p for p in full.split() if p]
            if len(parts) >= 2:
                out.setdefault(pid, (parts[0][0] + parts[-1][0]).upper())
    return out


def events(path=None, year=None):
    """One entry per event that has a destination, a date and someone onsite."""
    path = pathlib.Path(path) if path else find_sheet()
    if not path or not path.exists():
        return []
    year = year or _year_from(path)
    rows = _rows(path)
    month, out = None, []
    for cells in rows:
        label = cells.get("A", "")
        key = label.strip().upper()
        if key in MONTHS and not cells.get("B"):
            month = MONTHS[key]
            continue
        if month is None or not cells.get("B") or not cells.get("N"):
            continue
        span = _dates(cells.get("B", ""), month, year)
        if not span:
            continue
        place = (cells.get("F") or "").strip()
        if not place:
            continue
        out.append({
            "start": span[0], "end": span[1],
            "place": place,
            "client": (cells.get("C") or "").strip(),
            "event": (cells.get("D") or "").strip(),
            "onsite": _initials(cells.get("N", "")),
            "raw_onsite": cells.get("N", ""),
        })
    return out


def place_for(initials, day, evs):
    """Destination for someone with these initials on this day, if an event covers it."""
    for ev in evs:
        if initials in ev["onsite"] and ev["start"] <= day <= ev["end"]:
            return ev["place"]
    return ""


if __name__ == "__main__":
    path = find_sheet()
    print("sheet:", path)
    evs = events(path)
    print(f"{len(evs)} events with a destination and someone onsite")
    for ev in evs[-8:]:
        print(f"  {ev['start']} to {ev['end']}  {ev['place']:<22} {ev['raw_onsite']}")
    print("initials:", initials_of())
