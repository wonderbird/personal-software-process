from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Task:
    name: str
    start_date: str  # YYYY-MM-DD
    start_time: str  # HH:MM:SS
    end_date: str | None = None
    end_time: str | None = None

    def is_complete(self) -> bool:
        return self.end_date is not None and self.end_time is not None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(
            name=data["name"],
            start_date=data["start_date"],
            start_time=data["start_time"],
            end_date=data.get("end_date"),
            end_time=data.get("end_time"),
        )
