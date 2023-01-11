import inspect
import tempfile
from unittest import TestCase
from unittest.mock import patch

from bx_py_utils import stack_info
from bx_py_utils.stack_info import FrameNotFound


def indirect_call():
    return stack_info.last_frame_outside_path(file_path=stack_info.__file__)


class StackInfoTestCase(TestCase):
    def test_last_frame_outside_path(self):
        frame = stack_info.last_frame_outside_path(file_path=stack_info.__file__)
        assert frame.function == 'test_last_frame_outside_path'
        assert frame.filename == __file__
        assert 'frame = stack_info.last_frame_outside_path(' in frame.code_context[0]

    def test_last_frame_outside_path_indirect(self):
        frame = indirect_call()
        assert frame.function == 'indirect_call'
        assert frame.filename == __file__
        assert 'return stack_info.last_frame_outside_path(' in frame.code_context[0]

    def test_no_stack(self):
        with patch.object(inspect, 'stack', return_value=None):
            with self.assertRaises(RuntimeError) as cm:
                indirect_call()
        self.assertEqual(
            cm.exception.args,
            ('Can not get stack frame. Current interpreter has no support for them?',),
        )

    def test_not_existing_path(self):
        with self.assertRaises(NotADirectoryError) as cm:
            stack_info.last_frame_outside_path(file_path='/not/existing/path')
        self.assertEqual(
            cm.exception.args,
            ('Directory does not exists: "/not/existing"',),
        )

    def test_frame_not_found(self):
        with tempfile.NamedTemporaryFile() as tmp_file:
            with self.assertRaises(FrameNotFound) as cm:
                stack_info.last_frame_outside_path(file_path=tmp_file.name)
            self.assertEqual(
                str(cm.exception),
                f'Frame outside "{tmp_file.name}" not found!',
            )
