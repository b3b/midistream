import ctypes
import importlib.util
from pathlib import Path
from uuid import uuid4

import pytest


MODULE_PATH = Path(__file__).parents[1] / "midistream" / "mididriver.py"


class FakeFunc:
    def __init__(self, callback):
        self.callback = callback
        self.argtypes = None
        self.restype = None

    def __call__(self, *args):
        return self.callback(*args)


class FakeMidiLib:
    def __init__(self, result=1, with_config=True):
        self.result = result
        self.calls = []
        self.midi_init = FakeFunc(lambda: self._record("midi_init"))
        self.midi_shutdown = FakeFunc(lambda: self._record("midi_shutdown"))
        self.midi_write = FakeFunc(self._write)
        self.midi_setVolume = FakeFunc(
            lambda volume: self._record("midi_setVolume", volume)
        )
        self.midi_setReverb = FakeFunc(
            lambda reverb: self._record("midi_setReverb", reverb)
        )
        self._guid_buffer = ctypes.create_string_buffer(b"test-guid")

        if with_config:
            self.EAS_Config = FakeFunc(self._config)

    def _record(self, name, *args):
        self.calls.append((name, args))
        return self.result

    def _write(self, buf, length):
        payload = bytes(buf[:length])
        return self._record("midi_write", payload, length)

    def _config(self):
        config = self.config_type()
        config.libVersion = 0xAABBCCDD
        config.checkedVersion = 1
        config.maxVoices = 64
        config.numChannels = 16
        config.sampleRate = 44100
        config.mixBufferSize = 512
        config.filterEnabled = 0
        config.buildTimeStamp = 123456789
        config.buildGUID = ctypes.cast(self._guid_buffer, ctypes.c_void_p).value
        return ctypes.pointer(config)


def load_mididriver(monkeypatch, fake_lib):
    def fake_cdll(path):
        assert path == "libmidi.so"
        return fake_lib

    monkeypatch.setattr(ctypes, "CDLL", fake_cdll)

    module_name = f"_mididriver_under_test_{uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    fake_lib.config_type = module.S_EAS_LIB_CONFIG
    return module


def test_import_error_when_libmidi_cannot_be_loaded(monkeypatch):
    def fake_cdll(path):
        raise OSError("missing")

    monkeypatch.setattr(ctypes, "CDLL", fake_cdll)

    spec = importlib.util.spec_from_file_location("_missing_mididriver", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(ImportError, match="Unable to load libmidi.so"):
        spec.loader.exec_module(module)


def test_import_configures_ctypes_function_signatures(monkeypatch):
    fake_lib = FakeMidiLib()
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert fake_lib.EAS_Config.argtypes == []
    assert fake_lib.EAS_Config.restype == ctypes.POINTER(mididriver.S_EAS_LIB_CONFIG)
    assert fake_lib.midi_init.argtypes == []
    assert fake_lib.midi_init.restype is mididriver.JBOOLEAN
    assert fake_lib.midi_shutdown.argtypes == []
    assert fake_lib.midi_shutdown.restype is mididriver.JBOOLEAN
    assert fake_lib.midi_write.argtypes == [
        ctypes.POINTER(mididriver.EAS_U8),
        mididriver.EAS_I32,
    ]
    assert fake_lib.midi_write.restype is mididriver.JBOOLEAN
    assert fake_lib.midi_setVolume.argtypes == [mididriver.EAS_I32]
    assert fake_lib.midi_setVolume.restype is mididriver.JBOOLEAN
    assert fake_lib.midi_setReverb.argtypes == [mididriver.EAS_I32]
    assert fake_lib.midi_setReverb.restype is mididriver.JBOOLEAN


def test_config_struct_matches_native_layout(monkeypatch):
    fake_lib = FakeMidiLib()
    mididriver = load_mididriver(monkeypatch, fake_lib)

    class ExpectedConfig(ctypes.Structure):
        _fields_ = [
            ("libVersion", ctypes.c_ulong),
            ("checkedVersion", ctypes.c_uint),
            ("maxVoices", ctypes.c_long),
            ("numChannels", ctypes.c_long),
            ("sampleRate", ctypes.c_long),
            ("mixBufferSize", ctypes.c_long),
            ("filterEnabled", ctypes.c_uint),
            ("buildTimeStamp", ctypes.c_ulong),
            ("buildGUID", ctypes.c_void_p),
        ]

    assert ctypes.sizeof(mididriver.S_EAS_LIB_CONFIG) == ctypes.sizeof(ExpectedConfig)
    assert {
        name: getattr(mididriver.S_EAS_LIB_CONFIG, name).offset
        for name, _field_type in mididriver.S_EAS_LIB_CONFIG._fields_
    } == {
        name: getattr(ExpectedConfig, name).offset
        for name, _field_type in ExpectedConfig._fields_
    }


def test_init_and_shutdown_return_boolean_results(monkeypatch):
    fake_lib = FakeMidiLib(result=1)
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert mididriver.init() is True
    assert mididriver.close() is True
    assert mididriver.shutdown() is True

    fake_lib.result = 0

    assert mididriver.init() is False
    assert mididriver.close() is False


def test_get_config_returns_python_dictionary(monkeypatch):
    fake_lib = FakeMidiLib()
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert mididriver.get_config() == {
        "libVersion": 0xAABBCCDD,
        "checkedVersion": True,
        "maxVoices": 64,
        "numChannels": 16,
        "sampleRate": 44100,
        "mixBufferSize": 512,
        "filterEnabled": False,
        "buildTimeStamp": 123456789,
        "buildGUID": b"test-guid",
    }


def test_get_config_raises_when_symbol_is_missing(monkeypatch):
    mididriver = load_mididriver(monkeypatch, FakeMidiLib(with_config=False))

    with pytest.raises(NotImplementedError, match="EAS_Config is not exported"):
        mididriver.get_config()


@pytest.mark.parametrize(
    "data",
    (
        b"\x90\x3c\x7f",
        bytearray([0x90, 0x3C, 0x7F]),
        [0x90, 0x3C, 0x7F],
    ),
)
def test_write_converts_payload_to_ctypes_buffer(monkeypatch, data):
    fake_lib = FakeMidiLib()
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert mididriver.write(data) is True
    assert fake_lib.calls[-1] == ("midi_write", (b"\x90\x3c\x7f", 3))


def test_write_returns_false_when_native_write_fails(monkeypatch):
    fake_lib = FakeMidiLib(result=0)
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert mididriver.write(b"\x80\x3c\x00") is False


def test_volume_and_reverb_convert_values_to_int(monkeypatch):
    fake_lib = FakeMidiLib()
    mididriver = load_mididriver(monkeypatch, fake_lib)

    assert mididriver.set_volume("100") is True
    assert mididriver.setVolume(80.9) is True
    assert mididriver.set_reverb("-1") is True
    assert mididriver.setReverb(3.8) is True

    assert fake_lib.calls == [
        ("midi_setVolume", (100,)),
        ("midi_setVolume", (80,)),
        ("midi_setReverb", (-1,)),
        ("midi_setReverb", (3,)),
    ]
