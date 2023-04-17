from __future__ import annotations

import fnmatch


def filename_matcher(*, patterns: list | tuple, file_path: str) -> bool:
    """
    Enhance fnmatch that accept a list of patterns.

    >>> filename_matcher(patterns=['*bar.py'], file_path='/bar/test.py')
    False
    >>> filename_matcher(patterns=['*bar.py'], file_path='/foo/a-match-bar.py')
    True
    """
    assert isinstance(file_path, str), f'No string: {file_path=}'

    for pattern in patterns:
        assert isinstance(pattern, str), f'No string: {pattern=}'
        if fnmatch.fnmatch(file_path, pattern):
            return True  # File path match one of the pattern

    return False  # File path doesn't match any pattern
