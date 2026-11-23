# Setting up Hermes on a new machine

Written for a managed Mac. About forty minutes, most of it waiting for sign-ins.
Tested on 23 November 2026 on `TTEL-MMPK7Q3CV2`.

## What you need before you start

- The machine, an account that can install apps, and the person's OneDrive signed in
- The model key for that profile (DeepSeek, or whatever the profile uses)
- Access to the shared library: `OneDrive / TRIBE Group Tech / Hermes Library`

## 1. Install Hermes

Install the app as normal and open it once. The desktop app installs the runtime
under `~/.hermes` and starts a gateway that runs scheduled jobs.

Check it is alive:

```bash
hermes --version
hermes doctor
```

If the policy on the machine blocks unsigned apps or background services, stop
here and sort that with IT first. Everything else depends on the gateway running.

## 2. Let the app reach OneDrive

The app needs Files and Folders access the first time it writes into the
OneDrive container. The symptoms when it is missing are `Operation not permitted`
on `rsync` into `~/Library/CloudStorage/...`.

Grant it when the prompt appears. A launchd job cannot write there even with the
app approved, which is why backups run from the Hermes scheduler instead (D12).

## 3. Bring the profile onto the machine

Copy the published profile out of the shared library:

```bash
cd ~/tribe-hermes-library
./scripts/install-profile.sh ea
```

Then add that machine's credentials to `~/.hermes/profiles/ea/.env`. The library
never carries keys.

If the profile belongs to a named person, open `templates/org/org-map.html`, ask
them which card is theirs, and take the `id` rather than a typed job title. Ask
the relationship questions against the chart: who they report to, who reports to
them, who approves expenses and travel, who is copied on client mail, who covers
leave. Write the answers into their context, not into the chart. See
`docs/org-map.md`.

Name it before you start. The profile id follows the role (`assistant-kate`,
`office-manager`); the name the person sees is a label, set in the roster and
optionally in the first line of the soul. Do not rename the folder for a
nickname, since the library, the backup path and the scripts all key on it.

Start it and check the persona:

```bash
hermes -p ea chat
```

Ask it who it is and what its first rule is. If it answers in the wrong voice,
the soul did not land.

## 4. Make the machine back itself up

```bash
cd ~/tribe-hermes-library
./scripts/backup.sh          # once, by hand
./scripts/sync.sh            # publishes, commits, pushes
```

Then confirm the daily job exists and points at this machine:

```bash
hermes cron list
```

It should show `Hermes backup` at 17:00, running `hermes-backup.sh`. If this is a
fresh machine, create it:

```bash
mkdir -p ~/.hermes/scripts
printf '#!/usr/bin/env bash\nexec "$HOME/tribe-hermes-library/scripts/nightly.sh"\n' > ~/.hermes/scripts/hermes-backup.sh
chmod +x ~/.hermes/scripts/hermes-backup.sh
```

and create the job in the app under Cron, daily at 17:00, with no model attached.

## 4a. Windows machines

Most of the estate is Windows, and the same file works there.

- Run the scripts as `python scripts\hermes_files.py backup`, `sync`, `nightly`.
  Hermes ships a Python runtime, so nothing needs installing.
- There is no equivalent of the macOS Files and Folders prompt, so the OneDrive
  write that failed from a launchd job on the Mac has no counterpart here.
- Schedule the nightly run with the Hermes scheduler, exactly as on the Mac, or
  with Task Scheduler if the gateway is not always running.
- The OneDrive folder is named `OneDrive - TribeTravelandEvents` rather than
  `OneDrive-TribeTravelandEvents`. Set that path in `config.env`.
- `git` for Windows is required only if this machine pushes to the repo.

## 5. Microsoft access when the native apps will not sign in

This is the part that trips people up. On a managed Mac, the Microsoft account
can refuse to sign in to the native apps because of conditional access. Hermes
does not need those apps, and it does not need the account details either.

**Do not ask for the password.** Never type it, never accept it in chat.

What works, verified on this machine:

1. Open `https://outlook.office.com/mail/` in the preview pane beside the chat.
2. The person signs in there themselves. The password goes into the page, the
   session stays in the browser, and the agent never sees it.
3. The agent can then read the inbox and create drafts. Compose, fill the
   subject and body, then close the composer so Outlook saves it to Drafts.
4. Sending stays a human action.

Teams works the same way through `https://teams.microsoft.com`. Reading and
posting in the browser is enough for a pilot; the bot route in `architecture.md`
is the version that scales.

What this is not: Graph access. Mail on a schedule, without a browser open, needs
the app registration described as route 3 in `rollout.md`, plus an application
access policy scoped to one mailbox. Until then, the browser route is the whole
integration.

## 6. The security checklist

Before handing the machine to anyone:

- [ ] `~/.hermes/.env` and `auth.json` are not in the library, not in the repo, not in any backup
- [ ] The shared library has no `memories/` directories
- [ ] `approvals.mode` is `manual` on a role profile, so commands ask first
- [ ] The profile has only the toolsets it needs
- [ ] The daily job ran once and its output appears in `logs/backup.log`
- [ ] A restore has been tried at least once on a clean home directory

## 7. When it goes wrong

| Symptom | Cause |
|---|---|
| `Operation not permitted` writing to OneDrive | Files and Folders access not granted to the app, or the job runs from launchd |
| Backup folder missing | `HERMES_BACKUP_ONEDRIVE` in `config.env` still points at an old path |
| `The supported API model names are ...` | Profile points at a model its provider does not serve. Fix the model in that profile's config |
| Empty answers, no memory | Wrong profile. Memory is per profile, not per machine |
| Push rejected | SSH key for this machine not added to GitHub under its own title |
| Drafts folder empty after composing | The composer was discarded rather than closed |
