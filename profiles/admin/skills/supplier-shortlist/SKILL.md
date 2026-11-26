---
name: supplier-shortlist
description: "Shortlist suppliers and get comparable proposals."
version: 1.0.0
author: TRIBE admin profiles
license: MIT
metadata:
  hermes:
    tags: [procurement, suppliers, quotes, research, comparison, ea, admin-assistant]
---

# Shortlisting suppliers for a capability

The owner needs something bought — hosting, software, a service, a supplier for an
event — and wants six names and proposals they can compare. The work is not a list
of companies. It is fixing what is being bought, verifying that each name actually
sells it, and getting answers in a shape that compares.

## When to Use

- "Who could provide X, and can you get proposals to compare pricing?"
- A capability has to come from outside and the owner has one name in mind.
- An existing supplier set needs a price benchmark before renewal.

## Step 1 — fix the buying shape before shortlisting

Write the shape in one line and get it confirmed before researching: **shared or
dedicated, subscription or owned, managed or self-run, per-seat or per-unit.** These
are not details — they cut the candidate list in half, and a list built on the wrong
shape has to be rebuilt from scratch when the owner corrects it.

If the owner has not said, infer the most likely shape from their size and stated
need, say which shape you are working to, and invite the correction in the same
breath. When they do correct it, re-cut the list immediately and say which names
fall out and why. Do not keep previously recommended names in play to preserve the
work already done.

