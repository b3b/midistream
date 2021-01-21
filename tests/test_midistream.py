import pytest

import libmidi
from midistream import MIDIException, Synthesizer, ReverbPreset


@pytest.fixture(autouse=True)
def uninitialized_midi():
    Synthesizer._started = False
    libmidi._result = 1


def test_initizlized():
    Synthesizer()
    assert Synthesizer._started


def test_init_error():
    libmidi._result = 0
    with pytest.raises(MIDIException):
        Synthesizer()
    assert not Synthesizer._started


def test_config_returned():
    assert Synthesizer().config['libVersion'] == 0xAABBCCDD


def test_volume_set():
    assert Synthesizer().volume != 100
    Synthesizer().volume = 100
    assert Synthesizer().volume == 100


def test_volume_set_error():
    Synthesizer().volume = 1

    libmidi._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().volume = 100

    libmidi._result = 1
    assert Synthesizer().volume == 1


def test_reverb_set():
    assert Synthesizer().reverb != ReverbPreset.ROOM
    Synthesizer().reverb = ReverbPreset.ROOM
    assert Synthesizer().reverb == ReverbPreset.ROOM


def test_reverb_set_error():
    Synthesizer().reverb = ReverbPreset.OFF

    libmidi._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().reverb = ReverbPreset.ROOM

    libmidi._result = 1
    assert Synthesizer().reverb == ReverbPreset.OFF


def test_closed():
    Synthesizer().close()
    assert not Synthesizer._started


def test_write_completed():
    Synthesizer().write(b'test')


def test_write_error():
    libmidi._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().write(b'test')
