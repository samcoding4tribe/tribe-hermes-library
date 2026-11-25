---
name: link-batch-download
description: "Fetch a batch of links to files; verify and fix failures."
version: 1.0.0
author: TRIBE admin profiles
license: MIT
metadata:
  hermes:
    tags: [download, batch, http, troubleshooting, links, photos, admin]
---

# Batch download from links

A set of URLs has to arrive as usable files, provably, with a record of anything
that did not. Where the list came from is incidental: a spreadsheet, a PDF, a mail
body, a chat paste, a supplier portal page. The constant is the links and the
host's behaviour, so that is what this skill is about.

`scripts/fetch-images.py` fetches from a `.xlsx`, `.csv`, `.json`, `.pdf` or plain
text file — for everything except a spreadsheet it takes every `http(s)` URL it
finds — with retries, content-type validation, a per-file report and a
`failures.json` that a second pass can retry.

```bash
PY=$(hermes pm environment documents --extra documents --extra documents-pdf)
"$PY" scripts/fetch-images.py links.txt ~/Downloads/batch --limit 3      # sample
"$PY" scripts/fetch-images.py list.pdf ~/Downloads/batch --retry 3 --delay 0.3
"$PY" scripts/fetch-images.py sheet.xlsx ~/Downloads/batch --column "Post Photo Url"
"$PY" scripts/fetch-images.py any.xlsx ~/Downloads/batch --retry-failed ~/Downloads/batch/failures.json
```

Exit code 1 means at least one link failed; 0 means every link in the list is on
disk. Re-runs resume by filename, so nothing is fetched twice by accident.

## When to Use

- A list of links has to become files, and "mostly worked" is not good enough.
- Somebody sends photos, documents or assets as links from a supplier system.
- A previous batch looks wrong: empty files, broken images, suspiciously small sizes.

## Procedure

1. **Collect the links, whatever they arrived in.** Save the sheet, PDF, CSV or mail
   body to disk and let the script extract URLs. If the list is in a web page or a
   portal, read it with the browser and save the URLs to a `.txt`. Do not retype
   links by hand, and do not trust a link that arrived visibly truncated (`...`) in
   an email preview.
2. **Audit the list before fetching.** Count links, count unique ones, note blanks
   and obvious duplicates, and look for near-misses: trailing punctuation, `&amp;`
   escaping, http vs https, mixed domains. A sheet that carries several URL columns
   needs the right column confirmed (`Post Photo Url` beside `Contact Photo Url` is
the classic pair).
3. **Triage two links** with `curl -sSI`: expect `200` and a sensible
   `content-type`. This decides whether the batch is possible at all before any
   bulk work, and separates "the host wants a session" from "the links are wrong".
4. **Sample three, then ask.** Download three, show them in chat with `MEDIA:`
   lines, state the count, the size and the rough run time. The owner approves the
   full run from that message.
5. **Fetch sequentially with a small delay.** These hosts rate-limit; a 429 storm
   costs more than the wall-clock saved by parallelism. Raise `--retry` for a flaky
   host, never for one that is refusing (401/403/404).
6. **Work the failures.** `failures.json` names each link and a readable reason.
   Fix the cause — refresh an expired link, get a session, skip a deleted asset —
   then run `--retry-failed` rather than the whole batch.
7. **Verify** (below), then report the folder, count, total size, and the links
   that need a human.

## Troubleshooting

| Symptom | Usual cause | What to do |
|---|---|---|
| `200` but `content-type: text/html` | login page or error page served as success | the host wants a session. Ask for a fresh link or an authenticated export; never put session cookies in a script |
| `401` / `403` | signed link expired, or auth required | stop and report which links; retrying cannot fix it |
| `404` / `410` | asset deleted or stale | record as gone; do not substitute another file |
| `429` | rate limited | raise `--delay` to 1s, lower `--retry`, rerun; do not parallelise |
| timeouts / connection resets | flaky host or network | `--retry 4`; if it persists, fetch one link with `curl -O --retry 3 --retry-delay 2` to see the raw error |
| zero-byte files | redirect that returned nothing, CDN quirk | `curl -sSI` the link; if headers show a length, re-fetch that link alone |
| file opens as a broken image/document | truncated download | compare received bytes to `content-length`; retry with a longer `--timeout` |
| two files look identical | one asset posted twice, or two URLs to one object | compare downsampled hashes; report it, never delete silently |
| links redirect to a portal home page | expired or single-use links | ask for an export or a fresh share |
| the source file will not open | OneDrive / File Provider placeholder | see Pitfalls; get a real local copy |

## Pitfalls

- **Office attachments often have no Download button.** Save to OneDrive, then fetch a
  real copy with the SharePoint endpoint:
  `https://<tenant>-my.sharepoint.com/personal/<user>/_layouts/15/download.aspx?SourceUrl=<url-encoded path>`
- **OneDrive files are placeholders until read.** openpyxl raises `BadZipFile` and a
  plain read raises `Resource deadlock avoided`, even though a directory listing
  shows a size, and `brctl download` does not help on a managed mount. Get another
  copy rather than repairing it.
- **Office viewers are a separate browser target.** `js()` evaluates in the mail page
  while the screenshot shows the spreadsheet, and the grid sits behind shadow DOM.
  Stop scraping cells; download the file and parse it locally.
- **Public asset hosts need no credentials.** Prove reachability with `curl -I`
  before inventing an auth path, and never ship a cookie jar inside a fetch script.
- **Sanity-check the links, not just the responses.** A truncated or HTML-escaped URL
  can return a perfectly valid 404 page and waste the whole run.
- **Filenames are a separate concern.** Every organisation wants a different
  convention; agree it after the download is proven, keep any order-encoding number
  prefix distinct from the readable part, and treat the output folder as a
  parameter since it gets moved.
- **Deleting is the owner's call.** Show both files and let them choose.

## Verification

- File count matches the report's `downloaded` plus anything already on disk.
- No zero-byte files: `find . -size 0` returns nothing.
- Every file reports as its expected type (`file -b`), never HTML or ASCII text.
- Duplicates checked by content, not bytes: downsample each file
  (`sips -Z 32 -s format png in.jpg --out out.png`) and compare those hashes.
- Spot-check one file with `vision_analyze` when it is an image — an error page
  served with an image content type passes every other test.
- If anything failed, `failures.json` exists and every entry has a readable cause.

`scripts/ea-rename.py` is included only as an example of one naming convention
(numbered, date-first); it is not part of the download pipeline.
