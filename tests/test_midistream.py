import pytest

import libmidi
from midistream import MIDIException, Syntesizer, ReverbPreset


@pytest.fixture(autouse=True)
def uninitialized_midi():
    Syntesizer._started = False
    libmidi._result = 1


def test_initizlized():
    Syntesizer()
    assert Syntesizer._started


def test_init_error():
    libmidi._result = 0
    with pytest.raises(MIDIException):
        Syntesizer()
    assert not Syntesizer._started


def test_config_returned():
    assert Syntesizer().config['libVersion'] == 0xAABBCCDD


def test_volume_set():
    assert Syntesizer().volume != 100
    Syntesizer().volume = 100
    assert Syntesizer().volume == 100


def test_volume_set_error():
    Syntesizer().volume = 1

    libmidi._result = 0
    with pytest.raises(MIDIException):
        Syntesizer().volume = 100

    libmidi._result = 1
    assert Syntesizer().volume == 1


def test_reverb_set():
    assert Syntesizer().reverb != ReverbPreset.ROOM
    Syntesizer().reverb = ReverbPreset.ROOM
    assert Syntesizer().reverb == ReverbPreset.ROOM


def test_reverb_set_error():
    Syntesizer().reverb = ReverbPreset.OFF

    libmidi._result = 0
    with pytest.raises(MIDIException):
        Syntesizer().reverb = ReverbPreset.ROOM

    libmidi._result = 1
    assert Syntesizer().reverb == ReverbPreset.OFF


def test_closed():
    Syntesizer().close()
    assert not Syntesizer._started


def test_write_completed():
    Syntesizer().write(b'test')


def test_write_error():
    libmidi._result = 0
    with pytest.raises(MIDIException):
        Syntesizer().write(b'test')
