"""
    Assert complex output via auto updated snapshot files with nice diff error messages.
"""
import json
import pathlib
import pprint
import re
from collections import Counter
from typing import Any, Callable, Union

from bx_py_utils.compat import removeprefix
from bx_py_utils.path import assert_is_dir
from bx_py_utils.stack_info import last_frame_outside_path
from bx_py_utils.test_utils.assertion import (
    _unified_diff,
    assert_equal,
    assert_text_equal,
    pformat_unified_diff,
    text_unified_diff,
)


SELF_FILE_PATH = pathlib.Path(__file__)
_AUTO_SNAPSHOT_NAME_COUNTER = Counter()


def _write_json(obj, snapshot_file):
    with snapshot_file.open('w') as snapshot_handle:
        json.dump(obj, snapshot_handle, ensure_ascii=False, indent=4, sort_keys=True)


def _get_caller_names(root_dir: Union[pathlib.Path, str] = None, snapshot_name: str = None):
    """
    Helper to get snapshot directory and name by stack frame info, but only if not given.

    Note:
      This only works if this function is in the same file as the snapshot functions.
      Because we compare the file path in stack frame to get the caller frame.
      (If this function will be moved: the file path in last_frame_outside_path() must be updated, too.)
    """
    if root_dir:
        if not isinstance(root_dir, pathlib.Path):
            root_dir = pathlib.Path(root_dir)
        assert_is_dir(root_dir)

    if snapshot_name is not None:
        assert re.match(r'^[-_.a-zA-Z0-9]+$', snapshot_name), (
            f'Invalid snapshot name {snapshot_name!r}'
        )

    if not root_dir or not snapshot_name:
        # Set "root_dir" and "snapshot_name" if missing by stack frame info.

        # Get the caller stack frame (First frame that is outside this file path):
        external_stack_frame = last_frame_outside_path(file_path=SELF_FILE_PATH)
        caller_path = pathlib.Path(external_stack_frame.filename)
        assert caller_path.is_file()
        if not root_dir:
            root_dir = caller_path.parent

        if not snapshot_name:
            test_func_name = external_stack_frame.function
            test_func_name = removeprefix(test_func_name, 'test_')  # make it a little bit shorter

            snapshot_name = f'{caller_path.stem}_{test_func_name}'

            # Add a counter to the snapshot name, to support more than one
            # snapshot calls in the same test ;)
            counter_key = (root_dir, snapshot_name)
            _AUTO_SNAPSHOT_NAME_COUNTER[counter_key] += 1
            call_count = _AUTO_SNAPSHOT_NAME_COUNTER[counter_key]

            snapshot_name = f'{snapshot_name}_{call_count}.snapshot'

    return root_dir, snapshot_name


def assert_text_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: str = None,
    extension: str = '.txt',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = text_unified_diff
):
    """
    Assert "text" string via snapshot file
    """
    root_dir, snapshot_name = _get_caller_names(root_dir, snapshot_name)
    assert re.match(r'^[-_.a-zA-Z0-9]*$', extension), f'Invalid extension {extension!r}'
    assert isinstance(got, str)

    snapshot_file = pathlib.Path(root_dir) / f'{snapshot_name}.snapshot{extension}'
    try:
        expected = snapshot_file.read_text()
    except (FileNotFoundError, OSError):
        snapshot_file.write_text(got)
        raise

    if got != expected:
        snapshot_file.write_text(got)

        # display error message with diff:
        assert_text_equal(
            got, expected,
            fromfile=fromfile, tofile=tofile,
            diff_func=diff_func
        )


def assert_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: str = None,
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = pformat_unified_diff
):
    """
    Assert given data serialized to JSON snapshot file.
    """
    root_dir, snapshot_name = _get_caller_names(root_dir, snapshot_name)
    assert isinstance(got, (dict, list))

    snapshot_file = pathlib.Path(root_dir) / f'{snapshot_name}.json'
    try:
        with snapshot_file.open('r') as snapshot_handle:
            expected = json.load(snapshot_handle)
    except (ValueError, OSError, FileNotFoundError):
        _write_json(got, snapshot_file)
        raise

    if got != expected:
        _write_json(got, snapshot_file)

        # display error message with diff:
        assert_equal(
            got, expected,
            fromfile=fromfile, tofile=tofile,
            diff_func=diff_func
        )


def assert_py_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: Any = None,
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = _unified_diff
):
    """
    Assert complex python objects vio PrettyPrinter() snapshot file.

    Advantage over JSON:
     - More python object types are supported
     - The comparison is stricter. e.g.: UUID object instance vs. UUID string
    """
    root_dir, snapshot_name = _get_caller_names(root_dir, snapshot_name)

    got_str = pprint.pformat(got, indent=4, width=120)

    snapshot_file = pathlib.Path(root_dir) / f'{snapshot_name}.txt'
    try:
        expected_str = snapshot_file.read_text()
    except FileNotFoundError:
        snapshot_file.write_text(got_str)
        raise

    if got_str != expected_str:
        snapshot_file.write_text(got_str)

        # display error message with diff:
        assert_equal(
            got_str, expected_str,
            fromfile=fromfile, tofile=tofile,
            diff_func=diff_func
        )
