from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command.build_ext import build_ext
    sources=['midistream.c']
else:
    sources=['midistream.pyx']

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension('midistream', sources=sources),
    ],
)
