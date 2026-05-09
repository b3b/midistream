import sys
import types

import pytest


class FakeMidiDriver(types.ModuleType):
    def __init__(self):
        super().__init__("midistream.mididriver")
        self._result = 1

    def init(self):
        return bool(self._result)

    def get_config(self):
        return {
            "libVersion": 0xAABBCCDD,
        }

    def close(self):
        return bool(self._result)

    def write(self, data):
        return bool(self._result)

    def set_volume(self, volume):
        return bool(self._result)

    def set_reverb(self, reverb):
        return bool(self._result)


mididriver = FakeMidiDriver()
sys.modules["midistream.mididriver"] = mididriver

import midistream.facade as facade
from midistream import MIDIException, Synthesizer, ReverbPreset

facade.mididriver = mididriver


@pytest.fixture(autouse=True)
def uninitialized_midi():
    Synthesizer._started = False
    Synthesizer._volume = 90
    Synthesizer._reverb = ReverbPreset.OFF
    mididriver._result = 1


def test_initizlized():
    Synthesizer()
    assert Synthesizer._started


def test_init_error():
    mididriver._result = 0
    with pytest.raises(MIDIException):
        Synthesizer()
    assert not Synthesizer._started


def test_config_returned():
    assert Synthesizer().config["libVersion"] == 0xAABBCCDD


def test_volume_set():
    assert Synthesizer().volume != 100
    Synthesizer().volume = 100
    assert Synthesizer().volume == 100


def test_volume_set_error():
    Synthesizer().volume = 1

    mididriver._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().volume = 100

    mididriver._result = 1
    assert Synthesizer().volume == 1


def test_reverb_set():
    assert Synthesizer().reverb != ReverbPreset.ROOM
    Synthesizer().reverb = ReverbPreset.ROOM
    assert Synthesizer().reverb == ReverbPreset.ROOM


def test_reverb_set_error():
    Synthesizer().reverb = ReverbPreset.OFF

    mididriver._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().reverb = ReverbPreset.ROOM

    mididriver._result = 1
    assert Synthesizer().reverb == ReverbPreset.OFF


def test_closed():
    Synthesizer().close()
    assert not Synthesizer._started


def test_write_completed():
    Synthesizer().write(b"test")


def test_write_error():
    mididriver._result = 0
    with pytest.raises(MIDIException):
        Synthesizer().write(b"test")
