"""Wrapper for EAS and MidiDriver functions."""
from mididriver cimport *


def init():
    return midi_init()


def get_config():
    cdef S_EAS_LIB_CONFIG *pLibConfig
    pLibConfig = EAS_Config()
    return pLibConfig[0]


def set_volume(volume):
    return midi_setVolume(volume)


def set_reverb(preset):
    return midi_setReverb(preset)


def close():
    return midi_shutdown()


def write(data):
    return midi_write(data, len(data))
