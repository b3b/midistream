from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext

    sources = ["mididriver.c"]
else:
    sources = ["mididriver.pyx"]

setup(
    name="midistream",
    packages=["midistream"],
    cmdclass={"build_ext": build_ext},
    setup_requires=['setuptools_scm'],
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
