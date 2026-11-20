# Hermes library

Shared reference for the assistants Hermes runs at TRIBE Group. Readable by the
team; written from one machine at a time.

## What is here

| Folder | Contents |
|---|---|
| `templates/role/` | Blank starting point for a new role assistant. Soul with placeholders, config, instructions |
| `profiles/<name>/` | Published copy of each assistant: soul, config without credentials, custom skills |
| `docs/` | Architecture, the decisions behind it, the rollout plan |
| `_manifest.json` | Hash of every file and when it was written. If a local copy differs, this shows it |

## What is deliberately absent

Memories and session databases. They contain what a particular person said and
did, so they stay in the owner's private backup, not here. Credentials are also
absent: every machine holds its own `.env`.

## Starting an assistant from a template

1. Copy `templates/role` to a new folder named after the person or role.
2. Fill the placeholders in `SOUL.md`.
3. Create the profile on the machine and give it its facts.
4. Walk it through the job twice, then write the first skill.
5. Publish it back here by running the sync from the maintaining machine.

## Editing

Souls, memories and skills can be edited here by the maintainer. Changes are
pulled into the machine with a diff before they are applied, so nothing
overwrites a newer local version by accident. Skills are the exception: they
contain commands, so they are tested on a machine before they are published.

## The rule that keeps this simple

One writer at a time. This folder is a published copy, not a live agent. The
agent runs from a local profile on its own machine.
