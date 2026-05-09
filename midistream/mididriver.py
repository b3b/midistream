"""ctypes wrapper for Android MidiDriver libmidi.so."""

import ctypes

EAS_U8 = ctypes.c_uint8
EAS_U32 = ctypes.c_uint32
EAS_I32 = ctypes.c_int32
EAS_BOOL = ctypes.c_uint32
JBOOLEAN = ctypes.c_uint8
JINT = ctypes.c_int32


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
        ("buildGUID", ctypes.c_char_p),
    ]


try:
    _lib = ctypes.CDLL("libmidi.so")
except OSError as exc:
    raise ImportError("Unable to load libmidi.so") from exc

try:
    _lib.EAS_Config.argtypes = []
    _lib.EAS_Config.restype = ctypes.POINTER(S_EAS_LIB_CONFIG)
except AttributeError:
    pass

_lib.midi_init.argtypes = []
_lib.midi_init.restype = JBOOLEAN

_lib.midi_shutdown.argtypes = []
_lib.midi_shutdown.restype = JBOOLEAN

_lib.midi_write.argtypes = [
    ctypes.POINTER(EAS_U8),
    JINT,
]
_lib.midi_write.restype = JBOOLEAN

_lib.midi_setVolume.argtypes = [JINT]
_lib.midi_setVolume.restype = JBOOLEAN

_lib.midi_setReverb.argtypes = [JINT]
_lib.midi_setReverb.restype = JBOOLEAN


def init():
    return bool(_lib.midi_init())


def get_config():
    if not hasattr(_lib, "EAS_Config"):
        raise NotImplementedError("EAS_Config is not exported by libmidi.so")

    config = _lib.EAS_Config().contents
    return {
        "libVersion": int(config.libVersion),
        "checkedVersion": bool(config.checkedVersion),
        "maxVoices": int(config.maxVoices),
        "numChannels": int(config.numChannels),
        "sampleRate": int(config.sampleRate),
        "mixBufferSize": int(config.mixBufferSize),
        "filterEnabled": bool(config.filterEnabled),
        "buildTimeStamp": int(config.buildTimeStamp),
        "buildGUID": config.buildGUID.decode() if config.buildGUID else "",
    }


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
