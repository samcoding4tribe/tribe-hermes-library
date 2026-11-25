#!/usr/bin/env python3
"""Show every out-of-bounds file sitting in the synced libraries.

    python3 scripts/scope_check.py

Reads config/exclusions.txt and reports matches under the OneDrive libraries. It reads
names only, never file contents, and changes nothing.
"""

import fnmatch
import os
import pathlib
import sys

ROOT = pathlib.Path.home() / "Library/CloudStorage/OneDrive-TribeTravelandEvents"
LIBRARIES = ["TRIBE GROUP - Share Drive", "TRIBE GROUP - TRIBE Travel",
             "TRIBE GROUP - TRIBE Group Tech"]

# folder names that must never be ingested, whatever is in them
DIRECTORIES = ["CLIENT INFO", "Client quotes"]

PATTERNS = [
    "*passwords*", "*password list*", "*credentials*", "*.kdbx", "*.1pux",
    "*passport*", "*licence number*", "*licence no*",
]


def load_patterns(repo_root):
    path = repo_root / "config/exclusions.txt"
    if not path.exists():
        return PATTERNS
    found = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("- `") and "`" in line[4:]:
            pattern = line.split("`")[1].strip()
            if pattern and not pattern.startswith("TRIBE GROUP") and " " not in pattern:
                found.append(pattern.lower())
    return found or PATTERNS


def scan(patterns):
    hits = []
    for library in LIBRARIES:
        base = ROOT / library
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            here = pathlib.Path(dirpath)
            if any(part in DIRECTORIES for part in here.parts):
                hits.append((str(here.relative_to(ROOT)), "whole folder is out of bounds"))
                dirnames[:] = []
                continue
            for name in filenames:
                low = name.lower()
                for pattern in patterns:
                    if fnmatch.fnmatch(low, pattern.lower()) or pattern.strip("*") in low:
                        hits.append((str((here / name).relative_to(ROOT)), pattern))
                        break
    return hits


def main():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    hits = scan(load_patterns(repo_root))
    if not hits:
        print("no out-of-bounds files found in the synced libraries")
        return 0
    print(f"{len(hits)} out-of-bounds item(s). No agent may read these:\n")
    for path, why in hits:
        print(f"  {path}\n    matched: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
