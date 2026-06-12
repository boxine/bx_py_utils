# CLAUDE.md — Project Guide for Claude Code

> This file is read automatically by [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview).
> Keep it up to date: when conventions change, update this file in the same commit.

---

## Language

**Always respond and write in English**, regardless of the language used in the question or request.
This applies to code comments, commit messages, PR descriptions, documentation, and all other output.

---

## Version Management

The version is an **integer string** in `bx_py_utils/__init__.py` (e.g. `'117'`).
It is **not** managed in `pyproject.toml` — hatchling reads it from `__init__.py` via `[tool.hatch.version]`.

Every PR must increment the version by 1, so the project can be published immediately after merging.

---

## Testing

Tests use `unittest.TestCase`. Do **not** write flat `def test_*()` functions at module level.
There is an automated check (`test_no_ignored_test_function`) that enforces this and will fail the test run.

### Snapshot tests

Some tests use snapshot files (`*.snapshot.*`). To regenerate them, use `make update-test-snapshot-files`.

---

## Documentation

### README auto-generation

The section in `README.md` between the `✂✂✂ auto generated` markers is generated automatically
from module docstrings via `bx_py_utils.auto_doc`. The test `test_readme.py` enforces it is up to date
and rewrites the block in place when run. **Never edit that section manually.**

To exclude a docstring from appearing in the README, prefix it with `[no-doc]`:
```python
class Foo:
    """[no-doc]
    This docstring will not appear in the README.
    """
```

### doc_write system

The project has a custom doc system (`bx_py_utils/doc_write/`). Docstrings prefixed with `DocWrite:`
are collected and written to documentation files. Configuration is in `pyproject.toml` under
`[tool.bx_py_utils.doc_write]`.

When adding or modifying code, **actively add meaningful `DocWrite:` docstrings** where appropriate.
Prefer placing them in **test files** rather than production code to keep production code readable.

Format:
```python
def my_func():
    """DocWrite: some/file.md # Headline
    Description that will appear in the generated markdown file.
    """
```

The file path is relative to `output_base_path` (configured as `.` in `pyproject.toml`).
Reuse existing headlines to extend a section rather than creating new ones.

**Update workflow:** After changing any `DocWrite:` docstring, run the tests. The test
`test_up2date_docs` will auto-write the generated doc files but then **fail** with
"No files should be updated, commit the changes". Commit the updated files, then the test passes.

---

## Git Workflow

### Branches and PRs

Each new feature or fix is developed in a separate branch and submitted as a PR with **exactly one commit**.
Keep amending that single commit (`git commit --amend`) until everything is ready, then open the PR for review.

### Commit message

The subject line must be **50 characters or less**. Use the full budget to describe **what** was
changed as precisely as possible — a reader should understand the change without looking at the diff.

Use one of these prefixes:
- `New:` — new feature or utility
- `Fix:` — bug fix
- `Update:` — change to existing code

The body should explain **why** the change was made, not what — the what is visible in the diff.

When the change relates to an external package, website, or service, always include a link —
in the commit body, code comments, PR description, or documentation.
