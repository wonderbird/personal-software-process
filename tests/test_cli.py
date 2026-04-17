from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from psp.cli import cli
from psp.models import Task
from psp.storage import add_task


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def store(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


def _patch_storage(store: Path):
    """Patch all storage calls to use the tmp store."""
    return patch("psp.cli.DEFAULT_STORAGE_PATH", store), patch(
        "psp.storage.DEFAULT_STORAGE_PATH", store
    )


def test_start_creates_active_task(runner: CliRunner, store: Path) -> None:
    with patch("psp.cli.get_active_task", return_value=None), \
         patch("psp.cli.add_task") as mock_add, \
         patch("psp.cli._now", return_value=("2026-04-17", "09:00:00")):
        result = runner.invoke(cli, ["start", "my task"])
    assert result.exit_code == 0
    assert "Started 'my task'" in result.output
    mock_add.assert_called_once()


def test_start_blocks_when_active(runner: CliRunner, store: Path) -> None:
    active = Task(name="existing", start_date="2026-04-17", start_time="08:00:00")
    with patch("psp.cli.get_active_task", return_value=active):
        result = runner.invoke(cli, ["start", "new task"])
    assert result.exit_code == 1
    assert "already active" in result.output


def test_stop_completes_task(runner: CliRunner, store: Path) -> None:
    active = Task(name="coding", start_date="2026-04-17", start_time="09:00:00")
    with patch("psp.cli.get_active_task", return_value=active), \
         patch("psp.cli.complete_active_task") as mock_complete, \
         patch("psp.cli._now", return_value=("2026-04-17", "10:00:00")):
        result = runner.invoke(cli, ["stop"])
    assert result.exit_code == 0
    assert "Stopped 'coding'" in result.output
    mock_complete.assert_called_once_with(end_date="2026-04-17", end_time="10:00:00")


def test_stop_no_active_task(runner: CliRunner) -> None:
    with patch("psp.cli.get_active_task", return_value=None):
        result = runner.invoke(cli, ["stop"])
    assert result.exit_code == 1
    assert "no active task" in result.output


def test_log_empty(runner: CliRunner) -> None:
    with patch("psp.cli.get_all_tasks", return_value=[]):
        result = runner.invoke(cli, ["log"])
    assert result.exit_code == 0
    assert "start_date,start_time,end_date,end_time,task_name" in result.output


def test_log_shows_completed_tasks(runner: CliRunner) -> None:
    tasks = [
        Task("done task", "2026-04-17", "09:00:00", "2026-04-17", "10:00:00"),
        Task("active task", "2026-04-17", "11:00:00"),  # incomplete — excluded
    ]
    with patch("psp.cli.get_all_tasks", return_value=tasks):
        result = runner.invoke(cli, ["log"])
    assert result.exit_code == 0
    lines = result.output.strip().splitlines()
    assert len(lines) == 2  # header + 1 completed row
    assert "done task" in lines[1]
    assert "active task" not in result.output


def test_log_csv_format(runner: CliRunner) -> None:
    tasks = [Task("review", "2026-04-17", "08:00:00", "2026-04-17", "08:45:00")]
    with patch("psp.cli.get_all_tasks", return_value=tasks):
        result = runner.invoke(cli, ["log"])
    lines = result.output.strip().splitlines()
    assert lines[0] == "start_date,start_time,end_date,end_time,task_name"
    assert lines[1] == "2026-04-17,08:00:00,2026-04-17,08:45:00,review"
