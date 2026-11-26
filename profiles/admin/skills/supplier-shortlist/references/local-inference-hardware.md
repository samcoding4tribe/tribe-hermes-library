# Costing local inference hardware (Australian market)

For when the owner asks "what would it cost to just buy the boxes and run the models
ourselves". Answer with arithmetic, not a shopping list: whether a model fits, how fast it
decodes, whether it can serve the measured volume, and what that costs against the metered
bill. Most "we should buy a GPU" conversations end at step 3.

Re-check every price before quoting it. Figures below are anchors with the date they were
read, not a price list.

**Model generations move as fast as prices.** Open-weight families iterate every few months and
parameter counts change with them, so a table built from a generation you remembered is wrong by
the time it is read. Take the owner's generation if they name one, say which generation each row
assumes, and when you have not checked that generation's actual size and benchmarks, label the
figures as memory arithmetic at an assumed parameter count rather than measured performance.

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

**Pooling two machines into one model does work now, and the toolchain is the price.** RDMA over
Thunderbolt 5 (macOS 26.2 and later, on machines with TB5 ports), MLX's JACCL backend and exo all
let two to four Apple machines present their unified memory as one pool, with aggregate bandwidth
scaling close to linearly — Apple's own research ran an ~800B model across four M5 Ultras at over
30 tok/s. So do not tell the owner a cluster is impossible or that the link is a narrow pipe; that
was true of plain IP-over-Thunderbolt, not of RDMA.

The costs that remain, and the ones to quote: the pooling path is MLX or exo, not Ollama or
llama.cpp, so the serving stack has to be chosen for it; every node must run the same OS version
and be cabled properly; and a model that fits on one node gains nothing from the second. Price it
per configuration (2×, 3×, 4× nodes) against a single large-memory machine, and add the operational
count — machines, power bricks, and who keeps them in step.

**A cluster of purpose-built boxes is a slightly different case** and works for models around
300–400B because the vendor provisions the fabric. Same caveats: aggregated bandwidth does not
scale identically to memory, so four nodes are not four times one node on decode, and clustering
does not fix a low tensor-throughput machine's prefill on long agent contexts.

## 7. Serving several conversations at once

For an agentic setup, "does the model fit" is the wrong question — the constraint is how many
concurrent contexts stay resident. Weights take a fixed slice; the rest is KV cache per session:

```
resident sessions ≈ (memory − weights − ~4GB runtime) ÷ (context_k × KV per 1k tokens)
KV per 1k tokens ≈ 0.26GB for a 32B-class dense model at fp16 cache (halve it at fp8)
```

A 32B model at FP8 is ~34GB of weights, so 48GB leaves ~5 sessions at 8k context and one at 32k;
64GB leaves ~12 and three; 96GB leaves ~28 and seven. Quote the table rather than the total
memory, because the second and third agents are what the owner is actually buying the headroom for.

**Which model shape decides whether a low-bandwidth box is usable at all.** Dense 27–32B at FP8
decodes around 3–4 tok/s on a ~300GB/s machine and 7–9 on a ~600GB/s one, which is the difference
between unusable and tolerable in an agent loop. A MoE with ~3B active decodes at 35–40 and 70–80
tok/s on the same two boxes, where the bandwidth difference stops mattering. Ask which checkpoint
they intend to run before recommending either.
