import hashlib
import zipfile

import pytest
from setuptools.dist import Distribution

import setup


def make_fake_p4a_build(tmp_path):
    build_dir = tmp_path / "build"
    include_dir = (
        build_dir
        / "python-installs"
        / "demo"
        / "arm64-v8a"
        / "include"
        / "python3.11"
    )
    include_dir.mkdir(parents=True)

    return build_dir, include_dir


def make_fake_aar(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)

    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_p4a_path_parser_finds_native_libs_root(tmp_path, monkeypatch):
    build_dir, include_dir = make_fake_p4a_build(tmp_path)
    monkeypatch.setenv("CPPFLAGS", f"-I{include_dir}")

    paths = setup.P4APathParser()

    assert paths.build_dir == build_dir
    assert paths.distribution_name == "demo"
    assert paths.native_libs_root == build_dir / "libs_collections" / "demo"


def test_p4a_path_parser_handles_other_builds_python_layout(tmp_path, monkeypatch):
    build_dir = tmp_path / "build-arm64-v8a_armeabi-v7a_x86_64" / "build"
    include_dir = (
        build_dir
        / "other_builds"
        / "python3"
        / "armeabi-v7a__ndk_target_22"
        / "python3"
        / "android-build"
        / "android-root"
        / "include"
        / "python3.11"
    )
    libs_arch_dir = build_dir / "libs_collections" / "demo" / "armeabi-v7a"
    include_dir.mkdir(parents=True)
    libs_arch_dir.mkdir(parents=True)

    monkeypatch.setenv("CPPFLAGS", f"-DANDROID -I{include_dir}")
    monkeypatch.setenv("LDFLAGS", f"-lm -L{libs_arch_dir}")

    paths = setup.P4APathParser()

    assert paths.build_dir == build_dir
    assert paths.distribution_name == "demo"
    assert paths.native_libs_root == build_dir / "libs_collections" / "demo"


def test_install_mididriver_libs_from_cached_aar(tmp_path, monkeypatch):
    build_dir, include_dir = make_fake_p4a_build(tmp_path)
    cache_dir = build_dir / "midistream_cache"
    cache_dir.mkdir()
    aar_path = cache_dir / f"MidiDriver-v{setup.MIDIDRIVER_VERSION}.aar"
    checksum = make_fake_aar(
        aar_path,
        {
            "jni/arm64-v8a/libmidi.so": b"arm64",
            "jni/x86/libmidi.so": b"x86",
            "classes.jar": b"ignored",
        },
    )

    monkeypatch.setenv("CPPFLAGS", f"-I{include_dir}")
    monkeypatch.setattr(setup, "MIDIDRIVER_SHA256", checksum)

    setup.install_mididriver_libs_from_aar()

    assert (
        build_dir / "libs_collections" / "demo" / "arm64-v8a" / "libmidi.so"
    ).read_bytes() == b"arm64"
    assert (
        build_dir / "libs_collections" / "demo" / "x86" / "libmidi.so"
    ).read_bytes() == b"x86"


def test_install_mididriver_libs_requires_libmidi(tmp_path, monkeypatch):
    build_dir, include_dir = make_fake_p4a_build(tmp_path)
    cache_dir = build_dir / "midistream_cache"
    cache_dir.mkdir()
    aar_path = cache_dir / f"MidiDriver-v{setup.MIDIDRIVER_VERSION}.aar"
    checksum = make_fake_aar(aar_path, {"classes.jar": b"ignored"})

    monkeypatch.setenv("CPPFLAGS", f"-I{include_dir}")
    monkeypatch.setattr(setup, "MIDIDRIVER_SHA256", checksum)

    with pytest.raises(RuntimeError, match="No jni/.*/libmidi.so"):
        setup.install_mididriver_libs_from_aar()


def test_android_build_detection(monkeypatch):
    monkeypatch.delenv("ANDROIDAPI", raising=False)
    assert not setup.is_android_build()

    monkeypatch.setenv("ANDROIDAPI", "35")
    assert setup.is_android_build()


def test_bdist_wheel_runs_android_hook(monkeypatch):
    calls = []

    def fake_hook(stage):
        calls.append(stage)

    def fake_bdist_wheel_run(command):
        calls.append("base bdist_wheel")

    monkeypatch.setattr(setup, "maybe_install_mididriver_libs", fake_hook)
    monkeypatch.setattr(setup.bdist_wheel, "run", fake_bdist_wheel_run)

    command = setup.BDistWheelMidistream(Distribution())
    command.run()

    assert calls == ["bdist_wheel.run", "base bdist_wheel"]


def test_maybe_install_mididriver_libs_is_quiet_outside_android(monkeypatch, capsys):
    monkeypatch.delenv("ANDROIDAPI", raising=False)
    monkeypatch.setattr(
        setup,
        "install_mididriver_libs_from_aar",
        lambda: pytest.fail("unexpected Android AAR install"),
    )

    setup.maybe_install_mididriver_libs("test")

    assert capsys.readouterr().out == ""


def test_debug_p4a_context_prints_android_environment(monkeypatch, capsys):
    monkeypatch.setenv("ANDROIDAPI", "35")
    monkeypatch.setenv("P4A_ARCH", "arm64-v8a")

    setup.debug_p4a_context("test")

    output = capsys.readouterr().out

    assert "[midistream] ===== test =====" in output
    assert "[midistream] ANDROIDAPI=35" in output
    assert "[midistream] P4A_ARCH=arm64-v8a" in output
    assert "[midistream] ===== end test =====" in output


def test_debug_p4a_context_is_quiet_outside_android(monkeypatch, capsys):
    monkeypatch.delenv("ANDROIDAPI", raising=False)

    setup.debug_p4a_context("test")

    assert capsys.readouterr().out == ""


@pytest.mark.functional
def test_functional_downloads_and_extracts_mididriver_aar(tmp_path, monkeypatch):
    build_dir, include_dir = make_fake_p4a_build(tmp_path)

    monkeypatch.setenv("CPPFLAGS", f"-I{include_dir}")

    setup.install_mididriver_libs_from_aar()

    copied_libs = sorted(
        path.relative_to(build_dir / "libs_collections" / "demo")
        for path in (build_dir / "libs_collections" / "demo").glob("*/libmidi.so")
    )

    assert copied_libs
    assert (
        build_dir / "midistream_cache" / f"MidiDriver-v{setup.MIDIDRIVER_VERSION}.aar"
    ).is_file()
