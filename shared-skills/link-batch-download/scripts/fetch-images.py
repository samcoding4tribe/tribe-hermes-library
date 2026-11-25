#!/usr/bin/env python3
"""Fetch images from a sheet or list of links, with retries and a failure record.

    python3 fetch-images.py "sheet.xlsx" ~/Downloads/batch --column "Post Photo Url"
    python3 fetch-images.py links.csv outdir --limit 3            # sample first
    python3 fetch-images.py sheet.xlsx outdir --retry 4 --delay 0.3
    python3 fetch-images.py sheet.xlsx outdir --retry-failed outdir/failures.json

Sources: whatever the links arrived in — .xlsx (needs openpyxl), .csv, .json,
.pdf (needs pdfplumber), or plain text. For anything but a spreadsheet, every
http(s) URL found is used, so a mail body or a chat paste saved as .txt works.
Column choice matters for spreadsheets: a client sheet often carries several URL
columns and only one is the one asked for.

Output is deliberate and boring: one file per unique URL, a `download-report.json`
with status, content type, byte count and source URL per file, and
`failures.json` holding everything that did not arrive so a second pass can be
run with --retry-failed instead of re-downloading the successes.

Naming is kept simple on purpose: <date>_<contact-slug>_<urlhash8>.<ext>. Renaming
to an organisation's convention is a separate step, because every client wants a
different one.
"""

import argparse
import csv
import datetime as dt
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

EXT = {"image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
       "image/webp": ".webp", "image/gif": ".gif", "image/heic": ".heic",
       "image/tiff": ".tiff", "image/bmp": ".bmp", "image/svg+xml": ".svg"}
URL_RE = re.compile(r"https?://[^\s\"'<>]+")


def rows_from_sheet(path, column):
    from openpyxl import load_workbook

    ws = load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise SystemExit("sheet is empty")
    header = [str(h or "") for h in rows[0]]
    if column and column in header:
        idx = header.index(column)
    else:
        # Fall back to the first column that looks like URLs.
        idx = next((i for i, h in enumerate(rows[1]) if isinstance(h, str) and h.startswith("http")), None)
        if idx is None:
            raise SystemExit(f"no URL column found; headers are: {', '.join(header)}")
        print(f"note: using column {chr(65 + idx)} ({header[idx]!r})", file=sys.stderr)
    name_idx = header.index("Contact Name") if "Contact Name" in header else None
    date_idx = header.index("Posted Date") if "Posted Date" in header else None
    out = []
    for r in rows[1:]:
        if len(r) <= idx or not r[idx]:
            continue
        out.append({
            "url": str(r[idx]).strip(),
            "contact": r[name_idx] if name_idx is not None and len(r) > name_idx else "",
            "when": r[date_idx] if date_idx is not None and len(r) > date_idx else None,
        })
    return out


def rows_from_text(path):
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    return [{"url": u, "contact": "", "when": None} for u in URL_RE.findall(text)]


def rows_from_pdf(path):
    """Links printed on a page: quotes, invoices, itineraries, supplier lists."""
    import pdfplumber

    found = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for url in URL_RE.findall(page.extract_text() or ""):
                found.append(url)
    return [{"url": u, "contact": "", "when": None} for u in found]


def rows_from_json(path):
    """A list of strings, or objects carrying a url/URL/link field."""
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("urls") or data.get("links") or []
    out = []
    for item in items:
        if isinstance(item, str) and item.startswith("http"):
            out.append({"url": item, "contact": "", "when": None})
        elif isinstance(item, dict):
            url = item.get("url") or item.get("URL") or item.get("link")
            if url:
                out.append({"url": str(url), "contact": item.get("contact", ""), "when": item.get("when")})
    return out


def parse_when(value):
    if value is None:
        return ""
    if isinstance(value, (dt.datetime, dt.date)):
        return value.strftime("%Y-%m-%d")
    text = str(value).strip()
    for fmt in ("%B %d, %Y %I:%M %p", "%d %B %Y %I:%M %p", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", text)
    return m.group(0) if m else ""


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "-", str(text or "").strip()).strip("-").lower() or "unknown"


