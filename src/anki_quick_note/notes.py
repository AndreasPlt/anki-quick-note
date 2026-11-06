"""Quick notes as lines in a note field - no Anki imports.

A field holds one note per line. Lines written here are joined with `<br>`;
lines typed in Anki's own editor (desktop or phone) may come as `<div>`s instead,
so reading accepts both.
"""

from __future__ import annotations

import html
import re
from collections.abc import Mapping, Sequence
from datetime import date

_BREAK = re.compile(r"<br\s*/?>|</?(?:div|p)\b[^>]*>", re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class NoField(Exception):  # noqa: N818 - a refusal shown to the user, not an error
    """This note type takes no quick notes; the message says why."""


def field_for(note_type: str, field_names: Sequence[str], mapping: Mapping[str, str]) -> str:
    """The field quick notes go into for this note type."""
    field = mapping.get(note_type)
    if not field:
        raise NoField(f"No notes field configured for {note_type}")
    if field not in field_names:
        raise NoField(f"{note_type} has no field {field}")
    return field


def entry(text: str, prefix: str, card_type: str, deck: str, today: date | None = None) -> str:
    """The line to store: the configured prefix, filled in, then the text."""
    values = {"card_type": card_type, "deck": deck, "date": (today or date.today()).isoformat()}
    return prefix.format_map(values) + " ".join(text.split())


def append(field_html: str, line: str) -> str:
    escaped = html.escape(line, quote=False)
    return f"{field_html}<br>{escaped}" if lines(field_html) else escaped


def lines(field_html: str) -> list[str]:
    """The field's notes as plain text, one per line."""
    text = html.unescape(_TAG.sub("", _BREAK.sub("\n", field_html)))
    return [line.strip() for line in text.splitlines() if line.strip()]
