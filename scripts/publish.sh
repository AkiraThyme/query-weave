#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade build twine
python -m build
python -m twine upload dist/*
