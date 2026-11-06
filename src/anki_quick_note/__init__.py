"""Anki add-on: append a quick note to a field of the card under review.

Press the shortcut (default `n`) while reviewing, type a line, Enter. The line goes
into the field configured for the card's note type, without opening the editor.

* :mod:`anki_quick_note.notes` - field and line handling; no Anki imports.
* :mod:`anki_quick_note.dialog` - the input window.
"""

from __future__ import annotations

from . import notes

try:  # pragma: no cover - only available inside Anki
    from aqt import gui_hooks, mw
    from aqt.operations.note import update_note
    from aqt.utils import tooltip
except ImportError:  # imported outside Anki (tests)
    gui_hooks = mw = update_note = tooltip = None


def _config() -> dict:
    return mw.addonManager.getConfig(__name__) or {}


def _open() -> None:
    reviewer = mw.reviewer
    if reviewer.card is None:
        return
    card = reviewer.card
    note = card.note(reload=True)
    config = _config()
    try:
        field = notes.field_for(note.note_type()["name"], note.keys(), config.get("fields") or {})
    except notes.NoField as refusal:
        tooltip(str(refusal))
        return

    card_type = card.template()["name"]
    shown = notes.lines(note[field]) if reviewer.state == "answer" else []

    def save(text: str) -> None:
        try:
            line = notes.entry(
                text,
                str(config.get("prefix", "")),
                card_type=card_type,
                deck=mw.col.decks.name(card.current_deck_id()),
            )
        except (KeyError, ValueError) as error:
            tooltip(f"Quick Note: bad prefix in config ({error})")
            return
        # Write through the reviewer's own copy of the note, reloaded first: the save is
        # made as the reviewer's change so the card is not redrawn (no audio replay), which
        # also means the reviewer never reloads it - and the Edit window opens on that copy.
        # Had we saved a separate copy, a later Edit would show and save back the old field.
        fresh = card.note(reload=True)
        fresh[field] = notes.append(fresh[field], line)
        update_note(parent=mw, note=fresh).success(lambda _: tooltip("Noted")).run_in_background(
            initiator=reviewer
        )

    from .dialog import NoteDialog

    dialog = NoteDialog(mw, f"Note for {card_type} card · {field}", shown, save)
    dialog.finished.connect(lambda _: mw.web.setFocus())  # back to the reviewer's keys
    dialog.show()


def _on_shortcuts(state: str, shortcuts: list) -> None:
    if state == "review":
        shortcuts.append((_config().get("shortcut", "n"), _open))


if gui_hooks is not None:  # pragma: no cover - only inside Anki
    gui_hooks.state_shortcuts_will_change.append(_on_shortcuts)
