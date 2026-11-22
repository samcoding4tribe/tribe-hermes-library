#!/usr/bin/env bash
# Brings edits made in the OneDrive library back into the local profile.
#
#   ./scripts/pull.sh ea              show the differences
#   ./scripts/pull.sh ea --apply      write them into the local profile
#   ./scripts/pull.sh ea --from-repo  read the repo copy instead
#
# Souls, memories and custom skills come back. config.yaml does not: the
# published copy has credential lines stripped, so pulling it would remove
# settings the machine needs.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
[ -f "$ROOT/config.env" ] && . "$ROOT/config.env"

REPO="${HERMES_SYNC_REPO:-$HOME/tribe-hermes-library}"
ONEDRIVE="${HERMES_SYNC_ONEDRIVE:-$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/Hermes}"
HERMES="${HERMES_HOME:-$HOME/.hermes}"

name="${1:-}"; shift || true
[ -n "$name" ] || { echo "usage: pull.sh <profile-name> [--apply] [--from-repo]" >&2; exit 2; }

SOURCE="$ONEDRIVE" APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --from-repo) SOURCE="$REPO" ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

src="$SOURCE/profiles/$name"
dst="$HERMES/profiles/$name"
[ -d "$src" ] || { echo "no published copy of '$name' in $src" >&2; exit 1; }
[ -d "$dst" ] || { echo "$dst does not exist; install it first" >&2; exit 1; }

differ=0
while IFS= read -r rel; do
  case "$rel" in
    config.yaml|.env|auth.json) continue ;;
  esac
  a="$dst/$rel"; b="$src/$rel"
  [ -f "$b" ] || continue
  if [ ! -f "$a" ] || ! cmp -s "$a" "$b"; then
    differ=$((differ + 1))
    echo ""
    echo "### $rel"
    diff -u "$a" "$b" 2>/dev/null | sed -n '3,$p' || true
    if [ "$APPLY" = 1 ]; then
      mkdir -p "$(dirname "$a")"
      cp "$b" "$a"
      echo "  applied"
    fi
  fi
done < <(cd "$src" && find . -type f -not -name '.DS_Store' | sed 's|^\./||' | sort)

if [ "$differ" = 0 ]; then
  echo "no differences between $src and $dst"
elif [ "$APPLY" = 0 ]; then
  echo ""
  echo "$differ file(s) differ. Re-run with --apply to take the library version."
fi
