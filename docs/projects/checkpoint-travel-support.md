# Checkpoint: interactive support for travel consultants

> **Start here when you want to build it.** This one waits on design, not on work:
> Sam has ideas and has not written them down yet. Nothing should be built until the
> five topics are chosen. Read `docs/projects/travel-support.md` first.

## Where it stands

The brief is written: `docs/projects/travel-support.md`. Nothing built, nothing changed
on OneDrive.

What exists: 1,112 files in the Travel library, of which 707 are client personal files,
so the working corpus is a few hundred. The answerable material is split three ways, and
that is the actual problem: OneNote holds logins and commission, the after-hours manual
holds Virtuoso rate codes and the ATI handoff, and a client folder holds that client's
fees. Only the AFG fee table was found and read. Two "review what to keep" buckets hold
competing workflows and a quote template.

Blocker, shared with the events project: 1,093 of 1,112 files are online-only
placeholders and would not open, so most contents are unknown.

## Definition of done, for a pilot

1. Five topics chosen, each with a named owner and one page: the rule, the exception,
   the source, the owner, the review date.
2. A written refusal rule: if it is not in these sources, say so and name the person to
   call. This is the whole safety design and it is not optional.
3. One consultant running real questions against it for four weeks.
4. Twenty test questions, asked weekly, scored on correct and cited.
5. Escalation named: who a consultant rings when the assistant refuses.
6. A measured decision to continue, extend or stop, written down.

## Remaining work, in order

1. Sam's design work: what the consultant actually asks mid-call, and where the true
   answer sits today. This is the gate.
2. Choose the five topics and their owners: supplier and hotel programme, after-hours
   ticketing and ATI handoff, client fees, insurance referral, cancellation terms.
3. Write the five pages. Roughly a day each plus an hour a month, which is an estimate,
   not a measurement.
4. Choose the platform, on evidence: Copilot Studio if the refusal rule and control
   matter most, the SharePoint agent on pay-as-you-go if cost and no-code matter most.
5. Run the pilot and score it.

## What it needs from you

- Which five topics, and who owns each.
- Which fee schedule governs clients other than AFG, and where it lives.
- Whether OneNote remains the sanctioned source, or content moves to SharePoint and who
  maintains it there.
- Whether an Azure subscription exists, who the Power Platform admin is, and which
  Microsoft 365 licences are held. Nothing can be priced without this.
- Internal tool only, or may a consultant read an answer to a client.

## Keep out

Passwords, passports and `CLIENT INFO/` are already out of bounds in
`config/exclusions.txt`, and the scope check found eleven items. None of them may be
grounded into this assistant, whatever else it reads.
