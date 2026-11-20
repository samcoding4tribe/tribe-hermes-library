#!/usr/bin/env bash
# Daily run at 17:00, fired by the Hermes scheduler (no model involved).
# Backs up this machine, publishes the library, and prints one line only when
# something changed or a step failed. Empty output means a quiet day.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/logs"

backup_out="$("$ROOT/scripts/backup.sh" 2>&1)"; rc1=$?
{
  echo "--- $(date '+%Y-%m-%d %H:%M') backup"
  echo "$backup_out"
} >> "$ROOT/logs/backup.log"

sync_out="$("$ROOT/scripts/sync.sh" 2>&1)"; rc2=$?
{
  echo "--- $(date '+%Y-%m-%d %H:%M') sync"
  echo "$sync_out"
} >> "$ROOT/logs/sync.log"

if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then
  echo "Hermes backup failed at $(date '+%Y-%m-%d %H:%M')."
  echo "$backup_out" | tail -4
  echo "$sync_out" | tail -4
  exit 1
fi

if echo "$sync_out" | grep -q "nothing to commit"; then
  exit 0
fi

echo "Hermes backup $(date '+%Y-%m-%d %H:%M'): $(echo "$sync_out" | grep -E '^(git|onedrive):' | tr '\n' ' ')"
