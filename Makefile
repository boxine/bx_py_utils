SHELL := /bin/bash
MAX_LINE_LENGTH := 119

all: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "$(shell poetry --version 2>/dev/null)" == *"Poetry"* ]] ; \
	then \
		echo "Poetry found, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry:  ## install or update poetry
	curl -sSL https://install.python-poetry.org | python3 -

install: check-poetry  ## install project via poetry
	python3 -m venv .venv
	poetry install

update: check-poetry  ## update the sources and installation and generate "conf/requirements.txt"
	python3 -m venv .venv
	poetry self update
	poetry update -v
	poetry install

lint: ## Run code formatters and linter
	poetry run darker --diff --check
	poetry run isort --check-only .
	poetry run flake8 .

fix-code-style: ## Fix code formatting
	poetry run darker
	poetry run black --verbose --safe --line-length=${MAX_LINE_LENGTH} --skip-string-normalization .
	poetry run isort .

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run pytest via tox with all environments
	poetry run tox

tox-py38: check-poetry ## Run pytest via tox with *python v3.8*
	poetry run tox -e py38

tox-py39: check-poetry ## Run pytest via tox with *python v3.9*
	poetry run tox -e py39

tox-py310: check-poetry ## Run pytest via tox with *python v3.10*
	poetry run tox -e py310

pytest: check-poetry ## Run pytest
	poetry run pytest

pytest-ci: check-poetry ## Run pytest with CI settings
	poetry run pytest -c pytest-ci.ini

test: pytest

mypy:  ## Run mypy
	poetry run mypy .

publish: ## Release new version to PyPi
	poetry run publish

clean: ## Remove created files from the test project
	git clean -dfX bx_py_utils_tests/

.PHONY: help install lint fix pytest publish test clean