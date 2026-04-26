"""Main report engine."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

from django.db.models import QuerySet

from queryweave.aggregations.base import AggregationRegistry
from queryweave.exceptions import InvalidReportConfigError
from queryweave.filters.base import BaseFilter, FilterEngine
from queryweave.integrations.django import get_queryweave_settings
from queryweave.utils import redact_sql

logger = logging.getLogger("queryweave")


@dataclass(slots=True)
class Report:
    """Reusable ORM report descriptor."""

    queryset: QuerySet[Any]
    filters: dict[str, Any] = field(default_factory=dict)
    group_by: list[str] = field(default_factory=list)
    aggregates: dict[str, str] = field(default_factory=dict)
    order_by: list[str] = field(default_factory=list)
    page: int | None = None
    page_size: int | None = None
    debug: bool | None = None
    custom_filters: dict[str, BaseFilter] | None = None
    custom_aggregations: dict[str, Any] | None = None
    settings_override: dict[str, Any] | None = None

    def run(self) -> Any:
        """Execute the report and return a Python-native payload."""
        self._validate_config()
        effective_settings = get_queryweave_settings(self.settings_override)
        debug = effective_settings["DEBUG_SQL"] if self.debug is None else self.debug

        start = time.perf_counter()
        queryset = self.queryset
        queryset = FilterEngine(custom_filters=self.custom_filters).apply(queryset, self.filters)

        registry = AggregationRegistry()
        for name, factory in (self.custom_aggregations or {}).items():
            registry.register(name, factory)

        result: Any
        if self.group_by:
            orm_aggregates = registry.parse_map(self.aggregates)
            grouped = queryset.values(*self.group_by).annotate(**orm_aggregates)
            if self.order_by:
                grouped = grouped.order_by(*self.order_by)
            grouped = self._paginate(grouped)
            result = list(grouped)
        elif self.aggregates:
            orm_aggregates = registry.parse_map(self.aggregates)
            result = queryset.aggregate(**orm_aggregates)
        else:
            if self.order_by:
                queryset = queryset.order_by(*self.order_by)
            queryset = self._paginate(queryset)
            result = list(queryset.values())

        elapsed_ms = (time.perf_counter() - start) * 1000
        if debug:
            self._log_debug(queryset, elapsed_ms)
        self._log_if_slow(effective_settings["SLOW_QUERY_THRESHOLD_MS"], elapsed_ms)
        return result

    def _paginate(self, queryset: QuerySet[Any]) -> QuerySet[Any]:
        if self.page is None or self.page_size is None:
            return queryset
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        return queryset[start:end]

    def _validate_config(self) -> None:
        if not isinstance(self.queryset, QuerySet):
            raise InvalidReportConfigError("'queryset' must be a Django QuerySet instance")
        if self.page is not None and self.page < 1:
            raise InvalidReportConfigError("'page' must be >= 1")
        if self.page_size is not None and self.page_size < 1:
            raise InvalidReportConfigError("'page_size' must be >= 1")
        if (self.page is None) ^ (self.page_size is None):
            raise InvalidReportConfigError("'page' and 'page_size' must be provided together")

    def _log_debug(self, queryset: QuerySet[Any], elapsed_ms: float) -> None:
        redacted = redact_sql(str(queryset.query))
        logger.info("[QueryWeave] SQL=%s", redacted)
        logger.info("[QueryWeave] Execution time=%.2fms", elapsed_ms)
        has_rel = bool(queryset.model._meta.fields_map)
        if has_rel and not queryset.query.select_related:
            logger.info(
                "[QueryWeave] Potential N+1 risk detected. "
                "Consider select_related/prefetch_related."
            )

    def _log_if_slow(self, threshold_ms: int, elapsed_ms: float) -> None:
        if elapsed_ms > threshold_ms:
            logger.warning(
                "[QueryWeave] Slow report detected (%.2fms > %sms)",
                elapsed_ms,
                threshold_ms,
            )
