from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

    sources = ["midistream.c"]
else:
    sources = ["midistream.pyx"]

setup(
    name="midistream",
    packages=["midistream"],
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Extension(
            "libmidi",
            sources=["midi.c"],
            extra_link_args=["-o", "./libmidi.so"],
        ),
        Extension(
            "midistream.midistream",
            sources=sources,
            libraries=["midi"],
            extra_link_args=["-L", "."],
        ),
    ],
)
