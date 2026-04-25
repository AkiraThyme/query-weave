import pytest

from queryweave import Report
from queryweave.exceptions import InvalidFilterError
from queryweave.filters.base import BaseFilter


class CompletedOnlyFilter(BaseFilter):
    def apply(self, queryset, key, value):
        return queryset.filter(status="completed")


@pytest.mark.django_db
def test_filter_lookups(order_data):
    report = Report(
        queryset=order_data,
        filters={"price__gte": 70, "status__icontains": "com"},
    )
    rows = report.run()
    assert len(rows) == 2


@pytest.mark.django_db
def test_invalid_filter(order_data):
    with pytest.raises(InvalidFilterError):
        Report(queryset=order_data, filters={"unknown__gte": 1}).run()


@pytest.mark.django_db
def test_custom_filter(order_data):
    report = Report(
        queryset=order_data,
        filters={"completed": True},
        custom_filters={"completed": CompletedOnlyFilter()},
    )
    rows = report.run()
    assert len(rows) == 2
