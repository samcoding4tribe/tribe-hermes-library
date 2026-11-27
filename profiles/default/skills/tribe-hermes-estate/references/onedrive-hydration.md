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

## When the content is needed and the stub refuses

A refusal needs locating before it can be reported: one stalled file and a mount that refuses
every stub look identical from a single failed read. Probe three or four small stubs across
different top-level folders and print the outcome per file — a mix of successes and `Errno 11`
means a stalled file, all failures mean the provider, and the difference is what the person has
to act on.

```python
for p in small_dataless_files[:4]:      # skip 0-byte and >300 KB files
    try:
        with open(p, 'rb') as f: f.read(4); print("OK  ", p)
    except OSError as e: print("FAIL", e, p)
```

- **Do not reach for `brctl download`.** That is iCloud Drive's tool; against a OneDrive mount
  it answers `Logged out - iCloud Drive is not configured` and changes nothing. There is no
  shell equivalent for the OneDrive file provider, so a refused stub stays refused locally.
- **The content then comes from wherever the file is authored**, not from the mount: the app or
  web view that owns the record can export it, and that is a decision to hand back to the owner
  of the account rather than a download to keep retrying. Say the file is unreadable locally and
  offer the two shapes; do not narrate the probes as progress.
- **A browser session has to be proven signed in first.** The automated browser reports whether
  it carries the person's profile (`real_profile_unavailable` when the default browser is not
  Chromium-family — the fix is a Chromium default or the `browser.use_real_profile` toggle, not
  a retry). Read that before promising to fetch anything behind a Microsoft login.

## A count is true only of the moment it was taken

Sample numbers on this estate moved by an order of magnitude in a day because Sam downloaded
the working set: before, the tree had 3,714 visible files with most of them unreadable;
after, 194,848 files enumerated and the needed folders read cleanly. Pinning both changes
the numerator and makes previously invisible parts of the tree enumerable.

So never write "the scan was wrong" or "the earlier note was wrong" when a number moves.
Record which state the measurement was taken in: downloaded, partially pinned, or online-only.
A checkpoint that says "3,463 of 3,714 unreadable" is useless without that, and the next
reader will conclude the previous one could not measure.

## What the client already knows, before you theorise

`~/Library/Logs/OneDrive/Business1/SyncDiagnostics.log` is rewritten continuously and carries
running counters for the whole account:

```
numFileFailedDownloads = 95037
numFileFailedUploads   = 484
failedBytesUploadedTotal = 95552202
StallErrorSummary = [Source:3 Reason:111 Context:0 ... Files:1 Hits:3 Extensions:pptx;]
```

Read those four before designing a fix. On this estate they showed tens of thousands of
failed downloads and a single stalled `.pptx` while nothing surfaced in a form a person would
notice, which is why "the files are there but will not open" arrived as a mystery.

- **One file that never hydrates is a stall, not a policy.** `StallErrorSummary` names it and
the extension. The fix is a manual touch — open it once in its own app, or set "Always keep on
this device" on that file — not a client reset, and not a re-measurement.
- **Healthy machines need a second source.** The counters are per account, so a colleague's
problem is invisible from your machine; a bot chat that reports one dataless file will say
"there are 95k downloads failing" long before the user connects the two.
- **Dated logs are weak evidence.** `SyncEngine-*.odl` / `.aodl` files with a mtime of a minute
ago prove the engine is running now. Older dated log files stopping says nothing on its own.

## Conflict copies

`find -iname "*conflict*"` returns false positives that look alarming: a document genuinely
called `Conflict.png` and vendored `jSignature.min.noconflict.js`. Open or stat the hits
before reporting that a sync produced conflict copies; a real one carries the machine name in
the filename (`<name>-<MachineName>-conflicted copy`).
