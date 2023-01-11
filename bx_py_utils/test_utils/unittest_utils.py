import pprint
import re
from pathlib import Path

from bx_py_utils.path import assert_is_dir


def assert_no_flat_tests_functions(path: Path):
    """
    Check if there exists normal test functions (That will not be executed by normal unittests)
    """
    assert_is_dir(path)

    errors = {}
    for item in path.rglob('test_*.py'):
        content = item.read_text(encoding='UTF-8')
        matches = re.findall(r'^def (test_.+):$', content, re.MULTILINE)
        if matches:
            errors[str(item.relative_to(path))] = matches

    if errors:
        raise AssertionError(f'Flat test files found:\n{pprint.pformat(errors)}')
