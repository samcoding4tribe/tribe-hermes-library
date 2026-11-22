# To do

Recorded 20 November 2026. Delete a line when it is done, and say why in the commit.

## Next session

- [ ] **Create the remote repo.** Private, on GitHub or Azure DevOps, then
      `git remote add origin ...` and push. Until it exists, the local repo is a
      single copy on one disk and not a backup.
- [ ] **Credentials decision.** Left out of the backup for now. Needs a session
      on secure storage before any bot token exists: a vault Hermes reads from,
      or an age-encrypted archive, or re-entering by hand on restore.
- [ ] **Run the restore test.** Install `ea` from the shared library onto a
      clean home directory and confirm it starts and remembers. A backup that
      has never been restored is a guess.

## Done

- [x] **Memories out of git.** `sync.sh` no longer commits `memories/`, and the
      old copy was removed. Memories live only in the private OneDrive backup.
- [x] **Library named.** Shared folder is now `TRIBE Group Tech/Hermes Library`.
- [x] **Schedule the backup.** Hermes job `Hermes backup`, daily at 17:00,
      runs `scripts/nightly.sh` with no model involved. A launchd agent was
      tried first and failed: macOS blocks rsync writing into OneDrive from a
      launchd context, so the job runs from the scheduler instead.

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
