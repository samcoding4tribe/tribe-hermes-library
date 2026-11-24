#!/usr/bin/env python3
"""Build the Monday team summary: who is in, who is away, and where we know it.

    python3 weekly.py --xlsx "/path/Leave Calendar 2026.xlsx"
    python3 weekly.py --xlsx ... --week 2026-11-30 --out-prefix week

Reads the leave calendar for Monday to Friday, joins names to the org map through
`aliases.json`, adds place names from `where.json`, and writes:

    <prefix>.json   the data
    <prefix>.html   an email body, ready to paste or open
    <prefix>.txt    the same as plain lines, for a briefing

Nothing is sent. The email is a draft for a person to send after the meeting.
"""

import argparse
import datetime as dt
import json
import pathlib
import zipfile

import leave_calendar as lc

HERE = pathlib.Path(__file__).resolve().parent

SHORT = {
    "": "",
    "AL": "leave",
    "FM": "family",
    "OTH": "other leave",
    "DIL": "leave",
    "X": "away",
    "OS": "onsite",
    "S": "site visit",
    "PH": "public holiday",
}


def load_json(name, default):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else default


def monday_of(day):
    return day - dt.timedelta(days=day.weekday())


def place_for(person_id, code, when, where):
    """A place name only where the record covers that day and the code fits."""
    entry = where.get(person_id) or {}
    for loc in entry.get("locations", []):
        try:
            start = dt.date.fromisoformat(loc["from"])
            end = dt.date.fromisoformat(loc["to"])
        except (KeyError, ValueError):
            continue
        if not (start <= when <= end):
            continue
        kind = loc.get("kind", "")
        if kind == "work" and code in {"OS", "S"}:
            return loc.get("place", "")
        if kind == "holiday" and loc.get("public") and code in {"AL", "FM", "OTH", "DIL", "X"}:
            return loc.get("place", "")
    return ""


def build(xlsx, week_start, where, aliases):
    days = [week_start + dt.timedelta(days=i) for i in range(5)]
    with zipfile.ZipFile(xlsx) as z:
        strings = lc.shared_strings(z)
        paths = lc.sheet_paths(z)
        sheet = lc.pick_sheet(list(paths), week_start.year)
        grid = lc.read_grid(z, paths[sheet], strings)

    by_day = {d: lc.statuses_for(grid, lc.parse_day_blocks(grid), d) for d in days}
    people, skipped = {}, set()
    for d, rows in by_day.items():
        for row in rows:
            name = row["name"]
            if not name.strip() or lc.to_serial(name):
                continue
            pid = aliases.get(name)
            if not pid:
                # not on the org chart: skip, and report it so the sheet gets tidied
                skipped.add(name)
                continue
            entry = people.setdefault(name, {"name": name, "id": pid, "days": {}})
            entry["days"][d.isoformat()] = {
                "code": row["code"],
                "label": SHORT.get(row["code"], row["code"]),
                "place": place_for(pid, row["code"], d, where) if pid else "",
            }

    out_people = []
    for name in sorted(people):
        days_out = people[name]["days"]
        away = [d for d, v in days_out.items() if v["code"]]
        places = sorted({v["place"] for v in days_out.values() if v["place"]})
        out_people.append({
            "name": name,
            "id": people[name]["id"],
            "days": days_out,
            "away_days": len(away),
            "places": places,
        })
    return {"week_start": week_start.isoformat(), "sheet": sheet,
            "people": out_people, "skipped": sorted(skipped)}


def render_html(data, org_names):
    days = [data["week_start"]] + [
        (dt.date.fromisoformat(data["week_start"]) + dt.timedelta(days=i)).isoformat()
        for i in range(1, 5)
    ]
    labels = [dt.date.fromisoformat(d).strftime("%a %-d %b") for d in days]
    away = [p for p in data["people"] if p["away_days"]]
    rows = []
    for p in sorted(data["people"], key=lambda x: x["name"]):
        cells = []
        for d in days:
            v = p["days"].get(d, {})
            label = v.get("label", "")
            place = v.get("place", "")
            text = f"{label} · {place}" if place else label
            cells.append(f"<td>{text}</td>")
        rows.append(f"<tr><th>{p['name']}</th>{''.join(cells)}</tr>")

    away_lines = []
    for p in sorted(away, key=lambda x: -x["away_days"]):
        spans = []
        for d in days:
            v = p["days"].get(d, {})
            if v.get("code"):
                spans.append(f"{dt.date.fromisoformat(d).strftime('%a')} {v['label']}"
                             + (f" ({v['place']})" if v.get("place") else ""))
        away_lines.append(f"<li><b>{p['name']}</b>: {'; '.join(spans)}</li>")

    return f"""<html><body style="font-family:-apple-system,Segoe UI,Arial,sans-serif;font-size:14px;color:#222">
<p>Team whereabouts for the week of {labels[0]} to {labels[-1]}.</p>
<p><b>{len(away)} away at some point this week</b>, {len(data["people"]) - len(away)} in the office all week.</p>
<ul>{''.join(away_lines)}</ul>
<table cellspacing="0" cellpadding="6" style="border-collapse:collapse;font-size:12px">
<thead><tr><th align="left">Name</th>{''.join(f'<th align="left">{l}</th>' for l in labels)}</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
<p style="color:#666;font-size:12px">Blank means in the office. Place names appear only where
someone recorded them, and holiday destinations only where the person agreed to share.</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--week", help="a date in the target week, YYYY-MM-DD; default next Monday")
    ap.add_argument("--out-prefix", default="week")
    args = ap.parse_args()

    today = dt.date.today()
    week_start = monday_of(dt.date.fromisoformat(args.week)) if args.week else monday_of(today + dt.timedelta(days=7))

    where = load_json("where.json", {})
    aliases = load_json("aliases.json", {"map": {}})["map"]

    data = build(args.xlsx, week_start, where, aliases)
    prefix = HERE / args.out_prefix
    pathlib.Path(str(prefix) + ".json").write_text(json.dumps(data, indent=1))
    pathlib.Path(str(prefix) + ".html").write_text(render_html(data, {}))

    away = [p for p in data["people"] if p["away_days"]]
    lines = [f"Team whereabouts, week of {data['week_start']}",
             f"{len(away)} away at some point, {len(data['people']) - len(away)} in all week", ""]
    for p in sorted(away, key=lambda x: -x["away_days"]):
        bits = [f"{dt.date.fromisoformat(d).strftime('%a')} {v['label']}"
                + (f" ({v['place']})" if v.get("place") else "")
                for d, v in p["days"].items() if v.get("code")]
        lines.append(f"{p['name']}: " + "; ".join(bits))
    if data["skipped"]:
        lines += ["", "Not on the org chart, so not shown: " + ", ".join(data["skipped"])]
    pathlib.Path(str(prefix) + ".txt").write_text("\n".join(lines) + "\n")
    print(f"{data['week_start']}: {len(data['people'])} people, {len(away)} away")
    print("\n".join(lines[2:]))


if __name__ == "__main__":
    main()
