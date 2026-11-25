# The Hermes profile: the one that builds the others

Used once, on a new machine, before any assistant exists. It is the maintainer profile:
the thing that sets up the first assistant and then keeps the estate in step.

## Install it

1. Copy `SOUL.md` from this folder over the default profile's soul:

   ```
   cp templates/builder/SOUL.md ~/.hermes/SOUL.md          # macOS
   copy templates\builder\SOUL.md %LOCALAPPDATA%\hermes\SOUL.md   # Windows
   ```

2. Fill the four placeholders: `{{OWNER}}`, `{{ROLE}}`, `{{MACHINE}}`, `{{DATE}}`. The
   machine name is the OS asset name, not a nickname, because the backup folder uses it.

3. Confirming the label. The profile id stays `default`; the name people see is the label
   (D22). So:

   ```
   hermes chat -q "One line: who are you, whose machine is this, and what is your first rule?"
   ```

   If it answers as the builder, with the right owner and the right first rule, it is
   installed.

## What it does next

Its soul tells it the first job: run the set-up interview and create the owner's assistant
profile. Nothing else is scaffolded here — no skills, no cron, no persona for the assistant
itself. Those come from the interview and from watching the work.

## What it must not do

- Do not give the assistant profile its own persona from imagination. The interview
  supplies it.
- Do not copy one person's memory, working notes or context file into another profile, or
  into this template.
- Do not publish anything from this machine before the first successful backup: if the
  library has files this machine did not write, `sync` will replace them.
