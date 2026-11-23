#!/usr/bin/env python3
"""Build a review page for an extracted roster: mark who is still in the org.

    python3 roster-review.py roster-2026.json roster-review.html

The page is self-contained (data inlined, no fetch), so it works from file://
and inside the Hermes preview frame. Ticking a person "left" removes them from
the count and adds them to a copyable list, which is the fastest way to prune a
directory exported from a PDF.
"""

import json
import pathlib
import sys

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Roster review — __TITLE__</title>
<style>
  .wrap { font-family: inherit; color: var(--foreground, #e9e9ea); max-width: 960px; }
  h1 { font-size: 1.05rem; font-weight: 600; margin: 0 0 4px; }
  .sub { color: var(--muted-foreground, #a0a0a8); font-size: .8rem; margin: 0 0 18px; line-height: 1.45; }
  .toolbar { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 14px; }
  .count { font-size: .78rem; color: var(--muted-foreground, #a0a0a8); }
  .count b { color: var(--foreground, #e9e9ea); }
  button {
    font: inherit; font-size: .74rem; cursor: pointer; border-radius: 6px; padding: 5px 10px;
    background: transparent; color: var(--foreground, #e9e9ea);
    border: 1px solid var(--border, #3a3a40);
  }
  button:hover { border-color: var(--accent, #ff7a1a); color: var(--accent, #ff7a1a); }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  @media (max-width: 720px) { .cols { grid-template-columns: 1fr; } }
  h2 { font-size: .67rem; text-transform: uppercase; letter-spacing: .08em;
       color: var(--muted-foreground, #a0a0a8); margin: 0 0 8px; }
  .row { display: flex; align-items: center; gap: 8px; padding: 5px 0;
         border-bottom: 1px dashed var(--border, #3a3a40); font-size: .8rem; }
  .row .name { font-weight: 600; min-width: 84px; }
  .row .title { color: var(--muted-foreground, #a0a0a8); flex: 1; font-size: .74rem; }
  .badge {
    display: inline-block; font-size: .58rem; text-transform: uppercase; letter-spacing: .06em;
    border: 1px solid var(--border, #3a3a40); border-radius: 4px; padding: 0 4px;
    color: var(--muted-foreground, #a0a0a8); margin-left: 5px; vertical-align: 1px;
  }
  .badge.off { border-color: var(--accent, #ff7a1a); color: var(--accent, #ff7a1a); }
  .row.gone { opacity: .45; }
  .row.gone .name { text-decoration: line-through; }
  .seg { display: flex; border: 1px solid var(--border, #3a3a40); border-radius: 5px; overflow: hidden; }
  .seg button { border: 0; border-radius: 0; padding: 3px 8px; font-size: .68rem; opacity: .6; }
  .seg button.on { background: var(--accent, #ff7a1a); color: #12121a; opacity: 1; }
  .out { margin-top: 18px; padding: 10px; border: 1px solid var(--border, #3a3a40);
         border-radius: 6px; font-size: .74rem; white-space: pre-wrap;
         color: var(--muted-foreground, #a0a0a8); display: none; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Roster review — __TITLE__</h1>
  <p class="sub">__NOTE__</p>
  <div class="toolbar">
    <span class="count" id="count"></span>
    <button id="all-here">Everyone here</button>
    <button id="copy">Copy list of leavers</button>
  </div>
  <div class="cols" id="cols"></div>
  <div class="out" id="out"></div>
</div>
<script>
const ROSTER = __DATA__;
// Inside the Hermes frame the theme variables are injected; opened standalone they
// are missing, so fall back to a dark page rather than light text on white.
if (!getComputedStyle(document.documentElement).getPropertyValue('--foreground').trim()) {
  const r = document.documentElement.style;
  [['--foreground','#e9e9ea'],['--muted-foreground','#a0a0a8'],['--border','#3a3a40'],
   ['--card','#1b1b1f'],['--accent','#ff7a1a']].forEach(([k,v]) => r.setProperty(k,v));
  r.setProperty('background','#131316');
  document.documentElement.style.colorScheme = 'dark';
}

const state = {};
ROSTER.people.forEach(p => state[p.name] = p.status === "left" ? "left" : "here");

function render() {
  const cols = document.getElementById("cols");
  const byDiv = {};
  ROSTER.people.forEach(p => { (byDiv[p.division] = byDiv[p.division] || []).push(p); });
  cols.innerHTML = Object.keys(byDiv).map(div => `
    <div><h2>${div} (${byDiv[div].length})</h2>
      ${byDiv[div].map(p => `
        <div class="row ${state[p.name] === "left" ? "gone" : ""}" data-name="${p.name}">
          <span class="name">${p.name}</span>
          <span class="title">${p.title}${p.engagement && p.engagement !== "employee" ? `<span class="badge ${p.engagement === "offshore" ? "off" : ""}">${p.location}</span>` : ""}</span>
          <span class="seg">
            <button data-v="here" class="${state[p.name] !== "left" ? "on" : ""}">here</button>
            <button data-v="left" class="${state[p.name] === "left" ? "on" : ""}">left</button>
          </span>
        </div>`).join("")}
    </div>`).join("");

  const here = ROSTER.people.filter(p => state[p.name] !== "left").length;
  const left = ROSTER.people.length - here;
  const off = ROSTER.people.filter(p => p.engagement === "offshore" && state[p.name] !== "left").length;
  const con = ROSTER.people.filter(p => p.engagement === "consultant" && state[p.name] !== "left").length;
  document.getElementById("count").innerHTML =
    `<b>${here}</b> of ${ROSTER.people.length} still here · <b>${left}</b> marked left` +
    ` · <b>${off}</b> offshore · <b>${con}</b> consultant (not in-house)`;

  cols.querySelectorAll(".seg button").forEach(b => {
    b.onclick = () => {
      const name = b.closest(".row").dataset.name;
      state[name] = b.dataset.v;
      render();
    };
  });
}
window.roster = {
  leavers: () => ROSTER.people.filter(p => state[p.name] === "left").map(p => p.name),
  staying: () => ROSTER.people.filter(p => state[p.name] !== "left").map(p => p.name),
  summary: () => ({ total: ROSTER.people.length, left: window.roster.leavers(), here: window.roster.staying() })
};

document.getElementById("copy").onclick = () => {
  const gone = ROSTER.people.filter(p => state[p.name] === "left");
  const txt = gone.length
    ? `Gone (${gone.length}):\\n` + gone.map(p => `- ${p.name} — ${p.title}`).join("\\n")
    : "Nobody marked as left yet.";
  const out = document.getElementById("out");
  out.style.display = "block";
  out.textContent = txt;
  navigator.clipboard && navigator.clipboard.writeText(txt).catch(() => {});
};
document.getElementById("all-here").onclick = () => {
  ROSTER.people.forEach(p => state[p.name] = "here");
  render();
};
render();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src, dst = map(pathlib.Path, sys.argv[1:3])
    data = json.loads(src.read_text(encoding="utf-8"))
    html = (TEMPLATE
            .replace("__TITLE__", src.stem.replace("-", " "))
            .replace("__NOTE__", data.get("note", ""))
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    dst.write_text(html, encoding="utf-8")
    print(f"wrote {dst} ({len(data.get('people', []))} people)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
