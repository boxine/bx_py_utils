SHELL := /bin/bash

all: help

help:  ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -_]+:.*?## / {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-base-req:  ## Install needed base packages via apt
	sudo apt install python3-pip python3-venv

install:  ## Install the project in a Python virtualenv
	python3 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -U uv
	.venv/bin/uv sync

update-requirements:  ## Update requirements
	python3 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -U uv
	.venv/bin/uv lock --upgrade
	.venv/bin/uv sync

lint: ## Run code formatters and linter
	.venv/bin/darker --diff --check
	.venv/bin/flake8 .

fix-code-style: ## Fix code formatting
	.venv/bin/darker
	.venv/bin/flake8 .

tox-listenvs:  ## List all tox test environments
	.venv/bin/tox --listenvs

tox:  ## Run tests via tox with all environments
	.venv/bin/tox

test: ## Run tests
	.venv/bin/python3 -m unittest --verbose --locals

coverage:  ## Run tests with coverage
	.venv/bin/coverage run
	.venv/bin/coverage combine --append
	.venv/bin/coverage report
	.venv/bin/coverage xml
	.venv/bin/coverage json

update-test-snapshot-files:   ## Update all snapshot files (by remove and recreate all snapshot files)
	find . -type f -name '*.snapshot.*' -delete
	RAISE_SNAPSHOT_ERRORS=0 .venv/bin/python3 -m unittest

mypy:  ## Run mypy
	.venv/bin/mypy .

pip-audit:  ## Run https://github.com/pypa/pip-audit
	.venv/bin/uv export --no-header --frozen --no-editable --no-emit-project -o /tmp/temp_requirements.txt
	.venv/bin/pip-audit --strict --require-hashes -r /tmp/temp_requirements.txt

publish:  ## Release new version to PyPi
	.venv/bin/pip install -e .
	.venv/bin/python3 bx_py_utils_tests/publish.py

clean: ## Remove created files from the test project
	git clean -dfX bx_py_utils_tests/

.PHONY: help install lint fix publish test clean
