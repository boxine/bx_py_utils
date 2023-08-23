import bx_py_utils
import bx_py_utils_tests
from bx_py_utils.test_utils.unittest_utils import BaseDocTests, DocTestResults


class DocTests(BaseDocTests):
    def test_doctests(self):
        results = self.run_doctests(
            modules=(bx_py_utils, bx_py_utils_tests),
            excludes=('**/bx_py_utils_tests/tests/doctest_skip.py',),
        )
        self.assertIsInstance(results, DocTestResults)
        self.assertGreaterEqual(results.passed, 80)
        self.assertEqual(results.skipped, 1)  # doctest_skip.py
        self.assertLessEqual(results.failed, 0)  # Failing test in doctest_skip.py skipped?

    def test_doctests_without_excludes(self):
        results = self.run_doctests(
            modules=(bx_py_utils.test_utils,),
            excludes=None,  # <<< should be optional!
        )
        self.assertIsInstance(results, DocTestResults)
