from __future__ import annotations

import csv
import sys
from datetime import datetime

import click

from psp.models import Task
from psp.storage import (
    DEFAULT_STORAGE_PATH,
    add_task,
    complete_active_task,
    get_active_task,
    get_all_tasks,
)


def _now() -> tuple[str, str]:
    """Return (YYYY-MM-DD, HH:MM:SS) for the current moment."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")


@click.group()
def cli() -> None:
    """Personal Software Process time tracker."""


@cli.command()
@click.argument("task_name")
def start(task_name: str) -> None:
    """Start timing TASK_NAME."""
    active = get_active_task()
    if active is not None:
        click.echo(
            f"Error: task '{active.name}' is already active. Run 'psp stop' first.",
            err=True,
        )
        sys.exit(1)

    date, time = _now()
    task = Task(name=task_name, start_date=date, start_time=time)
    add_task(task)
    click.echo(f"Started '{task_name}' at {date} {time}")


@cli.command()
def stop() -> None:
    """Stop the active task."""
    active = get_active_task()
    if active is None:
        click.echo("Error: no active task. Run 'psp start <task>' first.", err=True)
        sys.exit(1)

    date, time = _now()
    complete_active_task(end_date=date, end_time=time)
    click.echo(f"Stopped '{active.name}' at {date} {time}")


@cli.command(name="log")
def log_tasks() -> None:
    """Print a CSV log of all completed tasks."""
    writer = csv.writer(sys.stdout)
    writer.writerow(["start_date", "start_time", "end_date", "end_time", "task_name"])
    for task in get_all_tasks():
        if task.is_complete():
            writer.writerow(
                [task.start_date, task.start_time, task.end_date, task.end_time, task.name]
            )
