"""Django integration helpers."""

from collections.abc import Mapping
from typing import Any

from django.conf import settings

DEFAULTS: dict[str, Any] = {
    "SLOW_QUERY_THRESHOLD_MS": 500,
    "DEBUG_SQL": False,
}


def get_queryweave_settings(overrides: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return effective QueryWeave settings from Django settings + optional overrides."""
    configured = getattr(settings, "QUERYWEAVE", {})
    merged = {**DEFAULTS, **configured}
    if overrides:
        merged.update(overrides)
    return merged
