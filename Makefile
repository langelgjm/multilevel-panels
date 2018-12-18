install:
	pip install -r requirements.txt
	pip install .

build:
	python setup.py bdist_wheel

develop:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	pip install -e .

test:
	python examples/example.py -v
	pytest --cov=multilevel_panels tests/
	mypy --ignore-missing-imports src/multilevel_panels/multilevel_panels.py tests/test_multilevel_panels.py examples/example.py
