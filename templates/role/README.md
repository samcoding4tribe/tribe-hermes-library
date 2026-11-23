# Turning this into a new profile

1. Copy the folder to a role-based id: `cp -r templates/role ~/tribe-hermes-library/profiles/<role-name>`.
   The id is not the assistant's name. A person may call theirs Jarvis; the folder
   stays `assistant-<their name>`.
2. Fill the placeholders in `SOUL.md`: owner, title, profile name, date.
3. Create the profile on the machine: `hermes profile create <name>`
4. Start it and give it the facts it needs: `hermes -p <name> chat`
5. Add the credentials it needs to `~/.hermes/profiles/<name>/.env`.
5. Watch the job being done twice. Only then write the first skill, from the
   steps you actually saw, not from what the role usually involves.
7. Sync: `./scripts/sync.sh <name>`

Keep the hard rules identical across profiles. Vary the facts, the skills, the
channels and the schedule, not the guardrails.
