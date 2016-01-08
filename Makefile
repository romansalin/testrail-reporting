PYTHON=`which python`

all:
	@echo "make source - Create source package"
	@echo "make clean - Get rid of scratch and byte files"
	@echo "clean-build - remove build artifacts"
    @echo "clean-test - remove test artifacts"
    @echo "clean-pyc - remove Python file artifacts"
    @echo "coverage - check code coverage quickly with the default Python"
    @echo "sdist - package"

.PHONY: help clean clean-pyc clean-build lint test test-all coverage sdist

source:
	$(PYTHON) setup.py sdist

clean: clean-build clean-test clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-test:
	rm -fr .cache/
	rm -fr .eggs/
	rm -fr .tox/
	rm -f .coverage

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +

coverage:
	coverage run setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

sdist: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist
