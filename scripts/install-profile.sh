#!/usr/bin/env bash
# Puts a synced profile onto this machine.
#
#   ./scripts/install-profile.sh ea                 from OneDrive (default)
#   ./scripts/install-profile.sh ea --from-repo
#   ./scripts/install-profile.sh ea --force         overwrite an existing profile
#
# It never writes keys. After it runs, add the credentials the profile needs
# to ~/.hermes/profiles/<name>/.env, then start it with: hermes -p <name> chat

set -euo pipefail

REPO="${HERMES_SYNC_REPO:-$HOME/hermes-agents}"
ONEDRIVE="${HERMES_SYNC_ONEDRIVE:-$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/Hermes}"
HERMES="${HERMES_HOME:-$HOME/.hermes}"

name="${1:-}"; shift || true
[ -n "$name" ] || { echo "usage: install-profile.sh <profile-name> [--from-repo] [--force]" >&2; exit 2; }

SOURCE="$ONEDRIVE"
FORCE=0
for arg in "$@"; do
  case "$arg" in
    --from-repo) SOURCE="$REPO" ;;
    --force) FORCE=1 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

src="$SOURCE/profiles/$name"
[ -d "$src" ] || { echo "no profile '$name' in $SOURCE/profiles" >&2; exit 1; }

dst="$HERMES/profiles/$name"
if [ -d "$dst" ] && [ "$FORCE" != 1 ]; then
  echo "$dst already exists. Re-run with --force to overwrite it." >&2
  exit 1
fi

mkdir -p "$dst"
rsync -a --exclude '.DS_Store' "$src/" "$dst/"
echo "installed $name -> $dst"
echo "next: add credentials to $dst/.env, then run: hermes -p $name chat"
