"""Simple CLI for running YAML-defined reports."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

from queryweave import Report
from queryweave.exporters.csv import CSVExporter
from queryweave.exporters.json import JSONExporter


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyYAML is required for CLI usage: pip install queryweave[cli]") from exc

    return yaml.safe_load(path.read_text())


def _resolve_queryset(path: str) -> Any:
    module_name, attr = path.split(":", maxsplit=1)
    module = importlib.import_module(module_name)
    return getattr(module, attr)


def main() -> int:
    parser = argparse.ArgumentParser(prog="queryweave", description="Run QueryWeave reports")
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Run a report from YAML")
    run.add_argument("config", type=Path)
    run.add_argument("--format", choices=["json", "csv"], default="json")

    args = parser.parse_args()

    if args.command != "run":
        parser.print_help()
        return 1

    try:
        config = _load_yaml(args.config)
        queryset = _resolve_queryset(config["queryset"])
        report = Report(
            queryset=queryset,
            filters=config.get("filters", {}),
            group_by=config.get("group_by", []),
            aggregates=config.get("aggregates", {}),
            order_by=config.get("order_by", []),
            page=config.get("page"),
            page_size=config.get("page_size"),
            debug=config.get("debug"),
        )
        data = report.run()
        if args.format == "csv":
            print(CSVExporter().export(data))
        else:
            print(JSONExporter().export(data))
        return 0
    except Exception as exc:  # pragma: no cover - integration pathway
        print(f"QueryWeave CLI error: {exc}")
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
