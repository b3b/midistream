from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext
    sources = ["midi.c"]
else:
    sources = ["midi.pyx"]


setup(
    name="midistream",
    packages=["midistream"],
    package_dir={"midistream": "."},
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Extension("midistream.midi", sources=sources),
    ],
)
