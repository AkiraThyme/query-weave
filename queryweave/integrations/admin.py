"""Optional admin integration stubs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SavedReportConfig:
    """In-memory report config DTO for optional admin workflows."""

    name: str
    config: dict[str, Any]
