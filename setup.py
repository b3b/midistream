import ast
import hashlib
import os
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install


PACKAGE_ROOT = Path(__file__).parent
MIDIDRIVER_VERSION = "1.19py31"
MIDIDRIVER_SHA256 = (
    "152003f72a8cc6adb77219b1edc4e5a6c7c32bfe853b31ef4d734e847f1f2e73"
)
MIDIDRIVER_AAR_URL = (
    "https://github.com/b3b/mididriver/releases/download/"
    f"v{MIDIDRIVER_VERSION}/MidiDriver-v{MIDIDRIVER_VERSION}.aar"
)


def read_package_version():
    version_path = PACKAGE_ROOT / "midistream" / "version.py"
    tree = ast.parse(version_path.read_text())

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__version__":
                return ast.literal_eval(node.value)

    raise RuntimeError(f"Cannot find __version__ in {version_path}")


def is_android_build():
    return "ANDROIDAPI" in os.environ


def debug_p4a_context(stage):
    if not is_android_build():
        return

    print(f"[midistream] ===== {stage} =====")

    for key in (
        "ANDROIDAPI",
        "ARCH",
        "P4A_ARCH",
        "CPPFLAGS",
        "LDFLAGS",
    ):
        value = os.environ.get(key)
        if value:
            print(f"[midistream] {key}={value}")

    print(f"[midistream] ===== end {stage} =====")


class P4APathParser:
    @property
    def cppflags(self):
        return os.environ.get("CPPFLAGS", "")

    @property
    def python_path(self):
        match = re.search(
            r"-I(/[^\s]+/build/python-installs/[^/\s]+/)",
            self.cppflags,
        )
        if match:
            return Path(match.group(1))

        match = re.search(
            r"-I(/[^\s]+/build/python-installs/[^/\s]+/[^/\s]+/include/python[0-9.]+)",
            self.cppflags,
        )
        if match:
            return Path(match.group(1)).parents[2]

        raise RuntimeError(
            "Cannot find p4a python-installs path in CPPFLAGS: "
            f"{self.cppflags}"
        )

    @property
    def python_installs_dir(self):
        path = self.python_path

        while path.name != "python-installs":
            if path.parent == path:
                raise RuntimeError("Cannot find python-installs directory")
            path = path.parent

        return path

    @property
    def build_dir(self):
        return self.python_installs_dir.parent

    @property
    def distribution_name(self):
        path = self.python_path

        while path.parent.name != "python-installs":
            if path.parent == path:
                raise RuntimeError("Cannot find distribution name")
            path = path.parent

        return path.name

    @property
    def native_libs_root(self):
        return self.build_dir / "libs_collections" / self.distribution_name


def file_sha256(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def verify_mididriver_aar(aar_path):
    actual = file_sha256(aar_path)

    if actual != MIDIDRIVER_SHA256:
        raise RuntimeError(
            "MidiDriver AAR checksum mismatch: "
            f"expected {MIDIDRIVER_SHA256}, got {actual}"
        )


def download_mididriver_aar(cache_dir):
    cache_dir.mkdir(parents=True, exist_ok=True)

    aar_path = cache_dir / f"MidiDriver-v{MIDIDRIVER_VERSION}.aar"

    if aar_path.exists() and aar_path.stat().st_size > 0:
        verify_mididriver_aar(aar_path)
        print(f"[midistream] using cached MidiDriver AAR: {aar_path}")
        return aar_path

    print("[midistream] downloading MidiDriver AAR:")
    print(f"[midistream]   {MIDIDRIVER_AAR_URL}")

    urllib.request.urlretrieve(MIDIDRIVER_AAR_URL, aar_path)

    if not aar_path.exists() or aar_path.stat().st_size == 0:
        raise RuntimeError(f"Downloaded AAR is missing or empty: {aar_path}")

    verify_mididriver_aar(aar_path)
    print(f"[midistream] downloaded MidiDriver AAR: {aar_path}")
    return aar_path


def install_mididriver_libs_from_aar():
    paths = P4APathParser()

    print(f"[midistream] p4a build dir: {paths.build_dir}")
    print(f"[midistream] p4a dist name: {paths.distribution_name}")
    print(f"[midistream] p4a native libs root: {paths.native_libs_root}")

    aar_path = download_mididriver_aar(paths.build_dir / "midistream_cache")
    copied = 0

    with zipfile.ZipFile(aar_path) as archive:
        members = [
            name
            for name in archive.namelist()
            if name.startswith("jni/") and name.endswith("/libmidi.so")
        ]

        if not members:
            raise RuntimeError(f"No jni/*/libmidi.so files found in {aar_path}")

        for member in sorted(members):
            parts = member.split("/")

            if len(parts) != 3:
                continue

            _, abi, filename = parts

            if filename != "libmidi.so":
                continue

            dst_dir = paths.native_libs_root / abi
            dst_dir.mkdir(parents=True, exist_ok=True)

            dst = dst_dir / "libmidi.so"

            with archive.open(member) as src, open(dst, "wb") as out:
                shutil.copyfileobj(src, out)

            copied += 1
            print(f"[midistream] installed {member} -> {dst}")

    if copied == 0:
        raise RuntimeError(f"No libmidi.so files copied from {aar_path}")

    print(f"[midistream] installed {copied} libmidi.so files")


class InstallMidistream(install):
    def run(self):
        debug_p4a_context("install.run")

        if is_android_build():
            install_mididriver_libs_from_aar()

        super().run()


def main():
    setup(
        name="midistream",
        version=read_package_version(),
        packages=["midistream"],
        cmdclass={
            "install": InstallMidistream,
        },
    )


if __name__ == "__main__":
    main()
