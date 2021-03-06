"""MIDI rendering and playback methods."""
from enum import IntEnum
from typing import AnyStr
import traceback

try:
    from . import mididriver
except ImportError:
    traceback.print_exc()

try:
    import libmidi  # noqa
except ImportError:
    pass


class MIDIException(Exception):
    """MIDI error."""


class ReverbPreset(IntEnum):
    """Parameter settings for reverb effect."""

    OFF = -1  #: Reverb effect off
    LARGE_HALL = 0  #: Large hall preset
    HALL = 1  #: Hall preset
    CHAMBER = 2  #: Chamber preset
    ROOM = 3  #: Room preset


class Synthesizer:
    """MIDI Synthesizer."""

    _started = False
    _volume = 90
    _reverb = ReverbPreset.OFF

    def __init__(self):
        if not Synthesizer._started:
            if not mididriver.init():
                raise MIDIException("MIDI init failed.")
            self.volume = 90
            self.reverb = ReverbPreset.OFF
            Synthesizer._started = True

    @property
    def config(self) -> dict:
        """Synthesizer configuration dictionary."""
        return mididriver.get_config()

    @property
    def volume(self) -> int:
        """Master volume in dB, 100 is max.

        :getter: Returns the volume for the mix engine.
        :setter: Set the master volume for the mix engine.
        """
        return Synthesizer._volume

    @volume.setter
    def volume(self, volume):
        if not mididriver.set_volume(volume):
            raise MIDIException("Set master volume failed.")
        Synthesizer._volume = volume

    @property
    def reverb(self) -> ReverbPreset:
        """Reverb effect preset.

        :getter: Returns curently used :class:`ReverbPreset`.
        :setter: Set :class:`ReverbPreset` to use.
        """
        return Synthesizer._reverb

    @reverb.setter
    def reverb(self, reverb):
        if not mididriver.set_reverb(reverb):
            raise MIDIException("Set reverb effect preset failed.")
        Synthesizer._reverb = reverb

    def close(self):
        """Stop MIDI rendering and playback."""
        mididriver.close()
        Synthesizer._started = False

    def write(self, data: AnyStr):
        """Write MIDI commands to synhtesizer stream."""
        if not mididriver.write(bytes(data)):
            raise MIDIException("Write MIDI stream failed.")
