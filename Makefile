.PHONY: test test-functional sync lock

test: sync
	uv run pytest -q

test-functional: sync
	uv run pytest -q -m functional

sync:
	uv sync --locked --group dev

lock:
	uv lock
