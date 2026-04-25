# Contributing

Thanks for contributing to QueryWeave!

## Development setup
1. Create virtual environment.
2. Install dependencies: `pip install -e .[dev]`
3. Run checks:
   - `pytest`
   - `ruff check .`
   - `black --check .`
   - `mypy queryweave`

## Pull requests
- Add/adjust tests for behavior changes.
- Keep changes scoped and documented.
- Update CHANGELOG.md for user-facing changes.
