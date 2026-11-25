#!/usr/bin/env python3
"""Add one person to the roster and the calendar aliases, in one step.

    python3 add_person.py --name "Ava Nguyen" --role "Event Coordinator" --reports-to vanessa
    python3 add_person.py --name "Ava Nguyen" --role "Event Coordinator" --reports-to vanessa --write

Dry run by default: it prints what would change and touches nothing. With `--write` it
updates both files the weekly note depends on, so a Monday morning addition is one
command rather than two hand edits that can drift apart.

Why both files: the leave calendar names people by full name, and the org chart names
them by id. The alias is the join between them. Adding a person to one without the other
is how someone silently disappears from the note.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
PEOPLE = HERE.parents[1] / "templates/org/people.json"
ALIASES = HERE / "aliases.json"


def slug(name):
    parts = [p for p in re.split(r"[^a-z]+", name.lower()) if p]
    return parts[0] if parts else ""


def load():
    people = json.loads(PEOPLE.read_text())
    aliases = json.loads(ALIASES.read_text())
    return people, aliases


def check(people, aliases, name, role, reports_to, calendar_name, person_id):
    problems = []
    ids = {p["id"] for p in people["people"]} | {p.get("id") for p in people.get("external", [])}
    if person_id in ids:
        problems.append(f"id '{person_id}' is already used")
    if reports_to and reports_to not in ids:
        problems.append(f"reports_to '{reports_to}' is not on the chart")
    if not role:
        problems.append("a role is required; an empty role is a record nobody can use")
    if calendar_name in aliases.get("map", {}):
        problems.append(f"'{calendar_name}' already maps to '{aliases['map'][calendar_name]}'")
    if not person_id:
        problems.append("could not derive an id from the name")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="full name, as it appears in the calendar")
    ap.add_argument("--role", required=True)
    ap.add_argument("--reports-to", default="", help="org id of their manager")
    ap.add_argument("--function", default="Events")
    ap.add_argument("--calendar-name", default="", help="defaults to --name")
    ap.add_argument("--known-as", default="")
    ap.add_argument("--write", action="store_true", help="apply the change; default is a dry run")
    args = ap.parse_args()

    people, aliases = load()
    person_id = slug(args.name)
    calendar_name = args.calendar_name or args.name
    known_as = args.known_as or args.name.split()[0]

    problems = check(people, aliases, args.name, args.role, args.reports_to,
                     calendar_name, person_id)
    print(f"id: {person_id}")
    print(f"name: {args.name}")
    print(f"known as: {known_as}")
    print(f"role: {args.role}")
    print(f"reports to: {args.reports_to or '(none)'}")
    print(f"calendar alias: {calendar_name} -> {person_id}")

    if problems:
        print("\ncannot add:")
        for problem in problems:
            print(f"  - {problem}")
        return 2

    if not args.write:
        print("\ndry run: nothing written. Add --write to apply.")
        return 0

    people["people"].append({
        "id": person_id,
        "name": args.name,
        "known_as": known_as,
        "role": args.role,
        "function": args.function,
        "reports_to": args.reports_to,
        "badges": [],
        "notes": "",
    })
    people["as_at"] = dt.date.today().isoformat()
    PEOPLE.write_text(json.dumps(people, indent=1) + "\n")

    aliases.setdefault("map", {})[calendar_name] = person_id
    ALIASES.write_text(json.dumps(aliases, indent=1) + "\n")

    print("\nwritten: templates/org/people.json and apps/team-map/aliases.json")
    print("next: python3 make_week.py --xlsx <leave calendar> --week <monday>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
