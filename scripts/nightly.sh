#!/usr/bin/env bash
# Daily run, 17:00, from launchd. Back up this machine, then publish the library.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/logs"
stamp() { date '+%Y-%m-%d %H:%M'; }

{
  echo "--- $(stamp) backup"
  "$ROOT/scripts/backup.sh" 2>&1
} >> "$ROOT/logs/backup.log"

{
  echo "--- $(stamp) sync"
  "$ROOT/scripts/sync.sh" 2>&1
} >> "$ROOT/logs/sync.log"
