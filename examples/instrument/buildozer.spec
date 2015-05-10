[app]
title = MIDI instrument example
version = 0.0.1
package.name = easinstrument
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = kivy,midistream

orientation = landscape
fullscreen = 1

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
