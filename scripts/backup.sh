#!/usr/bin/env bash
# Snapshots what cannot be downloaded again: souls, memories, configs without
# secrets, custom skills, cron definitions and the session databases.
#
#   ./scripts/backup.sh                 run it
#   ./scripts/backup.sh --dry-run       show what would happen
#   ./scripts/backup.sh --keep 5        keep five database snapshots (default 10)
#
# Databases are copied with sqlite3 .backup, which is safe while the gateway
# is running. Credentials are not included, by design.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
[ -f "$ROOT/config.env" ] && . "$ROOT/config.env"

HERMES="${HERMES_HOME:-$HOME/.hermes}"
DEST="${HERMES_BACKUP_ONEDRIVE:?set HERMES_BACKUP_ONEDRIVE in config.env}"
BUNDLED="$HERMES/hermes-agent/skills"
KEEP=10
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --keep) KEEP="${2:?--keep needs a number}"; shift ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
  shift
done

stamp="$(date '+%Y-%m-%d')"
TEXT="$DEST/text"
DBDIR="$DEST/db"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

sanitize_config() {
  awk '
    /^[[:space:]]*#/ { print; next }
    /(api_key|client_secret|secret|password|token|_KEY)[[:space:]]*:/ {
      if ($0 ~ /\$\{[A-Za-z_]+\}/) print;
      else print "  # (credential line removed by backup)"
      next
    }
    { print }
  ' "$1"
}

# text layer, into a staging copy so the mirror can be synced cleanly
copy_common() {           # $1 = source profile dir, $2 = dest dir
  local src="$1" dst="$2"
  mkdir -p "$dst"
  [ -f "$src/SOUL.md" ] && cp "$src/SOUL.md" "$dst/SOUL.md"
  if [ -f "$src/config.yaml" ]; then
    sanitize_config "$src/config.yaml" > "$dst/config.yaml"
  fi
  if [ -d "$src/memories" ]; then
    mkdir -p "$dst/memories"
    find "$src/memories" -maxdepth 1 -name '*.md' -exec cp {} "$dst/memories/" \;
  fi
  if [ -d "$src/cron" ]; then
    mkdir -p "$dst/cron"
    find "$src/cron" -maxdepth 1 -type f \( -name '*.json' -o -name '*.yaml' \) -exec cp {} "$dst/cron/" \;
  fi
  if [ -d "$src/skills" ]; then
    local skilldir name
    for skilldir in "$src"/skills/*/; do
      [ -d "$skilldir" ] || continue
      name="$(basename "$skilldir")"
      if find "$BUNDLED" -maxdepth 3 -type d -name "$name" 2>/dev/null | grep -q .; then
        continue
      fi
      mkdir -p "$dst/skills/$name"
      rsync -a --delete --exclude '.DS_Store' "$skilldir" "$dst/skills/$name/"
    done
  fi
}

copy_common "$HERMES" "$STAGE/default"
for p in "$HERMES"/profiles/*/; do
  [ -d "$p" ] || continue
  copy_common "$p" "$STAGE/profiles/$(basename "$p")"
done

echo "text: $(find "$STAGE" -type f | wc -l | tr -d ' ') files staged"

if [ "$DRY" = 1 ]; then
  echo "would write $TEXT/ and database snapshots in $DBDIR/"
  echo "would keep the newest $KEEP snapshots"
  exit 0
fi

mkdir -p "$TEXT" "$DBDIR"
rsync -a --delete "$STAGE/" "$TEXT/"

# database layer
snapshot_db() {           # $1 = db path, $2 = label
  local db="$1" label="$2"
  [ -f "$db" ] || return 0
  sqlite3 "$db" ".backup '$DBDIR/$stamp-$label.db'"
  echo "db: $label -> $stamp-$label.db ($(du -h "$DBDIR/$stamp-$label.db" | cut -f1))"
}
snapshot_db "$HERMES/state.db" "default"
for p in "$HERMES"/profiles/*/; do
  [ -d "$p" ] || continue
  snapshot_db "$p/state.db" "$(basename "$p")"
done

# prune old snapshots
if ls "$DBDIR"/*.db >/dev/null 2>&1; then
  ls -1t "$DBDIR"/*.db | tail -n +$((KEEP + 1)) | while read -r old; do
    rm -f "$old" "$old-wal" "$old-shm"
    echo "pruned $(basename "$old")"
  done
fi
# sidecars left behind by anything that opened a snapshot for inspection
rm -f "$DBDIR"/*.db-wal "$DBDIR"/*.db-shm

cat > "$DEST/README.md" <<'NOTE'
# Hermes backup for this machine

Written by `scripts/backup.sh` from the local `tribe-hermes-library` repo. Text is
mirrored on each run; databases are snapshots, ten kept by default.

| Path | What |
|---|---|
| `text/default/`, `text/profiles/<name>/` | SOUL.md, memories, config without credentials, custom skills, cron |
| `db/<date>-<profile>.db` | consistent copy of each session database |

## Restore

1. Quit Hermes, or stop the gateway (`hermes gateway stop`).
2. Copy `text/profiles/<name>/` to `~/.hermes/profiles/<name>/`, or for the
   default profile copy the files into `~/.hermes/`.
3. Put a database snapshot back as `state.db` in the same place.
4. Add credentials to `.env` from the vault. They are not in this backup.
5. Start Hermes and check `/memory` shows the expected entries.
NOTE

{
  echo "last backup: $(date '+%Y-%m-%d %H:%M')"
  echo "text: $(du -sh "$TEXT" | cut -f1)"
  echo "db snapshots: $(ls -1 "$DBDIR"/*.db 2>/dev/null | wc -l | tr -d ' ')"
} > "$DEST/last-backup.txt"

echo "backup written to $DEST"
cat "$DEST/last-backup.txt"
