# A sheet of links into a named, ordered folder

The task: someone sends a spreadsheet whose column D (or whichever) holds URLs to
photos, documents or attachments, and the owner wants those files on disk, named so
the next person can use them. Common with event platforms, CRMs and suppliers that
export a report rather than a zip.

Two passes, two scripts, one approval in between.

## 1. Get the sheet and find the column

Export the spreadsheet to disk first (Outlook attachments: see
`microsoft-365-web`, "Getting attachments and files onto disk"). Then, before any
download:

```python
from openpyxl import load_workbook
rows = list(load_workbook(path, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
header = rows[0]
for i, name in enumerate(header):
    vals = [r[i] for r in rows[1:] if len(r) > i and r[i]]
    print(i, name, len(vals), len({str(v) for v in vals}))
```

That prints every column with how many values are filled and how many are unique.
It answers the two questions that matter: which column the owner means, and whether
the links are one-per-row or repeated per contact. Report the header text back in
the reply — "column D, headed Post Photo Url, 74 unique links, 21 contacts" — so a
wrong guess costs a sentence rather than a folder.

Watch for adjacent columns that look alike: a contact photo and a post photo both
sit in the same export, and the column that repeats once per person is usually not
the one that repeats once per item. Video and thumbnail columns are often present
and entirely empty.

## 2. Sample, show, wait

```bash
python3 scripts/asset-download.py sheet.xlsx ~/Downloads/<job-name> --limit 3
```

Show the three files in the chat and state the size of the full job: how many
files, roughly how many MB, and that it runs in under a minute. Then stop. The
cost of asking is one message; the cost of downloading the wrong column is a folder
the owner has to unpick, and they cannot tell from filenames alone.

## 3. Full run

```bash
python3 scripts/asset-download.py sheet.xlsx ~/Downloads/<job-name>
```

The script fetches each URL, refuses anything whose content type is not an image,
skips duplicates by URL, skips files already on disk unless `--overwrite`, and
writes `download-report.json` mapping every filename to its size, type and source
URL. That report is the audit trail: it is what lets you answer "where did this
file come from" two months later, once the sheet itself has been archived.

Many of these links are public (no auth, no cookie), which is why plain `urllib`
works. If a run returns 401/403 across the board, the export needs the owner's
session, and the answer is the browser, not more retries.

## 4. Rename for the reader

```bash
python3 scripts/asset-rename.py ~/Downloads/<job-name>          # dry run, prints the plan
python3 scripts/asset-rename.py ~/Downloads/<job-name> --apply
```

Output shape, which is what the owner asked for and will ask for again:

```
1.2026-11-15-matt-masson.jpg
2.2026-11-15-claire-whiteman.jpg
...
74.2026-11-22-natalie-brean.jpg
```

- **Number first**, so the delivery order survives a copy to SharePoint, Drive or
a zip. Do not zero-pad unless asked: Finder, Explorer and macOS name sorting all
read `1.` `2.` `10.` in numeric order.
- **Date, then the person or subject**, taken from the row, not from the URL.
- **Drop the opaque hash** from the visible name, but keep it in the source report.
- **Write `rename-map.csv`** with new name, old name, date, time and contact. The
map is what makes the rename reversible and what proves to the owner that order was
preserved.

Two uploads by the same person in the same minute produce the same date-name. That
is not a collision: the number in front keeps the filename unique, and the tie order
falls to the source record's hash. Say so before the owner spots it and files it as
a bug.

## 5. Verify before reporting done

```bash
ls -1 *.jpg | wc -l                    # count matches the report
find . -size 0 | wc -l                 # no empty files
file -b *.jpg | sort | uniq -c         # every file a real image
ls -1 | sed 's/^[0-9]*\.//' | sort | uniq -d   # repeated date-name groups, expected
```

Name collisions, a stub file or a mismatch between the count and the report means
the run is not finished, whatever the script said.

## When the owner says a file looks wrong

Do not agree, and do not delete, on a hunch. Compare the actual pixels across the
folder: downsampling removes re-encoding differences, so identical pictures match.

```bash
mkdir -p /tmp/dupes && for f in *.jpg; do sips -Z 32 -s format png "$f" --out "/tmp/dupes/$(md5 -q "$f").png" >/dev/null; done
md5 -q /tmp/dupes/*.png | sort | uniq -d
```

No output means nothing is duplicated, and the honest answer is what the files
actually are: which rows they came from, their timestamps, and why two of them look
alike. Then let the owner decide whether the spare gets deleted. A wrongly named or
misplaced file is cheap to fix; a deleted original is not.
