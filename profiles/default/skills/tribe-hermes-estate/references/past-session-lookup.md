# Finding how a past session did something

"The previous session accessed it" is a testable claim. The answer is in a profile's
`state.db` — not in this chat, and not in the repo.

## Recipe

1. **Pick the store.** Each profile has its own: `~/.hermes/state.db` for the builder
   (`default`), `~/.hermes/profiles/<name>/state.db` for `admin`, `ea` and the rest. Day-job
   work (a form, a thread in the inbox, a diary change) is almost always in `admin`.
2. **Query read-only, with a distinctive phrase** — a filename, a form name, a counter
   label. Never open the store for writing:

```bash
cd ~/.hermes && python3 - <<'EOF'
import sqlite3
c = sqlite3.connect("file:profiles/admin/state.db?mode=ro", uri=True)
term = "discovery survey"
for sid, role, content in c.execute(
    "select session_id, role, content from messages where lower(content) like ? order by id",
    (f"%{term}%",)):
    i = content.lower().find(term)
    print(sid[:20], role, content[max(0, i-200):i+300].replace("\n", " "))
EOF
```

   Keep the printed window small. A whole session is hundreds of messages of tool output;
   the route is always in a 300-character window around the match.
3. **Prefer `role='tool'` matches for the route.** Tool output shows the URL, the path or the
   command that worked. Assistant prose says what was concluded, which is usually the part
   that has since gone stale.

## Schema traps

- `messages` keys on `session_id`; the `sessions` table's primary key is `id`, so joining on
  `s.session_id` fails with "no such column".
- Some assistant rows carry empty `content` — long replies can be stored elsewhere in the
  record. Scroll neighbouring rows instead of concluding the session is blank.
- The built-in history search can return zero sessions for a phrase the table plainly holds.
  When it does, fall back to the `LIKE` query above rather than telling the user the
  conversation does not exist.

## Report the route, not the old answer

The transcript proves how something was reached: which app, which URL, which file, which
command. That route is what a new session needs. The *content* it produced has moved on — old
response counts, old diary entries, old file contents — so state the route and mark the old
figures as dated.

A worked example: a form's response workbook sitting in OneDrive is a cloud stub, and the
app's "open results in Excel" handed the viewer an empty grid, so the responses were read
through the form's own web results page, respondent by respondent, in a browser that already
held the Microsoft login. The lesson a future session needs is "read responses in the web app,
not the workbook" — and that the login belongs to the profile that signed in, so the task has to
run in that profile.

## Boundary

This is for recovering a procedure that was already sanctioned on Sam's own machine. Do not go
mining another profile's conversation for personal content, never quote message text into the
repo, a doc or the shared library, and stop if the phrase you are searching for is one of the
things `config/exclusions.txt` protects.
