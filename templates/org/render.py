#!/usr/bin/env python3
"""Render a people map from people.json using org-map.html.tmpl.

    python3 render.py people.json out.html
    python3 render.py people.json out.html --template org-map.html.tmpl

Stdlib only, so it runs wherever Hermes runs. Validates the graph before
writing: a reports_to pointing at an unknown id, or a duplicate id, is reported
as an error rather than silently producing a broken chart.
"""

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
TOKEN = "__DATA__"


def validate(data):
    errors, warnings = [], []
    people = data.get("people") or []
    if not people:
        errors.append("no people in the data file")
    ids = [p.get("id") for p in people]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append(f"duplicate ids: {', '.join(map(str, dupes))}")
    known = set(ids)
    for p in people:
        parent = p.get("reports_to")
        if isinstance(parent, list):
            for one in parent:
                if one not in known:
                    errors.append(f"{p.get('id')} reports_to unknown id '{one}'")
        elif parent and parent not in known:
            errors.append(f"{p.get('id')} reports_to unknown id '{parent}'")
        if not p.get("name"):
            warnings.append(f"{p.get('id')} has no name")
    for g in data.get("groups") or []:
        for ref in g.get("under") or []:
            if ref not in known:
                errors.append(f"group '{g.get('label')}' refers to unknown id '{ref}'")
    roots = [p for p in people if not p.get("reports_to") and not p.get("unplaced")]
    if len(roots) > 1:
        warnings.append(f"{len(roots)} roots: " + ", ".join(r["id"] for r in roots))
    if not roots:
        errors.append("no root: every person has a reports_to, so the tree has nothing to hang from")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description="Render an org people map to HTML.")
    ap.add_argument("data", help="path to people.json")
    ap.add_argument("out", help="path to write the rendered .html")
    ap.add_argument("--template", default=str(HERE / "org-map.html.tmpl"))
    args = ap.parse_args()

    data = json.loads(pathlib.Path(args.data).read_text(encoding="utf-8"))
    errors, warnings = validate(data)

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    tmpl = pathlib.Path(args.template).read_text(encoding="utf-8")
    if TOKEN not in tmpl:
        print(f"error: template has no {TOKEN} placeholder", file=sys.stderr)
        return 2

    # json.dumps keeps the payload one line and escapes </script> safely enough
    # for a data literal; the extra replace guards the closing-tag case.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = tmpl.replace(TOKEN, payload).replace("__ORG__", data.get("org", "People map"))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(data.get('people') or [])} people, {len(data.get('groups') or [])} unnamed groups)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
