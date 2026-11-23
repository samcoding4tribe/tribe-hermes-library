#!/usr/bin/env python3
"""Portable Hermes profile housekeeping, one codebase for macOS, Windows and Linux.

    python3 hermes_files.py backup            snapshot text and databases
    python3 hermes_files.py sync              repo commit, publish, push
    python3 hermes_files.py pull [profile]    diff library against a local profile
    python3 hermes_files.py nightly           backup, then sync, quietly

Common flags: --dry-run, --no-git, --no-publish, --keep N, --profile NAME

Paths come from config.env next to the repo root, then from the environment:
HERMES_SYNC_REPO, HERMES_SYNC_ONEDRIVE, HERMES_BACKUP_ONEDRIVE, HERMES_HOME.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HOME = Path.home()
DEFAULT_CANDIDATES = [
    HOME / "Library/CloudStorage/OneDrive-TribeTravelandEvents",
    HOME / "OneDrive - TribeTravelandEvents",
    HOME / "OneDrive - Tribe Travel and Events",
]

CREDENTIAL_RE = re.compile(r"(api_key|client_secret|secret|password|token|_KEY)\s*:", re.I)


def expand(value: str) -> str:
    value = value.replace("$HOME", str(HOME)).replace("%USERPROFILE%", str(HOME))
    value = os.path.expanduser(os.path.expandvars(value))
    return value


def load_config() -> dict:
    cfg = {}
    env_file = Path(__file__).resolve().parent.parent / "config.env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            cfg[key.strip()] = expand(val.strip().strip('"').strip("'"))
    for key in ("HERMES_SYNC_REPO", "HERMES_SYNC_ONEDRIVE", "HERMES_BACKUP_ONEDRIVE", "HERMES_HOME"):
        if os.environ.get(key):
            cfg[key] = expand(os.environ[key])

    repo = Path(cfg.get("HERMES_SYNC_REPO") or Path(__file__).resolve().parent.parent)
    hermes = Path(cfg.get("HERMES_HOME") or HOME / ".hermes")
    library = Path(cfg["HERMES_SYNC_ONEDRIVE"]) if cfg.get("HERMES_SYNC_ONEDRIVE") else None
    backup = Path(cfg["HERMES_BACKUP_ONEDRIVE"]) if cfg.get("HERMES_BACKUP_ONEDRIVE") else None
    return {
        "repo": repo,
        "hermes": hermes,
        "library": library,
        "backup": backup,
        "bundled_skills": hermes / "hermes-agent" / "skills",
    }


def profiles(hermes: Path, only=None):
    """Named profiles plus the default home itself."""
    found = [("default", hermes)]
    prof_dir = hermes / "profiles"
    if prof_dir.is_dir():
        for p in sorted(prof_dir.iterdir()):
            if p.is_dir():
                found.append((p.name, p))
    if only:
        wanted = {only} if isinstance(only, str) else set(only)
        found = [p for p in found if p[0] in wanted]
    return found


def sanitize(text: str) -> str:
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            out.append(line)
            continue
        if CREDENTIAL_RE.search(line):
            out.append("  # (credential line removed by hermes_files)")
            continue
        out.append(line)
    return "\n".join(out) + "\n"


def custom_skills(src: Path, bundled: Path):
    """Skill folders that are not shipped with Hermes."""
    skills = src / "skills"
    if not skills.is_dir():
        return []
    known = {p.name for p in bundled.glob("*/*") if p.is_dir()} if bundled.exists() else set()
    known |= {p.name for p in bundled.iterdir() if p.is_dir()} if bundled.exists() else set()
    return [d for d in sorted(skills.iterdir()) if d.is_dir() and d.name not in known]


def copy_text(src: Path, dst: Path, include_memories: bool, bundled: Path):
    dst.mkdir(parents=True, exist_ok=True)
    if (src / "SOUL.md").exists():
        shutil.copy2(src / "SOUL.md", dst / "SOUL.md")
    if (src / "config.yaml").exists():
        (dst / "config.yaml").write_text(sanitize((src / "config.yaml").read_text(encoding="utf-8")), encoding="utf-8")
    if include_memories and (src / "workspace").is_dir():
        # per-profile notes (context, procedures in draft, decisions) are private:
        # backed up with the profile, never published or committed
        shutil.copytree(src / "workspace", dst / "workspace", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".DS_Store"))
    elif (dst / "workspace").exists():
        shutil.rmtree(dst / "workspace")
    if include_memories and (src / "memories").is_dir():
        mem_dst = dst / "memories"
        mem_dst.mkdir(exist_ok=True)
        for f in (src / "memories").glob("*.md"):
            shutil.copy2(f, mem_dst / f.name)
    elif (dst / "memories").exists():
        shutil.rmtree(dst / "memories")
    if (src / "cron").is_dir():
        cron_dst = dst / "cron"
        cron_dst.mkdir(exist_ok=True)
        for f in (src / "cron").iterdir():
            if f.is_file() and f.suffix in {".json", ".yaml"}:
                shutil.copy2(f, cron_dst / f.name)
    for skill in custom_skills(src, bundled):
        target = dst / "skills" / skill.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill, target, ignore=shutil.ignore_patterns(".DS_Store"))


def snapshot_db(db_path: Path, out_path: Path):
    if not db_path.exists():
        return False
    src = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        dst = sqlite3.connect(out_path)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    return True


def run(cmd, cwd=None, check=False):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def git(repo: Path, *args, check=False):
    return run(["git", *args], cwd=repo, check=check)


def cmd_backup(cfg, args):
    dest = cfg["backup"]
    if not dest:
        print("set HERMES_BACKUP_ONEDRIVE in config.env")
        return 1
    stamp = datetime.now().strftime("%Y-%m-%d")
    text_dir = dest / "text"
    db_dir = dest / "db"

    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp)
        for name, path in profiles(cfg["hermes"], args.profile):
            target = stage if name == "default" else stage / "profiles" / name
            copy_text(path, target, include_memories=True, bundled=cfg["bundled_skills"])
        staged = sum(1 for _ in stage.rglob("*") if _.is_file())
        print(f"text: {staged} files staged")
        if args.dry_run:
            print(f"would write {text_dir} and {db_dir}")
            return 0
        text_dir.mkdir(parents=True, exist_ok=True)
        db_dir.mkdir(parents=True, exist_ok=True)
        for item in list(text_dir.iterdir()):
            shutil.rmtree(item) if item.is_dir() else item.unlink()
        shutil.copytree(stage, text_dir, dirs_exist_ok=True)

    for name, path in profiles(cfg["hermes"], args.profile):
        out = db_dir / f"{stamp}-{name}.db"
        if snapshot_db(path / "state.db", out):
            print(f"db: {name} -> {out.name} ({out.stat().st_size // 1024} KB)")

    snaps = sorted(db_dir.glob("*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in snaps[args.keep:]:
        for f in (old, Path(str(old) + "-wal"), Path(str(old) + "-shm")):
            f.unlink(missing_ok=True)
        print(f"pruned {old.name}")

    (dest / "README.md").write_text(
        "# Hermes backup for this machine\n\n"
        "Written by `scripts/hermes_files.py backup`. Text is mirrored each run; "
        "databases are snapshots, ten kept by default.\n\n"
        "Restore: quit Hermes, copy `text/<profile>/` back to the matching profile "
        "folder, put a `db/<date>-<profile>.db` back as `state.db`, add credentials "
        "from the vault, then start Hermes and check memory.\n",
        encoding="utf-8",
    )
    snap_count = len(list(db_dir.glob("*.db")))
    (dest / "last-backup.txt").write_text(
        f"last backup: {datetime.now():%Y-%m-%d %H:%M}\ntext: {text_dir}\ndb snapshots: {snap_count}\n",
        encoding="utf-8",
    )
    print(f"backup written to {dest}")
    return 0


def cmd_sync(cfg, args):
    repo = cfg["repo"]
    for name, path in profiles(cfg["hermes"], args.profile):
        dst = repo / "profiles" / name if name != "default" else repo / "profiles" / "default"
        copy_text(path, dst, include_memories=False, bundled=cfg["bundled_skills"])
        print(f"synced {name}")

    if not args.dry_run and (repo / ".git").exists():
        git(repo, "add", "-A")
        if git(repo, "diff", "--cached", "--quiet").returncode != 0:
            git(repo, "commit", "-q", "-m", f"sync: {datetime.now():%Y-%m-%d %H:%M}")
            print(f"git: committed {datetime.now():%H:%M}")
        else:
            print("git: nothing to commit")
        if git(repo, "remote", "get-url", "origin").returncode == 0:
            push = git(repo, "push", "-q", "origin", "HEAD")
            print("git: pushed to origin" if push.returncode == 0 else "git: push failed")

    if args.no_publish or not cfg["library"]:
        return 0
    lib = cfg["library"]
    if args.dry_run:
        print(f"would publish to {lib}")
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp)
        shutil.copytree(repo / "profiles", stage / "profiles", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("memories", ".DS_Store"))
        for part in ("templates", "shared-skills", "apps"):
            if (repo / part).exists():
                shutil.copytree(repo / part, stage / part, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns(".DS_Store", "status-today.json"))
        if (repo / "docs").exists():
            shutil.copytree(repo / "docs", stage / "docs", dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".DS_Store", "library-readme.md"))
        if (repo / "docs" / "library-readme.md").exists():
            shutil.copy2(repo / "docs" / "library-readme.md", stage / "README.md")
        if (repo / "TODO.md").exists():
            shutil.copy2(repo / "TODO.md", stage / "TODO.md")
        lib.mkdir(parents=True, exist_ok=True)
        for item in list(lib.iterdir()):
            shutil.rmtree(item) if item.is_dir() else item.unlink()
        shutil.copytree(stage, lib, dirs_exist_ok=True)

    manifest, count = {}, 0
    for f in sorted(lib.rglob("*")):
        if f.is_file():
            rel = f.relative_to(lib).as_posix()
            manifest[rel] = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
            count += 1
    (lib / "_manifest.json").write_text(
        json.dumps({"generated": datetime.now().isoformat(timespec="seconds"), "files": manifest}, indent=1),
        encoding="utf-8",
    )
    print(f"published {count} files to {lib}")
    return 0


def cmd_pull(cfg, args):
    if not cfg["library"]:
        print("set HERMES_SYNC_ONEDRIVE in config.env")
        return 1
    name = args.name or args.profile or "default"
    src = cfg["library"] / "profiles" / name
    local = cfg["hermes"] if name == "default" else cfg["hermes"] / "profiles" / name
    if not src.is_dir():
        print(f"no published copy of {name} in {src}")
        return 1
    diffs = 0
    for f in src.rglob("*"):
        if not f.is_file() or f.name == ".DS_Store" or f.name == "config.yaml":
            continue
        rel = f.relative_to(src)
        here = local / rel
        if not here.exists() or here.read_bytes() != f.read_bytes():
            diffs += 1
            print(f"\n### {rel}")
            print(run(["diff", "-u", str(here), str(f)]).stdout or "(new file)")
            if args.apply:
                here.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, here)
                print("  applied")
    if not diffs:
        print(f"no differences for {name}")
    elif not args.apply:
        print(f"\n{diffs} file(s) differ. Re-run with --apply to take the library version.")
    return 0


def cmd_nightly(cfg, args):
    logs = cfg["repo"] / "logs"
    logs.mkdir(exist_ok=True)
    import io
    from contextlib import redirect_stdout

    outcomes = []
    for name, fn in (("backup", cmd_backup), ("sync", cmd_sync)):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = fn(cfg, args)
        out = stream.getvalue()
        outcomes.append((name, code, out))
        with (logs / f"{name}.log").open("a", encoding="utf-8") as log:
            log.write(f"--- {datetime.now():%Y-%m-%d %H:%M}\n{out}\n")

    failed = [n for n, c, _ in outcomes if c]
    if failed:
        print(f"Hermes backup failed: {', '.join(failed)} at {datetime.now():%Y-%m-%d %H:%M}")
        for name, _, out in outcomes:
            if name in failed:
                print(out.strip())
        return 1

    # quiet when nothing was committed and nothing was pruned or rewritten
    if "nothing to commit" in outcomes[1][2]:
        return 0
    print(f"Hermes backup {datetime.now():%Y-%m-%d %H:%M}: " + " | ".join(
        out.strip().splitlines()[-1] for _, _, out in outcomes if out.strip()))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["backup", "sync", "pull", "nightly"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--keep", type=int, default=10)
    ap.add_argument("--profile")
    ap.add_argument("name", nargs="?", help="profile name for pull")
    args = ap.parse_args()
    cfg = load_config()
    return {"backup": cmd_backup, "sync": cmd_sync, "pull": cmd_pull, "nightly": cmd_nightly}[args.command](cfg, args)


if __name__ == "__main__":
    sys.exit(main())
