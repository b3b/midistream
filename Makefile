.PHONY: test sync lock

test: sync
	uv run pytest -q

sync:
	uv sync --locked --group dev

lock:
	uv lock

