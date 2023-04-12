SHELL := /bin/bash
MAX_LINE_LENGTH := 119

all: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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
	poetry run isort .

tox-listenvs: check-poetry ## List all tox test environments
	poetry run tox --listenvs

tox: check-poetry ## Run tests via tox with all environments
	poetry run tox p

test: ## Run tests
	poetry run python -m unittest --verbose --locals

coverage:  ## Run tests with coverage
	poetry run coverage run
	poetry run coverage combine --append
	poetry run coverage report
	poetry run coverage xml
	poetry run coverage json

update-test-snapshot-files:   ## Update all snapshot files (by remove and recreate all snapshot files)
	find . -type f -name '*.snapshot.*' -delete
	RAISE_SNAPSHOT_ERRORS=0 poetry run python -m unittest

mypy:  ## Run mypy
	poetry run mypy .

safety:  ## Run https://github.com/pyupio/safety
	poetry run safety check --full-report

publish: install  ## Release new version to PyPi
	poetry run publish

clean: ## Remove created files from the test project
	git clean -dfX bx_py_utils_tests/

.PHONY: help install lint fix publish test clean
