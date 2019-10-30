test:
	python setup.py test

format:
#	pip install -e .[dev]
	black evilunit setup.py

lint:
#	pip install -e .[dev]
	flake8 evilunit --ignore W503,E203,E501

typing:
#	pip install -e .[dev]
	mypy --strict --strict-equality --ignore-missing-imports evilunit

examples:
	$(MAKE) -C examples/openapi

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/evilunit-$(shell cat VERSION)*
	twine upload dist/evilunit-$(shell cat VERSION)*

.PHONY: test format lint build upload examples typing
