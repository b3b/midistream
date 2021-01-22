Midistream
==========

Package to synthesize and playback MIDI commands from `Python for Android <https://github.com/kivy/python-for-android>`_.

*Midistream* is a wrapper for the Bill Farmer `Midi Driver <https://github.com/billthefarmer/mididriver>`_,
and includes *libmidi.so* libraries from the MidiDriver build.

`Previous <https://github.com/b3b/midistream/tree/py2>`_ version was using system version of Sonivox EAS library and `Audiostream <https://github.com/kivy/audiostream>`_ for playback.

Generated documentation: https://midistream.readthedocs.org


Related resources
-----------------

* `EAS documentation <https://github.com/android/platform_external_sonivox/tree/master/docs>`_
* `Android Issue 8201: Add a real-time MIDI API for Sonivox synthesizer <https://code.google.com/p/android/issues/detail?id=8201>`_
* `Android MIDI driver using Sonivox EAS library <https://github.com/billthefarmer/mididriver>`_


Quick start development environment
-----------------------------------

*midistream* is included in `PythonHere <https://herethere.me/>`_ app, together with the `Jupyter Notebook <https://jupyter.org/>`_ it could be used as a development environment.

Usage examples: https://herethere.me/examples/midi.html

  
Build
-----

The following instructions are for building app with `buildozer <https://github.com/kivy/buildozer/>`_ tool.

*buildozer.spec* requirements should include *midistream* and *mididriver*,
path to *midistream* recipes directory should be set::

   requirements = 
               mididriver,
               https://github.com/b3b/midistream/archive/master.zip,

  p4a.local_recipes = /path/to/cloned/repo/recipes


App configuration example: `buildozer.spec <https://github.com/b3b/midistream/blob/master/examples/instrument/buildozer.spec>`_


Examples
--------

See examples/ directory.


examples/instrument could be build with *buildozer*::

  cd examples/instrument
  buildozer android debug deploy run logcat
