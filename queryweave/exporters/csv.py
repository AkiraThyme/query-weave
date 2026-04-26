"""CSV exporter implementation."""

from __future__ import annotations

import csv
import io
from typing import Any

from queryweave.exporters.base import BaseExporter


class CSVExporter(BaseExporter):
    """Export report payloads to CSV."""

    def export(self, data: Any) -> str:
        rows: list[dict[str, Any]]
        if isinstance(data, dict):
            rows = [data]
        else:
            rows = list(data or [])

        if not rows:
            return ""

        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("CSV export expects a dict or an iterable of dict rows")

        header_keys: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in header_keys:
                    header_keys.append(key)

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=header_keys)
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()
