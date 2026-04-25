"""JSON exporter implementation."""

from __future__ import annotations

import json
from typing import Any

from queryweave.exporters.base import BaseExporter


class JSONExporter(BaseExporter):
    """Export report payloads to JSON."""

    def export(self, data: Any) -> str:
        return json.dumps(data, default=str, indent=2)
