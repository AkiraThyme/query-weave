#!/usr/bin/env bash
set -euo pipefail

# Local parity runner for .github/workflows/ci.yml
# Usage:
#   scripts/ci-local.sh
#   SKIP_INSTALL=1 scripts/ci-local.sh

if [[ "${SKIP_INSTALL:-0}" != "1" ]]; then
  python -m pip install --upgrade pip
  python -m pip install -e '.[dev,cli]'
fi

ruff check .
black --check .
mypy queryweave
pytest
