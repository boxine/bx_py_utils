SHELL := /bin/bash

all: help

.PHONY: help
help:  ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -_]+:.*?## / {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Keep local dev dependencies up to date automatically so developers can't forget to update them.
# Runs update-requirements only when uv.lock is missing or older than one day.
# All targets used during local development should call this first.
# Note: uv.lock is listed in .gitignore, so it is absent on a fresh clone.
.PHONY: auto-update-requirements
auto-update-requirements:
	@if [ ! -f uv.lock ] || [ -n "$$(find uv.lock -mtime +0)" ]; then \
		$(MAKE) update-requirements; \
	fi

.PHONY: install
install:  ## Install the project in a Python virtualenv
	$(MAKE) auto-update-requirements

.PHONY: update-requirements
update-requirements:  ## Update requirements
	uv lock --upgrade
	uv audit
	uv sync

.PHONY: lint
lint: ## Check/fix code style by running: "ruff check"
	$(MAKE) auto-update-requirements
	uv run ruff check

.PHONY: lint-fix
lint-fix: ## Check/fix code style by running: "ruff check --fix"
	$(MAKE) auto-update-requirements
	uv run ruff check --fix

.PHONY: coverage-report
coverage-report:  ## Creates coverage report
	$(MAKE) auto-update-requirements
	uv run coverage combine --append
	uv run coverage report
	uv run coverage xml
	uv run coverage json

.PHONY: coverage
coverage:  ## Run tests with coverage (prefer the "nox" target)
	uv run coverage run
	$(MAKE) coverage-report

.PHONY: nox
nox:  ## Run tests via nox with all environments and create coverage report
	uv run nox
	$(MAKE) coverage-report

.PHONY: test
test: ## Run tests
	$(MAKE) auto-update-requirements
	uv run python3 -m unittest --verbose --locals

.PHONY: update-test-snapshot-files
update-test-snapshot-files:   ## Update all snapshot files (by remove and recreate all snapshot files)
	$(MAKE) auto-update-requirements
	find . -type f -name '*.snapshot.*' -delete
	RAISE_SNAPSHOT_ERRORS=0 uv run python3 -m unittest

.PHONY: mypy
mypy:  ## Run mypy
	$(MAKE) auto-update-requirements
	uv run mypy .

.PHONY: pip-audit
pip-audit:  ## Run https://github.com/pypa/pip-audit
	$(MAKE) auto-update-requirements
	uv export --no-header --frozen --no-editable --no-emit-project -o /tmp/temp_requirements.txt
	uv run pip-audit --strict --require-hashes --disable-pip -r /tmp/temp_requirements.txt

.PHONY: publish
publish:  ## Release new version to PyPi
	$(MAKE) auto-update-requirements
	uv run python3 bx_py_utils_tests/publish.py

.PHONY: clean
clean: ## Remove created files from the test project
	git clean -dfX bx_py_utils_tests/
