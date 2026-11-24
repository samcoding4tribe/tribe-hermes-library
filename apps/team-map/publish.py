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
FOLDER = "Where is my TRIBE"     # sibling of Hermes Library, so publishing never touches it
KEEP_WEEKS = 2                   # this week and last; older folders are removed


def web_url(relative):
    return WEB_ROOT + "/" + urllib.parse.quote(relative)


def prune(keep=KEEP_WEEKS, protect=None):
    """Keep the newest reviewable weeks; older copies name who was on leave."""
    root = SYNC_ROOT / FOLDER
    if not root.exists():
        return []
    weeks = sorted((d for d in root.iterdir() if d.is_dir() and d.name[:2] == "20"),
                   key=lambda d: d.name)
    drop = weeks[:-keep] if keep else []
    for d in drop:
        if protect and d.name == protect:
            continue
        shutil.rmtree(d)
    return [d.name for d in drop]


def link_for(monday):
    """Where that week's published copy lives, preferring the document."""
    stem = f"Where is my TRIBE - {monday.isoformat()}"
    folder = SYNC_ROOT / FOLDER / monday.isoformat()
    name = f"{stem}.pdf" if (folder / f"{stem}.pdf").exists() else f"{stem}.png"
    return web_url(f"{FOLDER}/{monday.isoformat()}/{name}")


def publish(monday):
    src = HERE / "weeks" / monday.isoformat() / "map.png"
    if not src.exists():
        raise SystemExit(f"no map to publish at {src}; capture it first")

    dest_dir = SYNC_ROOT / FOLDER / monday.isoformat()
    dest_dir.mkdir(parents=True, exist_ok=True)

    # the image, and the same note as a document so the table travels with it
    png = dest_dir / f"Where is my TRIBE - {monday.isoformat()}.png"
    shutil.copy2(src, png)

    pdf_src = HERE / "weeks" / monday.isoformat() / "note.pdf"
    pdf = None
    if pdf_src.exists():
        pdf = dest_dir / f"Where is my TRIBE - {monday.isoformat()}.pdf"
        shutil.copy2(pdf_src, pdf)

    target = pdf or png
    url = web_url(f"{FOLDER}/{monday.isoformat()}/{target.name}")
    removed = prune(protect=monday.isoformat())

    page = HERE / "weeks" / monday.isoformat() / "email.html"
    if page.exists():
        html = page.read_text()
        import re
        html = re.sub(r'(<a class="fullsize" href=")[^"]*(")',
                      lambda m: m.group(1) + url + m.group(2), html)
        page.write_text(html)

    return target, url, removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help="any date in the week, YYYY-MM-DD")
    args = ap.parse_args()
    day = dt.date.fromisoformat(args.week)
    monday = day - dt.timedelta(days=day.weekday())

    dest, url, removed = publish(monday)
    print(f"copied to {dest}")
    print(f"link: {url}")
    if removed:
        print("removed older weeks: " + ", ".join(removed))


if __name__ == "__main__":
    main()
