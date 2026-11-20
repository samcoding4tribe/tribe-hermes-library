# Hermes at work: an executive assistant, then a template

Living document. We edit it in chat; every version stays on this Mac.

Last edited: 20 November 2026, by Hermes
Machine: this Mac (macOS, Apple silicon)
Author's context: testing a rollout to workmates before proposing it to the organisation

---

## 1. What exists right now

| Thing | State |
|---|---|
| Hermes version | v0.23.2, stable |
| Default profile | `default`, model deepseek-flash |
| New profile | `ea` at `~/.hermes/profiles/ea`, shell command `ea` |
| EA model | deepseek-flash via the DeepSeek key, set after the clone inherited a broken Anthropic model |
| EA persona | `~/.hermes/profiles/ea/SOUL.md` (drafts only, cite sources, protect time) |
| EA skills | 44, cloned from default; none written for the assistant role yet |
| Private backup | `OneDrive/TRIBE GROUP - samuelkn/Hermes`, text plus database snapshots |
| Shared library | `OneDrive/TRIBE GROUP - TRIBE Group Tech/Hermes`, templates and published copies |
| Repo | `~/hermes-agents`, local git only, no remote yet |
| Connectors | none |
| Scheduled jobs | none |
| Messaging channels | none; the gateway is running and multiplexed |

The Mac itself cannot sign into the Microsoft account through the native apps, so Outlook and Teams are used in the browser. That is a separate problem from Hermes and it shapes route 1 below.

---

## 2. Three routes into the Microsoft stack

### Route 1: the browser, this week, no permissions

A persistent browser session. Sam signs into `outlook.office.com` and `teams.microsoft.com` once. The password goes through the credential vault and never enters the conversation. Hermes then reads the inbox, pulls the calendar, drafts replies, and posts in Teams when asked.

- Cost: minutes
- Approval needed: none
- Limits: only works while the browser session lives; slower than an API; nothing runs unattended at 07:00
- Good for: proving the assistant is useful before asking IT for anything

### Route 2: Teams as a real channel

A bot the manager messages like a colleague. Direct messages always get an answer; channels and group chats need an @mention.

```bash
npm install -g @microsoft/teams.cli@preview
teams login
teams status --verbose          # gives your AAD object id for the allowlist
devtunnel create hermes-bot --allow-anonymous
devtunnel port create hermes-bot -p 3978 --protocol http
devtunnel host hermes-bot       # keep this running
teams app create --name "Hermes EA" --endpoint "https://<tunnel>/api/messages"
```

Then in `~/.hermes/.env`: `TEAMS_CLIENT_ID`, `TEAMS_CLIENT_SECRET`, `TEAMS_TENANT_ID`, and `TEAMS_ALLOWED_USERS` with the manager's AAD object id. Start with `hermes gateway setup` and pick Microsoft Teams, which walks the same steps.

- Cost: an afternoon
- Approval needed: someone in the tenant must allow the app install; a public HTTPS endpoint must exist (a tunnel is fine for a pilot, not for production)
- Limits: no voice; files and images are partial
- Good for: the manager talking to the assistant where they already work

### Route 3: Microsoft Graph, for mail and calendar in the background

App-only credentials, so the assistant can read the manager's mail and calendar on a schedule without a browser open.

1. `entra.microsoft.com` → App registrations → New registration, single tenant, no redirect URI.
2. Certificates and secrets → new client secret, copy the **Value**.
3. API permissions → Microsoft Graph → Application permissions: `Mail.Read`, `Calendars.Read`, `OnlineMeetings.Read.All`, `OnlineMeetingTranscript.Read.All`. Grant admin consent.
4. Scope it with an Application Access Policy so it reads only the manager's mailbox, not the tenant's.
5. Put `MSGRAPH_TENANT_ID`, `MSGRAPH_CLIENT_ID`, `MSGRAPH_CLIENT_SECRET` in `~/.hermes/.env`, `chmod 600`.

- Cost: a day, plus an admin
- Approval needed: tenant admin for consent and for the access policy
- Limits: Hermes ships this credential path for the Teams meeting pipeline. Reading mail on a schedule needs a small connector built on the same credentials. That connector is work we do once and reuse for every profile.
- Good for: the version that is actually an executive assistant

Recommended order: route 1 now, route 2 for the pilot, route 3 once the manager wants it running before they wake up.

---

## 3. Anatomy of a useful EA profile

A profile, not a personality. It has its own config, memory, skills, sessions and model, so the manager's context never mixes with anyone else's.

| Layer | What goes in it | Why |
|---|---|---|
| `SOUL.md` | Role, voice, hard rules: draft, never send; cite; protect time | Sets behaviour the model cannot drift from quietly |
| Memory | Who the manager is, who they answer to, this quarter's priorities, standing rules | Loaded every chat, so keep it to a page |
| Skills | Inbox triage, meeting prep, weekly review, travel or expense routines | Procedures, loaded only when the topic comes up |
| Cron | 07:30 brief, Friday wrap, meeting follow-ups | The part that earns the word assistant |
| Channels | Teams bot (route 2), or email replies | Where the manager already is |
| Guardrails | Drafts only, approval mode manual for sending, allowlist of addresses and people | The difference between helpful and dangerous |

Open questions for the manager: what time the brief lands, which senders are always urgent, who they never want to miss, what they want to see first when travelling.

---

## 4. Replicating across the organisation

The unit of replication is a profile, and a profile can be exported as one file.

```bash
hermes profile export ea -o ea-template.tar.gz
hermes profile install ./ea-template.tar.gz --name ea-marketing
```

What to parameterise per person, rather than copy:

1. Name, role, manager, timezone, working hours
2. Model and key, if departments differ
3. Channel identity: bot token, allowlist of who may talk to it
4. Cron times and delivery target
5. Data scope: which mailboxes, which folders, which drives
6. Guardrails: send or draft only, approval mode, which addresses are off limits

What to keep identical, so that rollouts behave the same everywhere:

- The persona skeleton and the hard rules
- The skill set for the role
- The shape of the brief
- The approval policy

Two things to settle before a wide rollout: one shared bot with an allowlist, or one bot per assistant (cleaner isolation, more tenant apps to manage); and where profiles live, since a profile on a laptop stops working when the laptop closes and a small always-on box or server does not.

---

## 5. Decisions still open

- [ ] Route 1 trial: which Outlook and Teams account signs in first
- [ ] Does the manager want a Teams bot, or email only
- [ ] 07:30 brief: is that the right hour, and is Teams the right place
- [ ] Who in IT can grant Graph consent when route 3 arrives
- [ ] Shared bot or one per person
- [ ] Does the pilot live on this Mac or on a small always-on machine
- [ ] Credentials: vault, encrypted archive, or re-enter by hand (security session first)
- [ ] Remote repo: create it, then push, before trusting the local one
- [ ] Backup schedule: what runs when, and where failure is reported

---

## Changelog

- 20 Nov 2026: first draft. Profile `ea` created, model corrected to deepseek-flash, persona written.
