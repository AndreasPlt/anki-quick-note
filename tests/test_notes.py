from __future__ import annotations

from datetime import date

import pytest

from anki_quick_note import notes

FIELDS = ["ZH", "Feedback", "PY"]
MAPPING = {"Chinese Vocab": "Feedback", "Basic": "Missing"}


def test_field_for_mapped_note_type():
    assert notes.field_for("Chinese Vocab", FIELDS, MAPPING) == "Feedback"


def test_unmapped_note_type_takes_no_notes():
    with pytest.raises(notes.NoField, match="No notes field configured for Cloze"):
        notes.field_for("Cloze", FIELDS, MAPPING)


def test_mapped_field_must_exist():
    with pytest.raises(notes.NoField, match="Basic has no field Missing"):
        notes.field_for("Basic", FIELDS, MAPPING)


def test_entry_fills_the_prefix_and_flattens_whitespace():
    line = notes.entry(
        "  sentence\tis  unclear ",
        "[{card_type} {date}] ",
        card_type="Listening",
        deck="Vocab",
        today=date(2026, 10, 16),
    )
    assert line == "[Listening 2026-10-16] sentence is unclear"


def test_entry_with_unknown_placeholder_raises():
    with pytest.raises(KeyError):
        notes.entry("x", "{nope}", card_type="Reading", deck="Vocab")


def test_append_to_empty_and_filled_field():
    assert notes.append("", "first") == "first"
    assert notes.append("first", "second") == "first<br>second"
    assert notes.append("<br>", "first") == "first"  # an editor-emptied field


def test_append_escapes_html():
    assert notes.append("", "a < b & c") == "a &lt; b &amp; c"
    assert notes.lines(notes.append("", "a < b & c")) == ["a < b & c"]


def test_lines_reads_our_breaks_and_editor_divs():
    assert notes.lines("one<br>two") == ["one", "two"]
    assert notes.lines("one<div>two</div><div>three&nbsp;</div>") == ["one", "two", "three"]
    assert notes.lines("") == []
