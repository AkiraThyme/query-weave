"""Sample QueryWeave report snippets."""

from queryweave import Report


def build_sales_report(order_queryset):
    return Report(
        queryset=order_queryset,
        filters={"status": "completed"},
        group_by=["product__category"],
        aggregates={"total_sales": "sum(price)", "order_count": "count(id)"},
        order_by=["-total_sales"],
    )
