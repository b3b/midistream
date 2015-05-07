Midistream
==========

Module to synthesize and playback MIDI commands from `Python for Android <https://github.com/kivy/python-for-android>`_.
Using Sonivox EAS API, that is not oficially suported by Android SDK/NDK.
`Audiostream <https://github.com/kivy/audiostream>`_ is used for playback.

Generated documentation: http://midistream.readthedocs.org

Example of instrument on Android: `video <http://www.youtube.com/watch?v=Ltf9x0rJQMc>`_.


Related resources
-----------------

* `EAS documentation <https://github.com/android/platform_external_sonivox/tree/master/docs>`_
* `Android Issue 8201: Add a real-time MIDI API for Sonivox synthesizer <https://code.google.com/p/android/issues/detail?id=8201>`_
* `Android midi driver using Sonivox EAS library <https://github.com/billthefarmer/mididriver>`_


Build
-----

Module is built from python-for-android recipe: `midistream/recipe.sh <https://github.com/b3b/python-for-android/blob/midistream/recipes/midistream/recipe.sh>`_.


Examples
--------

See examples/ directory.


examples/instrument could be build with `buildozer <https://github.com/kivy/buildozer>`_.
`make` command should be run first - this will use python-for-android fork with midistream recipe for building. Like::

  cd examples/instrument
  make
  buildozer android deploy run logcat
