#!/usr/bin/env python3
"""Build one week's note: data, map page and email, all dated.

    python3 make_week.py --xlsx "/path/Leave Calendar 2026.xlsx" --week 2026-11-23

Writes, all named after the Monday of that week:
    week-<date>.json / .txt      the data and a plain summary
    week-data-<date>.js          data for the map page
    map-<date>.html              the map, ready to screenshot as map-<date>.png
    email-<date>.html            the note, with the table generated from data

The map image itself is captured in the desktop app or a headless browser; this
script names the file and the page it should capture.
"""

import argparse
import datetime as dt
import json
import pathlib

import weekly
import workflow as wf

HERE = pathlib.Path(__file__).resolve().parent

EMAIL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8" />
<title>Where is my TRIBE? {range}</title>
<style>
  body{{margin:0;padding:24px;background:#f4f1ec;font-family:-apple-system,"Segoe UI",Arial,sans-serif;color:#24201c}}
  .mail{{max-width:720px;margin:0 auto;background:#fffdf9;border:1px solid #e6ded2;border-radius:14px;overflow:hidden}}
  .head{{padding:24px 28px 0}}
  .kicker{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#c8521d;margin:0 0 8px}}
  h1{{margin:0;font-size:24px;line-height:1.2;font-weight:600;letter-spacing:-.01em}}
  .mapWrap{{margin:18px 0 0;padding:0 18px}}
  .mapWrap img{{display:block;width:100%;height:auto;border-radius:10px;border:1px solid #e7dfd2}}
  .body{{padding:8px 28px 6px;font-size:14px;line-height:1.55}}
  h2{{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#8a7f72;margin:22px 0 8px;font-weight:600}}
  table{{width:100%;border-collapse:collapse;font-size:12.5px}}
  th,td{{text-align:left;padding:7px 8px;border-top:1px solid #efe8de}}
  th{{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:#8a7f72;font-weight:600;border-top:none;padding-bottom:4px}}
  td.name{{font-weight:600;white-space:nowrap}}
  td.blank{{color:#b9b0a4}}
  tr.rest td{{color:#8a7f72;font-style:italic}}
  .foot{{padding:14px 28px 22px;font-size:11.5px;color:#93887b;border-top:1px solid #efe8de;margin-top:16px}}
  .note{{margin:0 0 6px}}
  .fullsizeLine{{margin:10px 0 0;font-size:12px;color:#8a7f72}}
  .fullsizeLine a{{color:#c8521d;text-decoration:none;font-weight:600}}
</style></head>
<body>
<div class="mail">
  <div class="head">
    <p class="kicker">TRIBE · weekly whereabouts</p>
    <h1>Where is my TRIBE? {range}</h1>
  </div>
  <div class="mapWrap"><img src="map.png" alt="Map showing where the team is this week" /></div>
  <div class="body">
    <p class="fullsizeLine"><a class="fullsize" href="{link}">Open the full note</a> on the TRIBE group site</p>
    <h2>The week at a glance</h2>
    <table>
      <thead><tr><th>Name</th>{head}</tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p style="margin-top:14px;color:#5d5348;font-size:13px">{note}</p>
  </div>
  <div class="foot"><p class="note">{foot}</p></div>
</div>
</body></html>
"""


def published_url(monday):
    """The SharePoint address for that week's map, if it has been published."""
    try:
        import publish
        return publish.link_for(monday)
    except Exception:
        return "#"


def cell(day):
    if not day:
        return ""
    code, label, place = day.get("code", ""), day.get("label", ""), day.get("place", "")
    kind = day.get("kind", "")
    if place:
        word = "holiday" if kind == "holiday" else label
        return f"{word} · {place}"
    return label


def build_week(xlsx, monday):
    where = weekly.load_json("where.json", {})
    aliases = weekly.load_json("aliases.json", {"map": {}})["map"]
    sheet = wf.find_sheet()
    evs = wf.events(sheet) if sheet else []
    return weekly.build(xlsx, monday, where, aliases, evs, wf.initials_of()), sheet, len(evs)


def write_email(data, monday, out):
    days = [monday + dt.timedelta(days=i) for i in range(5)]
    labels = [d.strftime("%a %-d %b") for d in days]
    head = "".join(f"<th>{l.split()[0]}</th>" for l in labels)

    away = [p for p in data["people"] if any(v["code"] for v in p["days"].values())]
    rows = []
    for p in sorted(away, key=lambda x: x["name"]):
        cells = []
        for d in days:
            v = p["days"].get(d.isoformat(), {})
            txt = cell(v)
            cls = "blank" if not txt else ""
            if d.weekday() == 4 and not txt:
                txt, cls = "wfh", "blank"
            cells.append(f'<td class="{cls}">{txt}</td>')
        rows.append(f'<tr><td class="name">{p.get("short", p["name"])}</td>{"".join(cells)}</tr>')
    rows.append('<tr class="rest"><td class="name">Everyone else</td>'
                '<td>in</td><td>in</td><td>in</td><td>in</td><td>wfh</td></tr>')

    unplaced = [p for p in away if not (p["places"] or [])]
    note = ("Place names show once they are recorded: an onsite trip, a site visit, or a holiday "
            "someone has chosen to share.")
    if unplaced:
        note += (f" Today {len(unplaced)} of {len(away)} away have no location yet, so their "
                 "faces sit under the map until one is added.")

    rng = f"{days[0].strftime('%-d %b')} – {days[4].strftime('%-d %b')}"
    foot = ("Draft for review. Statuses from the leave calendar; travel side to follow. "
            "Friday is work from home unless stated.")
    html = EMAIL.format(range=rng, monday=monday.isoformat(), head=head,
                        rows="".join(rows), note=note, foot=foot,
                        link=published_url(monday))
    (out / "email.html").write_text(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--week", required=True, help="a date in the week, YYYY-MM-DD")
    args = ap.parse_args()

    monday = weekly.monday_of(dt.date.fromisoformat(args.week))
    data, sheet, n_events = build_week(args.xlsx, monday)
    stamp = monday.isoformat()

    out = HERE / "weeks" / stamp
    out.mkdir(parents=True, exist_ok=True)

    (out / "data.json").write_text(json.dumps(data, indent=1))
    (out / "data.js").write_text(
        "window.WEEK = " + json.dumps({
            "week_start": data["week_start"],
            "people": [{"name": p["name"], "short": p.get("short", p["name"].split()[0]),
                        "places": p["places"], "days": p["days"]}
                       for p in data["people"]],
        }) + ";\n")

    template = (HERE / "map.html").read_text()
    page = (template
            .replace('<script src="week-data.js"></script>', '<script src="data.js"></script>')
            .replace('src="lib/', 'src="../../lib/'))
    (out / "map.html").write_text(page)

    write_email(data, monday, out)

    away = [p for p in data["people"] if any(v["code"] for v in p["days"].values())]
    print(f"{stamp}: {len(data['people'])} people, {len(away)} away")
    print(f"  {out}/map.html  -> capture as {out}/map.png")
    print(f"  {out}/email.html")
    if sheet:
        print(f"  places: {sheet.name} ({n_events} events)")
    else:
        print("  places: workflow sheet not found, where.json only")


if __name__ == "__main__":
    main()
