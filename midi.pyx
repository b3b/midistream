"""Stub for MidiDriver."""
from midistream.mididriver cimport *

cdef S_EAS_LIB_CONFIG _config
_result = 1

cdef EAS_U8 midi_init():
    print("midi_init()")
    return _result

cdef EAS_U8 midi_shutdown():
    print("midi_shutdown()")
    return _result

cdef S_EAS_LIB_CONFIG *EAS_Config():
    print("EAS_Config()")
    _config.libVersion = 0xAABBCCDD
    _config.buildGUID = ''
    return &_config

cdef EAS_U8 midi_write(EAS_U8 *bytes, EAS_I32 length):
    print(f"midi_write({bytes})")
    return _result

cdef EAS_U8 midi_setVolume(EAS_I32 volume):
    print(f"midi_setVolume({volume})")
    return _result
