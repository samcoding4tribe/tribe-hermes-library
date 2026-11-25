# Two separate projects, tracked here

Both came from the same conversation on 25 November 2026 and are deliberately kept
apart: different users, different source content, different failure modes.

## 1. Events preferred supplier knowledge base

Brief: `events-suppliers.md`. Status: draft for review, nothing built.

The problem is content and metadata, not software: supplier paperwork is re-made per
event, the master list is named 2025 and was last saved in 2026, and insurance is
tracked by filename. The recommendation is a SharePoint list plus a documents
library with closed term sets and an append-only rates list, inside the existing
licence, with owner and expiry reminders in phase one.

## 2. Interactive support for travel consultants

Brief: `travel-support.md`. Status: draft for review, nothing built.

The problem is that an answer needs three places at once (OneNote for logins and
commission, the manual for rate codes, a client folder for fees), and the assistant
cannot be better than the content it reads. The recommendation is a Copilot Studio
agent piloted on five curated topics with one consultant, with a written refusal
rule, because a wrong fee reaching a client is the risk worth designing against.

## Shared blocker, found while researching both

Most of the source material will not open on this Mac. Files carry the `dataless`
flag, meaning OneDrive has them as online-only placeholders, and reading one fails
with `Resource deadlock avoided`. Counts at the time of research: 3,463 of 3,714
files in the Share Drive, and 1,093 of 1,112 in the Travel library.

Nothing above can be built on content that will not open, so hydrating those folders
comes before either phase one. It is also why both briefs mark document contents
UNKNOWN rather than guessing.

## A security note worth acting on separately

`TRIBE GROUP - TRIBE Travel/XXX - KELLY to review what to keep/Copy of Passwords (002).xlsx`
is a plaintext-looking credential file sitting in a live folder. Whatever happens with
these projects, that one should be moved to a password manager and deleted.
