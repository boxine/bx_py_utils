import bx_py_utils
from bx_py_utils.test_utils.unittest_utils import BaseDocTests


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(modules=(bx_py_utils,))
