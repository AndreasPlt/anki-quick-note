# anki-quick-note

Anki add-on: append a quick note to a field of the card under review, without opening the
editor.

- `n` while reviewing (question or answer side) opens a one-line input. Enter appends the line
  to the note's configured field, Esc cancels. Undo with ⌘Z / Ctrl+Z.
- The field is configured per note type; note types that are not listed take no notes.
- Each note is one line, prefixed with the card type by default: `[Listening] sentence unclear`.
- On the answer side the input also shows the notes already on the card.

The field must exist in the note type; the add-on never creates it. Notes typed into the same
field in Anki's editor (desktop or phone) live alongside these.

## Install

```bash
uv run python scripts/install.py
```

This builds `dist/anki_quick_note.ankiaddon` and opens it with Anki. Confirm the install and
restart Anki. `uv run python scripts/build.py` only builds the file. Configure under Tools → Add-ons → Quick Note → Config; see
[`config.md`](src/anki_quick_note/config.md).

## Layout

- `notes.py` — which field, the line format, reading and appending. No Anki imports.
- `dialog.py` — the input window. A window of its own, so the reviewer's keys cannot fire while
  typing.
- `__init__.py` — the shortcut and the write, made as the reviewer's own change so the card is
  not redrawn (no audio replay).

## Development

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```
