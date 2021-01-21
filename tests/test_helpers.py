import pytest

from midistream.helpers import note_name


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
