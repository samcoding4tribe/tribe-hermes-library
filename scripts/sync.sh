#!/usr/bin/env bash
# Copies the portable parts of every Hermes profile into this repo,
# commits them, then publishes a read-only copy into OneDrive.
#
#   ./scripts/sync.sh                 sync every named profile
#   ./scripts/sync.sh ea              sync one profile
#   ./scripts/sync.sh --dry-run       show what would change
#   ./scripts/sync.sh --no-git        skip the commit
#   ./scripts/sync.sh --no-onedrive   skip the OneDrive copy
#
# Secrets are never copied. Only SOUL.md, memories, cron definitions,
# skills you wrote yourself, and a config.yaml with key lines stripped.

set -euo pipefail

REPO="${HERMES_SYNC_REPO:-$HOME/hermes-agents}"
ONEDRIVE="${HERMES_SYNC_ONEDRIVE:-$HOME/Library/CloudStorage/OneDrive-TribeTravelandEvents/Hermes}"
HERMES="${HERMES_HOME:-$HOME/.hermes}"
BUNDLED_SKILLS="$HERMES/hermes-agent/skills"
DOC="$HOME/Downloads/Hermes EA and Org Rollout.md"

DRY=0 GIT=1 ONEDRIVE_ON=1
PROFILES=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --no-git) GIT=0 ;;
    --no-onedrive) ONEDRIVE_ON=0 ;;
    -*) echo "unknown flag: $arg" >&2; exit 2 ;;
    *) PROFILES+=("$arg") ;;
  esac
done

run() {
  if [ "$DRY" = 1 ]; then echo "  would: $*"; else "$@"; fi
}

mkdir -p "$REPO/profiles"
cd "$REPO"

if [ ${#PROFILES[@]} -eq 0 ]; then
  for d in "$HERMES"/profiles/*/; do
    [ -d "$d" ] || continue
    PROFILES+=("$(basename "$d")")
  done
fi

[ ${#PROFILES[@]} -gt 0 ] || { echo "no profiles found"; exit 0; }

# config.yaml with credential lines removed; ${VAR} references are kept
sanitize_config() {
  awk '
    /^[[:space:]]*#/ { print; next }
    /(api_key|client_secret|secret|password|token|_KEY)[[:space:]]*:/ {
      if ($0 ~ /\$\{[A-Za-z_]+\}/) print;   # a ${VAR} reference is safe
      else print "  # (credential line removed by sync)"
      next
    }
    { print }
  ' "$1"
}

changed=0
for p in "${PROFILES[@]}"; do
  src="$HERMES/profiles/$p"
  [ -d "$src" ] || { echo "skip $p: not found"; continue; }
  dst="$REPO/profiles/$p"
  mkdir -p "$dst"

  if [ -f "$src/SOUL.md" ]; then
    run cp "$src/SOUL.md" "$dst/SOUL.md"
  fi

  if [ -f "$src/config.yaml" ]; then
    if [ "$DRY" = 1 ]; then
      echo "  would: sanitize config.yaml -> profiles/$p/config.yaml"
    else
      sanitize_config "$src/config.yaml" > "$dst/config.yaml"
    fi
  fi

  if [ -d "$src/memories" ]; then
    run mkdir -p "$dst/memories"
    for f in "$src"/memories/*.md; do
      [ -f "$f" ] && run cp "$f" "$dst/memories/"
    done
  fi

  if [ -d "$src/cron" ]; then
    run mkdir -p "$dst/cron"
    find "$src/cron" -maxdepth 1 -name '*.json' -o -maxdepth 1 -name '*.yaml' 2>/dev/null | while read -r f; do
      run cp "$f" "$dst/cron/"
    done
  fi

  # only skills that are not shipped with Hermes
  if [ -d "$src/skills" ]; then
    for skilldir in "$src"/skills/*/; do
      [ -d "$skilldir" ] || continue
      name="$(basename "$skilldir")"
      if find "$BUNDLED_SKILLS" -maxdepth 3 -type d -name "$name" 2>/dev/null | grep -q .; then
        continue
      fi
      run mkdir -p "$dst/skills/$name"
      run rsync -a --delete --exclude '.DS_Store' "$skilldir" "$dst/skills/$name/"
    done
  fi
  echo "synced $p"
done

if [ -f "$DOC" ]; then
  run mkdir -p "$REPO/docs"
  run cp "$DOC" "$REPO/docs/rollout.md"
fi

if [ "$GIT" = 1 ]; then
  git add -A
  if git diff --cached --quiet; then
    echo "git: nothing to commit"
  elif [ "$DRY" = 1 ]; then
    echo "git: would commit"
  else
    git commit -q -m "sync: $(date '+%Y-%m-%d %H:%M') ${PROFILES[*]}"
    echo "git: committed $(date '+%Y-%m-%d %H:%M')"
  fi
fi

if [ "$ONEDRIVE_ON" = 1 ]; then
  if [ -d "$ONEDRIVE" ] || [ "$DRY" = 1 ]; then
    run mkdir -p "$ONEDRIVE"
    run rsync -a --delete --exclude '.git' --exclude '.DS_Store' \
      "$REPO/profiles/" "$ONEDRIVE/profiles/"
    run rsync -a --exclude '.DS_Store' "$REPO/templates/" "$ONEDRIVE/templates/" 2>/dev/null || true
    run rsync -a --exclude '.DS_Store' "$REPO/docs/" "$ONEDRIVE/docs/" 2>/dev/null || true
    echo "onedrive: published to $ONEDRIVE"
  else
    echo "onedrive: folder not found, skipped"
  fi
fi
