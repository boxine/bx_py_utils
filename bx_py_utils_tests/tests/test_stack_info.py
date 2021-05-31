import inspect
import tempfile
from unittest.mock import patch

import pytest

from bx_py_utils import stack_info
from bx_py_utils.stack_info import FrameNotFound


def indirect_call():
    return stack_info.last_frame_outside_path(file_path=stack_info.__file__)


def test_last_frame_outside_path():
    frame = stack_info.last_frame_outside_path(file_path=stack_info.__file__)
    assert frame.function == 'test_last_frame_outside_path'
    assert frame.filename == __file__
    assert 'frame = stack_info.last_frame_outside_path(' in frame.code_context[0]


def test_last_frame_outside_path_indirect():
    frame = indirect_call()
    assert frame.function == 'indirect_call'
    assert frame.filename == __file__
    assert 'return stack_info.last_frame_outside_path(' in frame.code_context[0]


def test_no_stack():
    with patch.object(inspect, 'stack', return_value=None):
        with pytest.raises(RuntimeError) as cm:
            indirect_call()
    assert str(cm.value) == 'Can not get stack frame. Current interpreter has no support for them?'


def test_not_existing_path():
    with pytest.raises(NotADirectoryError) as cm:
        stack_info.last_frame_outside_path(file_path='/not/existing/path')
    assert str(cm.value) == 'Directory does not exists: "/not/existing"'


def test_frame_not_found():
    with tempfile.NamedTemporaryFile() as tmp_file:
        with pytest.raises(FrameNotFound) as cm:
            stack_info.last_frame_outside_path(file_path=tmp_file.name)
        assert str(cm.value) == f'Frame outside "{tmp_file.name}" not found!'
