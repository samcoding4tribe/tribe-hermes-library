# Supplier knowledge for agents: what to build it on

27 November 2026. Research note. No decision taken, nothing built. Companion to
`events-suppliers-phase1.md` (the list itself) and to the vault note *Shared preferred supplier
record, maintained by the assistants* (the relationship layer).

The ambition is bigger than a tidy list: one place an agent can query to help design an event,
draft a proposal and build a budget, without a person assembling the facts first. That changes the
requirements. A list a human reads can live in a spreadsheet; a list an agent reasons over needs
stable identity, typed values, provenance, recency and an access path that does not require
someone logged in.

## 1. What "AI-ready" has to mean, concretely

Six properties, each of which the 2025 sheet fails today and the phase-one list supplies:

| Property | Why the agent needs it | Today |
|---|---|---|
| Stable ID per supplier | Every reference from a proposal, an event or a rate row points at something that does not change when the name is corrected | None; identity is a string in column A |
| Typed, closed values | "Melbourne", "melb" and "VIC" are three regions to a model, one to a person | 26 raw STATE strings |
| Provenance | The agent must be able to say where a fact came from and when | Nothing traced to a source cell |
| Recency | A supplier record with no date is a rumour | No dates anywhere, except free text in Notes |
| Relationships as fields, not prose | "which hotels in Queenstown do we use" is a join, not a search | Chain, country and city are sheet names and one column each |
| A machine access path | An agent cannot open a browser session for each question | Files on a synced OneDrive folder only |

The last one is the whole design problem. The first five are phase one's job.

## 2. The realistic options, in this estate

The constraint that decides most of this: TRIBE is a Windows estate with two or three Macs, Hermes
runs on the Macs as ordinary user accounts, and nobody has confirmed who holds Global Administrator
or what licences are held. Anything needing tenant-wide admin consent is a project with another
team in it; anything needing only the synced folder works this week.

**A. SharePoint list + library as the system of record, read by agents through Work IQ MCP.**
Work IQ is Microsoft's agent layer over Microsoft 365, and its MCP endpoint
(`https://workiq.svc.cloud.microsoft/mcp`) is now the supported way for a non-Microsoft agent to
work with SharePoint. SharePoint tools in Work IQ entered public preview on 3 November 2026 with
more than 60 native operations — discover lists and their schemas, query large lists including in
natural language, add and update items, read file and folder metadata — and Microsoft's own
comparison against calling Graph directly claims a success-rate lift of up to 77% depending on
task, with 16% fewer tokens in their evals. Two new least-privilege scopes, `WorkIQ.Read` and
`WorkIQ.Act`, exist precisely for this. Every call runs as the signed-in user, so an agent sees
only what that colleague can already see. Hermes supports it directly: `hermes mcp add` takes a
remote OAuth server, and the config already anticipates MCP result spillover.

What it costs: an admin has to enable Work IQ in the tenant, consent to the app, and allow the
SharePoint paths in tenant policy; billing is usage-based through Copilot Credits, which is
independent of Microsoft 365 Copilot licensing for a custom application, but needs a billing
method and a spending policy. The permission set Work IQ asks for at the app level is broad —
`Sites.Read.All`, `Mail.Read`, `People.Read.All`, `Chat.Read`, `ChannelMessage.Read.All`,
`OnlineMeetingTranscript.Read.All`, `ExternalItem.Read.All` — because it is the Copilot Chat API
underneath. That is a conversation with whoever runs the tenant, not a switch.

**B. The same record, exported nightly to JSON, read from the synced folder.**
A flow writes the list to `suppliers.json` (plus a flat CSV for spreadsheets) in a folder OneDrive
already syncs. An agent reads a local file with the tools it already has: no admin, no billing, no
new permission model, and it inherits the estate's existing idiom — the backup job and the library
sync already work this way. What it gives up: it is a day stale, it carries no per-record
permissions (whoever can read the folder reads every field, including rates), and every agent
needs the file re-read on each session rather than a live query. At 176 suppliers the whole record
is a few tens of kilobytes, so staleness and size are the only real costs.

**C. Copilot in SharePoint / a SharePoint agent on the site.**
Microsoft shipped Copilot in SharePoint to general availability in September 2026, and a SharePoint
agent answers questions over the site's lists and libraries with citations, no build and no code.
Cheapest credible route for *people* asking "who do we use for AV in Brisbane". It is not a
knowledge base for Hermes: the answers arrive in SharePoint, not in the agent's context, and the
quality depends on the site being tidy — which is the same work as phase one.

**D. A bespoke vector store or RAG pipeline (Azure AI Search, embeddings, a chunking job).**
The reflex answer, and the wrong first move here. 445 supplier files and 176 rows is not a corpus
that needs approximate retrieval; it needs a schema and a filter. A vector store also creates a
second permission model that has to be kept in step with SharePoint forever, which is the failure
mode that makes people distrust the KB. Microsoft's own guidance now points the other way: the
Retrieval API and Foundry knowledge sources exist so you do not stand up a parallel index. Revisit
only if the document library grows past a few thousand files with genuinely unstructured content.

**E. Dataverse, with its own MCP server, as the relational model.**
A proper relational store with relationships, and an MCP server so agents can call it. It also
means a new platform, a Power Platform licence, and a fourth place where supplier data lives, next
to EventsAir and the SharePoint list. Only defensible if the whole events system moves to the Power
Platform, which is not on the table.

## 3. The knowledge-graph question

