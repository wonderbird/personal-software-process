from pathlib import Path

import pytest

from psp.models import Task
from psp.storage import add_task, complete_active_task, get_active_task, get_all_tasks


@pytest.fixture
def tmp_store(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def test_empty_store(tmp_store: Path) -> None:
    assert get_all_tasks(tmp_store) == []
    assert get_active_task(tmp_store) is None


def test_add_and_retrieve(tmp_store: Path) -> None:
    task = Task(name="coding", start_date="2026-04-17", start_time="09:00:00")
    add_task(task, tmp_store)
    tasks = get_all_tasks(tmp_store)
    assert len(tasks) == 1
    assert tasks[0].name == "coding"
    assert tasks[0].end_date is None


def test_active_task(tmp_store: Path) -> None:
    task = Task(name="review", start_date="2026-04-17", start_time="10:00:00")
    add_task(task, tmp_store)
    active = get_active_task(tmp_store)
    assert active is not None
    assert active.name == "review"


def test_complete_active_task(tmp_store: Path) -> None:
    task = Task(name="design", start_date="2026-04-17", start_time="08:00:00")
    add_task(task, tmp_store)
    completed = complete_active_task("2026-04-17", "09:30:00", tmp_store)
    assert completed is not None
    assert completed.end_date == "2026-04-17"
    assert completed.end_time == "09:30:00"
    assert get_active_task(tmp_store) is None


def test_no_active_task_to_complete(tmp_store: Path) -> None:
    result = complete_active_task("2026-04-17", "09:00:00", tmp_store)
    assert result is None


def test_multiple_tasks(tmp_store: Path) -> None:
    t1 = Task(name="t1", start_date="2026-04-17", start_time="08:00:00",
               end_date="2026-04-17", end_time="09:00:00")
    t2 = Task(name="t2", start_date="2026-04-17", start_time="10:00:00")
    add_task(t1, tmp_store)
    add_task(t2, tmp_store)
    assert len(get_all_tasks(tmp_store)) == 2
    active = get_active_task(tmp_store)
    assert active is not None
    assert active.name == "t2"
