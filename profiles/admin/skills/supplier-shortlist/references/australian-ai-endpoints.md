# Australian-hosted model endpoints, by layer

The buying shape decides which of these layers matters. Keep the layers distinct in
any shortlist: they are different counterparties, different contracts and different
price mechanics. Verify current products and prices on each supplier's own pages before
quoting them — this is a map of the market, not a price list. Names below were checked
once and will drift; treat every one as a lead to re-verify, not a recommendation.

## Layer 1 — managed shared endpoints (per token, no infrastructure)

The usual answer for an SME: someone else hosts the open-weight model, you call an
OpenAI-compatible API, and you pay per million tokens. No capacity planning, and the
supplier owns upgrades.

Operators seen in this layer in Australia:

- **Xinference** — hosted in Australia, OpenAI-compatible, publishes per-token rates in
  USD and will invoice in AUD. Publishes a claim of being materially cheaper than the same
  open model on a hyperscaler's Sydney region; treat that as a hypothesis to test with the
  owner's own prompts.
- **AI Compute Australia** — inference API served from NSW, zero prompt retention, AUD
  billing, own hardware assembled locally; appliance and workspace tiers alongside the API.
  Its pricing page states no SLA and that the API is not for regulated or production data —
  fine for a trial, not for a staff rollout without a contract conversation.
- **Amaze** — sovereign multimodel inferencing from Sydney and Melbourne, a large
  open-weight catalogue, zero retention, ISO 27001, AUD. Endpoint tier is quote-only while
  GPU capacity is priced publicly.
- **ToothFairyAI** — regional OpenAI-compatible endpoints with published per-region rates
  and zero retention; self-serve, no seats.
- **ResetData** — managed platform on sovereign GPUs, OpenAI-compatible, quote only.

Hyperscaler regions are the benchmark rather than the shortlist: an offshore provider's
Australian region serves open weights with public per-token pricing and a data-processing
agreement, which makes it the number every sovereign quote has to beat. Bedrock's Sydney
region serves open-weight models through an OpenAI-compatible endpoint; confirm the specific
model and region before counting it in scope.

## Layer 1b — models bundled inside a platform you already run

A growing shape that is easy to mistake for Layer 1: a vendor builds apps, agents or
software factories inside the customer's own cloud tenant and runs the model in there with
them ("on your Azure, on your soil"). Sovereignty is real, the model genuinely runs on the
customer's soil, and it is still not a bare endpoint — you are buying the platform and the
model arrives inside it. Price the bundled model as a separate line, ask what it costs per
month on its own, and do not drop the vendor for "not selling hosting" until the collateral
and architecture sheets have been read.

## Layer 2 — neoclouds and GPU-as-a-service (per GPU-month, you run the model)

Neoclouds rent GPUs inside someone else's data centre and leave you running vLLM or
similar. Dedicated, single tenant, priced per GPU-hour or per GPU-month, with a
monthly minimum. This is the right layer only when volume is high and steady, or the
workload needs a checkpoint nobody hosts.

These are the companies customers mistake for the data-centre operator. They are not:
the operator owns the building, certifies it (Tier ratings, hosting-framework status)
and sells power, cooling and interconnection; the neocloud sells compute on top. A
provider that advertises Tier IV facilities and Certified Strategic status is usually the
neocloud tenant, not the landlord.

A single-GPU list price is the fastest reality check on any dedicated option: one modern
accelerator at list runs to five figures a year, which is the number a per-token quote has
to be measured against.

## Layer 3 — colocation and sovereign cloud (build it yourself)

Facility and private-cloud providers for organisations that must run their own stack,
usually because of a regulated workload, an accreditation the public layers cannot meet,
or a group policy that forbids managed inference. Heaviest compliance envelope, longest
contract, and the wrong answer for a first deployment.

## Layer 4 — turnkey workspaces (per seat)

"Give the team a private ChatGPT" is a different purchase: a seat-based workspace with
chat, documents and shared assistants, usually with an API bolted on. Cheap and fast to
roll out, and not comparable with an endpoint for agents. Do not put the two in the same
table without saying so. Several Layer 1 operators also sell this tier alongside their API,
which is a convenience for staff and not a substitute for an endpoint.

## Questions that separate the layers quickly

- "Is the model hosted by you, or do we run it on your GPUs?" — Layer 1 or Layer 2.
- "Do you own the data centre?" — separates the operator from the neocloud.
- "Per token or per GPU-month?" — the whole pricing model in one answer.
- "Can we bring our own checkpoint?" — Layer 1 cannot, Layer 2 and 3 can, Layer 1b depends.
- "Who decides when the model version changes?" — managed means they do, and it
  matters more than the price difference when an agent depends on behaviour.
- "Where does the model actually run when we buy your platform?" — the Layer 1b question.

## Naming caution on open-weight models

A vendor's hosted model name (a "flash" or "mini" tier) usually does not map one-to-one
onto an open checkpoint, and different suppliers serving the same label can be on
different checkpoints. Ask which checkpoint is behind the name, and check that model's
licence before committing — some open-weight licences carry use restrictions that matter
to a commercial deployment.

## Counterparty caution

A founder or contact may operate more than one company, in more than one jurisdiction,
under similar branding — an Australian endpoint business and an offshore or "decentralised"
inference service are not interchangeable when the reason for buying is data residency.
Establish which entity would contract and where inference runs before the enquiry goes out.
