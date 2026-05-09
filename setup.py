import ast
from pathlib import Path

from distutils.core import setup
from distutils.extension import Extension


PACKAGE_ROOT = Path(__file__).parent


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


try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

    sources = ["mididriver.c"]
else:
    sources = ["mididriver.pyx"]

def main():
    setup(
        name="midistream",
        version=read_package_version(),
        packages=["midistream"],
        cmdclass={"build_ext": build_ext},
        setup_requires=['setuptools_scm',
                        'setuptools>=18.0',
                        'cython'],
        ext_modules=[
            Extension(
                "libmidi",
                sources=["midi.pyx"],
                extra_link_args=["-o", "./libmidi.so"],
            ),
            Extension(
                "midistream.mididriver",
                sources=sources,
                libraries=["midi"],
                extra_link_args=["-L", "."],
            ),
        ],
    )


if __name__ == "__main__":
    main()
