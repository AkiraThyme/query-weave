"""Exporter abstractions."""

from __future__ import annotations

from typing import Any


class BaseExporter:
    """Simple exporter contract."""

    def export(self, data: Any) -> str:
        raise NotImplementedError
