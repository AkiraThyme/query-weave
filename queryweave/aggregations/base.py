"""Aggregation parser and registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.aggregates import Aggregate

from queryweave.exceptions import InvalidAggregationError
from queryweave.types import AggregateFactory
from queryweave.utils import AGGREGATION_PATTERN

DEFAULT_AGGREGATIONS: dict[str, AggregateFactory] = {
    "count": lambda field: Count(field),
    "sum": lambda field: Sum(field),
    "avg": lambda field: Avg(field),
    "min": lambda field: Min(field),
    "max": lambda field: Max(field),
}


@dataclass(slots=True)
class AggregationRegistry:
    """Registry for builtin + custom aggregation factories."""

    factories: dict[str, AggregateFactory] = field(default_factory=lambda: dict(DEFAULT_AGGREGATIONS))

    def register(self, name: str, factory: AggregateFactory) -> None:
        self.factories[name.lower()] = factory

    def parse(self, expression: str) -> Aggregate:
        matched = AGGREGATION_PATTERN.match(expression.strip())
        if not matched:
            raise InvalidAggregationError(
                f"Invalid aggregation expression '{expression}'. Use e.g. sum(price)."
            )
        fn = matched.group("fn").lower()
        field_name = matched.group("field")
        factory = self.factories.get(fn)
        if factory is None:
            raise InvalidAggregationError(f"Unsupported aggregation function '{fn}'")
        return factory(field_name)

    def parse_map(self, aggregates: dict[str, str]) -> dict[str, Aggregate]:
        return {alias: self.parse(expression) for alias, expression in aggregates.items()}
