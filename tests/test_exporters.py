import json

import pytest

from queryweave import Report
from queryweave.exporters.csv import CSVExporter
from queryweave.exporters.json import JSONExporter


@pytest.mark.django_db
def test_csv_export(order_data):
    data = Report(queryset=order_data, filters={"status": "completed"}).run()
    output = CSVExporter().export(data)
    assert "status" in output
    assert "completed" in output


@pytest.mark.django_db
def test_json_export(order_data):
    data = Report(queryset=order_data, filters={"status": "completed"}).run()
    output = JSONExporter().export(data)
    parsed = json.loads(output)
    assert len(parsed) == 2


def test_empty_exporters():
    assert CSVExporter().export([]) == ""
    assert JSONExporter().export([]) == "[]"


def test_csv_export_rejects_non_dict_rows():
    with pytest.raises(ValueError):
        CSVExporter().export(["not-a-dict"])
