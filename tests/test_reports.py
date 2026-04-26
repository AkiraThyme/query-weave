import logging

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from queryweave import Report
from queryweave.exceptions import InvalidReportConfigError
from tests.testapp.models import Order


@pytest.mark.django_db
def test_report_creation(order_data):
    report = Report(queryset=order_data, filters={"status": "completed"})
    rows = report.run()
    assert len(rows) == 2


@pytest.mark.django_db
def test_grouped_reports(order_data):
    report = Report(
        queryset=order_data,
        group_by=["product__category"],
        aggregates={"total_sales": "sum(price)", "order_count": "count(id)"},
        order_by=["-total_sales"],
    )
    rows = report.run()
    assert rows[0]["total_sales"] >= rows[1]["total_sales"]


@pytest.mark.django_db
def test_pagination(order_data):
    report = Report(queryset=order_data, order_by=["id"], page=1, page_size=2)
    rows = report.run()
    assert len(rows) == 2


@pytest.mark.django_db
def test_invalid_report_config():
    with pytest.raises(InvalidReportConfigError):
        Report(queryset=Order.objects, page=0).run()  # type: ignore[arg-type]

    with pytest.raises(InvalidReportConfigError):
        Report(queryset=Order.objects.all(), page=1).run()

    with pytest.raises(InvalidReportConfigError):
        Report(queryset=Order.objects.all(), page_size=10).run()


@pytest.mark.django_db
def test_debug_mode_logs(order_data, caplog):
    caplog.set_level(logging.INFO, logger="queryweave")
    report = Report(queryset=order_data, debug=True)
    report.run()
    assert any("SQL=" in rec.message for rec in caplog.records)


@pytest.mark.django_db
def test_report_executes_single_query(order_data):
    with CaptureQueriesContext(connection) as queries:
        Report(queryset=order_data).run()
    assert len(queries) == 1


@pytest.mark.django_db
def test_grouped_report_executes_single_query(order_data):
    with CaptureQueriesContext(connection) as queries:
        Report(
            queryset=order_data,
            group_by=["product__category"],
            aggregates={"total_sales": "sum(price)", "order_count": "count(id)"},
            order_by=["-total_sales"],
        ).run()
    assert len(queries) == 1


@pytest.mark.django_db
def test_related_filter_executes_single_query(order_data):
    with CaptureQueriesContext(connection) as queries:
        Report(
            queryset=order_data,
            filters={"product__category__icontains": "book"},
        ).run()
    assert len(queries) == 1
