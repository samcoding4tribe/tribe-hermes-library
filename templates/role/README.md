# Turning this into a new profile

1. Copy the folder to a role-based id:
   `cp -r templates/role ~/tribe-hermes-library/profiles/<role-name>`. The id is
   not the assistant's name. A person may call theirs Jarvis; the folder stays
   `assistant-<their name>`.
2. Fill the placeholders in `SOUL.md`: owner, title, profile name, date.
3. Create the profile on the machine: `hermes profile create <name>`
4. Add the credentials it needs to `~/.hermes/profiles/<name>/.env`.
5. Start it and give it the facts it needs: `hermes -p <name> chat`. Use the org
   chart for the reporting lines, taking the person's id rather than a typed title.
6. Watch the job being done twice. Write the steps in `workspace/procedures.md`
   first, then promote them to a skill once they hold. See `docs/profile-notes.md`.
7. Sync: `python3 scripts/hermes_files.py sync`

Keep the hard rules identical across profiles. Vary the facts, the skills, the
channels and the schedule, not the guardrails.
