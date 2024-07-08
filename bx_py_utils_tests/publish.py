"""
    Helper to publish this Project to PyPi
"""

import subprocess
from pathlib import Path

from manageprojects.utilities.publish import publish_package

import bx_py_utils
from bx_py_utils.path import assert_is_file


def publish():
    """
    Publish to PyPi
    Call this via:
        $ make publish
    """
    PACKAGE_ROOT = Path(__file__).parent.parent
    assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

    subprocess.check_call(['make', 'test'])  # don't publish if tests fail
    subprocess.check_call(['make', 'fix-code-style'])  # don't publish if code style wrong

    publish_package(module=bx_py_utils, package_path=PACKAGE_ROOT)


if __name__ == '__main__':
    publish()