Sizing belongs here too. Multiply a plausible unit by a plausible volume ("a heavy
user at 3M tokens a month, twenty users") so the answer lands as a monthly range. If
that range is trivial, say so plainly — it is the strongest argument against the
more impressive purchase, and it is usually the owner's real question.

**Find out what produced any volume the owner quotes before multiplying it.** A figure
measured while building, migrating, testing or running a one-off project is not a
forecast: it can sit an order of magnitude above steady state, and annualising it turns
a spike into a scare number that drives the wrong purchase. Ask what they were doing
when they measured it, then size the rollout separately — per seat at light, moderate
and heavy use, against the seat count — and show both in the same table so the spike is
visibly the outlier. If you published an annual figure before asking, correct it out
loud rather than quietly replacing it.

**Price metered subscriptions as metered, not as seats.** Per-seat plans frequently
bill consumption on top at per-unit rates, so the seat price is a floor rather than the
cost. Cost the seat base and the metered usage as two lines, total them, and compare
that total with the alternative; a seat plan quoted at sticker price always flatters
itself.

**A seat fleet is not a cheaper way to buy the same tokens.** Usage bought inside a
vendor's product cannot fund a separate agent platform, which needs its own provider
account behind it. When the owner weighs seats against an endpoint, say that the money is
one-or-the-other rather than additive, then concede the arithmetic plainly if the seats win
on base fee, and move the comparison to what each actually buys, whose terms apply, and
where the data leaves the country. Presenting seats as a discount on tokens is the error
that makes the whole table untrustworthy.

**Check whether the unit is a person or a block of people.** Platform fees are sometimes
quoted per *N* users rather than per seat ("A$500 a month covers ten people"), which scales
differently in both directions: the cost per person falls inside a block and steps up at the
boundary, while a seat fleet rises with every hire. Convert both to cost per person per month
at the owner's actual headcount, and say which way each moves as the team grows — that
asymmetry usually outlasts the sticker-price comparison.

**Separate the pilot from the steady state when the owner intends to self-host.** A hosted
service bought to learn what people actually use, before moving the same tool onto their own
machines, is a test bed and not the destination. Cost it as a pilot (one-off, cheap to stop)
and cost the end state separately (hardware, plus whoever administers updates and backups),
and never present the two as alternatives competing on price — they answer different questions
and are funded from different places. State also what self-hosting does **not** fix: prompts
still leave the building unless the model endpoint is onshore or on-device too.

## Step 2 — separate what a supplier sells from what it sits next to

Search results and industry pages blur the layers deliberately. A data-centre
operator hosts the company that sells you the thing; a reseller sells someone else's
endpoint; a platform is not a provider. Check each candidate's own product page for
the words that describe the transaction ("per token", "per GPU-month", "subscription",
"colocation", "managed service") and drop anything whose own page does not sell what
was asked for.

Say which layer each survivor sits at in the deliverable. It is the difference
between a shortlist and a list of names the owner has to research again.

## Step 3 — collect public price anchors first

One published price beats six quotes in progress, because it turns the quote-only
suppliers into a comparison instead of a waiting room. Convert every figure to a
common unit — per 1,000 typical queries, or per month at the assumed volume — and
name the assumptions. Where a supplier publishes rates in another currency, convert and
**state the rate you used with its date** in the deliverable, so the figures can be
re-checked rather than trusted; a table mixing USD list prices, AUD platform fees and a
converted total is quietly wrong within a month otherwise.

**Price hardware from current retailer listings, never from an aggregator's snapshot.** Blog
and comparison pages reproduce a price table captured months earlier, and the same chip ships
in several chassis at very different prices. Pull two or three live retailer listings, quote a
range with the date you read it, and say plainly when a figure you gave earlier turns out to
be stale rather than quietly replacing it. Hardware-cost arithmetic — fit, decode speed,
prefill against measured volume — is in `references/local-inference-hardware.md`.

Quote-only is the normal state of this market, not a signal of expense. Note who
publishes and who does not in the table; the absence is information about the sales
motion.

## Step 4 — one identical enquiry, sent in parallel

The same numbered question list goes to every candidate, in the same week, so the
answers compare line by line. Adapt the wording to the category, never the structure:
identity of what is being bought, where it physically runs, data handling in writing,
limits and capacity, price in AUD with every fee, how changes are notified, security
and compliance posture, exit and deletion, plus a trial.

- **Ask for the exact thing, not the category.** Model checkpoints, SKUs, versions,
  tiers. Marketing names do not map to delivered product.
- **Ask for retention and deletion in writing.** It is usually the reason the owner
  is buying privately at all.
- **Ask how changes are announced**, in both directions: upgrades that can break a
  working setup, and price or tier changes.
- **Ask for a trial at realistic volume**, with the owner's own inputs. It costs the
  supplier nothing to say yes and it settles quality faster than any comparison table.

The reusable question set, with the AUD and trial wording, is in
`references/enquiry-template.md`.

## Step 5 — do not block on an internal introduction

A warm contact inside a supplier is worth having and is never worth waiting for. Send
the parallel enquiries the day the owner asks, and ask for the introduction in the
same message so it can be mentioned when that particular one goes in. A fortnight
spent waiting for a name is a fortnight of no comparison, and the enquiry is the same
letter either way.

## Step 6 — compare on the terms that bite

Feature matrices look thorough and decide nothing. The comparison is: cost at the
assumed volume, retention and data-handling terms, what happens when a version or
price changes, the limit we will actually hit and its overage, how hard exit is, and
whether the supplier will sign the owner's terms rather than their own. Marketing
claims of the "53% cheaper than X" kind are hypotheses to test with the owner's own
inputs, not facts to put in the table.

## Deliverable shape

A markdown file in the workspace, and a short message that stands alone:

1. One line correcting or confirming the buying shape, if the brief moved.
2. A table: supplier / what we would actually buy / where it runs / what is offered /
   published price.
3. The one published anchor, with the scale check it implies.
4. The enquiry text, ready to send.
5. A recommended sequence: what to trial first, what to quote in parallel, what is
   the benchmark.
6. A gaps section: which prices are unpublished, which claims are unverified, and
   what volume assumption the whole comparison rests on.

End with what the owner decides, not with a recommendation dressed as a decision. The
shape of the purchase is theirs.

Two things to do before the table is written:

- **Read what the owner already holds.** A vendor proposal, quote or contract sits in their
downloads, notes or inbox more often than not, and it fixes the incumbent's prices, units and
block sizes. A comparison built without it costs the wrong thing; cite it as the source for
those lines.
- **Write the numbers into the file the owner will actually open.** If they keep a decision
note or a knowledge base, the cost tables belong inline there, not only in a workspace file
with a pointer to it. A meeting note that says "see the workspace" gets read without the
numbers in front of anyone. Keep the workspace copy as the research record and mirror the
tables across.

## Pitfalls

- **Do not narrate the owner's organisation as a problem.** Staff using a tool the owner is
  uneasy about, or a team that will keep one vendor alongside the new one, are facts about how
  the business runs, not friction to frame as resistance, shadow IT or a discipline issue. Write
  them as constraints plus the decision they create ("a couple of seats stay; the question is
  how many"). If a draft already reads that way, rewrite the passage — do not append a retraction
  underneath it.
- **A company that owns the building does not sell the endpoint.** The neocloud
  inside the data centre is the counterparty. Naming the landlord sends the enquiry
  to someone who will politely redirect it.
- **"Hosted in Australia" on a landing page is a claim, not a specification.** It may
  cover inference but not logging, telemetry or support access. Ask which parts of the
  request path stay in country, in writing.
- **A vendor's own tier name is not the delivered product.** Ask for the exact
  checkpoint, SKU or instance type behind the marketing label; two suppliers using the
  same label are often serving different versions.
- **Absence of a public price is not evidence of expense.** It is evidence of an
  enterprise sales motion, and the quote will come back in the same range as the
  published ones or it will not.
- **Do not let the shortlist quietly become a purchase.** Recommending a supplier is
  fine; deciding the shape of the deal is the owner's call, and presenting one option
  as settled forfeits the comparison they asked for.
- **Re-cut on correction rather than defending the list.** When the owner narrows the
  requirement, the previous recommendation goes, even if it took an hour to build.
- **Do not rule a supplier out on one landing page.** A product page describes the
  headline transaction, and a company that builds platforms often runs models or
  hosting inside them without selling either separately. Read the collateral and
  architecture sheets before telling the owner that a name they supplied is the wrong
  shape. If it turns out to be bundled, say which layer it sits at and name the missing
  number — usually the monthly cost of the bundled component — rather than dropping it.
- **Verify the counterparty, not just the brand.** A named contact may run more than one
  company, in more than one jurisdiction, under similar branding. Check which entity
  would actually contract and where it is hosted; the difference matters when the owner
  is buying sovereignty.
- **Caveats hide on the pricing page.** SLA exclusions and "not for production or
  regulated data" notes are often stated there and nowhere else. Read it properly before
  recommending a cheap option for a staff rollout.
- **A cheaper base fee is not a cheaper answer, and should not be dressed as one.** When the
  alternative wins on sticker price, concede it in the deliverable and then say what the extra
  buys — administration, one visible bill, the option to change models. Arguing the price the
  wrong way round costs credibility on every other number in the table.

## References

- `references/enquiry-template.md` — the numbered question set to adapt per category.
- `references/australian-ai-endpoints.md` — the provider map for Australian-hosted
  model endpoints, by layer, for when the buying shape is settled and the names are
  needed.
- `references/local-inference-hardware.md` — costing your own silicon: fit, decode and
  prefill arithmetic, Australian price anchors, and when buying beats metered.
