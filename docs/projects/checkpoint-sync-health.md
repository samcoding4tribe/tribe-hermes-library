# Is everyone's OneDrive actually syncing?

Raised 26 November 2026, out of thread 0. Thread 0 was about this Mac failing to read files.
This is the larger question behind it: this machine's client reported 95,037 failed downloads
and one persistently stalled file, and the same failure on a colleague's machine looks like
"the file is there but won't open" — which nobody reports as a sync problem.

## What this machine's client says

From `~/Library/Logs/OneDrive/Business1/SyncDiagnostics.log`, 26 November 2026:

```
numFileFailedDownloads  = 95037
numFileFailedUploads    = 484
failedBytesUploadedTotal = 95552202
StallErrorSummary = [Source:3 Reason:111 Context:0 ... Files:1 Hits:3 Extensions:pptx;]
```

So the client knew, counted, and kept going. The stalled file is the one PowerPoint that is
still dataless. Nothing surfaced to a person until it was measured from outside.

## The test worth having on every machine

Cheap, no model in the loop, safe to run anywhere:

1. Count files with the `dataless` flag in the folders that matter (Python: `os.lstat().st_flags & 0x40000000`).
2. Read one byte from a sample; count failures.
3. Pull the two counters above out of the newest `SyncDiagnostics.log`.
4. Report counts, never contents.

On a machine that is healthy the answer is "0 dataless, 0 read failures, 0 stalls". Anything
else is a person who thinks their files are there.

## The two layers, and who can see which

- **Per machine:** the check above, run by that machine's builder or by the person's own
  assistant. This is the only way to see a colleague's problem from inside the estate.
- **Per tenant:** Microsoft's own OneDrive sync health reports in the admin centre, if this
  organisation has the licence and Sam has the role. Whether he does is UNKNOWN.

## What it needs from Sam

- Whether M365 sync health reporting is available to him; if yes, it is the cheapest estate view.
- Whether the per-machine check runs from the delegated builder as part of its maintenance
  pass, or as a standalone weekly job.
- What counts as reportable: one dataless file, or only failures older than a day.

## Not the same as

Thread 0, which was about this Mac being unable to read anything at all. That one is nearly
closed; this one is about the other machines, where the same fault would be invisible.
