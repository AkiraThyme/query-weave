"""Custom exceptions for QueryWeave."""


class QueryWeaveError(Exception):
    """Base package error."""


class InvalidReportConfigError(QueryWeaveError):
    """Raised when a report configuration is invalid."""


class InvalidFilterError(QueryWeaveError):
    """Raised when filters are malformed or unsafe."""


class InvalidAggregationError(QueryWeaveError):
    """Raised when an aggregation expression is malformed or unsafe."""


class ExportError(QueryWeaveError):
    """Raised when exporting report data fails."""
