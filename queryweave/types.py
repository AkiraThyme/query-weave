"""Type aliases used by QueryWeave."""

from typing import Any, Callable, Mapping

from django.db.models import Aggregate, QuerySet

FilterValue = Any
Filters = Mapping[str, FilterValue]
Aggregates = Mapping[str, str]
Rows = list[dict[str, Any]]
AggregateFactory = Callable[[str], Aggregate]
QuerysetLike = QuerySet[Any]
