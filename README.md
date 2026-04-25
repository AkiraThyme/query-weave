# QueryWeave

[![Tests](https://img.shields.io/github/actions/workflow/status/AkiraThyme/query-weave/ci.yml?label=tests)](https://github.com/AkiraThyme/query-weave/actions)
[![PyPI](https://img.shields.io/pypi/v/queryweave)](https://pypi.org/project/queryweave/)
[![License](https://img.shields.io/github/license/AkiraThyme/query-weave)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/queryweave)](https://pypi.org/project/queryweave/)

**Reusable Django ORM reporting toolkit for filters, groupings, aggregations, and exports.**

## Why QueryWeave?
Django teams often repeat similar filtering, grouping, and export logic across services. QueryWeave provides a reusable report engine so you can define reports declaratively and keep business query logic clean and testable.

## Features
- QuerySet-based report engine
- Safe reusable filters with Django lookup support
- Grouping + aggregation parser (`sum(price)`, `count(id)`)
- JSON and CSV exporters
- Debug mode with SQL + execution timing
- Slow query warning logs
- Extension points for custom filters, aggregations, and exporters
- CLI support for YAML report configs

## Installation
### Local editable install
```bash
pip install -e .
```

### From GitHub
```bash
pip install git+https://github.com/AkiraThyme/query-weave.git
```

### From PyPI (after publishing)
```bash
pip install queryweave
```

## Quickstart
```python
from queryweave import Report

report = Report(
    queryset=Order.objects.all(),
    filters={"status": "completed", "created_at__gte": "2026-01-01"},
    group_by=["category"],
    aggregates={"total_sales": "sum(price)", "order_count": "count(id)"},
    order_by=["-total_sales"],
)

rows = report.run()
```

## Export examples
```python
from queryweave.exporters.csv import CSVExporter
from queryweave.exporters.json import JSONExporter

payload = report.run()
print(JSONExporter().export(payload))
print(CSVExporter().export(payload))
```

## Custom filter example
```python
from queryweave.filters.base import BaseFilter

class RecentDaysFilter(BaseFilter):
    def apply(self, queryset, key, value):
        return queryset.filter(created_at__gte=value)
```

## Custom exporter example
Subclass `queryweave.exporters.base.BaseExporter` and implement `export(data) -> str`.

## Build and publish
```bash
./scripts/build.sh
./scripts/publish-test.sh
./scripts/publish.sh
```

## Versioning and releases
QueryWeave follows semantic versioning: `MAJOR.MINOR.PATCH`.

Before publishing:
1. Bump `version` in `pyproject.toml`.
2. Rebuild distributions: `./scripts/build.sh`.
3. Verify package metadata: `python -m twine check dist/*`.
4. Publish to TestPyPI first: `./scripts/publish-test.sh`.
5. Publish to PyPI: `./scripts/publish.sh`.

You can also publish from GitHub Actions by pushing a version tag, e.g. `v0.1.1`, after configuring `PYPI_API_TOKEN` repository secret.

## Development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
ruff check .
black --check .
mypy queryweave
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT. See [LICENSE](LICENSE).
