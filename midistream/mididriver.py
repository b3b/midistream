"""ctypes wrapper for Android MidiDriver libmidi.so."""

import ctypes

EAS_U8 = ctypes.c_uint8
EAS_U32 = ctypes.c_ulong
EAS_I32 = ctypes.c_long
EAS_BOOL = ctypes.c_uint
JBOOLEAN = ctypes.c_uint8


class S_EAS_LIB_CONFIG(ctypes.Structure):
    _fields_ = [
        ("libVersion", EAS_U32),
        ("checkedVersion", EAS_BOOL),
        ("maxVoices", EAS_I32),
        ("numChannels", EAS_I32),
        ("sampleRate", EAS_I32),
        ("mixBufferSize", EAS_I32),
        ("filterEnabled", EAS_BOOL),
        ("buildTimeStamp", EAS_U32),
        ("buildGUID", ctypes.c_void_p),
    ]


def _load_library():
    try:
        return ctypes.CDLL("libmidi.so")
    except OSError as exc:
        raise ImportError("Unable to load libmidi.so") from exc


def _configure_library(lib):
    try:
        lib.EAS_Config.argtypes = []
        lib.EAS_Config.restype = ctypes.POINTER(S_EAS_LIB_CONFIG)
    except AttributeError:
        pass

    lib.midi_init.argtypes = []
    lib.midi_init.restype = JBOOLEAN

    lib.midi_shutdown.argtypes = []
    lib.midi_shutdown.restype = JBOOLEAN

    lib.midi_write.argtypes = [
        ctypes.POINTER(EAS_U8),
        EAS_I32,
    ]
    lib.midi_write.restype = JBOOLEAN

    lib.midi_setVolume.argtypes = [EAS_I32]
    lib.midi_setVolume.restype = JBOOLEAN

    lib.midi_setReverb.argtypes = [EAS_I32]
    lib.midi_setReverb.restype = JBOOLEAN
    return lib


_lib = _configure_library(_load_library())


def init():
    return bool(_lib.midi_init())


def get_config():
    if not hasattr(_lib, "EAS_Config"):
        raise NotImplementedError("EAS_Config is not exported by libmidi.so")

    config_pointer = _lib.EAS_Config()
    if not config_pointer:
        raise RuntimeError("EAS_Config returned NULL")

    return _config_to_dict(config_pointer.contents)


def _config_to_dict(config):
    build_guid = _read_build_guid(config.buildGUID)

    return {
        "libVersion": int(config.libVersion),
        "checkedVersion": bool(config.checkedVersion),
        "maxVoices": int(config.maxVoices),
        "numChannels": int(config.numChannels),
        "sampleRate": int(config.sampleRate),
        "mixBufferSize": int(config.mixBufferSize),
        "filterEnabled": bool(config.filterEnabled),
        "buildTimeStamp": int(config.buildTimeStamp),
        "buildGUID": build_guid,
    }


def _read_build_guid(address):
    if not address:
        return b""

    return ctypes.cast(address, ctypes.c_char_p).value or b""


def close():
    return bool(_lib.midi_shutdown())


def shutdown():
    return close()


def write(data):
    payload = data if isinstance(data, bytes) else bytes(data)
    buf = (EAS_U8 * len(payload)).from_buffer_copy(payload)
    return bool(_lib.midi_write(buf, len(payload)))


def set_volume(volume):
    return bool(_lib.midi_setVolume(int(volume)))


def setVolume(volume):
    return set_volume(volume)


def set_reverb(reverb):
    return bool(_lib.midi_setReverb(int(reverb)))


def setReverb(reverb):
    return set_reverb(reverb)
