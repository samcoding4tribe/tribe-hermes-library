# Costing local inference hardware (Australian market)

For when the owner asks "what would it cost to just buy the boxes and run the models
ourselves". Answer with arithmetic, not a shopping list: whether a model fits, how fast it
decodes, whether it can serve the measured volume, and what that costs against the metered
bill. Most "we should buy a GPU" conversations end at step 3.

Re-check every price before quoting it. Figures below are anchors with the date they were
read, not a price list.

## 1. Does the model fit

```
FP8 weights GB  ≈ total parameters (B) × 1.05
4-bit weights GB ≈ total parameters (B) × 0.55
```

Add room for KV cache and activations — 20–30% of the weight figure for a working context,
more for long context. Unified-memory machines (Apple, GB10 boxes) mean weights and KV share
one pool, so headroom is headroom.

Fit is set by **total** parameters, not active ones: a 284B Mixture-of-Experts model at FP8
is ~298GB even though only ~13B fire per token.

| Model class | FP8 | 4-bit | Fits a 128GB box? |
|---|---|---|---|
| Dense 70B | ~74GB | ~38GB | yes |
| MoE 125B (6B active) | ~131GB | ~69GB | 4-bit only |
| MoE 284B (13B active) | ~298GB | ~156GB | no — 2 boxes at 4-bit, 3 at FP8 |
| MoE 320B (18B active) | ~336GB | ~176GB | no |
| MoE ~1T | ~1,050GB | ~550GB | no |

## 2. How fast it decodes

Decode is memory-bandwidth bound, not compute bound:

```
ceiling tok/s  ≈ memory bandwidth (GB/s) ÷ (active parameters (B) × bytes per weight)
realistic      ≈ 40% of that
```

Worked example, 284B MoE with 13B active at FP8 (≈13.7GB moved per token): a 273GB/s box
ceils near 20 tok/s and behaves like 8; a 1.2TB/s box ceils near 88 and behaves like 35.

## 3. Can it serve the measured volume

Agentic work is input-heavy, so **prefill** decides whether one box can carry a team:

```
hours per day of prefill = daily input tokens ÷ prefill tok/s ÷ 3600
```

At 200M input tokens a day, a box at 1,375–3,072 tok/s prefill needs 18–40 hours a day, and
a high-bandwidth workstation GPU still needs ~5. Run this before recommending any purchase —
it usually reframes the question from "buy one box" to "buy one box for one person".

## 4. Price anchors, Australia

Read November 2026; ranges reflect multiple retailers on the same date. Treat as a scale, not
a quote.

| Class | Memory / bandwidth | A$ incl GST |
|---|---|---|
| GB10 desktop, budget (Corsair WS300 class) | 128GB unified / ~273GB/s | ~7,000 |
| DGX Spark Founders, MSI EdgeXpert (GB10) | 128GB / ~273GB/s | ~9,000–9,700 |
| ASUS Ascent GX10 (same GB10 chip, own chassis) | 128GB / ~273GB/s | ~11,000–14,000 |
| Workstation GPU, RTX PRO 6000 class | 96GB GDDR7 / ~1,790GB/s | ~20,000–32,000 (volatile) |
| Apple Mac Studio, top unified config | 512GB unified / ~1.2TB/s | ~34,000 |

- GB10 boxes: the model number matters less than the chip, but chassis and support differ —
  the same superchip spans a 2x price range across brands and storage tiers.
- The 512GB Apple box is the only single machine that holds a ~300GB model at FP8 with room
  for context, and its weakness is prefill: unified memory bandwidth is high, tensor throughput
  is not.
- Workstation-GPU pricing moves weekly; a tracker's "12-month low" is not a current quote.

**When the owner's remembered price is much higher than yours, they are usually thinking of a
different product in the same family.** DGX-branded hardware spans a desktop superchip, rebranded
chassis from other vendors, and a full rack station at ten times the price; a round-up table from
months ago will also show launch pricing. Name the product they are picturing, give its price, and
say which one your figure refers to — do not simply repeat the lower number as if it settled the
point.

## 5. When buying beats metered, and when it does not

Buy only when all three hold: the model fits one box, one user's interactive speed is enough,
and the annual metered bill at measured volume exceeds the hardware inside a plausible life.

- One box serves **one person at a time**. A team workload needs throughput, which is exactly
  what a metered endpoint sells.
- Hardware is a capex with an owner: updates, backups, driver and model-version churn land on
  whoever runs it. Name that person before proposing the purchase.
- Self-hosting does not fix data residency on its own — the endpoint behind the model can still
  be offshore.
- Compare at **total system price for the models actually wanted**, not per-box price: quote
  "2 boxes for this model / 4 for that one / one big unified box instead", and express each total as
a multiple of the annual metered bill. A per-box table invites the owner to multiply it wrong.

## 6. Choosing the config, including discounted purchasing

**When two configs have the same memory, the bandwidth decides.** A compact desktop at 64GB and
~300GB/s and a base studio at 64GB and ~600GB/s differ by a few hundred dollars and by roughly
2x on every token generated for the life of the machine. Never trade bandwidth for storage; an
external drive is cheap forever, and the owner feels the bandwidth difference on the first long
prompt.

**Apply any staff, partner or education discount to list price and compare the after-discount
totals**, but check the eligibility first: institutional discounts commonly cover standard
configurations only, not built-to-order memory upgrades. If the discount will not extend to the
larger unified-memory tier, the upgraded machine silently reverts to full price and the
recommendation changes — say so before the owner orders, not after.

**Two linked small machines are not one large machine.** A consumer interconnect between desktop
boxes runs at roughly an order of magnitude less bandwidth than the memory inside each box
(~10GB/s link against 300–600GB/s unified memory). Splitting a model across that link makes every
token wait on the pipe, so it suits two people running two independent models, or batch work that
tolerates latency — not one person's interactive session. Quote the aggregate memory, then explain
why the aggregate is not real: the arithmetic, not a verdict on the vendor's software.

**A cluster of purpose-built boxes is a different case** and does work for models around 300–400B
because the vendor provisions the fabric. Say that plainly while keeping the caveat: aggregated
bandwidth does not scale like memory, so four nodes are not four times one node on decode, and no
amount of clustering fixes a low tensor-throughput machine's prefill on long agent contexts.
