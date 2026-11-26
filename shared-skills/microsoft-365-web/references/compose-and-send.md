# Composing and sending in Outlook web

The compose pane is a small editor with its own rules, and the send surface is one click from
sent. These steps were exercised end to end; follow them in order rather than improvising clicks.

## Filling the message

1. **New mail**: click the button whose accessible name matches `/New mail|New message/`.
2. **To**: click the To row, `cdp('Input.insertText', text=address)`, then dispatch an Enter key
event so the address resolves into a recipient chip. Verify a chip appeared with the person's
name; a raw string in the field is not a recipient.
3. **Cc/Bcc**: the `Cc` button opens the address book rather than a field. Cancel it and type into
the Cc row, or the recipient goes into the wrong place.
4. **Subject**: `document.querySelector('input[aria-label=Subject]')`, focus it, then insertText.
5. **Body**: `document.querySelector('[contenteditable=true][role=textbox]')`, focus it, and send
the whole body in one `cdp('Input.insertText')` call. Newlines survive as paragraph breaks, so
write the prose you want rather than assembling it line by line.
6. **Verify before and after sending**: the compose header reading `Draft saved at HH:MM` plus a
row in Drafts proves the draft; a row in **Sent Items** with the recipient, subject and time
proves the send. A closed compose window proves nothing.

## Attaching a file

Use `DOM.setFileInputFiles` on an unrestricted input, never the image one:

```python
doc = cdp('DOM.getDocument', depth=1)
ids = cdp('DOM.querySelectorAll', nodeId=doc['root']['nodeId'], selector='input[type=file]')['nodeIds']
cdp('DOM.setFileInputFiles', files=['/abs/path/report.pdf'], nodeId=ids[1])
```

The compose pane holds four `input[type=file]` elements. The first carries `accept="image/*"`
and answers anything else with "wasn't inserted because it isn't a supported image file type" —
that message means the wrong input was used, not that attachments are impossible. Enumerate, skip
the one with `accept`, set the file on the next, then wait for the attachment chip showing filename
and size before doing anything else. Confirm the sent message in Sent Items afterwards.

- **Synthetic drag-and-drop does not attach.** `Input.dispatchDragEvent` carrying `files` returns
  success and leaves the message with no attachment. Do not spend calls on it.
- **A set aimed at the image input can take the compose window down.** If the window vanishes
  mid-attempt, look in Drafts: the message and any attachment usually survive intact.
- **The "Attachment reminder" modal** appears when the body mentions an attachment and none is
  present. It has **Send** and **Don't send**, and the send is not complete until the modal's Send
  is clicked.

## Sending a document to read later

When the owner asks for research, cost tables or a briefing "as a file I can read later", send a
typeset PDF. Markdown pasted into a mail body loses its tables, wraps badly on a phone, and reads
as a work in progress.

1. Write styled HTML: A4 `@page` margins, a sans-serif stack, thin table rules, `td.num` for right
aligned figures, `page-break-inside: avoid` on tables.
2. Print it with the Chrome already on the machine:

   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
     --no-pdf-header-footer --print-to-pdf="brief.pdf" "file://$PWD/brief.html"
   ```

3. Check the file exists and the page count came out as intended before sending.
4. Attach it, and hand the owner the PDF in the chat as well so they have it whether or not the
   mail lands where they expected.

Reserve the inline-markdown fallback (a ~13k character document inserts and renders in one
`insertText` call) for when attachment genuinely fails, and say in the message that the content is
inline rather than attached.

**External personal addresses.** Sending work material to a personal mailbox is the owner's call,
not a boundary to argue: confirm the recipient is one they named, say what you checked is not in
the file (client names, contact details, another party's pricing), then send. If something
sensitive is in it, flag it and let them decide rather than refusing.

## Rewriting a body

- **A DOM Range plus Backspace does not clear the body.** Selecting with `selectNodeContents` and
  pressing Backspace can leave the old text in place, and the replacement lands on top of it. To
  rewrite: `el.focus()`, `document.execCommand('selectAll', false, null)`, dispatch Delete, then
  check `el.innerText.length` is about zero before inserting the new body.
- **Clicking an unrelated row while compose is open opens another draft under you.** Read the
  subject input and the To chips before editing, or a "rewrite" lands in somebody else's message.
- **Update the existing draft rather than composing a second one.** A reply to "make it more
  casual" is an edit of the draft they already have; two drafts to one person is clutter the
  principal cleans up.
- **One `insertText` call per field.** Typing a paragraph character by character through key
  events is slow enough to hit tool timeouts.
