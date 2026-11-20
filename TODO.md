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

- [x] **Schedule the backup.** Hermes job `Hermes backup`, daily at 17:00,
      runs `scripts/nightly.sh` with no model involved. A launchd agent was
      tried first and failed: macOS blocks rsync writing into OneDrive from a
      launchd context, so the job runs from the scheduler instead.

## Later

- [ ] Add `age` and encrypt `.env` plus `auth.json` into the private backup.
- [ ] Add the check on push: secret scan, unfilled placeholders, skills parse,
      clean install.
- [ ] Decide the OneDrive library owner, so two people do not edit at once.

## Waiting on other people

- [ ] Tenant permission to install the Teams bot.
- [ ] Who in IT can grant Graph consent, when route 3 arrives.
