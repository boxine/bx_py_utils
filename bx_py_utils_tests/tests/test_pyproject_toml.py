import inspect
from pathlib import Path
from unittest import TestCase

import bx_py_utils
from bx_py_utils.path import ChangeCurrentWorkDir, MockCurrentWorkDir, assert_is_file
from bx_py_utils.pyproject_toml import get_pyproject_config


class PyProjectTomlTestCase(TestCase):
    def test_get_pyproject_config(self):
        with MockCurrentWorkDir(prefix='test_get_pyproject_config'):
            pyproject_toml_path = Path.cwd() / 'pyproject.toml'
            self.assertIs(pyproject_toml_path.exists(), False)

            value = get_pyproject_config(section=('foo', 'bar'))
            self.assertIs(value, None)

            pyproject_toml_path.write_text(
                inspect.cleandoc(
                    """
                    [foo]
                    no_bar_yet=1
                    """
                )
            )

            value = get_pyproject_config(section=('foo', 'bar'))
            self.assertIs(value, None)

            pyproject_toml_path.write_text(
                inspect.cleandoc(
                    """
                    [foo]
                    bar="exists"
                    """
                )
            )

            value = get_pyproject_config(section=('foo', 'bar'), base_path=Path('/not/exists'))
            self.assertIs(value, None)

            value = get_pyproject_config(section=('foo', 'bar'))
            self.assertEqual(value, 'exists')

            value = get_pyproject_config(section=('foo',))
            self.assertEqual(value, {'bar': 'exists'})

        # Read bx_py_utils toml file:

        pkg_root_path = Path(bx_py_utils.__file__).parent.parent
        assert_is_file(pkg_root_path / 'pyproject.toml')

        with ChangeCurrentWorkDir(pkg_root_path):
            package_name = get_pyproject_config(section=('project', 'name'))
        self.assertEqual(package_name, 'bx_py_utils')
