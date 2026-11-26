# Turning this into a new profile

This folder is the blank soul for a role that neither baseline fits. For anybody else, install
`profiles/admin` instead — the route table is `config/routing.json`.

The procedure is the interview kit: `docs/profiles/interview/README.md`. It holds the order, the
name rule, the questions, and the four artefacts a setup must produce. This file covers only the
mechanics that are not part of that conversation, so the two cannot drift apart.

1. Copy this folder to a role-based id: `cp -r templates/role profiles/<role-name>`. The id is
   the role, never the assistant's name and never the person's (D22). A person may call theirs
   Jarvis; the folder stays something like `assistant-coordinator`.
2. Fill the placeholders in `SOUL.md`: owner, title, profile name, date.
3. Create the profile on the machine and give it its credentials:
   `hermes profile create <name>`, then the keys it needs in
   `~/.hermes/profiles/<name>/.env`.
4. Set the model explicitly, then prove it answers before handing it over.
5. Publish: `python3 scripts/hermes_files.py sync`.

Notes about the work itself — what goes in `workspace/procedures.md`, when a procedure becomes a
skill — are in `docs/profile-notes.md`. The organisation's reporting lines are in the org chart,
`templates/org/people.json`; take the person's id from there rather than a typed job title.

Keep the hard rules identical across profiles. Vary the facts, the skills, the channels and the
schedule, not the guardrails.
