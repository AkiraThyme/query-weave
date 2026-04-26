"""Filter primitives and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.core.exceptions import FieldDoesNotExist
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
        lookup = "exact"
        field_path = parts
        if len(parts) > 1 and parts[-1] in ALLOWED_LOOKUPS:
            lookup = parts[-1]
            field_path = parts[:-1]
            self._validate_field_path(model, field_path)
        else:
            try:
                self._validate_field_path(model, field_path)
            except InvalidFilterError as field_path_error:
                if len(parts) > 1 and self._is_valid_field_path(model, parts[:-1]):
                    raise InvalidFilterError(
                        f"Unsupported lookup '{parts[-1]}' in filter '{key}'"
                    ) from field_path_error
                raise

        if lookup == "in" and not isinstance(value, (list, tuple, set)):
            raise InvalidFilterError(f"Filter '{key}' expects a sequence for '__in' lookup")
        if lookup == "range" and (not isinstance(value, (list, tuple)) or len(value) != 2):
            raise InvalidFilterError(f"Filter '{key}' expects two values for '__range' lookup")

    def _validate_field_path(self, model: type[Model], path: list[str]) -> None:
        current_model = model
        for idx, field_name in enumerate(path):
            try:
                field = current_model._meta.get_field(field_name)
            except FieldDoesNotExist as exc:
                raise InvalidFilterError(f"Unknown filter field: '{field_name}'") from exc

            is_last_part = idx == len(path) - 1
            if is_last_part:
                return

            related_model = getattr(field, "related_model", None)
            if related_model is None:
                raise InvalidFilterError(f"Field '{field_name}' in filter path is not a relation")
            current_model = related_model

    def _is_valid_field_path(self, model: type[Model], path: list[str]) -> bool:
        try:
            self._validate_field_path(model, path)
            return True
        except InvalidFilterError:
            return False
