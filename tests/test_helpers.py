import pytest

from midistream.helpers import Note, note_name, parse_note


@pytest.mark.parametrize(
    "note,expected", (
        (21, "A0"),
        (12, "C0"),
        (60, "C4"),
        (61, "Cs4"),
        (59, "B3"),
        (127, "G9"),
        (1000000, "E83332"),
        (11, "B-1"),
        (0, "C-1"),
        (-1000000, "Gs-83335"),
    )
)
def test_note_name(note, expected):
    assert note_name(note) == expected


@pytest.mark.parametrize(
    "text,expected", (
        ("A0", 21),
        ("C0", 12),
        ("C4", 60),
        ("Cs4", 61),
        ("Cb4", 59),
        ("cS4", 61),
        ("Db4", 61),
        ("Cb0", 11),
        ("G9", 127),
        ("Gs9", None),
        ("A9", None),
        ("A01", None),
        ("A-1", None),
    )
)
def test_parse_note(text, expected):
    if expected is None:
        with pytest.raises(ValueError):
            parse_note(text)
    else:
        assert parse_note(text) == expected


@pytest.mark.parametrize(
    "text,expected", (
        ("A0", 21),
        ("cb0", 11),
        ("A", None),
    )
)
def test_note(text, expected):
    if expected is None:
        with pytest.raises(ValueError):
            getattr(Note, text)
    else:
        assert getattr(Note, text) == expected
