"""Filter primitives and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.db.models import Model, QuerySet

from queryweave.exceptions import InvalidFilterError

ALLOWED_LOOKUPS = {"exact", "gte", "lte", "icontains", "in", "range"}


class BaseFilter:
    """Base class for reusable custom filters."""

    def apply(self, queryset: QuerySet[Any], key: str, value: Any) -> QuerySet[Any]:
        raise NotImplementedError


@dataclass(slots=True)
class FilterEngine:
    """Safely validates and applies filter dictionaries to querysets."""

    custom_filters: dict[str, BaseFilter] | None = None

    def apply(self, queryset: QuerySet[Any], filters: dict[str, Any]) -> QuerySet[Any]:
        custom = self.custom_filters or {}
        for key, value in filters.items():
            if key in custom:
                queryset = custom[key].apply(queryset, key, value)
                continue
            self._validate_filter_key(queryset.model, key, value)
            queryset = queryset.filter(**{key: value})
        return queryset

    def _validate_filter_key(self, model: type[Model], key: str, value: Any) -> None:
        parts = key.split("__")
        field_name = parts[0]
        lookup = parts[-1] if len(parts) > 1 else "exact"

        try:
            model._meta.get_field(field_name)
        except Exception as exc:  # pragma: no cover - django specific internals
            raise InvalidFilterError(f"Unknown filter field: '{field_name}'") from exc

        if lookup not in ALLOWED_LOOKUPS and len(parts) > 1:
            raise InvalidFilterError(f"Unsupported lookup '{lookup}' in filter '{key}'")

        if lookup == "in" and not isinstance(value, (list, tuple, set)):
            raise InvalidFilterError(f"Filter '{key}' expects a sequence for '__in' lookup")
        if lookup == "range" and (
            not isinstance(value, (list, tuple)) or len(value) != 2
        ):
            raise InvalidFilterError(f"Filter '{key}' expects two values for '__range' lookup")
