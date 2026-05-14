Changelog
=========

0.3.1 - 2026-05-14
------------------

* Changed the wheel platform tag to avoid installing ``midistream`` from a
  cached pure-Python wheel and skipping the ``libmidi.so`` copy hook.

0.3.0 - 2026-05-11
------------------

* Published ``midistream`` on PyPI for Buildozer installs, replacing the old
  GitHub ``master.zip`` requirement.
* Replaced the legacy Cython MIDI driver binding with a ``ctypes`` wrapper.
