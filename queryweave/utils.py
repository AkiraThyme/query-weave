"""Shared package utilities."""

import re
from typing import Final

AGGREGATION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?P<fn>[a-zA-Z_][a-zA-Z0-9_]*)\((?P<field>[a-zA-Z_][a-zA-Z0-9_]*)\)$"
)


def redact_sql(sql: str) -> str:
    """Very lightly redact quoted literals in SQL logs."""
    return re.sub(r"'[^']*'", "'***'", sql)
