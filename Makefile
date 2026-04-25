install:
	pip install -e .

build:
	python -m build

publish:
	twine upload dist/*

publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
