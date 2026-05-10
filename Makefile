.PHONY: test test-functional sync lock clean

test: sync
	uv run pytest -q

test-functional: sync
	uv run pytest -q -m functional

sync:
	uv sync --locked --group dev

lock:
	uv lock

libmidi.so: stub_midi.c
	gcc -shared -fPIC stub_midi.c -o libmidi.so

clean:
	rm -f libmidi.so
