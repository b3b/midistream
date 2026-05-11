[app]
title = Midistream demo
version = 0.0.1
package.name = midistreamdemo
package.domain = org.midistream

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements =
             python3==3.11.5,
             hostpython3==3.11.5,
             kivy==2.3.1,
             filetype,
             midistream,

android.api = 35
android.minapi = 22
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a, x86_64

p4a.branch = v2024.01.21

orientation = landscape
fullscreen = 0

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
