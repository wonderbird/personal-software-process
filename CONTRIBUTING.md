# Contributing

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

```bash
git clone <repo>
cd personal-software-process
uv sync --extra dev
```

This creates a `.venv` and installs the `psp` command and all dev dependencies.

## Running the CLI

```bash
uv run psp start "task name"   # begin timing a task
uv run psp stop                # end the active task
uv run psp log                 # print CSV of completed tasks
```

Task data is stored at `~/.psp/tasks.json`.

## Running Tests

```bash
uv run pytest -v
```

## Project Structure

```
psp/
  cli.py        # Click commands (start, stop, log)
  storage.py    # JSON persistence layer
  models.py     # Task dataclass
tests/
  test_cli.py       # CLI integration tests
  test_storage.py   # Storage unit tests
pyproject.toml      # Package definition and entry point
```

## Making Changes

1. Edit source under `psp/`
2. Run `uv run pytest` to verify nothing is broken
3. The `psp` entry point re-reads source on each invocation — no rebuild needed
