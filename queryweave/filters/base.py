"""Filter primitives and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field, Model, QuerySet

from queryweave.exceptions import InvalidFilterError


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
        terminal_field: Field[Any, Any]
        try:
            terminal_field = self._validate_field_path(model, parts)
        except InvalidFilterError as field_path_error:
            if len(parts) <= 1:
                raise

            terminal_field_or_none = self._terminal_field_if_valid(model, parts[:-1])
            if terminal_field_or_none is None:
                raise

            terminal_field = terminal_field_or_none
            lookup = parts[-1]
            if terminal_field.get_lookup(lookup) is None:
                raise InvalidFilterError(
                    f"Unsupported lookup '{lookup}' in filter '{key}'"
                ) from field_path_error

        if lookup == "in" and not isinstance(value, (list, tuple, set)):
            raise InvalidFilterError(f"Filter '{key}' expects a sequence for '__in' lookup")
        if lookup == "range" and (not isinstance(value, (list, tuple)) or len(value) != 2):
            raise InvalidFilterError(f"Filter '{key}' expects two values for '__range' lookup")

    def _validate_field_path(self, model: type[Model], path: list[str]) -> Field[Any, Any]:
        current_model = model
        terminal_field: Field[Any, Any] | None = None
        for idx, field_name in enumerate(path):
            try:
                field = current_model._meta.get_field(field_name)
            except FieldDoesNotExist as exc:
                raise InvalidFilterError(f"Unknown filter field: '{field_name}'") from exc
            terminal_field = field

            is_last_part = idx == len(path) - 1
            if is_last_part:
                return field

            related_model = getattr(field, "related_model", None)
            if related_model is None:
                raise InvalidFilterError(f"Field '{field_name}' in filter path is not a relation")
            current_model = related_model
        if terminal_field is None:
            raise InvalidFilterError("Filter key cannot be empty")
        return terminal_field

    def _terminal_field_if_valid(
        self, model: type[Model], path: list[str]
    ) -> Field[Any, Any] | None:
        try:
            return self._validate_field_path(model, path)
        except InvalidFilterError:
            return None
