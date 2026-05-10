import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

import midistream
import setup


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_version_module():
    spec = importlib.util.spec_from_file_location(
        "midistream_version",
        PROJECT_ROOT / "midistream" / "version.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_version_module_defines_string():
    version = load_version_module().__version__

    assert isinstance(version, str)
    assert version


def test_setup_reads_package_version():
    version = load_version_module().__version__

    assert setup.read_package_version() == version


def test_package_exports_version():
    version = load_version_module().__version__

    assert midistream.__version__ == version


def test_setup_version_reader_does_not_execute_version_file(tmp_path, monkeypatch):
    package_dir = tmp_path / "midistream"
    package_dir.mkdir()
    (package_dir / "version.py").write_text(
        '__version__ = "9.8.7"\nraise RuntimeError("version.py was executed")\n'
    )
    monkeypatch.setattr(setup, "PACKAGE_ROOT", tmp_path)

    assert setup.read_package_version() == "9.8.7"


def test_setup_version_reader_requires_version(tmp_path, monkeypatch):
    package_dir = tmp_path / "midistream"
    package_dir.mkdir()
    (package_dir / "version.py").write_text('OTHER = "0.0.0"\n')
    monkeypatch.setattr(setup, "PACKAGE_ROOT", tmp_path)

    with pytest.raises(RuntimeError):
        setup.read_package_version()


def test_setup_py_reports_package_version():
    version = load_version_module().__version__

    result = subprocess.run(
        [sys.executable, "setup.py", "--version"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip().splitlines()[-1] == version
