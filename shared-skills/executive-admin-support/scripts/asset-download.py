#!/usr/bin/env python3
"""Download the files listed in a spreadsheet column into a folder.

    python3 asset-download.py sheet.xlsx ~/Downloads/job-name            # all rows
    python3 asset-download.py sheet.xlsx ~/Downloads/job-name --limit 3  # sample first
    python3 asset-download.py sheet.xlsx ~/Downloads/job-name --column "Post Photo Url"

Without --column it picks the column whose header mentions a url/photo and whose
cells are mostly http links, then prints which one it chose — check that line before
trusting a long run.

Names files <date>_<time>_<who>_<hash8>.<ext>, skips URLs already handled, refuses
non-image responses, and writes download-report.json (name, bytes, content type,
source URL) as the audit trail. asset-rename.py turns these into 1.date-name.jpg.

Stdlib plus openpyxl, which the Hermes documents environment carries.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
NAME_HINTS = ("contact name", "name", "who", "contact")
DATE_HINTS = ("posted date", "date", "created", "timestamp")


def load_rows(path):
    from openpyxl import load_workbook

    ws = load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise SystemExit("sheet is empty")
    return [str(h or "") for h in rows[0]], rows[1:]


def pick_url_column(header, rows):
    best = None
    for i, name in enumerate(header):
        vals = [str(r[i]) for r in rows if len(r) > i and r[i]]
        if not vals:
            continue
        http = sum(1 for v in vals if v.startswith("http"))
        if http / len(vals) < 0.8:
            continue
        score = http + (100 if re.search(r"photo|image|url|link", name, re.I) else 0)
        if best is None or score > best[0]:
            best = (score, i)
    if best is None:
        raise SystemExit("no column looks like a list of links; pass --column explicitly")
    return best[1]


def parse_when(value):
    """Platforms write prose dates ('November 22, 2026 11:56 PM'); return date, time."""
    if value is None:
        return "", ""
    text = str(value).strip()
    for fmt in ("%B %d, %Y %I:%M %p", "%d %B %Y %I:%M %p", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
        try:
            when = dt.datetime.strptime(text, fmt)
            return when.strftime("%Y-%m-%d"), when.strftime("%H%M")
        except ValueError:
            continue
    digits = re.sub(r"[^0-9]", "", text)[:8]
    return digits, ""


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "-", str(text or "").strip()).strip("-").lower() or "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("outdir")
    ap.add_argument("--column", help="header text of the link column")
    ap.add_argument("--limit", type=int, default=0, help="stop after N files (sample run)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--allow-non-image", action="store_true", help="accept any content type")
    args = ap.parse_args()

    header, rows = load_rows(args.sheet)
    if args.column:
        if args.column not in header:
            raise SystemExit(f"column {args.column!r} not in sheet; found: {', '.join(header)}")
        idx_url = header.index(args.column)
    else:
        idx_url = pick_url_column(header, rows)
    print(f"column: {header[idx_url]!r} (index {idx_url})")

    idx_name = next((header.index(h) for h in header if h.lower() in NAME_HINTS), None)
    idx_date = next((header.index(h) for h in header if h.lower() in DATE_HINTS), None)

    out = pathlib.Path(args.outdir).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    seen, done, failed, skipped = set(), [], [], []
    for row in rows:
        url = row[idx_url] if len(row) > idx_url else None
        if not url or not str(url).startswith("http"):
            continue
        url = str(url).strip()
        if url in seen:
            skipped.append(url)
            continue
        if args.limit and len(done) + len(failed) >= args.limit:
            break
        seen.add(url)

        who = row[idx_name] if idx_name is not None and len(row) > idx_name else ""
        date, time = parse_when(row[idx_date] if idx_date is not None and len(row) > idx_date else None)

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Hermes admin)"})
            with urllib.request.urlopen(req, timeout=args.timeout) as response:
                ctype = response.headers.get("Content-Type", "").split(";")[0]
                data = response.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            failed.append({"url": url, "error": str(exc)})
            continue

        if not args.allow_non_image and not ctype.startswith(("image/", "application/pdf")):
            failed.append({"url": url, "error": f"unexpected content type: {ctype}"})
            continue

        stem = "_".join(p for p in (date, time, slug(who), url.rsplit("/", 1)[-1][:8]) if p)
        target = out / f"{stem}{EXT.get(ctype, '.pdf' if ctype == 'application/pdf' else '.bin')}"
        if target.exists() and not args.overwrite:
            skipped.append(url)
            continue
        target.write_bytes(data)
        done.append({"file": target.name, "bytes": len(data), "type": ctype, "url": url})

    report = {
        "sheet": str(args.sheet), "column": header[idx_url], "outdir": str(out),
        "downloaded": len(done), "skipped": len(skipped), "failed": failed,
        "total_mb": round(sum(d["bytes"] for d in done) / 1_048_576, 1), "files": done,
    }
    (out / "download-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{len(done)} downloaded, {len(skipped)} skipped, {len(failed)} failed, "
          f"{report['total_mb']} MB -> {out}")
    for f in failed[:10]:
        print("  failed:", f["url"], f["error"], file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
