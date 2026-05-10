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

import midistream.synthesizer as synthesizer
from midistream import MIDIException, Synthesizer, ReverbPreset

synthesizer.mididriver = mididriver
synthesizer._mididriver_import_error = None


@pytest.fixture(autouse=True)
def uninitialized_midi():
    Synthesizer._started = False
    Synthesizer._volume = 90
    Synthesizer._reverb = ReverbPreset.OFF
    mididriver._result = 1
    synthesizer.mididriver = mididriver
    synthesizer._mididriver_import_error = None


def test_initizlized():
    Synthesizer()
    assert Synthesizer._started


def test_init_error():
    mididriver._result = 0
    with pytest.raises(MIDIException):
        Synthesizer()
    assert not Synthesizer._started


def test_missing_mididriver_raises_midi_exception(monkeypatch):
    import_error = ImportError("missing libmidi.so")

    monkeypatch.setattr(synthesizer, "_mididriver_import_error", import_error)
    monkeypatch.setattr(synthesizer, "mididriver", None)

    with pytest.raises(MIDIException, match="MIDI driver is unavailable") as exc_info:
        Synthesizer()

    assert exc_info.value.__cause__ is import_error
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
