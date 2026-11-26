# Measuring OneDrive hydration on macOS

OneDrive keeps most files as stubs: a name, a logical size, and a `dataless` flag, with the
bytes still in the cloud. The file provider is supposed to fetch a stub the moment something
opens it. This estate has a provider that instead returns `EDEADLK` — `OSError: [Errno 11]
Resource deadlock avoided` — in about zero seconds. That signature is what tells "provider
refusing" apart from "slow download" or "no permission": a hydrated file reads instantly, a
stub fails instantly, never in between.

## Counting without downloading

Read the flag, never the file. Every read of a stub triggers the download, so a survey that
opens files to see whether they open will pull gigabytes and take an hour.

```python
import os
DATALESS = 0x40000000          # SF_DATALESS, macOS st_flags
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        if os.path.isdir(p):
            continue
        if os.lstat(p).st_flags & DATALESS:
            dataless += 1
```

Do this in Python, not shell. `find | while read` breaks on the spaces in `TRIBE GROUP -
Share Drive`, and macOS `head` has no `-z` for NUL-separated lists. Count per top-level folder
so the answer says where the weight sits, which is usually the whole point: the client
archive can be 30% stubs while the supplier and workflow folders are fully hydrated.

To test the fetch path itself, pick a `dataless` file whose logical size is small (under a
even couple of MB) and open it. Anything larger costs a real download for one data point.

## A count is true only of the moment it was taken

Sample numbers on this estate moved by an order of magnitude in a day because Sam downloaded
the working set: before, the tree had 3,714 visible files with most of them unreadable;
after, 194,848 files enumerated and the needed folders read cleanly. Pinning both changes
the numerator and makes previously invisible parts of the tree enumerable.

So never write "the scan was wrong" or "the earlier note was wrong" when a number moves.
Record which state the measurement was taken in: downloaded, partially pinned, or online-only.
A checkpoint that says "3,463 of 3,714 unreadable" is useless without that, and the next
reader will conclude the previous one could not measure.

## Conflict copies

`find -iname "*conflict*"` returns false positives that look alarming: a document genuinely
called `Conflict.png` and vendored `jSignature.min.noconflict.js`. Open or stat the hits
before reporting that a sync produced conflict copies; a real one carries the machine name in
the filename (`<name>-<MachineName>-conflicted copy`).
