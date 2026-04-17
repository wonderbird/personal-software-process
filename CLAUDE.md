# CLAUDE.md — Agent Onboarding

## What This Repo Is

A Python CLI for the Personal Software Process (PSP) — tracks time spent on tasks and exports a CSV log.

## Quick Orient

```
psp/cli.py        # Click entry-points: start, stop, log
psp/storage.py    # JSON persistence at ~/.psp/tasks.json
psp/models.py     # Task dataclass
tests/            # pytest suite (13 tests)
pyproject.toml    # packaging + entry point: psp = psp.cli:cli
CONTRIBUTING.md   # setup and dev workflow
```

## Toolchain

- **Runtime**: Python 3.12 (system), managed by `uv`
- **Install**: `uv sync --extra dev` — creates `.venv`, installs `psp` command
- **Tests**: `uv run pytest -v`
- **CLI**: `uv run psp <command>`
- No Makefile, no Docker, no database — plain JSON file storage

## MVP Features (complete)

1. `psp start <name>` — record task start datetime
2. `psp stop` — record task end datetime
3. `psp log` — print CSV: `start_date,start_time,end_date,end_time,task_name`

## Key Conventions

- Python 3.10+ style: `str | None` not `Optional[str]`, `from __future__ import annotations` at top of every module
- No comments unless the WHY is non-obvious
- Errors go to stderr (`err=True`) and exit with code 1
- `storage.py` functions accept an optional `path` argument for testability (tests pass `tmp_path`)
- Tests mock at the `psp.cli` boundary, not at the `psp.storage` level for CLI tests

## Data File

`~/.psp/tasks.json` — list of task dicts. An entry with `end_date == null` is the active task. At most one active task at a time.
