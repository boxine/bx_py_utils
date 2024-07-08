import subprocess
from importlib.metadata import version
from pathlib import Path
from unittest import TestCase

from packaging.version import Version

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
            self.assertIn('flake8', output)

    def test_pipenv_check(self):
        output = subprocess.check_output(['pipenv', 'check'], cwd=PACKAGE_ROOT, text=True)
        self.assertIn('Passed!\n', output)
        self.assertIn('No known security vulnerabilities found.', output)

    def test_no_ignored_test_function(self):
        # In the past we used pytest ;)
        # Check if we still have some flat test function that will be not executed by unittests
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'bx_py_utils')
        assert_no_flat_tests_functions(PACKAGE_ROOT / 'bx_py_utils_tests')

    def test_version(self):
        # We get a version string:
        bx_py_utils_version_str = version('bx_py_utils')
        self.assertIsInstance(bx_py_utils_version_str, str)
        self.assertTrue(bx_py_utils_version_str)

        # Note: The actual installed version may be different from the one in the __init__.py file.
        # So check this too:
        self.assertIsInstance(bx_py_utils.__version__, str)
        bx_py_utils_version = Version(bx_py_utils.__version__)
        self.assertIsInstance(bx_py_utils_version, Version)
        self.assertEqual(str(bx_py_utils_version), bx_py_utils.__version__)  # Don't allow wrong formatting
