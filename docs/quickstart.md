# Quickstart

```python
from queryweave import Report

report = Report(
    queryset=Order.objects.all(),
    filters={"status": "completed"},
    aggregates={"total_sales": "sum(price)"},
)
print(report.run())
```