A graph is worth its cost when the questions are about *paths between things* — which supplier
worked which client's event, at which venue, at what price, through which relationship holder — and
when those paths are deep or frequently changing. Two facts decide it here:

- The supplier side of that graph is 176 nodes and four or five relations. A graph database is not
  the constraint; the missing data is.
- The event, client and budget side of the graph is not in the supplier files at all. It lives in
  EventsAir (`Share Drive/SYSTEMS/EventsAIR/` confirms it is in use), alongside Sabre for travel
  and Xero for finance. A graph built only from the supplier folder would answer "who do we use"
  and nothing about "what did this cost last time".

So the recommendation is to build the graph's *shape* without a graph server: a canonical
`supplier_id`, lookup columns for category, region and relationship holder, and a nightly export
that carries both a flat table and a small edge list (supplier→category, supplier→region,
supplier→owner, supplier→document). An agent can reason over that directly, and joining it to
EventsAir later is a key match rather than a migration. A real triple store or graph database only
becomes right if cross-entity questions become routine and EventsAir's own reporting cannot answer
them — which is a question about EventsAir, not about SharePoint.

## 4. Recommended sequence

1. **Build the phase-one list**, as proposed. It is the schema, and every option below consumes it.
   Nothing in this note changes that work.
2. **Add the export.** Nightly JSON plus CSV into a synced folder under `TRIBE Group Tech`, written
   by the same kind of job that already backs up the estate. Agents read the file. This is the
   access path that exists on the day the list is finished, needs no admin, and costs nothing per
   query. Days, not weeks.
3. **Ask the three tenant questions** that gate everything better: who is Global Administrator,
   which Microsoft 365 licences are held, and whether a Copilot Credits billing method with a
   spending cap can be set. The answers decide whether Work IQ MCP replaces the export or sits
   beside it.
4. **Turn on Work IQ MCP for one agent first** (the builder, or the events profile) with
   `WorkIQ.Read` only, scoped by tenant policy to the Tech site. Read-only until the record has
   proven itself. Keep the export as the fallback so nothing depends on a preview endpoint.
5. **Retrieval over the documents** — contracts, capability decks, menus, certificates — starts as
   a SharePoint agent, not a pipeline. If the 368 confidentiality files and 97 supplier agreements
   need to be searchable by an agent, that is a library problem: content types and columns first,
   retrieval second.
6. **Join to EventsAir** for budget and history questions, which is a separate thread with its own
   access question: whether EventsAir exports or has an API available on the current plan is
   UNKNOWN.

## 5. What each option needs from IT

| Option | Admin consent | Licence or billing | Build effort | Agent access |
|---|---|---|---|---|
| A. Work IQ MCP | Global Administrator to enable Work IQ, consent the app, set tenant policy | Copilot Credits, usage-based, spending policy | Days, once unblocked | Live, delegated, per-user |
| B. Nightly export | None beyond folder permissions | None | Hours | File read, day-stale |
| C. SharePoint agent | SharePoint admin to create it | Included in SharePoint, or Copilot seats for Copilot in SharePoint | Hours | In SharePoint only, not in Hermes |
| D. Custom RAG | Azure subscription, index permissions | Azure AI Search | Weeks | Live, second permission model |
| E. Dataverse | Power Platform admin | Per-user or per-app | Weeks | Live via MCP, new system of record |

## 6. What is UNKNOWN, and how it gets confirmed

- **Who is Global Administrator / who can consent.** Ask Kate or whoever owns the Microsoft
  account. `docs/rollout.md` already lists this as an open item for the Graph route; the same person
  answers this one.
- **The Microsoft 365 plan and whether Copilot seats exist.** Ask for the licence list from the
  admin centre. Nothing above can be priced without it.
- **Whether a Copilot Credits billing method can be set with a monthly cap.** Admin centre →
  Copilot → Cost Management; needs Global or Billing Administrator.
- **Whether EventsAir exports or has an API on the current plan.** Ask TRIBE's EventsAir account
  manager, or look for an export in `SYSTEMS/EventsAIR/` — only two files there today, a video and
  a tips document.
- **Who may see rates.** Unchanged from the phase-one proposal and still the decision that most
  affects whether option B is viable at all: a synced file has no field-level permissions.

## Sources

- Microsoft Tech Community, *Introducing SharePoint tools in Work IQ*, 3 November 2026 —
  https://techcommunity.microsoft.com/blog/spblog/introducing-sharepoint-tools-in-work-iq/4569917
- Microsoft Learn, *Understand MCP server options in Agent 365*, updated 19 November 2026 —
  https://learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview
- Microsoft Learn, *Connect agents to Microsoft 365 with Work IQ (preview)* (billing, consent,
  endpoint) —
  https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/work-iq
- Microsoft Learn, *Work IQ API permissions reference* (`WorkIQ.Read`, admin consent), updated
  30 October 2026 — https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/permissions
- Microsoft 365 Developer Blog, *Build AI-powered apps without creating a vector database*,
  13 October 2026 —
  https://devblogs.microsoft.com/microsoft365dev/build-ai-powered-apps-without-creating-a-vector-database/
- Estate facts measured 27 November 2026: `SUPPLIERS/` 445 files (0 dataless), 176 name rows, 165
  distinct suppliers, 14 category sheets, 26 raw STATE values; `EVENTS CLIENTS/` 97 supplier
  agreement files, 368 confidentiality files, 61 contracts folders; `SYSTEMS/EventsAIR/` present.
- `hermes mcp add` supports a remote OAuth MCP server (checked on this machine, 27 November 2026).
