import sys
from pathlib import Path

import bx_py_utils
from bx_py_utils.auto_doc import assert_readme


BASE_PATH = Path(bx_py_utils.__file__).parent


def test_auto_doc_in_readme():
    if sys.version_info < (3, 7):
        # pdoc is not compatible with Python 3.6
        return

    readme_path = BASE_PATH.parent / 'README.md'

    assert_readme(
        readme_path=readme_path,
        modules=['bx_py_utils'],
        start_marker_line='[comment]: <> (✂✂✂ auto generated start ✂✂✂)',
        end_marker_line='[comment]: <> (✂✂✂ auto generated end ✂✂✂)',
        start_level=2,
    )
