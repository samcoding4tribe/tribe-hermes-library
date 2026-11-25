# To do

Recorded 20 November 2026. Delete a line when it is done, and say why in the commit.

## Next session

- [x] **Create the remote repo.** `tribe-hermes-library`, private, pushed on
      every sync.
- [ ] **Credentials decision.** Left out of the backup for now. Needs a session
      on secure storage before any bot token exists: a vault Hermes reads from,
      or an age-encrypted archive, or re-entering by hand on restore.
- [ ] **Run the restore test.** Install `ea` from the shared library onto a
      clean home directory and confirm it starts and remembers. A backup that
      has never been restored is a guess.

## Profiles and skills

- [ ] **Relationship and alignment skill.** Not the setup interview: the ongoing habit of
      checking that the assistant still works the way the person wants. Three jobs. Ask a
      question from the setup interview again, at random, to confirm the answer still holds.
      Notice when a change (role, team, supplier, system) means something recorded earlier is
      now wrong. Push a corrected fact to the places it is reflected, so the person is not
      asked twice and two records do not disagree.
      The distinction that matters: this is about **on-device personalisation** — the settings
      and context that belong to one person on one machine — not the general role profile used
      to stand a new one up. A change in the general profile is a deployment decision; a change
      in personalisation is theirs, and should be applied without a rebuild.



- [ ] **Travel and expenses skill.** Claims, bookings, approvals and thresholds, run when
      the first real claim or booking appears rather than during setup. Deliberately not
      built yet: people should see the assistant working before they are asked for paperwork
      preferences. The interview block was removed on 25 Nov 2026 and points here instead.

## Done

- [x] **Memories out of git.** `sync.sh` no longer commits `memories/`, and the
      old copy was removed. Memories live only in the private OneDrive backup.
- [x] **Library named.** Shared folder is now `TRIBE Group Tech/Hermes Library`.
- [x] **Schedule the backup.** Hermes job `Hermes backup`, daily at 17:00,
      runs `scripts/nightly.sh` with no model involved. A launchd agent was
      tried first and failed: macOS blocks rsync writing into OneDrive from a
      launchd context, so the job runs from the scheduler instead.

- [ ] **Run the whole flow on one Windows machine.** The Python implementation has
      only been exercised on this Mac so far: backup, publish, push, and the
      scheduled run.
- [ ] **Set edit permissions on `Hermes Library/templates/org`.** Leon, Kelly,
      Jodie and Vanessa edit; everyone else reads. Needs whoever administers the
      SharePoint library, since git cannot express it.
- [ ] **Write the collision procedure.** How a published profile is merged onto
      a machine that already has one, what wins when both changed, and how a new
      assistant is assembled from a template without copying a stranger's memory.
- [ ] **Central backup, when the first manager's assistant goes live.** A
      copy that survives the owner's account being deprovisioned. Access for two
      named people, database snapshots encrypted. Not before, since it puts
      conversations in a shared place.

- [ ] **Restrict `Hermes Backups` to owner plus one IT person.** It now sits in
      the Tech library, so anyone with library access can read memories unless
      the folder permissions say otherwise.

## Later

- [ ] Add `age` and encrypt `.env` plus `auth.json` into the private backup.
- [ ] Add the check on push: secret scan, unfilled placeholders, skills parse,
      clean install.
- [ ] Decide the OneDrive library owner, so two people do not edit at once.
- [ ] Container isolation for role profiles: `terminal.backend: docker` with
      Docker Desktop or Colima, neither installed yet. Worth doing before an
      assistant is handed to someone else, not for the single-machine pilot.
- [ ] Give each role profile only the toolsets it needs, instead of the default
      set. `hermes tools` per profile.

## Waiting on other people

- [ ] Tenant permission to install the Teams bot.
- [ ] Who in IT can grant Graph consent, when route 3 arrives.

## Projects opened 25 November 2026

- [ ] Fix OneDrive placeholder hydration on this Mac: right-click `SUPPLIERS` and
      `TRIBE Travel` in Finder, choose Always keep on this device, then prove one file
      opens. Until then no content migration can be done from this machine.
- [ ] Events supplier knowledge base: agree the owner, the tier definition and whether
      rates are visible to all events staff, then build phase one.
- [ ] Travel support pilot: choose the five topics and their owners, confirm whether an
      Azure subscription and Copilot licensing exist.
- [ ] Move `Copy of Passwords (002).xlsx` out of the live travel folder into a password
      manager and delete the file.
