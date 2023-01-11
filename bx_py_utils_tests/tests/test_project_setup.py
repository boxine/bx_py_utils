import subprocess
from pathlib import Path
from unittest import TestCase

import bx_py_utils
from bx_py_utils.path import assert_is_dir, assert_is_file
from bx_py_utils.test_utils.unittest_utils import assert_no_flat_tests_functions


PACKAGE_ROOT = Path(bx_py_utils.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT)
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')


class ProjectSetupTestCase(TestCase):
    def test_code_style(self):
        try:
            output = subprocess.check_output(['make', 'lint'], stderr=subprocess.STDOUT, cwd=PACKAGE_ROOT, text=True)
        except subprocess.CalledProcessError:
            # Code style is not correct -> Try to fix it
            subprocess.check_call(['make', 'fix-code-style'], stderr=subprocess.STDOUT, cwd=PACKAGE_ROOT)

            # Check again:
            subprocess.check_call(['make', 'lint'], cwd=PACKAGE_ROOT)
        else:
            self.assertIn('darker', output)
            self.assertIn('isort', output)
            self.assertIn('flake8', output)

    def test_poetry_check(self):
        output = subprocess.check_output(['poetry', 'check'], cwd=PACKAGE_ROOT, text=True)
        self.assertEqual(output, 'All set!\n')

    def test_no_ignored_test_function(self):
        # In the past we used pytest ;)
        # Check if we still have some flat test function that will be not executed by unittests
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'bx_py_utils')
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'bx_py_utils_tests')
