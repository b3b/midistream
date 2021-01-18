"""MIDI rendering and playback methods."""
from typing import AnyStr
import traceback

try:
    from . import mididriver
except ImportError:
    traceback.print_exc()

try:
    import libmidi
except ImportError:
    pass


class MIDIException(Exception):
    """MIDI error."""


class Syntesizer:
    """MIDI Syntesizer."""

    _started = False
    _volume = 90

    def __init__(self):
        if not Syntesizer._started:
            if not mididriver.init():
                raise MIDIException("MIDI init failed.")
            self.volume = 90
            Syntesizer._started = True

    @property
    def config(self) -> dict:
        """Syntesizer configuration dictionary."""
        return mididriver.get_config()

    @property
    def volume(self) -> int:
        """Master volume in dB, 100 is max.

        :getter: Returns the volume for the mix engine.
        :setter: Set the master volume for the mix engine.
        """
        return Syntesizer._volume

    @volume.setter
    def volume(self, volume):
        if not mididriver.set_volume(volume):
            raise MIDIException("Set master volume failed.")
        Syntesizer._volume = volume

    def close(self):
        """Stop MIDI rendering and playback."""
        mididriver.close()
        Syntesizer._started = False

    def write(self, data: AnyStr):
        """Write MIDI commands to syntesizer stream."""
        if not mididriver.write(bytes(data)):
            raise MIDIException("Write MIDI stream failed.")
