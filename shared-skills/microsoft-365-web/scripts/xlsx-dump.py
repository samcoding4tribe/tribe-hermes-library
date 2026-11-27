#!/usr/bin/env python3
"""Dump a .xlsx to TSV using only the standard library.

Usage: python3 xlsx-dump.py FILE.xlsx [SHEET_INDEX]

Why: openpyxl is not present in every interpreter this runs under, and a Forms
response export only needs shared strings plus one sheet. The row count goes to
stderr so the caller can compare it with the number of responses before trusting
the contents -- a short count means the export is stale.
"""

import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
SML = {"m": NS[1:-1]}


def col_index(ref):
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read(path, sheet=1):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", SML):
                shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
        target = "xl/worksheets/sheet%d.xml" % sheet
        if target not in names:
            sheets = sorted(n for n in names if n.startswith("xl/worksheets/sheet"))
            target = sheets[sheet - 1]
        root = ET.fromstring(z.read(target))
        rows = []
        for row in root.iter(NS + "row"):
            cells = {}
            for c in row:
                ref = c.get("r") or ""
                kind = c.get("t")
                v = c.find("m:v", SML)
                inline = c.find("m:is", SML)
                if kind == "s" and v is not None:
                    val = shared[int(v.text)]
                elif v is not None:
                    val = v.text
                elif inline is not None:
                    val = "".join(x.text or "" for x in inline.iter(NS + "t"))
                else:
                    val = ""
                if ref:
                    cells[col_index(ref)] = val or ""
            if cells:
                width = max(cells) + 1
                rows.append([cells.get(i, "") for i in range(width)])
        return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    sheet = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rows = read(sys.argv[1], sheet)
    for r in rows:
        print("\t".join((c or "").replace("\t", " ").replace("\n", " / ") for c in r))
    print("rows: %d (including the header row)" % len(rows), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
