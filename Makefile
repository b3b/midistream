.PHONY: test test-functional build-sdist check-dist sync lock clean

test: sync
	uv run pytest -q

test-functional: sync
	uv run pytest -q -m functional

build-sdist: clean sync
	uv run python -m build --sdist

check-dist:
	uv run twine check dist/*.tar.gz

sync:
	uv sync --locked --group dev

lock:
	uv lock

libmidi.so: stub_midi.c
	gcc -shared -fPIC stub_midi.c -o libmidi.so

clean:
	rm -rf build dist *.egg-info
	rm -f libmidi.so
