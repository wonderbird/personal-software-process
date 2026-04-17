from __future__ import annotations

import json
from pathlib import Path
from psp.models import Task

DEFAULT_STORAGE_PATH = Path.home() / ".psp" / "tasks.json"


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return json.load(f)


def _save(path: Path, tasks: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(tasks, f, indent=2)


def get_all_tasks(path: Path = DEFAULT_STORAGE_PATH) -> list[Task]:
    return [Task.from_dict(d) for d in _load(path)]


def get_active_task(path: Path = DEFAULT_STORAGE_PATH) -> Task | None:
    for task in get_all_tasks(path):
        if not task.is_complete():
            return task
    return None


def add_task(task: Task, path: Path = DEFAULT_STORAGE_PATH) -> None:
    tasks = _load(path)
    tasks.append(task.to_dict())
    _save(path, tasks)


def complete_active_task(
    end_date: str, end_time: str, path: Path = DEFAULT_STORAGE_PATH
) -> Task | None:
    tasks = _load(path)
    completed: Task | None = None
    for entry in tasks:
        if entry.get("end_date") is None:
            entry["end_date"] = end_date
            entry["end_time"] = end_time
            completed = Task.from_dict(entry)
            break
    if completed is not None:
        _save(path, tasks)
    return completed
