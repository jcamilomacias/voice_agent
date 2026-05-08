.PHONY: install test run

install:
	uv sync --all-extras

test:
	uv run pytest

run:
	uv run python -m src.pipeline
