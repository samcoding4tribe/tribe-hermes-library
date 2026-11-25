# Interactive real-time support for TRIBE Travel consultants

Prices checked November 2026.

## 1. What exists

`TRIBE GROUP - TRIBE Travel` holds 1,112 files: 392 PDF, 112 DOCX, 95 spreadsheets, 262 JPG, 15 video. 707 are client personal files under `CLIENT INFO/`, so the working corpus is a few hundred files.

Answerable material is spread across `TRIBE TRAVEL - DOCS/`, `TRIBE TRAVEL - OFFICE/`, `Supplier - SABRE/` and `Supplier - VIRTUOSO/`, plus two undecided buckets, `XXX - KELLY to review what to keep/` (115 files) and `XXX - LUCI to review what  to keep/` (13). `WORKFLOW/`, `VIRTUOSO/` and `Checklist/2025/` are empty locally.

The real store is OneNote: `TRIBE TRAVEL - One Note - back up/` holds a 2026 export of 904 MB, and the manual sends readers there for logins, commission and the hotel program.

Read in full: `ATI BUSINESS GROUP - After Hours/Operations Manual - After Hours Emergency Assistance.docx`, the ATI ticketing instructions beside it, and `CLIENT - AFG/AFG TRIBE TRAVEL FEES 2025.pdf`. They carry Virtuoso rate codes, the preferred partner table, negotiated air and car codes, and AFG fees (domestic $89 plus 3.3 percent, after-hours $108 per call).

Hard today:

- One question needs three places: OneNote for logins and commission, the manual for rate codes, a client folder for fees. Only AFG's fee table opened; no group-wide one found.
- Competing workflows: `XXX - KELLY to review what to keep/Workflow TRIBE Travel mar 2024.xlsx` and another in `TRIBE GROUP - Share Drive/WORKFLOW/`.
- 28 quotes in `Client quotes/`, no single template; the only template file is `XXX - KELLY.../TRIBE Travel Quote Template.mht`.
- `Copy of Passwords (002).xlsx` sits in a live folder and must never be groundable.
- Only 19 of 1,112 files were readable here; the rest are online-only.

## 2. Options

- **M365 Copilot plus SharePoint agent.** AU$44.90 per user per month annual. No code; IT assigns the licence. Good citations, but it trusts whatever is in scope.
- **SharePoint agent, pay-as-you-go.** About $0.12 per question (12 messages at $0.01), no per-user licence. Needs an Azure subscription, SharePoint admin and a billing policy. Same engine, less control; plain search finds documents, not answers.
- **Copilot Studio agent.** $200 per 25,000 messages per tenant per month, or $0.01 per message. Low-code. Needs a Power Platform environment, security group and Teams admin approval. Best control of refusal and escalation.
- **Teams bot.** Azure Bot F0 free, Teams a standard channel, hosting about $25 per month. Needs a developer, an app registration and custom app upload enabled. More to break.
- **Power Apps or Power Pages.** $20 per user per month; $200 per 100 users. Wrong tool for free-text questions.
- **Local Hermes agent.** Near zero, no IT. Highest precision on five topics, one machine, no Teams presence.

All fail alike: permissions trim results silently, stale documents get cited, and models answer outside their sources unless told to refuse.

## 3. Content

Retrieval is the easy half. Over a 904 MB notebook and undated folders, it will be confidently wrong.

1. Choose five topics consultants ask about: partner rate rules, after-hours ticketing and the ATI handoff, client fees, insurance referral, cancellation and terms.
2. One page per topic in one SharePoint library: rule, exception, source, owner, review date.
3. One owner each: Kelly for supplier and hotel program, Iva for ticketing, finance for fees. Sam edits; nothing enters unreviewed.
4. Client tables (AFG's was the only one found) in a client area. Passwords, passports and `CLIENT INFO/` out.

About a day per topic plus an hour a month, my estimate, not measured.

## 4. Architectures

```
A. SharePoint "Travel Knowledge" -> SharePoint agent -> Teams, browser
```

Month one: five pages, library, billing policy, 20 tests.

```
B. SharePoint library -> Copilot Studio -> Teams app (security group)
                             |
                       cite or refuse, escalate to a named consultant
```

Month one: content, environment, refusal rule, Teams approval.

```
C. OneDrive export -> markdown corpus -> local skills -> chat on that Mac
```

Month one: clean five topics, write skills, no IT.

## 5. Recommendation

Pilot B: Copilot Studio, one consultant, five topics, four weeks. Measure correct and cited answers out of 20 weekly test questions, time to answer against today, refusal rate, and any insurance advice given, which the manual forbids.

Cheapest credible: SharePoint agent pay-as-you-go, adding no licence and no code, only a billing policy.

Recommended: Copilot Studio, because only there can you write "if it is not in these five documents, say so and name the consultant to call", which keeps a wrong fee away from a client.

## 6. Open questions

1. Which five topics, and who owns each?
2. Which fee schedule governs non-AFG clients, and where is it?
3. Is OneNote the sanctioned source, or does content move to SharePoint, maintained by whom?
4. Is there an Azure subscription, who is Global and Power Platform admin, and which Microsoft 365 licences are held?
5. Internal only, or may a consultant read an answer to a client?
6. Who approves a page change, and how often?
7. Is the pilot on Mac or Windows, and can they install software?
8. Confirm passwords, passports and `CLIENT INFO/` stay out.

Unverified: the 1,093 files that would not open; whether a Copilot licence or Azure subscription exists; Virtuoso benefits beyond the manual's rate codes; any visa or entry document, since only client visa PDFs were found.
