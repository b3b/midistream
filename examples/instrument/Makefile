debug: midistream-python-for-android
	buildozer android debug

midistream-python-for-android:
	git clone -b midistream --single-branch --depth=1 https://github.com/b3b/python-for-android.git midistream-python-for-android

clean:
	rm -rfv midistream-python-for-android/ bin/ .buildozer/ *.pyc *.pyo state.cfg

.PHONY: debug clean
