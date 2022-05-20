"""
    Assert complex output via auto updated snapshot files with nice diff error messages.

    To update all snapshot files, run your tests with RAISE_SNAPSHOT_ERRORS=0 in environment.
"""
import hashlib
import json
import os
import pathlib
import pprint
import re
from collections import Counter
from typing import Any, Callable, Optional, Union

from bx_py_utils.html_utils import get_html_elements, pretty_format_html, validate_html


try:
    from lxml import html  # lxml is optional requirement
except ModuleNotFoundError:
    html = None


try:
    from bs4 import BeautifulSoup  # BeautifulSoup4 is optional requirement
except ModuleNotFoundError:
    BeautifulSoup = None


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


RAISE_SNAPSHOT_ERRORS = os.environ.get('RAISE_SNAPSHOT_ERRORS') not in ('0', 'false')
SELF_FILE_PATH = pathlib.Path(__file__)
_AUTO_SNAPSHOT_NAME_COUNTER = Counter()
_UNIFY_NEWLINES_RE = r'\r?\n'


def _write_json(obj, snapshot_file):
    with snapshot_file.open('w') as snapshot_handle:
        json.dump(obj, snapshot_handle, ensure_ascii=False, indent=4, sort_keys=True)


def _get_caller_names(
        root_dir: Union[pathlib.Path, str] = None,
        snapshot_name: str = None,
        self_file_path: Union[pathlib.Path, str] = None):
    """
    Helper to get snapshot directory and name by stack frame info, but only if not given.

    self_file_path is used to get the stack frame outside of the caller for set path/filename.
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

        if not self_file_path:
            self_file_path = SELF_FILE_PATH

        # Get the caller stack frame (First frame that is outside this file path):
        external_stack_frame = last_frame_outside_path(file_path=self_file_path)
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


def _get_snapshot_file(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    extension: str = None,
    self_file_path: Union[pathlib.Path, str] = None,
):
    # Auto set dir/name via stask information, if not set:
    root_dir, snapshot_name = _get_caller_names(root_dir, snapshot_name, self_file_path)

    assert re.match(r'^[-_.a-zA-Z0-9]*$', extension), f'Invalid extension {extension!r}'

    if not snapshot_name.endswith('.snapshot'):
        snapshot_name += '.snapshot'

    snapshot_file = pathlib.Path(root_dir) / f'{snapshot_name}{extension}'
    return snapshot_file


def assert_text_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: str = None,
    extension: str = '.txt',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = text_unified_diff,
    self_file_path: Union[pathlib.Path, str] = None,
):
    """
    Assert "text" string via snapshot file
    """
    assert isinstance(got, str)

    snapshot_file = _get_snapshot_file(root_dir, snapshot_name, extension, self_file_path)
    try:
        expected = snapshot_file.read_bytes().decode('utf-8')
    except (FileNotFoundError, OSError):
        snapshot_file.write_bytes(got.encode('utf-8'))
        if not RAISE_SNAPSHOT_ERRORS:
            return
        raise

    if got != expected:
        snapshot_file.write_bytes(got.encode('utf-8'))

        if re.sub(_UNIFY_NEWLINES_RE, '', got) == re.sub(_UNIFY_NEWLINES_RE, '', expected):
            raise AssertionError(f'Differing newlines: Expected {expected!r}, got {got!r}')

        if RAISE_SNAPSHOT_ERRORS:
            # display error message with diff:
            assert_text_equal(
                got, expected,
                fromfile=fromfile, tofile=tofile,
                diff_func=diff_func
            )


def assert_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: Optional[Union[dict, list]] = None,
    extension: str = '.json',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = pformat_unified_diff,
    self_file_path: Union[pathlib.Path, str] = None,
):
    """
    Assert given data serialized to JSON snapshot file.

    Note: You can't assert objects that contains tuple() !
          Use assert_py_snapshot() in this case.
    """
    assert got is None or isinstance(got, (dict, list)), \
        f'Not JSON-serializable: {got!r} is not a dict or list, but a {type(got).__name__}'

    snapshot_file = _get_snapshot_file(root_dir, snapshot_name, extension, self_file_path)
    try:
        with snapshot_file.open('r') as snapshot_handle:
            expected = json.load(snapshot_handle)
    except (ValueError, OSError, FileNotFoundError):
        _write_json(got, snapshot_file)
        if not RAISE_SNAPSHOT_ERRORS:
            return
        raise

    if got != expected:
        _write_json(got, snapshot_file)

        if RAISE_SNAPSHOT_ERRORS:
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
    extension: str = '.txt',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = _unified_diff,
    self_file_path: Union[pathlib.Path, str] = None,
):
    """
    Assert complex python objects vio PrettyPrinter() snapshot file.

    Advantage over JSON:
     - More python object types are supported
     - The comparison is stricter. e.g.: UUID object instance vs. UUID string
    """
    got_str = pprint.pformat(got, indent=4, width=120)

    snapshot_file = _get_snapshot_file(root_dir, snapshot_name, extension, self_file_path)
    try:
        expected_str = snapshot_file.read_text()
    except FileNotFoundError:
        snapshot_file.write_text(got_str)
        if not RAISE_SNAPSHOT_ERRORS:
            return
        raise

    if got_str != expected_str:
        snapshot_file.write_text(got_str)

        if RAISE_SNAPSHOT_ERRORS:
            # display error message with diff:
            assert_equal(
                got_str, expected_str,
                fromfile=fromfile, tofile=tofile,
                diff_func=diff_func
            )


def assert_html_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: str = None,
    extension: str = '.html',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = text_unified_diff,
    self_file_path: Union[pathlib.Path, str] = None,
    validate: bool = True,
    validate_kwargs: dict = None,
    pretty_format: bool = True,
    pretty_kwargs: dict = None,
    query_selector: str = None,
    query_selector_kwargs: dict = None
):
    """
    Assert "html" string via snapshot file with validate and pretty format
    Use "query_selector" to limit the snapshot to one or more elements. If the selector does not
    find any elements, an ElementsNotFoundError is raised.
    """
    assert isinstance(got, str)

    if validate:
        if validate_kwargs is None:
            validate_kwargs = {}
        validate_html(got, **validate_kwargs)

    if query_selector:
        if query_selector_kwargs is None:
            query_selector_kwargs = {}
        got = get_html_elements(got, query_selector, **query_selector_kwargs)

    if pretty_format:
        if pretty_kwargs is None:
            pretty_kwargs = {}
        got = pretty_format_html(got, **pretty_kwargs)

    assert_text_snapshot(
        root_dir=root_dir,
        snapshot_name=snapshot_name,
        got=got,
        extension=extension,
        fromfile=fromfile,
        tofile=tofile,
        diff_func=diff_func,
        self_file_path=self_file_path,
    )


def _binary_str(data):
    return f'{len(data)} Bytes, MD5 {hashlib.md5(data).hexdigest()}'


def binary_diff(got, expected, fromfile, tofile):
    expected_repr = _binary_str(expected)
    got_repr = _binary_str(got)
    return (
        f'{tofile}: {expected_repr}\n'
        f'{fromfile}: {got_repr}'
    )


def assert_binary_snapshot(
    root_dir: Union[pathlib.Path, str] = None,
    snapshot_name: str = None,
    got: str = None,
    extension: str = '.bin',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func: Callable = binary_diff,
    self_file_path: Union[pathlib.Path, str] = None,
):
    """
    Assert binary data via snapshot file
    """
    assert isinstance(got, bytes)

    snapshot_file = _get_snapshot_file(root_dir, snapshot_name, extension, self_file_path)
    try:
        expected = snapshot_file.read_bytes()
    except (FileNotFoundError, OSError):
        snapshot_file.write_bytes(got)
        if not RAISE_SNAPSHOT_ERRORS:
            return
        raise

    if got != expected:
        snapshot_file.write_bytes(got)

        if RAISE_SNAPSHOT_ERRORS:
            assert_equal(
                got, expected,
                fromfile=fromfile, tofile=tofile,
                diff_func=diff_func
            )
