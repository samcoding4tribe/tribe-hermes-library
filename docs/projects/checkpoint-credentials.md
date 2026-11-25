# Protecting keys across the estate

Parked 26 November 2026. Raised by Sam while working the interview thread, and
deliberately not started: it is a rabbit hole that would stall the rollout.

## The problem

Every profile needs credentials to be useful — mail, calendar, connectors, model
keys. Today each lives in `~/.hermes/profiles/<name>/.env`, `chmod 600`, re-entered
by hand after a restore. That is D11's holding position, not a solution.

At two profiles on one Mac it is fine. Across a company it is one copy per machine,
no rotation, no record of who holds what, and no way to see when one has moved.

## Options seen so far, none evaluated

- OS keychain on each machine, entered once by the owner.
- Encrypted secrets in OneDrive (`age` or `sops`), key held separately.
- A secrets manager, which adds a service to run and a thing to pay for.
- Encryption at rest only, which protects a lost laptop and not a shared folder.

Sam raised Kubernetes as a control plane for this kind of problem. Recorded as an
option, not a recommendation: at this size it is very likely heavier than the
problem, and it belongs to the same family as the storage question in D11 and the
access question in D20 — all three are the same decision wearing different clothes.

## Trigger to pick it up

Any one of: more than three machines, the first always-on shared server, or the
first credential that matters more than a signed-in browser session.

## Not now

Nothing here blocks the rollout. D11 and D20 stay as they are until the open
threads in `docs/projects/README.md` close.
