"""CSV exporter implementation."""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping
from typing import Any

from queryweave.exporters.base import BaseExporter


class CSVExporter(BaseExporter):
    """Export report payloads to CSV."""

    def export(self, data: Any) -> str:
        rows: list[Mapping[str, Any]]
        if isinstance(data, Mapping):
            rows = [data]
        else:
            rows = list(data or [])

        if not rows:
            return ""

        for row in rows:
            if not isinstance(row, Mapping):
                raise ValueError("CSV export expects a mapping or an iterable of mapping rows")

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
