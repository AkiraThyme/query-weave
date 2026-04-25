#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade build twine
python -m build
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

echo "Install from TestPyPI:"
echo "pip install -i https://test.pypi.org/simple/ queryweave"
