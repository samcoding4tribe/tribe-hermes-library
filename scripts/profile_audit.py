#!/usr/bin/env python3
"""Measure one profile against the context budget and flag what is over.

Read-only by design: this script opens files for reading, opens `state.db` with
SQLite's mode=ro, and writes nothing anywhere. It never edits a soul, a memory
file, a skill or a database. The pass that uses it proposes; the person applies.

Usage:
    python3 scripts/profile_audit.py                 # the profile Hermes runs as here
    python3 scripts/profile_audit.py --all           # every profile on this machine
    python3 scripts/profile_audit.py --profile admin
    python3 scripts/profile_audit.py --profile /path/to/profile --json

Thresholds are named constants at the top. The soul band is PROVISIONAL: Sam has
not fixed it, so the report shows the band it used and the next decision is his.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# --- thresholds -------------------------------------------------------------
# Memory caps come from the profile's own config.yaml, not from here.
MEMORY_FLAG_PCT = 90.0            # checkpoint-maintenance.md: "above ninety per cent"
STATE_DB_WATCH_MB = 100.0         # docs/context-budget.md watch line
SOUL_BAND_KB = (1.2, 3.0)         # PROVISIONAL band, measured souls are 1.2-3.6 KB
DUP_MIN_CHARS = 40                # shorter lines are too generic to call a duplicate
DUP_RATIO = 0.85                  # near-duplicate threshold for difflib
STATE_DB_WATCH_MESSAGES = None    # no message watch line agreed yet


# --- helpers ----------------------------------------------------------------
def hermes_home() -> Path:
    """HERMES_HOME from the environment, or from config.env, or the default."""
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env).expanduser()
    cfg = REPO / "config.env"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r'\s*HERMES_HOME="?([^"#]+)"?', line)
            if m:
                return Path(m.group(1).strip()).expanduser()
    return Path.home() / ".hermes"


def resolve_profiles(selector: str | None, home: Path) -> list[tuple[str, Path]]:
    """(id, path) pairs. The root profile is Hermes home itself."""
    prof_dir = home / "profiles"
    if selector and selector not in ("all", "@active"):
        p = Path(selector).expanduser()
        if p.is_dir():
            return [(p.name, p)]
        if (prof_dir / selector).is_dir():
            return [(selector, prof_dir / selector)]
        if selector == "default" and (home / "SOUL.md").exists():
            return [("default", home)]
        raise SystemExit(f"no profile called {selector!r} under {prof_dir}")

    out = []
    if (home / "SOUL.md").exists() and not (prof_dir / "default").is_dir():
        out.append(("default", home))
    if prof_dir.is_dir():
        for child in sorted(prof_dir.iterdir()):
            if child.is_dir() and (child / "config.yaml").exists():
                out.append((child.name, child))
    if selector != "all" and len(out) > 1:
        # No selector: report only the profile this script was invoked under.
        active = os.environ.get("HERMES_PROFILE")
        if active:
            out = [x for x in out if x[0] == active] or out
    return out


def memory_caps(profile: Path) -> tuple[int, int]:
    """memory.memory_char_limit and memory.user_char_limit from config.yaml."""
    mem, user = 2200, 1375
    cfg = profile / "config.yaml"
    if not cfg.exists():
        return mem, user
    text = cfg.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^\s*memory_char_limit:\s*(\d+)", text, re.M)
    if m:
        mem = int(m.group(1))
    m = re.search(r"^\s*user_char_limit:\s*(\d+)", text, re.M)
    if m:
        user = int(m.group(1))
    return mem, user


def external_dirs(profile: Path) -> list[str]:
    cfg = profile / "config.yaml"
    if not cfg.exists():
        return []
    text = cfg.read_text(encoding="utf-8", errors="replace")
    block = re.search(r"^skills:\n(?:.*\n)*?^  external_dirs:\n((?:    - .*\n)+)", text, re.M)
    if not block:
        return []
    return [ln.strip().lstrip("- ").strip("\"'") for ln in block.group(1).splitlines()]


def count_skills(profile: Path) -> int:
    """SKILL.md files only. A skills/ folder can hold just .locks and .hub."""
    root = profile / "skills"
    if not root.is_dir():
        return 0
    n = 0
    for path in root.rglob("SKILL.md"):
        parts = set(path.parts)
        if ".locks" in parts or ".hub" in parts:
            continue
        n += 1
    return n


def soul_path(profile: Path, home: Path) -> Path:
    return profile / "SOUL.md"


def norm(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", line)
    line = re.sub(r"\*\*|__|`", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip(" .,:;").lower()


def content_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    out = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        n = norm(raw)
        if len(n) >= DUP_MIN_CHARS:
            out.append(n)
    return out


STOPWORDS = {"you", "your", "the", "a", "an", "of", "to", "for", "and", "or", "in", "is",
             "it", "that", "this", "with", "be", "not", "from", "if", "at", "on", "as",
             "by", "do", "does", "are", "was", "when", "what", "who", "there", "their",
             "them", "they", "one", "so", "but", "then", "than", "into", "out", "up",
             "has", "have", "had", "will", "would", "can", "may", "must", "also", "its"}


def words(line: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", line) if w not in STOPWORDS and len(w) > 2}


def same_rule(a: str, b: str) -> bool:
    """Same rule said twice? Exact, near-identical, or the same significant words.

    Souls restate a rule with a different qualifier on the end, so neither a pure
    similarity ratio nor substring containment catches every copy: compare the
    content words, ignoring the ones every rule shares.
    """
    if a == b:
        return True
    short, long = (a, b) if len(a) <= len(b) else (b, a)
    if len(short) >= DUP_MIN_CHARS and short in long:
        return True
    if difflib.SequenceMatcher(None, a, b).ratio() >= DUP_RATIO:
        return True
    wa, wb = words(short), words(long)
    if len(wa) >= 3 and wa and wa <= wb:
        return True
    if len(wa) >= 4 and len(wa & wb) / len(wa) >= 0.75:
        return True
    return False


def split_soul(path: Path) -> tuple[list[str], list[str]]:
    """(lines the profile says itself, lines inside its marked shared block).

    The marked block is what the profile inherits from the baseline (D36); a rule
    repeated *outside* it is a second copy of a rule it already carries.
    """
    if not path.exists():
        return [], []
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<!-- shared:start -->(.*?)<!-- shared:end -->", text, re.S)
    shared = [norm(x) for x in (m.group(1) if m else "").splitlines()]
    outside = text[:m.start()] + text[m.end():] if m else text
    return ([n for n in (norm(x) for x in outside.splitlines()) if len(n) >= DUP_MIN_CHARS],
            [s for s in shared if len(s) >= DUP_MIN_CHARS])


def shipped_rules() -> list[str]:
    """The rules the baseline ships: the shared block of profiles/admin/SOUL.md."""
    soul = REPO / "profiles" / "admin" / "SOUL.md"
    if soul.exists():
        text = soul.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<!-- shared:start -->(.*?)<!-- shared:end -->", text, re.S)
        if m:
            rules = [norm(x) for x in m.group(1).splitlines()]
            return [r for r in rules if len(r) >= DUP_MIN_CHARS]
    alt = REPO / "baseline" / "soul-rules" / "admin.md"
    if alt.exists():
        return [norm(x) for x in content_lines(alt)]
    return []


def db_stats(profile: Path) -> dict:
    db = profile / "state.db"
    if not db.exists():
        return {"exists": False}
    info = {"exists": True, "mb": round(db.stat().st_size / 1048576, 2)}
    wal = profile / "state.db-wal"
    if wal.exists():
        info["wal_mb"] = round(wal.stat().st_size / 1048576, 2)
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=5)
        try:
            info["messages"] = con.execute("select count(*) from messages").fetchone()[0]
            try:
                info["sessions"] = con.execute("select count(*) from sessions").fetchone()[0]
            except sqlite3.Error:
                pass
            try:
                rows = con.execute(
                    "select name, round(sum(pgsize)/1048576.0,2) mb from dbstat "
                    "group by name order by mb desc limit 5").fetchall()
                info["top_tables"] = [{"name": r[0], "mb": r[1]} for r in rows]
            except sqlite3.Error:
                info["top_tables"] = []
        finally:
            con.close()
    except sqlite3.Error as exc:
        info["error"] = str(exc)[:120]
    return info


# --- the pass ---------------------------------------------------------------
def audit_one(pid: str, profile: Path, home: Path, baseline_rules: list[str]) -> dict:
    flags: list[dict] = []
    soul = soul_path(profile, home)
    mem_file = profile / "memories" / "MEMORY.md"
    user_file = profile / "memories" / "USER.md"
    mem_cap, user_cap = memory_caps(profile)

    soul_bytes = soul.stat().st_size if soul.exists() else 0
    mem_chars = len(mem_file.read_text(encoding="utf-8", errors="replace")) if mem_file.exists() else 0
    user_chars = len(user_file.read_text(encoding="utf-8", errors="replace")) if user_file.exists() else 0
    skills = count_skills(profile)
    db = db_stats(profile)

    rec = {
        "profile": pid,
        "path": str(profile),
        "soul_bytes": soul_bytes,
        "soul_kb": round(soul_bytes / 1024, 2),
        "memory_chars": mem_chars,
        "memory_cap": mem_cap,
        "memory_pct": round(mem_chars / mem_cap * 100, 1) if mem_cap else None,
        "user_chars": user_chars,
        "user_cap": user_cap,
        "user_pct": round(user_chars / user_cap * 100, 1) if user_cap else None,
        "skills": skills,
        "external_dirs": external_dirs(profile),
        "state_db": db,
        "flags": flags,
    }

    # soul size against the provisional band: only going over it is a problem
    lo, hi = SOUL_BAND_KB
    if soul_bytes > hi * 1024:
        flags.append({"code": "soul_band", "level": "flag",
                      "detail": f"soul {rec['soul_kb']} KB over the {lo}-{hi} KB band "
                                f"(band is provisional, not a decided rule)"})
    elif soul_bytes and soul_bytes < lo * 1024:
        flags.append({"code": "soul_thin", "level": "info",
                      "detail": f"soul {rec['soul_kb']} KB, under the {lo} KB floor — "
                                f"check the rules are present, not that it is short"})

    # memory against its caps
    if mem_file.exists() and mem_cap and rec["memory_pct"] >= MEMORY_FLAG_PCT:
        flags.append({"code": "memory_pct", "level": "flag",
                      "detail": f"MEMORY.md at {mem_chars}/{mem_cap} chars ({rec['memory_pct']}%)"})
    if user_file.exists() and user_cap and rec["user_pct"] >= MEMORY_FLAG_PCT:
        flags.append({"code": "user_pct", "level": "flag",
                      "detail": f"USER.md at {user_chars}/{user_cap} chars ({rec['user_pct']}%)"})
    if not mem_file.exists() and not user_file.exists():
        flags.append({"code": "memory_absent", "level": "info",
                      "detail": "no memory files yet (unused profile)"})

    # a line present in both soul and memory
    soul_lines = content_lines(soul)
    mem_lines = content_lines(mem_file) + content_lines(user_file)
    for line in soul_lines:
        for other in mem_lines:
            if same_rule(line, other):
                flags.append({"code": "soul_memory_dup", "level": "flag",
                              "detail": f"in soul and memory: {line[:110]}"})
                break

    # a rule restated outside the soul's marked block
    own_lines, shared_lines = split_soul(soul)
    for line in own_lines:
        for rule in baseline_rules + shared_lines:
            if same_rule(line, rule):
                flags.append({"code": "baseline_dup", "level": "flag",
                              "detail": f"rule restated outside the marked block: {line[:110]}"})
                break
    for i, line in enumerate(own_lines):
        for other in own_lines[i + 1:]:
            if same_rule(line, other):
                flags.append({"code": "soul_self_dup", "level": "flag",
                              "detail": f"said twice in one soul: {line[:110]}"})
                break

    # the store on disk
    if db.get("exists"):
        if db["mb"] >= STATE_DB_WATCH_MB:
            flags.append({"code": "state_db", "level": "flag",
                          "detail": f"state.db {db['mb']} MB is past the "
                                    f"{STATE_DB_WATCH_MB:.0f} MB watch line "
                                    f"({db.get('messages', '?')} messages)"})
        elif (db.get("messages", 0) >= 100 and db.get("messages") and
              db["mb"] / db["messages"] > 0.02):
            flags.append({"code": "state_db_density", "level": "info",
                          "detail": f"{db['mb']} MB over {db['messages']} messages — "
                                    f"few long sessions rather than many short ones"})

    return rec


def render(records: list[dict]) -> str:
    out = []
    for r in records:
        out.append(f"profile {r['profile']}  ({r['path']})")
        out.append(f"  soul            {r['soul_kb']} KB")
        mem = f"{r['memory_chars']}/{r['memory_cap']} chars" if r["memory_cap"] else "?"
        usr = f"{r['user_chars']}/{r['user_cap']} chars" if r["user_cap"] else "?"
        out.append(f"  MEMORY.md       {mem}" + (f"  ({r['memory_pct']}%)" if r["memory_pct"] else ""))
        out.append(f"  USER.md         {usr}" + (f"  ({r['user_pct']}%)" if r["user_pct"] else ""))
        out.append(f"  skills          {r['skills']} SKILL.md files (local)" +
                   (f"; external: {', '.join(r['external_dirs'])}" if r["external_dirs"] else ""))
        db = r["state_db"]
        if db.get("exists"):
            wal = f" (+{db['wal_mb']} MB WAL)" if db.get("wal_mb") else ""
            out.append(f"  state.db        {db['mb']} MB{wal}"
                       + (f", {db['messages']} messages" if "messages" in db else ""))
        else:
            out.append("  state.db        absent")
        if r["flags"]:
            out.append("  flags:")
            for f in r["flags"]:
                out.append(f"    [{f['level']}] {f['code']}: {f['detail']}")
        else:
            out.append("  flags: none")
        out.append("")
    total = sum(1 for r in records for f in r["flags"] if f["level"] == "flag")
    out.append(f"{len(records)} profile(s), {total} flag(s). "
               f"Read-only pass: nothing changed. Propose a diff; the person applies it.")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only context audit of a Hermes profile.")
    ap.add_argument("--profile", default=None,
                    help="profile id, or a path to a profile directory, or 'all'")
    ap.add_argument("--all", action="store_true", help="every profile on this machine")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    home = hermes_home()
    selector = "all" if args.all else args.profile
    targets = resolve_profiles(selector, home)
    if not targets:
        raise SystemExit(f"no profiles found under {home}")

    rules = shipped_rules()
    records = [audit_one(pid, path, home, rules) for pid, path in targets]
    if args.json:
        print(json.dumps({"hermes_home": str(home), "profiles": records,
                          "soul_band_kb": list(SOUL_BAND_KB),
                          "state_db_watch_mb": STATE_DB_WATCH_MB}, indent=2))
    else:
        print(render(records))


if __name__ == "__main__":
    main()
