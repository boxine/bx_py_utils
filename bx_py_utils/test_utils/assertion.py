import difflib
import pprint
from typing import Any, Type

from bx_py_utils.humanize.pformat import pformat


def text_ndiff(txt1, txt2, fromfile=None, tofile=None):
    """
    Generate a `ndiff` between two text strings.
    (fromfile/tofile are ignored, only for compatibility with text_unified_diff signature)
    """
    return '\n'.join(difflib.ndiff(txt1.splitlines(), txt2.splitlines()))


def pformat_ndiff(obj1, obj2, fromfile=None, tofile=None):
    """
    Generate a `ndiff` from two objects, using `pformat()`
    (fromfile/tofile are ignored, only for compatibility with pformat_unified_diff signature)
    """
    return '\n'.join(
        difflib.ndiff(
            pformat(obj1).splitlines(),
            pformat(obj2).splitlines()
        )
    )


def _unified_diff(txt1, txt2, fromfile: str = 'got', tofile: str = 'expected'):
    assert isinstance(txt1, str)
    assert isinstance(txt2, str)
    return '\n'.join(
        difflib.unified_diff(
            txt1.splitlines(), txt2.splitlines(),
            fromfile=fromfile, tofile=tofile
        )
    )


def text_unified_diff(txt1, txt2, fromfile: str = 'got', tofile: str = 'expected'):
    """
    Generate a unified diff between two text strings.
    """
    return _unified_diff(txt1, txt2, fromfile=fromfile, tofile=tofile)


def pformat_unified_diff(obj1, obj2, fromfile: str = 'got', tofile: str = 'expected'):
    """
    Generate a unified diff from two objects, using `pformat()`
    Fallback to pprint.pformat() if JSON is equal
    """
    obj1_pformat = pformat(obj1)
    obj2_pformat = pformat(obj2)
    if obj1 != obj2 and obj1_pformat == obj2_pformat:
        # The python objects are not equal, but the JSON representation are equal!
        # This can happen if tuple() are used: JSON will convert them to lists.
        # Work-a-round: Generate the diff with pformat:
        obj1_pformat = pprint.pformat(obj1, width=120)
        obj2_pformat = pprint.pformat(obj2, width=120)

    return _unified_diff(obj1_pformat, obj2_pformat, fromfile=fromfile, tofile=tofile)


def assert_equal(
    obj1,
    obj2,
    msg: Any = 'Objects are not equal:',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func=pformat_unified_diff,
    raise_cls: Type[Exception] = AssertionError,
):
    """
    Check if the two objects are the same. Display a nice diff, using `pformat()`
    """
    if obj1 != obj2:
        raise raise_cls(f'{msg}\n{diff_func(obj1, obj2, fromfile=fromfile, tofile=tofile)}')


def assert_text_equal(
    txt1,
    txt2,
    msg: Any = 'Text not equal:',
    fromfile: str = 'got',
    tofile: str = 'expected',
    diff_func=text_unified_diff,
    raise_cls: Type[Exception] = AssertionError,
):
    """
    Check if the two text strings are the same. Display an error message with a diff.
    """
    assert isinstance(txt1, str)
    assert isinstance(txt2, str)
    if txt1 != txt2:
        raise raise_cls(f'{msg}\n{diff_func(txt1, txt2, fromfile=fromfile, tofile=tofile)}')