def fetch(url, timeout, retry, delay):
    """Return (bytes, content_type, status) or raise RuntimeError with a readable reason."""
    last = ""
    for attempt in range(1, retry + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/157.0 Safari/537.36",
                "Accept": "image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                data = r.read()
                status = r.status
            if not data:
                raise RuntimeError("empty response body")
            if ctype not in EXT and not ctype.startswith("image/"):
                raise RuntimeError(f"not an image (content-type {ctype or 'none'}) — "
                                   f"usually a login page or an error page served as 200")
            return data, ctype, status
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 401, 403, 404, 410):
                raise RuntimeError(f"{last} — {e.reason}")  # not worth retrying
        except urllib.error.URLError as e:
            last = f"connection error: {e.reason}"
        except (TimeoutError, RuntimeError) as e:
            last = str(e)
        if attempt < retry:
            time.sleep(min(2 ** attempt * 0.5, 5))
    raise RuntimeError(f"{last} (after {retry} attempts)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="xlsx, csv, json, pdf or txt file holding the links")
    ap.add_argument("outdir")
    ap.add_argument("--column", default="", help="URL column name for spreadsheets")
    ap.add_argument("--limit", type=int, default=0, help="only the first N unique links")
    ap.add_argument("--retry", type=int, default=3)
    ap.add_argument("--delay", type=float, default=0.2, help="seconds between requests, be polite")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--retry-failed", default="", help="path to a failures.json from a previous run")
    args = ap.parse_args()

    out = pathlib.Path(args.outdir).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    if args.retry_failed:
        items = [{"url": f["url"], "contact": f.get("contact", ""), "when": f.get("when")}
                 for f in json.loads(pathlib.Path(args.retry_failed).read_text())]
        print(f"retrying {len(items)} previously failed links", file=sys.stderr)
    else:
        src = pathlib.Path(args.source)
        if not src.exists():
            raise SystemExit(f"not found: {src}")
        suffix = src.suffix.lower()
        if suffix in (".xlsx", ".xlsm"):
            items = rows_from_sheet(src, args.column)
        elif suffix == ".pdf":
            items = rows_from_pdf(src)
        elif suffix == ".json":
            items = rows_from_json(src)
        else:
            items = rows_from_text(src)

    seen, done, skipped, failed = set(), [], [], []
    for item in items:
        url = item["url"]
        if not url.startswith("http") or url in seen:
            continue
        seen.add(url)
        if args.limit and len(done) + len(failed) >= args.limit:
            break

        stem = "_".join(p for p in (parse_when(item.get("when")), slug(item.get("contact")),
                                    url.rsplit("/", 1)[-1][:8]) if p)
        existing = list(out.glob(f"{stem}.*")) if stem else []
        if existing and not args.overwrite:
            skipped.append(url)
            continue

        try:
            data, ctype, status = fetch(url, args.timeout, args.retry, args.delay)
        except RuntimeError as exc:
            failed.append({"url": url, "contact": item.get("contact", ""),
                           "when": str(item.get("when") or ""), "error": str(exc)})
            print(f"  FAIL {url} — {exc}", file=sys.stderr)
            continue

        target = out / f"{stem}{EXT.get(ctype, '.bin')}"
        target.write_bytes(data)
        done.append({"file": target.name, "bytes": len(data), "type": ctype,
                     "status": status, "url": url})
        if args.delay:
            time.sleep(args.delay)

    report = {"source": str(args.source), "outdir": str(out), "downloaded": len(done),
              "skipped": len(skipped), "failed": len(failed),
              "total_mb": round(sum(d["bytes"] for d in done) / 1_048_576, 1), "files": done}
    (out / "download-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if failed:
        (out / "failures.json").write_text(json.dumps(failed, indent=2), encoding="utf-8")
    print(f"{len(done)} downloaded, {len(skipped)} skipped, {len(failed)} failed, "
          f"{report['total_mb']} MB -> {out}")
    if failed:
        print(f"failure detail: {out / 'failures.json'} (rerun with --retry-failed)", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
