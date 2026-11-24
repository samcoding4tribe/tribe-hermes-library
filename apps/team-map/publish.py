"""Publish one week's map to SharePoint and put the link in the note.

The email travels with the map embedded, so it reads in any client. This adds the
second half: a copy on the TRIBE GROUP site, linked from the note, for anyone who
wants it full size, on a phone, or on a screen in the office.

    python3 publish.py --week 2026-11-30

Writes the map to the synced library, which OneDrive carries to the site, then
rewrites the "full size" line in that week's email.html with the web address.
"""

import argparse
import datetime as dt
import pathlib
import shutil
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent

# The synced library on this Mac maps to this folder on the site.
SYNC_ROOT = pathlib.Path(
    "~/Library/CloudStorage/OneDrive-TribeTravelandEvents/TRIBE GROUP - TRIBE Group Tech"
).expanduser()
WEB_ROOT = ("https://tribemanagement.sharepoint.com/"
            "Shared%20Documents/TRIBE%20Group%20Tech")
FOLDER = "Whereabouts"          # sibling of Hermes Library, so publishing never touches it


def web_url(relative):
    return WEB_ROOT + "/" + urllib.parse.quote(relative)


def publish(monday):
    src = HERE / "weeks" / monday.isoformat() / "map.png"
    if not src.exists():
        raise SystemExit(f"no map to publish at {src}; capture it first")

    dest_dir = SYNC_ROOT / FOLDER / monday.isoformat()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"whereabouts-{monday.isoformat()}.png"
    shutil.copy2(src, dest)

    url = web_url(f"{FOLDER}/{monday.isoformat()}/{dest.name}")

    page = HERE / "weeks" / monday.isoformat() / "email.html"
    if page.exists():
        html = page.read_text()
        import re
        html = re.sub(r'(<a class="fullsize" href=")[^"]*(")',
                      lambda m: m.group(1) + url + m.group(2), html)
        page.write_text(html)

    return dest, url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="any date in the week, YYYY-MM-DD")
    args = ap.parse_args()
    day = dt.date.fromisoformat(args.week)
    monday = day - dt.timedelta(days=day.weekday())

    dest, url = publish(monday)
    print(f"copied to {dest}")
    print(f"link: {url}")


if __name__ == "__main__":
    main()
