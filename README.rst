Midistream
==========

Package to synthesize and playback MIDI commands from `Python for Android <https://github.com/kivy/python-for-android>`_.

*Midistream* is a wrapper for Bill Farmer's `Midi Driver <https://github.com/billthefarmer/mididriver>`_,
and includes *libmidi.so* libraries from the MidiDriver build.
The bundled MidiDriver components are licensed under the `Apache License 2.0 <https://github.com/billthefarmer/mididriver/blob/master/Apache-2.0.txt>`_.

`Previous <https://github.com/b3b/midistream/tree/py2>`_ version was using system version of Sonivox EAS library and `Audiostream <https://github.com/kivy/audiostream>`_ for playback.

Documentation: https://herethere.me/midistream


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

*buildozer.spec* requirements should include *midistream*::

   requirements = python3,kivy,midistream


App configuration example: `buildozer.spec <https://github.com/b3b/midistream/blob/master/examples/demo/buildozer.spec>`_


Examples
--------

See `examples/ <https://github.com/b3b/midistream/tree/master/examples>`_ directory.

`examples/demo <https://github.com/b3b/midistream/tree/master/examples/demo>`_ is an app that shows how to initialize the
synthesizer, inspect configuration, set volume and reverb, and play MIDI notes::

  cd examples/demo
  buildozer android debug deploy run logcat
