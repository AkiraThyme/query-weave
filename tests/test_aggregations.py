import pytest
from django.db.models import Sum

from queryweave import Report
from queryweave.exceptions import InvalidAggregationError


@pytest.mark.django_db
def test_aggregations(order_data):
    report = Report(
        queryset=order_data,
        filters={"status": "completed"},
        aggregates={"total": "sum(price)", "avg_rating": "avg(rating)"},
    )
    data = report.run()
    assert data["total"] == 175


@pytest.mark.django_db
def test_invalid_aggregation(order_data):
    with pytest.raises(InvalidAggregationError):
        Report(queryset=order_data, aggregates={"bad": "median(price)"}).run()


@pytest.mark.django_db
def test_custom_aggregation(order_data):
    report = Report(
        queryset=order_data,
        aggregates={"total": "totalsum(price)"},
        custom_aggregations={"totalsum": lambda field: Sum(field)},
    )
    data = report.run()
    assert data["total"] == 205
