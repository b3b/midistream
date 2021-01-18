Midistream
==========

Package to synthesize and playback MIDI commands from `Python for Android <https://github.com/kivy/python-for-android>`_.
Using Sonivox EAS API, that is not officially suported by Android SDK/NDK.
`Audiostream <https://github.com/kivy/audiostream>`_ is used for playback.

Generated documentation: http://midistream.readthedocs.org

Example of instrument on Android: `video <http://www.youtube.com/watch?v=Ltf9x0rJQMc>`_.

Since Android no longer allow access to the system `libsonivox.so`, application should contain its own copy of the library.
*Midistream* uses compiled *libmidi.so* libraries from the Bill Farmer `Midi Driver <https://github.com/billthefarmer/mididriver>`_ releases.


Related resources
-----------------

* `EAS documentation <https://github.com/android/platform_external_sonivox/tree/master/docs>`_
* `Android Issue 8201: Add a real-time MIDI API for Sonivox synthesizer <https://code.google.com/p/android/issues/detail?id=8201>`_
* `Android midi driver using Sonivox EAS library <https://github.com/billthefarmer/mididriver>`_


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
